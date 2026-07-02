---
name: claude-review
description: Use when the user asks for a cross-review by Claude (e.g. types "claude-review", "/claude-review", or "have Claude review this"). Invokes Claude Code headlessly to review the current branch/changes, prints Claude's findings verbatim, then triages them skeptically instead of auto-agreeing.
metadata:
  short-description: Claude reviews this branch; you triage skeptically
---

# Cross-Review: Claude reviews, you triage

You are running **inside a Codex session**. This skill hands the current change
off to **Claude Code** (a different model + harness) for an independent review,
shows the user exactly what Claude said, and then makes you stress-test those
findings instead of rubber-stamping them.

The point is an adversarial second opinion: Claude is the reviewer, you are the
skeptic. Do **not** assume Claude is right, and do **not** assume it is wrong.
Verify against the actual code.

If the user passed a scope or focus argument with the invocation, use it (Step
1). Otherwise default to reviewing this branch vs `main`. For scenario-sensitive
work such as copy, diagnostics, remediation guidance, detector precision, error
classification, permissions/security posture, or UI states, include the scenario
list in Claude's prompt and ask Claude to validate each scenario explicitly.

---

## Step 1 — Resolve scope

```bash
git status --short
git log --oneline main..HEAD 2>/dev/null | head -20
git rev-parse HEAD
```

- no argument → review the branch diff against `main` (fall back to `master`,
  then the default upstream if `main` is absent)
- `uncommitted` / `wip` → review staged + unstaged + untracked changes
- a hex sha → review just that commit
- anything else → treat it as the base branch name

State the resolved scope and exact reviewed ref/SHA before invoking Claude:
branch reviews use `HEAD`, commit-scope reviews use the requested commit SHA,
and uncommitted/WIP reviews use `HEAD` plus the dirty worktree. Claude's verdict
applies only to that reviewed ref plus any uncommitted changes included in scope.
If you later amend, commit, or push fixes, do not say Claude reviewed the final
head unless you reran Claude on that new head.

## Step 2 — Run Claude's review (headless)

Invoke Claude Code in print mode with a read-only review prompt. Whitelist only
read/search/git tools so the review can't mutate the tree. Build the
`<SCOPE>` clause from Step 1 (e.g. "this branch vs main", "the uncommitted
changes", "commit <sha>"). Preserve any user-specified focus or scenario matrix
in the prompt; do not collapse it into generic "review this PR" wording.

```bash
claude -p "You are doing a READ-ONLY code review. Do NOT modify files, do NOT run builds or tests, do NOT commit. Use git to inspect <SCOPE> (e.g. 'git diff main...HEAD'), read the changed files, and report findings. FIRST judge the whole change at altitude: is this the right thing to build, is the design/approach sound (architecture, abstractions, and for UI the layout + user journey), and is the practical risk/blast radius understood and mitigated by tests or guardrails — a clean implementation of the wrong thing is still wrong, so raise design/intent/risk problems first and loudest. THEN find correctness bugs, security issues, silent failures, race conditions, logic errors, and breaking API changes in the changed code. For each finding give: severity, file:line, what actually breaks, and a concrete fix. Skip pure style nits. Output a concise numbered findings list." \
  --model opus \
  --permission-mode default \
  --allowedTools Read Grep Glob Bash \
  --no-session-persistence \
  --output-format stream-json \
  --include-partial-messages \
  --verbose
```

Notes:
- **Use streaming output.** Plain `claude -p` buffers until the final answer, so
  real reviews can look hung while Claude is reading, thinking, or running
  tools. With `stream-json`, treat streamed `tool_use`, `thinking_tokens`, and
  `ping` events as progress. Do not interrupt solely because no final prose has
  appeared.
- **Allow several minutes** — a cross-model review is slow and consumes a full
  Claude turn. This runs in your sandbox; the network/process call may need
  escalation. If your shell enforces a short command timeout, raise it (5–10 min).
- **Model:** pinned to `--model opus` so the reviewer is always Claude's strong
  model regardless of the user's day-to-day default. `opus` is an alias that
  tracks the latest Opus. Swap it only if the user asks for a specific model.
- If Claude errors (not logged in, no diff, etc.), surface the raw error and
  stop — don't fabricate findings.
- `Bash` is whitelisted so Claude can run `git`; the prompt constrains it to
  read-only. For a stricter posture, drop `Bash` and Claude reviews from the
  files alone.
- **Auth / sandbox (important):** `claude -p` reads its login from the macOS
  **Keychain** (`Claude Code-credentials`), which Codex's sandbox can't reach — so
  it reports `Not logged in · /login` **even though Claude is fully logged in**
  (a plain-shell `claude -p "ok"` proves it). Run this call **escalated /
  unsandboxed** (request approval) so it can read the Keychain and use the
  subscription. **Do NOT fall back to `ANTHROPIC_API_KEY`** — cross-review stays on
  the subscription, never billed via the API. If escalation is unavailable, **stop
  and tell the user the cross-review is blocked** (do a self-triaged pass, marked
  as a gap) rather than working around it. Never conclude Claude is logged out
  from this error — it's a sandbox-vs-Keychain gap.

## Step 3 — Print Claude's findings **as-is**

From the streamed JSON, extract the final `result` value and reproduce that text
**verbatim** in a fenced block — do not summarize, reword, re-rank, or drop
anything. Do not paste the JSON event stream, signed thinking metadata, or tool
event noise as the review. The user wants the raw second opinion first.

```
## 🟣 Claude's review (verbatim)

<exact stdout from claude -p>
```

Verbatim means verbatim, even if long.

## Step 4 — Triage skeptically (do NOT auto-agree)

For **each** finding Claude raised:

1. **Understand the claim** — restate what Claude is actually asserting.
2. **Read the real code** at the referenced `file:line` yourself — don't trust
   the pasted snippet; it may be stale or out of context.
3. **Validity** — real, or a false positive? Did Claude misread control flow,
   miss a caller-side guarantee, miss validation elsewhere, or misunderstand the
   framework? Cross-model reviewers often flag things already handled.
4. **Severity** — practical or theoretical? Default to **Skip** for defensive
   guards against impossible states, redundant-with-framework checks, missing
   tests for trivial code, and speculative future concerns. Default to **Fix**
   when it's genuinely correct and clearly better — correctness matters, size
   doesn't.
5. **Fix** — if valid, the right fix (which may differ from Claude's suggestion).

Then emit the triage table:

| # | Claude finding | Verdict | Why (verified against code) | Action |
|---|----------------|---------|-----------------------------|--------|

Verdicts: **Fix** · **Skip** · **Discuss**.

For every **Skip**, name specifically what Claude missed (cite the file:line of
the mitigating code). A bare "disagree" is not acceptable — show the evidence.

## Step 5 — Confirm before changing anything

End with a one-line scoreboard ("Claude raised N · Fix X · Skip Y · Discuss Z")
and ask: **"Want me to apply the confirmed fixes?"**

Do not edit, commit, or push as part of this skill — fixes happen only after
the user says go.
