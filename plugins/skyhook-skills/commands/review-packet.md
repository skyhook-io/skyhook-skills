---
description: Package work for effective guided review — an artifact that pairs each claim with the evidence for it and puts the decisions you need made up front
argument-hint: "[pr|set|design|research] [focus]  (default: auto-detect from the work in this session)"
---

# Review Packet — make the review easy to *do*, not just easy to read

A review packet is not a summary of what you built. It is a **decision instrument**:
it puts the calls the reviewer has to make at the top, and beside every claim it
puts the evidence that lets them disagree with you.

Reach for this when review would otherwise mean scrolling a diff, replaying an
investigation, or taking your word for it: a large PR or a **set** of related PRs,
a rendered UI change, a design or architecture proposal, competitive research.
Skip it for small, self-evident changes — a packet for a typo fix is ceremony.

**Prerequisite: have something to show.** Run `/visual-test`, `/product-review`,
`/review-loop` or `/competitive-research` *first* if their output is the substance.
This command packages evidence; it does not manufacture it.

## The rule that makes packets work

> **Every claim sits next to the artifact that proves it, and every dilemma gets
> its own visual slot.**

A reviewer who cannot see what you saw is being asked to trust you. A dilemma
buried in a paragraph gets skimmed. Those two failures are what packets exist to
prevent.

## Build it

### 1. Decide what the reader must *do*

Open with **the calls for you** — the open questions, as an indexed list that jumps
to the frame arguing each one. Three to six is right; more means you have not
triaged. If nothing needs deciding, stop: write a report, not a packet.

Everything else on the page earns its place by supporting one of those calls, or by
being the proof that the work is sound.

### 2. Gather real evidence, not illustrations

Prefer artifacts the work actually produced — live screenshots, real runs against
real systems, actual tool output, genuine diff excerpts. **Real material surfaces
dilemmas you would not have invented**, and reviewers can tell the difference.

Crop to the subject. A full-window screenshot hides the thing you are pointing at.

### 3. Split proof from decisions

Two different reading modes; tag them visibly:

- **Proof** — this works, here is it working. Reviewer skims.
- **Decision** — here is a real tension, here are the options. Reviewer stops.

### 4. Show the counterfactual for anything invisible

**Evidence of a guardrail working looks like nothing happening.** A screenshot of a
warning that correctly *did not* disappear means nothing until you state what the
old behaviour would have been on that same screen. Same for a race that no longer
occurs, a query no longer issued, a state no longer reachable. Say what the reader
would have seen instead.

### 5. Be honest in the packet itself

- **What you could not verify**, plainly.
- Findings you **deferred**, and why — a packet that only shows wins is marketing.
- Where you and a cross-model reviewer **disagreed**, and who you think is right.
- Verdict / scoreboard at the **end**. The top belongs to the reader's decisions.

## Components to reach for

Pick what the material needs; do not use them all.

| Component | Use when |
|---|---|
| **Frame**: evidence beside prose | The default unit. Screenshot/excerpt on one side, claim + dilemma on the other |
| **Decision box** | Any open call — give it a distinct block, never inline prose |
| **Before / after pair** | Behaviour changed and the change is visible |
| **Counterfactual note** | The improvement is an absence (see step 4) |
| **Journey table** | Product/UX work — rank how well each journey is served |
| **Agreement matrix** | Multiple reviewers — where they agreed, where they split |
| **Per-item state table** | A **set** of PRs/items — state, blockers, merge order |
| **Scoreboard** | Closing verdict across dimensions |
| **Provenance line** | Always: what was run, against what, when |

## Ship it as an artifact

Publish with the **Artifact** tool so it is a link the team can open, not a file.

- **Load the `artifact-design` skill first** — treatment is a deliberate choice.
  A review packet is a polished *document*, not a landing page.
- **Images must be embedded** — the artifact CSP blocks external image hosts.
  Crop, downscale (~1100px wide is legible for UI), convert to JPEG, and inline as
  `data:` URIs. Keep the page comfortably under the size cap; check the total before
  publishing. For many or large assets, use the artifact `assets` capability instead.
- **Ground the design in the subject.** If you are reviewing a product's UI, let the
  packet borrow that product's own accent and semantic colours so the chips in your
  prose read the same as the chips in the screenshots.
- Sticky evidence beside scrolling prose reads well on wide screens; stack on narrow.
- Give it a real name, and a one-line `description` for the gallery card.

Then hand over the **link** plus a short orientation: what is in it, which frame to
look at first, and what you are asking them to decide.

## Anti-patterns

- A changelog with pictures. If the subject of your sentences is the work rather
  than the reader's decision, start over.
- Screenshots without claims, or claims without screenshots.
- Burying the one frame that matters at position seven.
- Only wins. Defer list and "could not verify" are load-bearing.
- Re-litigating the build process. The reader wants the state and the choices, not
  the route (`/pr`'s rule applies here too).

## Progress output

Announce phases with the shared glyphs: 🔭 scope · 🧾 evidence · 🖼 frames ·
⚖️ decisions · 📦 publish. Close with:

```
📦 review-packet · <subject>
 🔗 https://claude.ai/code/artifact/…
 🧾 evidence      9 live runs · 2 clusters · 11 captures
 🖼 frames        8 (3 proof · 5 decision)
 ⚖️ decisions     5 open for you
 first look: frame 01 — <why that one>
```
