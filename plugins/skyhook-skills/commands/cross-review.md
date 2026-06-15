---
description: Cross-model review by the configured secondary reviewer (codex or cursor), printed verbatim, then triaged skeptically
argument-hint: "[codex|cursor] [--base <ref>] [focus…]   (default: configured reviewer)"
---

# Cross-Review — configured secondary reviewer

Hand the current change to a **different model** for an independent review, print
its findings verbatim, then stress-test them (never auto-accept). The reviewer is
**configurable** — codex or cursor — so the whole loop switches by changing one
setting, not by editing commands.

## Step 1 — Resolve the reviewer + model
Pick in this order (first wins):
1. **Directive in `$ARGUMENTS`** — `codex` / `cursor` (and `use <model>` / a bare
   model id like `gpt-5.5-high`).
2. **Env** — `SKYHOOK_REVIEWER` (`codex|cursor`), `SKYHOOK_REVIEW_MODEL`.
3. **Config file** — `~/.claude/skyhook-skills.json`, fields `reviewer` + `model`
   (read it: `cat ~/.claude/skyhook-skills.json 2>/dev/null`).
4. **Default** — `codex`.

Announce what you resolved, e.g. `### 🔁 CROSS-REVIEW · cursor (gpt-5.5-high)`.

## Step 2 — Resolve scope
Default: branch vs `main` (`git diff main...HEAD` + uncommitted). `--base <ref>` /
`--commit <sha>` / `uncommitted` narrow it. Announce it.

## Step 3 — Run the reviewer (foreground, 10-min Bash timeout)

**codex** — via the official codex plugin's companion (scope flags only on
`review`; focus text ⇒ `adversarial-review`):
```bash
SCRIPT="$(ls -t ~/.claude/plugins/cache/openai-codex/codex/*/scripts/codex-companion.mjs 2>/dev/null | head -1)"
node "$SCRIPT" review --base <ref>                      # or: adversarial-review --base <ref> "focus…"
```

**cursor** — via the Cursor CLI, pinned to the resolved model:
```bash
cursor-agent -p "You are doing a READ-ONLY code review. Inspect <SCOPE> (e.g. run 'git diff main...HEAD'), read the changed files, and report findings. FIRST judge whether this is the right thing to build and the design/approach is sound (a clean implementation of the wrong thing is still wrong); THEN correctness bugs, security, silent failures, races, logic errors, breaking API. For each: severity, file:line, what breaks, concrete fix. Do NOT modify files, do NOT commit. Concise numbered list." \
  --output-format text --model "<model>" --force
```
- Cursor default model: **`gpt-5.5-high`**. For a genuine second opinion when
  driving from Claude, keep it on a non-Claude model.
- Needs Cursor auth (`cursor-agent` logged in or `CURSOR_API_KEY`). `--force` lets
  it read files + run `git` headless; the prompt keeps it read-only.
- If the reviewer errors (not installed / not logged in / no diff), surface it
  verbatim and stop — don't fabricate findings.

## Step 4 — Print findings **verbatim**
Reproduce the reviewer's stdout exactly, no summarizing/re-ranking:
```
## 🔁 <reviewer> (<model>) review — verbatim

<exact stdout>
```

## Step 5 — Triage skeptically (do NOT auto-accept)
Apply `/triage-findings`: read the real code at each `file:line`, validate against
reality, **cite evidence on every Skip**, default-skip false positives. A
cross-model reviewer is often right about blind spots and often wrong about things
already handled — you decide. Emit the verdict table (Fix · Skip · Discuss) and a
one-line scoreboard. Don't edit/commit — fixes happen after the user's go.
