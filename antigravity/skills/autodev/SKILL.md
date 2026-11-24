---
name: autodev
description: Use when the user asks to take a task end-to-end autonomously (e.g. "autodev", "/autodev", "build this on autopilot"). Runs the full chain — plan, implement, review, PR, converge — stopping only at real decisions.
---

# Autodev (Antigravity)

Full-pipeline autopilot adapted for Antigravity (`agy`).

**Canonical procedure:** read `../../../plugins/skyhook-skills/commands/autodev.md` relative to this skill's directory and follow it (chain, modes, plan gate, the `--auto` ceiling, definition of done, hand-back). Apply these **Antigravity translations** wherever it names a command:

| Canonical command | Antigravity equivalent |
|---|---|
| `/plan-loop` | the `plan-loop` skill (`../plan-loop/SKILL.md`) |
| `/review-loop` | the `review-loop` skill (`../review-loop/SKILL.md`) |
| `/cross-review` | the `cross-review` skill (`../cross-review/SKILL.md`) — from Antigravity, cross-review with another model family (**Codex** or **Claude**; honor the user's directive, or ask which second model to use if unspecified) |
| `/product-review` | the `product-review` skill (`../product-review/SKILL.md`) |
| `/competitive-research` | the `competitive-research` skill (`../competitive-research/SKILL.md`) |
| `/qa` | read the repo's `.claude/commands/qa.md` and follow it (fast tier while iterating; full suite once at the end, and CI on the pushed head counts) |
| `/pr` | follow `../../../plugins/skyhook-skills/commands/pr.md` via `git` + `gh` (relevant files only, `--force-with-lease`, re-derive body from final state) |
| `/fix-pr-loop` | follow `../../../plugins/skyhook-skills/commands/fix-pr-loop.md` inline (full feedback inventory, skeptical triage, fix, push, close every thread) |
| `/request-approval` | follow `../../../plugins/skyhook-skills/commands/request-approval.md` inline |
| `/review-packet` | the `review-packet` skill (`../review-packet/SKILL.md`) |
| `/review`, `/simple`, `/triage-findings`, `/fix-findings` | follow the corresponding canonical files under `../../../plugins/skyhook-skills/commands/` |

**Non-negotiable invariants:**
- Default mode gates on the plan before coding; `--auto` logs assumptions to `NOTES.md` and still stops for the autonomy ceiling.
- Triage every reviewer skeptically; never auto-accept; cite evidence on skips. Cross-review only when nontrivial.
- Run `/product-review` for user-visible changes before opening the PR, and build a scenario ledger for scenario-sensitive work.
- Finish with the Definition of Done audit on the final head SHA, narrate phases with the canonical glyph banners, and close with the end-of-run summary ledger.
- Never merge, deploy, push to `main`, hard-`--force`, or stage unrelated files.
