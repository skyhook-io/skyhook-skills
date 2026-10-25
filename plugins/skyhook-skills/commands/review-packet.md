---
description: Package work for guided review — explains the change from first principles, then puts the evidence beside each claim and the open calls at the end
argument-hint: "[pr|set|design|research] [focus]  (default: auto-detect from the work in this session)"
---

# Review Packet — make the change understood, then easy to judge

A review packet is a design document with its proof attached. The reader arrives
with no context: they haven't seen the session, the ticket or the code. Before
they can judge anything, the packet has to make them understand the change: what
was wrong, what the change does, how it works, why this design, what it costs,
and what else was considered. Only then does the evidence mean anything, and only
then can the reader answer an open question with judgment instead of a guess.

This holds for every packet, not only large ones. A small change gets the same
explanation at a smaller scale, a paragraph per part instead of a section, never
a shortcut straight to evidence and questions.

Reach for this when review would otherwise mean scrolling a diff, replaying an
investigation, or taking your word for it: a PR or a **set** of related PRs, a
rendered UI change, a design or architecture proposal, competitive research. A
typo fix needs no packet.

**Prerequisite: have something to show.** Run `/visual-test`, `/product-review`,
`/review-loop` or `/competitive-research` *first* if their output is the substance.
This command packages evidence; it does not manufacture it.

## The rules that make packets work

> **1. Explain before you prove or ask.** The reader understands the change before
> they see evidence or an open question.
>
> **2. Every claim sits next to the artifact that proves it, and every dilemma gets
> its own visual slot.**

Evidence for a change the reader doesn't understand gets skimmed. A question asked
without the context to answer it gets rubber-stamped. A claim the reader can't
check asks them to trust you. Packets exist to prevent those three failures.

## Build it

### 1. Explain the change first

Order the page so it reads top to bottom for someone new to it. First, what they
need to understand the change:

1. **Orientation.** One paragraph on what changed and why it matters, and a status
   line (revision, checks, mergeability). When the page is long, add reading
   paths: the sections a short review needs, and the full order.
2. **The problem.** What was wrong or missing, shown concretely in the reader's
   terms: the real behavior before the change, with real output when you have it.
3. **The idea.** The change in a few sentences, and the rule or invariant it
   establishes.
4. **Terms.** Every word the change introduces, and any domain or session term
   the reader needs. Nothing appears before it is defined.
5. **How it works.** One concrete case walked from input to output. An annotated
   example or a diagram usually beats a description here.
6. **Where it lives.** The parts of the change, how they depend on each other, and
   the files that hold each, with sizes that separate code from tests.

Then what they need to judge it:

7. **Why this design.** The principles it follows, each tied to the failure it
   prevents.
