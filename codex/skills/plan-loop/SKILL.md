---
name: plan-loop
description: Use when the user asks to plan a task before coding (e.g. "plan-loop", "/plan-loop", "plan this out first"). Draft a detailed plan, cross-review it with Claude, triage skeptically, iterate, then gate for sign-off.
metadata:
  short-description: Plan → cross-review with Claude → triage → gate
---

# Plan Loop (Codex)

Settle a plan before any code, Codex-side. Same workflow as Claude's
`/plan-loop`.

**Canonical procedure:** read `~/.codex/skills/skyhook-skills-commands/plan-loop.md` and follow it
(detailed plan with `file:line` evidence + Certain/Confident/Needs-input tiers,
cross-review, triage, iterate, gate). **Codex translations:**

- **Cross-review the plan with the OTHER model — Claude, not Codex.** Hand the
  plan to Claude via the **claude-review** skill, or directly:
  ```bash
  claude -p "Critique this implementation plan as a skeptical senior engineer. Find flawed assumptions, missing steps, hidden complexity, simpler alternatives, and risks. Challenge it; don't rewrite it. PLAN:\n\n<the full plan>" --model opus --permission-mode default --allowedTools Read Grep Glob Bash --no-session-persistence --output-format stream-json --include-partial-messages --verbose
  ```
  (Trivial plans skip this.) **`claude -p` needs Keychain access** — run it
  escalated/unsandboxed (see the **claude-review** skill's auth note), or it
  falsely reports "Not logged in" from inside Codex's sandbox. Use the streamed
  JSON to monitor progress; plain `claude -p` buffers until the final answer and
  can look hung during a long critique. Triage the final `result` text, not the
  JSON event noise.
- **Triage Claude's critique inline** — never auto-accept it; verify each point
  against the actual code, integrate the valid ones, reject weak ones with a
  stated reason. Cap at 2 cross-review cycles.
- **Gate:** default mode **stops for sign-off** before coding; `--auto` resolves
  Needs-input with best judgment, logs each call to `NOTES.md`, and proceeds —
  except a ceiling decision (prod/deploy/data-migrations · external-publish/money
  · security/auth/secrets · breaking-API/destructive-file-ops) stops regardless.

Narrate phases with the glyph-tagged banners and close with the short summary
ledger defined in the canonical file. When invoked by the **autodev** skill, the
approved/assumed plan flows straight into implementation.
