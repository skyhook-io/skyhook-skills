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

## Build and publish the document

Choose the delivery route from the running agent, honoring an explicit local-only
request before publishing:

| Agent / request | Delivery |
|---|---|
| Claude | Publish with the **Artifact** tool; load `artifact-design` first |
| Codex | Publish with **Sites**, following its available skills and current tool instructions |
| Explicit local-only request, or publishing unavailable | Self-contained HTML file with a clickable absolute local path |
| Other agents (including Cursor) | Use an available publishing integration when requested; otherwise local HTML |

Do not invoke Claude's Artifact tool or require `artifact-design` from Codex.
If the selected publishing tool is unavailable or fails, finish and hand over the
local HTML, explain the publishing gap, and do not claim it is a hosted link.
Do not install an unrelated hosting service automatically. A local request needs
only HTML; generate a PDF only if explicitly requested.

### Shared document treatment

- Make a polished *document*, not a landing page. Use readable typography,
  restrained color, stable decision anchors, and evidence beside each claim.
- Ground the design in the subject: borrow the product's accent and semantic
  colors so the prose and screenshots use the same visual language.
- Stack evidence and prose on narrow screens; use columns on wide screens.
  Keep images legible or expandable to full size. Keep substantive content
  accessible without JavaScript.
- Embed images as `data:` URIs. Crop to the subject and downscale only while
  preserving legibility (~1100px wide often works). Choose PNG for sharp text or
  JPEG for photographic material. Check total size against the chosen host's
  limits. Claude's Artifact `assets` capability is an option for large assets;
  keep a local HTML deliverable self-contained.
- For local HTML and Sites, inline CSS and any small optional scripts; use system
  fonts. Escape evidence excerpts as text, never executable markup. Keep source
  links and provenance beside evidence; external references are not dependencies.
- Give the document a real name and a one-line description.

### Codex: Sites publishing

Prepare and inspect the self-contained HTML before publishing. Use a dedicated
packet directory outside tracked application source unless the user chose a
location. The Sites tools may provide more detailed instructions; follow those.
The static route exercised for this workflow is:

1. Put the HTML at `dist/index.html`. Configure `.openai/hosting.json` with
   `{"static":{"directory":"dist"}}`, preserving existing configuration.
2. Read that configuration before creating a site. Reuse its `project_id` on
   updates. If absent, create the site once and immediately persist the returned
   ID atomically. Never invent IDs or recreate a site to retry a failed step.
3. Push the exact source state to the site's returned Git repository/branch using
   its short-lived credential and per-command authentication. Do not print or
   persist the credential. After a successful push, run
   `git rev-parse --verify HEAD` and use its full output as `commit_sha`.
4. Package `.openai/hosting.json` and the configured static output from that
   same source state, excluding `.git` and unrelated files. Use the Sites
   packaging helper when available; otherwise create and validate a tar archive
   containing `.openai/hosting.json` and `dist/index.html`. Save a version with
   the archive and exact pushed SHA.
5. Deploy the returned saved version. New sites start owner-private; preserve
   existing access on updates. Use the private deployment operation only for
   known owner-private sites. Follow current tool instructions for other access
   modes; publishing is not permission to broaden the audience.
6. Poll a nonterminal deployment until success or failure. On success, return
   the server's final URL and state who can open it. A private URL is not a team
   handoff until the intended reviewers have access. Do not generate a bypass
   token or change sharing just to inspect the page.

For an existing packet, reuse its directory, site, and URL. If publication fails,
retain the site/version identifiers for recovery and report the failing step
alongside the finished local file.

### Verify and hand over

Reuse evidence already gathered. When more is needed, read the repo's
`.claude/commands/qa.md` if present and run the relevant commands. Capture UI
when a visual claim needs it; nonvisual work does not require visual-test.
Distinguish observed results from proposed behavior and label illustrations.

Open the document with an available browser tool. Check wide/narrow layouts,
decision anchors, and image readability. For self-contained HTML, check image
loading without external network access or sibling assets. If browser access or
hosted authentication prevents inspection, report that exact gap; successful
publication alone does not prove the page rendered correctly.

Hand over the hosted **link** (or a clickable absolute local file path for local
output), plus a short orientation: the first frame to inspect and the calls
needed. A local path or localhost address is not a hosted URL. Keep local files
available after handoff. Do not claim an agent renders HTML inline.

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
 🔗 <published URL or clickable local HTML link>
 🧾 evidence      9 live runs · 2 clusters · 11 captures
 🖼 frames        8 (3 proof · 5 decision)
 ⚖️ decisions     5 open for you
 first look: frame 01 — <why that one>
```