8. **Alternatives.** The real options that were weighed, why each lost, and what
   settled it (the user's decision, a cross-model review, a measurement). Label
   options you only weighed while writing the packet. Never invent alternatives
   to fill the section.
9. **Costs and drawbacks.** What the change costs (compatibility, complexity,
   performance, migration, new failure modes), who feels it, and the mitigation.
   A packet without drawbacks is marketing.
10. **Where it runs.** Behavior in each operating context that matters: modes,
    roles and permissions, scale, newer and older clients or servers. Say how
    each was checked: live, by tests, or by tracing the code.
11. **How to review it.** A reading order through the diff and what to ask of each
    part. For a large change, say whether it splits into pieces that can be
    reviewed or merged separately, and check that the split actually builds.

Scale each part to the subject. In a small change several fold into one
paragraph; the order stays, and none is skipped because the change is small.

**Show it when seeing is faster than reading.** For each part, ask whether a
visual would let the reader grasp it quicker than prose: a flow of data or calls
across components, states and the transitions between them, what each item in a
set looks like before and after (a grid of namespaces, rows of permissions), a
dependency or layer map, a timeline of a race. Those are often far easier to
review drawn than described. Draw it in HTML/CSS or Mermaid, with real names and
values from the change, and say in a caption what the reader should notice. Skip
it when a sentence or a table is just as clear; a diagram that restates the
prose, or decorates it, only costs the reader time. Most packets need one to
three, not one per section.

### 2. Then the evidence: real, not illustrations

Prefer artifacts the work actually produced — live screenshots, real runs against
real systems, actual tool output, genuine diff excerpts. **Real material surfaces
dilemmas you would not have invented**, and reviewers can tell the difference.

Crop to the subject. A full-window screenshot hides the thing you are pointing at.
A short before/after excerpt can also illustrate the problem in section 2 of the
explanation; the full proof comes here.

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

### 5. Then the calls

After the explanation and the evidence, give each open call its own decision box:
the question, the context it depends on (pointing back to the sections that
explain it), the options, and your recommendation. When the options are shapes (a
schema, an API, a message's wording), show each one as the payload it would
produce for the same case, beside the others, with why it was designed that
way: a reader can't choose between shapes from descriptions of them. The orientation may link to
the calls so a returning reader can jump to them, but each call is argued where
the reader already has the context. Use the actual number of decisions; approval
of the change can be the only call. Do not invent dilemmas to fill a quota. If
nothing needs deciding, not even approval, write a short report instead of a
packet.

### 6. Be honest in the packet itself

- **What you could not verify**, plainly.
- Findings you **deferred**, and why — a packet that only shows wins is marketing.
- Where you and a cross-model reviewer **disagreed**, and who you think is right.
- Verdict / scoreboard at the **end**.
- State the reviewed revision and when verification was checked. Publishing a
  current evidence snapshot does not require waiting for CI: list pending or
  failing checks by name with links, and update their status later. Do not call
  the PR settled, merge-ready, or ready to ship until required checks pass on
  the final head and the required review and end-to-end verification are clean.
  Publication success is evidence that the document was delivered, not that the
  change passed its completion gate.

### Cold-reader check

Before publishing, read the whole page as someone with no prior conversation,
ticket, or domain context. At every point, they must be able to follow it with
only what came before:

- No term, code, ticket number or call number appears before it is explained.
- The problem, the idea and how it works are clear before any evidence.
- The complete user or operator journey is covered, including failure states and
  the conditions that enable an action.
- Supported scope and limits are stated: what works generically, what needs
  explicit integration, what remains unsupported.
- The design's boundaries, alternatives and costs are explained, and where future
  additions belong when extensibility matters.
- The evidence says what it proves, what is test-only or historical, and what
  remains unverified, and the calls make sense on their own.

When updating a packet, re-derive the whole narrative from the complete final
state, as `/pr` does: rewrite rather than append review-fix bullets. Keep review
history, raw logs, and exhaustive captures in supporting material; the main
narrative should stand alone. Retain decision-relevant disagreements and gaps
beside the claims they qualify.

## Components to reach for

Pick what the material needs; do not use them all.

| Component | Use when |
|---|---|
| **Walk-through**: one case, input to output | Always, at some scale: it is how the reader learns how the change works |
| **Diagram**: flow, states, before/after grid, layer map | Structure or change is easier seen than read. Not by default: skip it when prose or a table is as clear |
| **Glossary** | The change introduces terms, or the domain has terms the reader needs |
| **Layer or dependency map** | The change has parts; show what lives where and what depends on what |
| **Alternatives table** | Always when options were weighed: option, why not, what settled it |
| **Costs table** | Always: cost, who feels it, mitigation |
| **Operating-context table** | Behavior differs by mode, role, scale or version |
| **Reading order / split plan** | The diff is large or has separable parts |
| **Frame**: evidence beside prose | The default evidence unit. Screenshot/excerpt on one side, claim on the other |
| **Decision box** | Any open call — give it a distinct block, never inline prose |
| **Option payloads side by side** | A call about a data shape, an API or wording: each option's actual payload or output for the same case, the design reason behind it, and what a reader would conclude from it |
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
  restrained color, a contents list with stable section and decision anchors,
  and evidence beside each claim.
- Ground the design in the subject: borrow the product's accent and semantic
  colors so the prose and screenshots use the same visual language.
- Stack evidence and prose on narrow screens; use columns on wide screens.
  Make every evidence image click-to-expand to full size (lightbox or a plain
  link to the full-res `data:` URI both work; the no-JS link must work standalone).
  Keep substantive content accessible without JavaScript.
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

Prepare and inspect the self-contained HTML before publishing. Reuse the packet
directory from the session or the user's chosen location. Otherwise use
`${CODEX_HOME:-$HOME/.codex}/review-packets/<repo>/<packet-slug>/`, with a stable
repo identity (owner/repository when available) and subject slug. Check that
location for an existing packet before creating anything. When updating a known
published packet whose local state is missing, locate the existing site through
Sites discovery instead of creating a replacement.
The Sites tools may provide more detailed instructions; follow those. The static
route exercised for this workflow is:

1. Put the HTML at `dist/index.html`. Configure `.openai/hosting.json` with
   `{"static":{"directory":"dist"}}`, preserving existing configuration.
   The packet directory must own its Git repository: initialize it if absent,
   and verify `git rev-parse --show-toplevel` resolves to that directory. Do not
   use an enclosing application's repository for the Sites push.
2. Read that configuration before creating a site. Reuse its `project_id` on
   updates. If absent, create the site once and immediately persist the returned
   ID atomically. Never invent IDs or recreate a site to retry a failed step.
3. Commit `.openai/hosting.json` and `dist/index.html` in the packet repository;
   verify both are tracked even if a global ignore rule excludes `dist/`.
   Push that exact source state to the site's returned Git repository/branch
   using its short-lived credential and per-command authentication. Obtain a new
   credential for the existing site when absent or expired. Do not print or
   persist the credential. After a successful push, run
   `git rev-parse --verify HEAD` in the packet repository and use its full output
   as `commit_sha`.
4. Package `.openai/hosting.json` and the configured static output from that
   same source state, excluding `.git` and unrelated files. Use the Sites
   packaging helper when available; otherwise create and validate a tar archive
   containing `.openai/hosting.json` and `dist/index.html`. Save a version with
   the archive and exact pushed SHA.
5. Deploy the returned saved version. New sites start owner-private; preserve
   existing access on updates. Use the private deployment operation only for
   known owner-private sites. Follow current tool instructions for other access
   modes. Apply an audience explicitly requested by the user through the access
   tools; otherwise keep access unchanged. Publishing alone is not permission
   to broaden the audience.
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
output), plus a short orientation: where to start reading, the reading path for
a short review, and the calls needed. A local path or localhost address is not a hosted URL. Keep local files
available after handoff. Do not claim an agent renders HTML inline.

## Anti-patterns

- Opening with evidence or open questions before the reader knows what the change
  is, how it works and why it was built this way.
- Writing for someone who followed the session: undefined shorthand, ticket or
  call numbers before they are introduced, "as discussed".
- Skipping the explanation because the change is small. Shrink it instead.
- A changelog with pictures. Explain the problem, journey, and design as needed
  to support the reader's decision; do not substitute a list of implementation
  or review steps for that explanation.
- Screenshots without claims, or claims without screenshots.
- Burying the one frame that matters at position seven.
- Only wins. Defer list and "could not verify" are load-bearing.
- Re-litigating the build process. The reader wants the state and the choices, not
  the route (`/pr`'s rule applies here too).

## Progress output

Announce phases with the shared glyphs: 🔭 scope · 📖 context · 🧾 evidence ·
🖼 frames · ⚖️ decisions · 📦 publish. Close with:

```
📦 review-packet · <subject>
 🔗 <published URL or clickable local HTML link>
 🔒 access        <verified audience, or local file only>
 📖 context       problem · walk-through · 4 alternatives · costs · reading order
 🧾 evidence      9 live runs · 2 clusters · 11 captures
 🖼 frames        8 (3 proof · 5 decision)
 ⚖️ decisions     5 open for you
 start here: section 1, the problem — then <the short reading path>
```
