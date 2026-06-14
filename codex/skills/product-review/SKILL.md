---
name: product-review
description: Use when the user wants a product/design/UX critique (e.g. "product-review", "/product-review", "is this the right thing to build / the right UX?"). Questions what to build and how users will perceive it, not just code correctness.
metadata:
  short-description: Critique what & how to build, not just whether it's correct
---

# Product Review (Codex)

Product/design/UX critique — same workflow as Claude's `/product-review`.

**Canonical procedure:** read `~/.codex/skills/skyhook-skills-commands/product-review.md` and follow it
(premise → journeys (8–10, ranked 0–10) → UX shape → comprehension → states →
AI-slop/design-system → 0–10 + "what a 10 looks like" + severity triage). **Codex
notes:**

- This is model-driven critique — no special tools needed; apply the forcing
  functions directly. Take a skeptical product+design lead's voice; question the
  premise and the chosen shape **before** execution.
- For the rendered-UI lens, use the repo's visual-test if available (see
  `.claude/commands/qa.md`).
- **Surface taste/product decisions to the user — never silently "fix" them.**
  Lead with premise/journey problems; a beautiful implementation of the wrong thing
  is still wrong. Don't ping-pong with prior reviewers.
