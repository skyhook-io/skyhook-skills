---
name: review-loop
description: Use when the user wants the current code proactively reviewed and fixed (e.g. "review-loop", "/review-loop", "review what I have and fix it"). Runs self + cross-model review, triages skeptically, fixes confirmed issues, updates the PR, and loops until clean.
---

# Review Loop (Antigravity)

Proactively review the current code and fix it from Antigravity (`agy`).

**Canonical procedure:** read `../../../plugins/skyhook-skills/commands/review-loop.md` relative to this skill's directory and follow it (whole-PR default scope, two-altitude review, skeptical triage, fix, update PR, loop until clean, caps, safety).

**Antigravity translations:**
- **Self-review:** apply `../../../plugins/skyhook-skills/commands/review.md` and `../../../plugins/skyhook-skills/commands/simple.md` thoroughly.
- **Cross-model review** (nontrivial changes only): use the `cross-review` skill (`../cross-review/SKILL.md`) to consult **Codex** or **Claude** (honor caller directives such as `consult codex` / `consult claude`, or ask which second model to use if unspecified).
- **Product review** (UI/product-facing changes): use the `product-review` skill (`../product-review/SKILL.md`).
- **Triage & fix:** apply `../../../plugins/skyhook-skills/commands/triage-findings.md` and `../../../plugins/skyhook-skills/commands/fix-findings.md` inline. Never auto-accept; cite `file:line` evidence on every Skip.
- **`/qa`:** read the repo's `.claude/commands/qa.md` and follow it (fast tier while iterating; full suite once at the end, and CI on the pushed head counts).
- **Update PR:** follow `../../../plugins/skyhook-skills/commands/pr.md` via `git` + `gh` (relevant files only, `--force-with-lease`, re-derive body from final state). No PR yet ⇒ leave commits local and say so.

Narrate phases with the canonical glyph banners and end with the run-summary ledger.
