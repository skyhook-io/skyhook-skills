# Create PR

Prepare and create a pull request for recent changes.

## Scope: Determine what to include

### 1. Understand current state
```bash
# Check current branch and status
git status

# See all commits in this branch
git log main..HEAD --oneline

# See all changes in branch vs main
git diff main..HEAD

# See uncommitted changes
git diff
```

### 2. Identify relevant changes
- **Include**: Files related to the current feature/fix
- **Exclude**: Unrelated local modifications
  - Build artifacts, generated files
  - Local config changes (.env, config/local.yaml)
  - Unrelated experiments or work-in-progress
  - Files you didn't intentionally modify
- **When in doubt**: List excluded files and ask

## Process

### 1. Branch Strategy
- **CRITICAL: Never push or commit directly to main/master.** If on main/master, create a feature branch first (`fix/<description>` or `feature/<description>`) before committing.
- **If on feature branch**: Use current branch
- **If unsure**: Ask what to do

### 2. Staging
- Stage only relevant files related to this work
- Use `git add <specific-files>` not `git add .`
- Double-check with `git diff --staged`

### 3. Commit
- **Check recent commits**: `git log -3 --oneline`
- **If last commit was < 1 hour ago AND related**: Consider amending
- **Otherwise**: Create new commit
- **Message style**: Brief, clear, explains what and why
  - Good: "Add user authentication with JWT tokens"
  - Bad: "Updated files and fixed stuff"

### 4. Create/Update PR
- **Title**: clear, conveys the real scope (don't undersell a feature as "fix X").

> ## 🚫 THE BODY DESCRIBES THE FINAL END-STATE — NOT HOW IT WAS BUILT OR REVIEWED
>
> This is the #1 rule and the most common mistake. The PR body is a description of
> **what the change is and does, as it stands right now** — written as if the
> design was always this way. It is **NOT** a story of the build/review process.
>
> **NEVER put any of these in a PR body** (instant rewrite if present):
> - "Cross-review / Codex / Cursor / Bugbot caught N issues" · "review found X"
> - "Scenarios reviewed" · "what was already OK" · "what got fixed by this PR"
> - "Round 1 / round 2" · "initially did X, then changed to Y" · "I reconsidered"
> - "tightened X", "now requires Y evidence", "suppressed empty Z rows",
>   "switched to component W" — review-fix minutiae of any kind
> - any framing where the *subject* is the process (a reviewer, a round, a catch)
>   rather than the *feature*
>
> If a review fix changed real behavior, fold **only that behavioral outcome** into
> "What changed" as if it was the design from the start — no mention that a review
> surfaced it. The reader wants the destination, never the route. When in doubt,
> ask: "does this sentence describe the shipped behavior, or the journey to it?"
> Journey → cut.

- **Description — depth proportional to the change; substance, not brevity.** A
  1500-line feature is not 4 bullets; a typo fix is not 4 paragraphs. Structure:
  - **Summary (lead with why + impact):** 1–3 sentences on what this does for the
    user/operator and the problem it solves — the *motivation*, not a changelog.
    Someone unfamiliar should grasp *why this exists* and *what it enables*.
  - **What changed (the substance):** the real design — key components, approach,
    how it's structured — grouped logically, **not a flat per-commit list**. For a
    nontrivial PR this is where the depth goes: the architecture, the notable
    decisions, and **what a reviewer should focus on** or that's non-obvious.
  - **Testing:** commands run + visual-test status (ran ⇒ what was covered;
    skipped ⇒ why). When risk is material, say what the tests/live checks
    mitigate. Screenshots for UI (uploaded/linked — never local paths).
  - **Notes / tradeoffs / follow-ups:** brief, only if real. Include practical
    risk/blast radius and residual risk here when it would help the reviewer; do
    not add a boilerplate risk section for trivial or obviously low-risk changes.

#### If a PR already exists for this branch
Don't just push the new commit and stop. Re-evaluate the PR title + body against the **full branch diff vs main**, not just the latest commit or this session's work. PRs accumulate scope across sessions and the description goes stale silently.

1. Run `gh pr view <num> --json title,body` and `git log --reverse origin/main..HEAD --oneline` to see everything that's actually in the PR.
2. Read the existing description and check whether each commit (or commit cluster) is reflected. Things that commonly drift:
   - New sub-features added in later commits but missing from the Summary
   - Title that undersells the scope (e.g. "fix X" when the PR also cuts a whole sub-flow)
   - Removed fields / disabled flows that aren't called out
   - Dependencies on other repos that were added later
   - Bullet points describing fields/labels that were since renamed or dropped
3. If the description no longer matches reality, **re-derive the narrative from the full diff as if writing it fresh — rewrite, don't append.** Accreting a fix bullet each review round turns the body into a review-fix changelog instead of a description of the feature. Propose the rewritten title + body and update with `gh pr edit <num> --title ... --body ...`.
4. Only skip the description refresh if the new commit is genuinely a small follow-up that the existing description already covers (e.g. fixing a typo flagged in review on a feature already described).

## Guidelines
- **Concise ≠ shallow**: cut fluff, incidental detail, and review-fix trivia — but give a nontrivial PR the real motivation + design depth a reviewer needs. Don't reduce a big feature to a handful of bullets.
- **Be clear**: Someone unfamiliar with the code should understand the change
- **Be honest**: If something is incomplete or needs follow-up, say so
- Do not include local filesystem paths in PR descriptions, including screenshot artifact paths. If screenshots matter, upload/attach them to GitHub and link them; otherwise summarize what was visually verified.

## Example Flow
```
1. git status → See what's changed
2. git log main..HEAD → See branch commits
3. Identify core feature files vs. incidental changes
4. git add src/auth/ src/middleware/jwt.go
5. git commit (or amend if appropriate)
6. git push -u origin feature/jwt-auth
7. gh pr create --title "..." --body "..."
```
