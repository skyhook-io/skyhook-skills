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

Use:

```bash
gh pr checks <pr-number> --watch
gh pr view <pr-number> --json comments,reviews,latestReviews,headRefOid
gh api repos/:owner/:repo/pulls/<pr-number>/comments
```

Treat these as feedback sources:
- Failing CI checks.
- GitHub Actions annotations that are visible from failed jobs.
- Cursor Bugbot.
- CodeRabbit, Claude, Copilot, github-actions, CodeQL, or other bot review comments.
- Human review comments.

**Slow-check cap (CodeQL etc.):** CodeQL and similar security scans can run far
longer than the rest of CI. **Don't block the loop on CodeQL for more than ~5
minutes.** Don't `gh pr checks --watch` indefinitely on it — poll instead, and if
CodeQL (or another known-slow scanner) is the *only* thing still pending past ~5
min, proceed with the round rather than waiting; its results, if actionable, get
picked up next round. Note it as `CodeQL pending` in the status/summary so the gap
is visible.

If checks are still pending after the wait timeout, continue only if there are
already actionable findings — **or if the only laggard is a slow scanner like
CodeQL** (per the cap above). Otherwise stop and report that review is still
pending.

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

Converged means:
- All required checks pass or are intentionally skipped.
- Latest automated reviewer pass has no open actionable findings.
- No human reviewer has unresolved blocking feedback.
- Branch has no tracked local changes.
- PR description still matches the full branch diff.

When converged, report:

```text
PR loop converged.
- PR: <url>
- Rounds: <n>
- Final commit: <sha>
- Checks: <summary>
- Reviewers: <summary>
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
