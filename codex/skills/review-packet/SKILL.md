---
name: review-packet
description: Use when the user wants work packaged for review (e.g. "review packet", "/review-packet", "prepare this for review", "make it easy to review this PR set / design / research"). Builds a decision-first page that pairs every claim with the evidence for it.
metadata:
  short-description: Package work for guided review — decisions up front, evidence beside every claim
---

# Review Packet (Codex)

Package work so review is easy to *do*: decisions first, evidence beside claims,
and a document the reviewer can open.

Read `../skyhook-skills-commands/review-packet.md` relative to this skill's
installed directory. In this repository, the source is
`../../../plugins/skyhook-skills/commands/review-packet.md`.
Follow that canonical procedure, including its **Codex: Sites publishing** route.

- **Publish through Sites by default.** Use the available Sites tools and their
  current instructions; do not require Claude's Artifact tool or `artifact-design`.
- **Local-only means self-contained HTML.** Honor that request without publishing.
  If Sites is unavailable or publication fails, hand over the completed HTML and
  explain the gap. Do not generate a PDF unless explicitly requested.
- Reuse the packet's saved Sites configuration on updates, preserve its audience,
  and verify deployment success before returning a hosted URL. State who can
  access it; owner-private does not mean team-accessible.
- Reuse real evidence from the session. Capture UI only when a visual claim needs
  it. Keep deferred findings, verification gaps, and reviewer disagreements.
- Put the reader's decisions at the top and the verdict at the bottom. If there
  is no open decision, write a short report instead of manufacturing a packet.

These adapters are also installed for Cursor. When running there, follow the
canonical procedure's **Other agents** route instead of assuming Sites exists.
