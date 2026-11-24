---
name: cross-review
description: Use when the user asks for an independent cross-model code review (e.g. "cross-review", "/cross-review", "have Codex or Claude review this"). Invokes another model family headlessly, prints findings verbatim, then triages them skeptically.
---

# Cross-Review (Antigravity)

Hand the current change to a **different model family** (**Codex** or **Claude**, or **Cursor** if requested) for an independent review, print its findings verbatim, then triage skeptically (never auto-accept).

**Canonical procedure:** read `../../../plugins/skyhook-skills/commands/cross-review.md` relative to this skill's directory and follow its scope resolution, framing rules (never brief the reviewer with your conclusions), verbatim output format, and skeptical triage steps.

## Step 1 — Pick the secondary reviewer
1. **Caller directive** — `codex`, `claude`, or `cursor` (plus optional model override).
2. **Env / config** — `SKYHOOK_REVIEWER` / `SKYHOOK_REVIEW_MODEL` or `~/.claude/skyhook-skills.json` (ignore if it points back to `agy`).
3. **If still unspecified** — ask the user whether to consult **Codex** (`gpt-6.2-sol`) or **Claude** (`opus`).

## Step 2 — Run the reviewer (foreground, unsandboxed for network/auth, 10-min timeout)

**codex** (default model `gpt-6.2-sol`; always redirect stdin `< /dev/null` so `codex exec` does not hang):
```bash
codex exec -m "<model>" -c model_reasoning_effort=high -s read-only "You are doing a READ-ONLY code review. Do NOT modify files, do NOT run builds or tests, do NOT commit. Use git to inspect <SCOPE> (e.g. 'git diff main...HEAD'), read the changed files, and report findings. FIRST judge the whole change at altitude: is this the right thing to build, is the design/approach sound, and is the practical risk/blast radius understood and mitigated — a clean implementation of the wrong thing is still wrong, so raise design/intent/risk problems first and loudest. THEN find correctness bugs, security issues, silent failures, races, logic errors, and breaking API changes. For each finding give: severity, file:line, what breaks, and a concrete fix. Skip pure style nits. Output a concise numbered findings list." < /dev/null
```

**claude** (default model `opus`; on macOS run unsandboxed so `claude -p` can read Keychain auth — do NOT fall back to `ANTHROPIC_API_KEY`; extract the final `result` text from the stream):
```bash
claude -p "You are doing a READ-ONLY code review. Do NOT modify files, do NOT run builds or tests, do NOT commit. Use git to inspect <SCOPE> (e.g. 'git diff main...HEAD'), read the changed files, and report findings. FIRST judge the whole change at altitude: is this the right thing to build, is the design/approach sound (architecture, abstractions, and for UI the layout + user journey), and is the practical risk/blast radius understood and mitigated by tests or guardrails — a clean implementation of the wrong thing is still wrong, so raise design/intent/risk problems first and loudest. THEN find correctness bugs, security issues, silent failures, race conditions, logic errors, and breaking API changes in the changed code. For each finding give: severity, file:line, what actually breaks, and a concrete fix. Skip pure style nits. Output a concise numbered findings list." \
  --model "<model>" \
  --permission-mode default \
  --allowedTools Read Grep Glob Bash \
  --no-session-persistence \
  --output-format stream-json \
  --include-partial-messages \
  --verbose
```

**cursor** — follow the `cursor-agent` command in `../../../plugins/skyhook-skills/commands/cross-review.md` (default model `gpt-5.6-high`).

## Step 3 — Print verbatim & triage skeptically
Follow Steps 4–5 of `../../../plugins/skyhook-skills/commands/cross-review.md`: reproduce the reviewer's final text verbatim, verify every finding against the actual code at `file:line`, emit the Fix · Skip · Discuss table (citing evidence on every Skip), and wait for confirmation before editing.
