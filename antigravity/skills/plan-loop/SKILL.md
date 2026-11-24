---
name: plan-loop
description: Use when the user asks to plan a task before coding (e.g. "plan-loop", "/plan-loop", "plan this out first"). Drafts a detailed plan, cross-reviews it with another model family, triages skeptically, iterates, and gates for sign-off.
---

# Plan Loop (Antigravity)

Settle a plan before any code from Antigravity (`agy`).

**Canonical procedure:** read `../../../plugins/skyhook-skills/commands/plan-loop.md` relative to this skill's directory and follow it (detailed plan with `file:line` evidence, Certain/Confident/Needs-input tiers, cross-review, skeptical triage, iterate, gate).

**Antigravity translations:**
- **Cross-review with another model family (Codex or Claude, nontrivial plans only):**
  - Honor any steering in the invocation (`consult codex`, `consult claude`, or a specific model). If the user did not specify which second model to use, check `SKYHOOK_REVIEWER` / `~/.claude/skyhook-skills.json` (when it names a non-`agy` reviewer) or ask the user whether to consult **Codex** or **Claude**.
  - Write the plan to a file (e.g. `/tmp/plan.md`) to avoid argv quoting issues:
    - **Codex** (redirect stdin or `codex exec` hangs; needs network/outside-sandbox access):
      ```bash
      codex exec -m gpt-6.2-sol -c model_reasoning_effort=high -s read-only "Critique this implementation plan as a skeptical senior engineer. FIRST challenge the premise: is this the right thing to build and the right approach, or is there a fundamentally simpler/different design? Then find flawed assumptions, missing steps, hidden complexity, and risks. Don't just check internal consistency — question whether the whole direction is correct. Before agreeing anything is unused, search open PR branches too. Be specific; challenge it, don't rewrite it. The plan is in the <stdin> block." < /tmp/plan.md
      ```
    - **Claude** (run unsandboxed on macOS so `claude -p` can read Keychain auth; do NOT fall back to `ANTHROPIC_API_KEY`; monitor streamed JSON and extract the final `result` field):
      ```bash
      claude -p "Read /tmp/plan.md and critique it as a skeptical senior engineer. FIRST challenge the premise: is this the right thing to build and the right approach, or is there a fundamentally simpler/different design? Then find flawed assumptions, missing steps, hidden complexity, simpler alternatives, and risks. Challenge it; don't rewrite it. Return ranked findings only." --model opus --permission-mode default --allowedTools Read Grep Glob Bash --no-session-persistence --output-format stream-json --include-partial-messages --verbose
      ```
- **Triage skeptically** — verify every point against the actual code, fold valid ones, reject weak ones with evidence. Cap at 2 cross-review cycles.
- **Gate:** default mode stops for sign-off; `--auto` logs decisions to `NOTES.md` and stops only on the autonomy ceiling.
