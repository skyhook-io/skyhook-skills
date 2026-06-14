---
description: Product/design/UX critique — question what should be built and how users will perceive it, not just whether the code is correct
argument-hint: "[plan|ui|pr] [focus]  (default: auto-detect stage; gated to product/UI-facing work)"
---

# Product Review — critique *what* & *how*, not just *whether*

Forces product/design/UX thinking: is this the **right thing to build**, is it the
**right shape**, and will the user actually **understand and succeed** with it? It
counters the default failure mode where the agent optimizes implementation details
of something that may be the wrong thing, or the wrong UX.

This is a **critique, not a checklist** — surface the taste/product calls for the
user (the founder) to decide; **don't silently "fix" them**. Apply `/simple`'s
"don't ping-pong with the reviewer" rule — product critique is the most tempting
place to thrash. **A beautiful implementation of the wrong thing is still wrong:**
lead with premise/journey problems, not pixels.

## When it runs
- **Manually:** anytime — `/product-review [focus]`.
- **Plan stage** (via `/plan-loop`): pre-flight, before code — premise, journeys,
  IA, scope. Fixes are cheapest here.
- **Review stage** (via `/review-loop`'s intent/design altitude): on the rendered
  UI — lean on `/visual-test` for live screens.
- **Gated by relevance:** product / UI-facing / user-perceived work only. Pure
  backend / refactor / infra → skip and say so. Judge the *actual* change.

## How to think — force the mindset, don't go with the flow
Take a skeptical product+design lead's voice. Question the premise and the chosen
shape **before** evaluating execution. Work these passes:

### 1. Premise — what is this *actually* for?
- What real user job does this serve? Is the feature the right product, or a
  literal reading of a ticket? What would the 10× version look like?
- State a **scope decision:** expand (dream bigger) · selective · hold · reduce
  (MVP only) — and why.

### 2. Journeys — coverage, ranked (forcing function)
- List the **8–10 most important user journeys** that touch this area.
- Rate **0–10** how well this change serves each. Name the **weakest** and why.
- Are we moving a critical journey, or polishing a peripheral one?

### 3. UX shape — interrogate the decisions
- For each surface/control: is this the right shape? **One card or two? Merged or
  separate control?** Does the grouping match the user's **mental model** — or just
  the data model / API shape?
- Is there a simpler arrangement the user would grasp faster?

### 4. Comprehension — will *this* user get it?
- Who's the target user (for a domain-heavy tool, often a **non-expert** in that domain — e.g. a non-k8s-expert operator for a Kubernetes UI)? Will they
  understand the words, labels, and what action to take?
- Does the screen give enough **context to act** — what this is, why it matters,
  what happens when they click? Where's the jargon that needs plain language or a
  tooltip?

### 5. States & robustness
- Enumerate **loading / empty / error / partial / edge** explicitly. What does the
  user see with no data, too much data, or on failure?

### 6. AI-slop & design-system
- Flag lazy generic patterns (icon-cards, gradient hero, dump-the-fields form).
- Does it align with the project's established patterns + design tokens (its design doc, e.g. **DESIGN.md**), or
  invent inconsistent ones?

## Output
Per dimension, a **0–10 score + one line on "what a 10 looks like"** — quantify the
gap, don't wave at it. Then findings triaged by severity:
**[Blocker]** wrong thing / unusable · **[High]** real UX or comprehension harm ·
**[Medium]** worth improving · **[Nitpick]**.

Describe **impact, not pixel-fixes** — "the two cards fragment one decision so the
user hunts," not "merge into one card with `p-4`." Lead with anything at the
**premise or journey** level.

Close with **the taste/product calls for the user** (you decide these) and a
one-line scoreboard: `🎯 product-review · blockers B · high H · weakest journey: <X>`.
