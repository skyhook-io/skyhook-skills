---
name: review-packet
description: Use when the user wants work packaged for review (e.g. "review packet", "/review-packet", "prepare this for review", "make it easy to review this PR set / design / research"). Builds a decision-first page that pairs every claim with the evidence for it.
metadata:
  short-description: Package work for guided review — decisions up front, evidence beside every claim
---

# Review Packet (Codex)

Package work so review is easy to *do* — same workflow as Claude's `/review-packet`.

**Canonical procedure:** read `~/.codex/skills/skyhook-skills-commands/review-packet.md`
and follow it (decisions first → real evidence → proof vs decision → counterfactual
for invisible wins → honest deferrals → publish). **Codex notes:**

- **Output is a self-contained `.html` file** written to the repo or a scratch dir,
  not a hosted artifact — Codex has no Artifact tool. Tell the user the path and
  offer to open it. Everything else in the procedure applies unchanged.
- **Embed images as `data:` URIs** regardless, so the single file survives being
  emailed, attached to a PR, or opened from anywhere. Crop to the subject and
  downscale (~1100px wide) before inlining; check the total file size.
- Gather evidence *before* writing: run the repo's visual-test (see
  `.claude/commands/qa.md`), the relevant tools, or the real commands. Prefer live
  output over illustrations — real material surfaces dilemmas you would not invent.
- **The reader's decisions go at the top**, the verdict at the bottom. If nothing
  needs deciding, say so and write a short report instead of a packet.
- Keep the deferral list and the "what I could not verify" section. A packet that
  only shows wins is marketing, and reviewers stop trusting it.
