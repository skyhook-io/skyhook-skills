# Fix PR Loop

Autonomously iterate on the current PR until CI and automated reviewers converge, or until a human decision is needed.

This command composes the behavior of:
- `/fix-pr` for fetching PR feedback and prioritizing real review issues.
- `/triage-findings` for validating each finding against the actual code.
- `/fix-findings` for immediately fixing confirmed issues.
- `/pr` for staging only relevant files, committing/amending, pushing, and keeping the PR title/body accurate.

## Goal

Run the PR feedback loop without needing the user to babysit every reviewer pass:

1. Inspect the current branch and PR.
2. Wait for CI and automated reviewers.
3. Triage every new finding.
4. Fix valid issues.
5. Update the PR.
6. Repeat until there are no new valid issues and all required checks pass.

Stop only when converged, blocked, or when a reviewer asks for a product/design/API decision that should not be guessed.

## Inputs And Defaults

- Current branch must have an open PR.
- Default max rounds: `5`.
- Default wait timeout per round: `20m`.
- If the user provides numbers in the prompt, treat them as overrides, e.g. `fix-pr-loop max=8 wait=30m`.

## Safety Rules

- Never run this on `main` or `master`; stop and ask for a feature branch.
- Never merge the PR.
- Never resolve merge conflicts automatically.
- Never force-push with plain `--force`; use `--force-with-lease`.
- Do not stage unrelated local files. Use `git add <specific-files>`.
- Preserve unrelated untracked files.
- If a human reviewer asks an ambiguous question or requests a scope/product decision, stop and ask the user.
- If the same finding remains after two fix attempts, stop and summarize the blocker instead of looping.

## Round 0: Establish State

Run:

```bash
git status --short --branch
git branch --show-current
git log --reverse origin/main..HEAD --oneline
gh pr view --json number,state,title,body,headRefName,baseRefName,headRefOid,url
gh pr checks --watch=false
```

Report briefly:
- Branch and PR number.
- Whether tracked files are dirty.
- Commits ahead of `origin/main`.
- Current CI/reviewer status.

If there are dirty tracked files, decide whether they are part of the PR work. If they are unrelated, stop and ask. If they are clearly from the current PR work, continue and include them in the next `/pr`-style update.

## Wait For Reviewers

At the start of each round, wait until automated feedback has settled.

Use the feedback inventory below; `gh pr checks <pr-number> --watch=false` gives
the quick CI rollup.

### Feedback inventory — check every source

Bots spread findings across different GitHub surfaces. Qodo posts its review as
PR conversation comments and inline threads; Cursor Bugbot uses inline threads
and a check run; CodeRabbit posts reviews. Checking one surface misses the
others, so each round and the final convergence check read all of them:

```bash
# Unresolved review threads, the source of truth for "open inline comments".
# --paginate walks every page of threads; read every reply in a thread, since a
# human can reply between a bot's finding and its acknowledgment.
gh api graphql --paginate -f query='query($owner:String!,$repo:String!,$pr:Int!,$endCursor:String){repository(owner:$owner,name:$repo){pullRequest(number:$pr){reviewThreads(first:100,after:$endCursor){pageInfo{hasNextPage endCursor} nodes{id isResolved isOutdated path line comments(first:100){totalCount nodes{databaseId author{login} body createdAt url}}}}}}}' \
  -f owner=<owner> -f repo=<repo> -F pr=<pr-number> \
  --jq '.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved|not)'
# Review bodies (summary findings, CHANGES_REQUESTED) and which commit each covered
gh api repos/<owner>/<repo>/pulls/<pr-number>/reviews --paginate \
  --jq '.[] | {user:.user.login, state, commit_id, submitted_at, body}'
# PR conversation comments; compare updated_at, since some bots edit one comment in place
gh api repos/<owner>/<repo>/issues/<pr-number>/comments --paginate \
  --jq '.[] | {user:.user.login, created_at, updated_at, body}'
# Check runs on the head SHA, including bot output and annotation counts
gh api repos/<owner>/<repo>/commits/<head-sha>/check-runs --paginate \
  --jq '.check_runs[] | {id, name, status, conclusion, head_sha, url:.html_url, title:.output.title, summary:.output.summary, text:.output.text, annotations:.output.annotations_count}'
# For any check run with annotations > 0 (warnings can sit on passing checks)
gh api repos/<owner>/<repo>/check-runs/<check-run-id>/annotations --paginate
```

