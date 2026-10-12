---
name: competitive-research
description: Use when the user asks how competitors, similar tools, or OSS projects handle a problem, or wants an evidence-backed implementation, product, UX, feature, positioning, or marketing comparison.
metadata:
  short-description: Research comparable products and recommend what to adopt
---

# Competitive Research (Codex)

Find decision-relevant prior art and compare it with the current approach. Scale
the research altitude to the active task: source-level OSS behavior for technical
decisions, official product evidence for UX and feature questions, and first-party
market material for positioning.

**Canonical procedure:** read
`~/.codex/skills/skyhook-skills-commands/competitive-research.md` and follow it.

Codex notes:

- Browse the web because product behavior, docs, source, and positioning change.
  Prefer primary sources and cite exact pages or permanent source links near each
  claim.
- When the comparison is against current code, inspect the local repository or
  diff first. Use source search to verify behavior end to end; do not compare a
  competitor's shipped implementation with only our intended design.
- Default to a read-only report. Research does not authorize implementation,
  external messaging, or copying third-party code.
- Lead with the recommendation and explain tradeoffs when different contexts have
  different winners. A common pattern is evidence, not proof that it is right for
  this product.
