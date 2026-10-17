---
name: review-packet
description: Use when the user wants work packaged for review (e.g. "review packet", "/review-packet", "prepare this for review", "make it easy to review this PR set / design / research"). Builds a page that explains the change from first principles, then pairs every claim with the evidence for it and ends with the open calls.
metadata:
  short-description: Package work for guided review — full context first, evidence beside every claim, calls last
---

# Review Packet (Codex)

Package work so review is easy to *do*: explain the change completely first, then
put the evidence beside each claim and the open calls at the end, in a document the
reviewer can open.

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
- Apply the canonical cold-reader check: explain the complete final-state
  problem, journey, scope, design, and verification gaps; rewrite on updates.
  Publishing a snapshot can precede CI completion when pending checks are named
  and linked. A settled/merge-ready verdict still requires the completion gates.
- Put the reader's decisions at the top and the verdict at the bottom. If there
  is no open decision, write a short report instead of manufacturing a packet.

These adapters are also installed for Cursor. When running there, follow the
canonical procedure's **Other agents** route instead of assuming Sites exists.