An outdated thread (`isOutdated`) can still be unaddressed: the line moved, but
the problem may remain. Triage it like any other.

Triage check annotations by relevance to the change. Runner notices (for
example, image migration notices) are not PR feedback. A warning in code the PR
didn't touch is pre-existing only if the base branch's run shows it too or it is
clearly unrelated to the change; a changed caller or config can surface a new
finding in untouched code.

**The automated reviewers are the primary signal** — the whole point of a round is
their findings (Cursor Bugbot, CodeRabbit, Claude/Copilot review comments) plus any
failing build/test CI. Those are what you wait for and triage. Security scanners like
CodeQL are secondary: useful when they flag something, but not worth stalling a round
on when they're slow (see the cap below).

Prefer polling over one long `gh pr checks --watch`: wait for the AI reviewers and
ordinary build/test CI to settle, then poll known-slow scanners separately.

Treat these as feedback sources:
- Failing CI checks.
- GitHub Actions annotations that are visible from failed jobs.
- Cursor Bugbot.
- CodeRabbit, Claude, Copilot, github-actions, CodeQL, or other bot review comments.
- Human review comments.

**Slow-check cap (CodeQL/static analysis):** CodeQL and similar security scans can
run far longer than the rest of CI. **Don't block the loop on CodeQL for more than
~2 minutes** — the reviewers are the point of the round, not the scanner. Treat
CodeQL workflow children as slow scanners even when the visible check name is only
`Analyze (go)` or `Analyze (javascript-typescript)`; identify them via the check-run
workflow/name/path (`CodeQL`, `.github/workflows/codeql.yml`) or details URL. If a
CodeQL/static-analysis job is the *only* thing still pending past ~2 min, proceed
with the round rather than waiting; its results, if actionable, get picked up next
round. Note it as `CodeQL pending` or `Analyze (go) pending
(CodeQL)` in the status/summary so the gap is visible.

This cap does **not** apply to AI reviewers or normal build/test CI. Wait for
Cursor Bugbot, CodeRabbit, Claude/Copilot review comments, and failing build/test
jobs, or triage their output before declaring the round settled.

If checks are still pending after the wait timeout, continue only if there are
already actionable findings — **or if the only laggard is a slow scanner like
CodeQL** (per the cap above). Otherwise stop and report that review is still
pending.

**Settled on the head, not just quiet.** A reviewer has settled on the current
head only with evidence tied to that SHA: its check run for the head SHA is
complete, its latest review's `commit_id` is the head, or it posted a finished
review result that names the head commit (Qodo, for example, notes the commit a
review covers). A progress note ("reviewing <sha>…") is not a result, even when
it names the head. A comment that is merely newer than the push is not enough
either: it can be output from a run that started before the push. Without SHA-tied evidence by the
wait timeout, report that reviewer as `pending on <sha>`, not settled. A bot that
doesn't re-review every push still leaves its earlier findings open until you
close them. After every push, the previous round's "no findings" no longer
counts.

## Triage Findings

For each round, consider only findings that are new or still relevant to the current `headRefOid`. Older comments may be obsolete after prior commits.

Apply `/fix-pr` priority buckets:

- Must Fix: real bugs, realistic security issues, production-breaking behavior, silent failures.
- Worth Considering: confusing user-facing errors, resource leaks, clear debugging or performance problems.
- Quick Wins: typos, unused imports, formatting, trivial naming confusion.
- Deprioritized: generic test coverage asks, theoretical concerns, speculative refactors.

Then apply `/triage-findings` validity checks:

- Read the referenced code.
- Confirm the reviewer’s claim matches the actual code.
- Identify mitigations the reviewer missed.
- Decide `Fix`, `Skip`, or `Discuss`.

Output a compact table each round:

| # | Source | Issue | Verdict | Reasoning | Action |
|---|--------|-------|---------|-----------|--------|

Rules:
- Fix all `Fix` items immediately.
- Skip `Skip` items without code churn.
- Stop on `Discuss` items unless they are clearly answerable from repo context.

## Apply Fixes

For all `Fix` items:

