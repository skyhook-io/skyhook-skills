---
description: Cross-model review by the configured secondary reviewer (codex or cursor; agy opt-in when requested), printed verbatim, then triaged skeptically
argument-hint: "[codex|cursor|agy] [--base <ref>] [focus…]   (default: configured reviewer)"
---

# Cross-Review — configured secondary reviewer

Hand the current change to a **different model** for an independent review, print
its findings verbatim, then stress-test them (never auto-accept). The reviewer is
**configurable** — codex or cursor by default (plus **agy** / Antigravity CLI
when explicitly requested) — so the whole loop switches by changing one setting,
not by editing commands.

## Step 1 — Resolve the reviewer + model
Pick in this order (first wins):
1. **Directive in `$ARGUMENTS`** — `codex` / `cursor` / `agy` (or `gemini`,
   which maps to `agy`; plus `use <model>` / a bare model id like `gpt-6.2-sol`
   or `gemini-4-neon-high`).
2. **Env** — `SKYHOOK_REVIEWER` (`codex|cursor|agy`), `SKYHOOK_REVIEW_MODEL`.
3. **Config file** — `~/.claude/skyhook-skills.json`, fields `reviewer` + `model`
   (read it: `cat ~/.claude/skyhook-skills.json 2>/dev/null`).
4. **Default** — reviewer `codex`; model per reviewer: codex → **`gpt-6.2-sol`**
   (the latest Sol tier — Codex has no moving `sol` alias, so bump this id when a
   newer Sol ships), cursor → `gpt-5.6-high`, agy → **`gemini-4-neon-high`**
   (only used when explicitly requested via directive, env, or config — never as
   an implicit default).

Announce what you resolved, e.g. `### 🔁 CROSS-REVIEW · codex (gpt-6.2-sol)`.

## Step 2 — Resolve scope
Default: branch vs `main` (`git diff main...HEAD` + uncommitted). `--base <ref>` /
`--commit <sha>` / `uncommitted` narrow it. Announce it.

## Step 3 — Run the reviewer (foreground, 10-min Bash timeout)

**Don't brief the reviewer with your conclusions.** Give scope and focus
*areas*, never your summary of what the change does, why it is correct, or what
to sign off on. Your assumptions are what is under review: an author's comment
stating an assumption gets accepted by every reviewer who reads it as context.
Final rounds use an adversarial review of the full scope, not "verify these
fixes." Run the review through the documented command; a hand-written prompt is
where framing creeps in.

**codex** — via the official codex plugin's companion (scope flags only on
`review`; focus text ⇒ `adversarial-review`):
```bash
SCRIPT="$(ls -t ~/.claude/plugins/cache/openai-codex/codex/*/scripts/codex-companion.mjs 2>/dev/null | head -1)"
node "$SCRIPT" review --base <ref> --model "<model>"    # or: adversarial-review --base <ref> --model "<model>" "focus…"
```
- Always pass `--model` with the resolved model, so the review runs on the
  latest Sol even when `~/.codex/config.toml` defaults to something lighter.
  Reasoning effort still comes from the codex config (the companion has no
  `--effort` on reviews); `high`+ is recommended for review depth.

**cursor** — via the Cursor CLI, pinned to the resolved model:
```bash
cursor-agent -p "You are doing a READ-ONLY code review. Inspect <SCOPE> (e.g. run 'git diff main...HEAD'), read the changed files, and report findings. FIRST judge whether this is the right thing to build and the design/approach is sound (a clean implementation of the wrong thing is still wrong); THEN correctness bugs, security, silent failures, races, logic errors, breaking API. For each: severity, file:line, what breaks, concrete fix. Do NOT modify files, do NOT commit. Concise numbered list." \
  --output-format text --model "<model>" --force
```
- Cursor default model: **`gpt-5.6-high`**. For a genuine second opinion when
  driving from Claude, keep it on a non-Claude model.
- Needs Cursor auth (`cursor-agent` logged in or `CURSOR_API_KEY`). `--force` lets
  it read files + run `git` headless; the prompt keeps it read-only.
- If the reviewer errors (not installed / not logged in / no diff), surface it
  verbatim and stop — don't fabricate findings.
- If `--base` dies with `spawnSync git ENOBUFS`, the diff includes binary files
  (images, fonts) that overflow the subprocess buffer. Narrow the diff to text
  files, or skip git scoping with `node "$SCRIPT" task "<prompt naming the files to
  review>"` so Codex reads the paths itself.

**agy (Antigravity CLI — only when explicitly requested)** — pinned to the
resolved model (default **`gemini-4-neon-high`**):
```bash
agy -p "You are doing a READ-ONLY code review. Do NOT modify files, do NOT run builds or tests, do NOT commit. Use git to inspect <SCOPE> (e.g. 'git diff main...HEAD'), read the changed files, and report findings. FIRST judge whether this is the right thing to build and the design/approach is sound (a clean implementation of the wrong thing is still wrong); THEN correctness bugs, security, silent failures, races, logic errors, breaking API. For each: severity, file:line, what breaks, concrete fix. Concise numbered list." \
  --model "<model>" --sandbox --settings '{"toolPermission":"proceed-in-sandbox","enableTerminalSandbox":true}' --disable-slash-commands --output-format text --print-timeout 10m
```
- Only use `agy` when explicitly asked (`agy` / `gemini` directive,
  `SKYHOOK_REVIEWER=agy`, or `"reviewer": "agy"` in config).
- Needs prior interactive `agy` authentication. `--sandbox` with
  `toolPermission: "proceed-in-sandbox"` lets read-only `git` commands run
  headlessly inside the OS sandbox on all account types (whereas `--mode auto`
  isn't available on business/enterprise accounts, and plain `default` mode
  soft-denies unapproved shell commands and still exits `0`).
- If `agy` is not installed, not authenticated, or errors, surface the error
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