1. Make the smallest coherent code change.
2. Keep changes scoped to the issue.
3. **Bugs of-a-kind cluster — fix the pattern, not just the reported site.** When a finding is a *kind* of bug (a wrong call shape, a missing guard, an unsafe unwrap), grep the codebase for the same pattern before calling it fixed. Patching only the flagged line ships the same bug at the sibling sites — and the next reviewer/bot just re-flags them. Fix every instance; if you deliberately leave one, say why.
4. Add or adjust tests only when they protect behavior that can regress.
5. Run focused validation first, then broader validation if risk warrants it.

Use the repo’s existing commands and local guidance. If unsure, inspect `Makefile`, package scripts, and nearby tests.

## Close Every Item

Every inventory item ends the round with a disposition, visible on the PR:

- **Fixed (bot thread):** push the fix, then resolve the thread:
  `gh api graphql -f query='mutation($id:ID!){resolveReviewThread(input:{threadId:$id}){thread{isResolved}}}' -f id=<thread-id>`
- **Skipped (bot thread):** reply with a one-line reason and the evidence, then
  resolve it. `<comment-id>` is the `databaseId` of the thread's first comment:
  `gh api repos/<owner>/<repo>/pulls/<pr-number>/comments/<comment-id>/replies -F body=@<reply-file>`
- **Bot conversation comments** (no thread to resolve): the round's triage table
  records the disposition. Reply on the PR only if the bot expects it.
- **Human comments:** never resolve a human's thread. Answer clear factual
  questions; otherwise draft the reply, and list it as open for the user.
- **Discuss:** leave it open and list it for the user.

This covers PRs this workflow owns. On someone else's PR, draft replies and ask
before posting or resolving anything.

Write reply text to a file with a quoted heredoc (`cat > <reply-file> <<'EOF'`)
and pass it as `-F body=@<reply-file>`, so backticks, `$`, and quotes survive.

## Update PR

After fixes, follow `/pr` discipline:

1. Stage only relevant files with `git add <specific-files>`.
2. Check `git diff --staged --check`.
3. Commit or amend:
   - If the branch has one cohesive PR commit, prefer `git commit --amend --no-edit`.
   - If the fix is a distinct reviewer follow-up and the branch already has meaningful separate commits, create a new focused commit.
4. Push:
   - Existing PR branch: `git push --force-with-lease` after amend/rebase, otherwise normal `git push`.
5. Re-evaluate the PR title/body against the full branch diff.
6. Update the PR body if verification, scope, or behavior changed — **re-derive the narrative per `/pr`'s description guidance, don't append a fix bullet each round.** The body describes the feature's end state and value, NOT the review journey; keep review-fix trivia ("now requires X evidence", "suppressed Y rows") out of it.
7. Before updating the PR body, remove local filesystem paths (e.g. `.playwright-mcp/`, `/tmp/`, workspace paths). Replace screenshot artifact paths with uploaded GitHub links or a short description of what was visually verified.

## Convergence Check

After pushing, start the next round.

Converged means, **all checked on the final head SHA after the last push**:
- All required checks pass or are intentionally skipped (slow scanners named).
- Every AI reviewer has settled on that head (see "Settled on the head").
- The feedback inventory shows **zero unresolved review threads** except ones
  explicitly listed for the user, and every review body and conversation comment
  has a disposition.
- No human reviewer has unresolved blocking feedback.
- Branch has no tracked local changes.
- PR description still matches the full branch diff.

If the last push was a fix, you are not converged yet: wait for reviewers to
settle on it and read the inventory again.

When converged, report:

```text
PR loop converged.
- PR: <url>
- Rounds: <n>
- Final commit: <sha>
- Checks: <summary>
- Reviewers: <summary, each settled on the final head>
- Threads: <n resolved this run · 0 open, or the open ones listed for the user>
- Validation run: <commands>
```

## Stop Conditions

Stop and report clearly when:

- Merge/rebase conflicts occur.
- A finding requires user/product/design judgment.
- A required external system is unavailable.
- CI is still pending after the wait timeout and no actionable findings are available.
- The same issue persists after two fix attempts.
- Max rounds are reached.

In the stop report, include:
- What was completed.
- What remains.
- The exact command or review item that blocked progress.
- Recommended next action.
