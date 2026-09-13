---
description: Evidence-driven comparison of how relevant products handle a problem, from OSS implementation details to product UX and market positioning
argument-hint: "[implementation|product|positioning|hybrid] [question or focus]"
---

# Competitive Research — find the useful prior art

Research how relevant products handle the decision in front of us, then compare
their choices with the current approach. This is not a generic landscape dump or
a feature-counting exercise: gather only the evidence that can change the active
implementation, product, UX, or positioning decision.

Default to a read-only research report. Do not modify the product, copy code, or
expand the task into implementation unless the user asks.

## 1. Set the altitude from the current task

Read `$ARGUMENTS` and the surrounding conversation. State the concrete decision
the research should inform and choose the narrowest useful altitude:

- **Implementation:** exact runtime behavior, defaults, config precedence, data
  flow, API contracts, edge cases, migrations, or failure handling. Inspect actual
  source and tests in comparable OSS projects.
- **Product/UX:** user journey, information architecture, controls, defaults,
  states, terminology, and operator comprehension. Start with official docs and
  rendered product evidence; inspect code when it resolves an important ambiguity.
- **Positioning:** target user, category, promises, differentiation, packaging,
  pricing, and proof. Use current first-party product and marketing sources.
- **Hybrid:** combine only the layers needed for the decision. Do not research
  marketing because the task is a parser detail, or reverse-engineer internals for
  a messaging question.

Honor an altitude the user names explicitly. Otherwise infer it from the active
decision, and say what you chose so the user can correct the scope early.

If comparing against work in the current repository, inspect that code, diff, or
design first. Describe what it actually does rather than relying on a ticket,
prior summary, or intended behavior.

## 2. Define comparison axes before searching

Choose a small set of decision-relevant axes. Examples include source of truth,
precedence, fallback, user override, ambiguity handling, observability, backwards
compatibility, setup cost, and failure UX. For positioning work they may instead
be audience, problem framing, promise, proof, packaging, and differentiation.

Keep the axes specific enough that evidence can answer them. Avoid broad columns
such as "features" or "ease of use" unless the user explicitly wants a landscape.

## 3. Select a representative comparison set

Search rather than relying on recalled names. Usually inspect 3–6 products:

- direct peers that solve the same job;
- the upstream or de facto standard when it shapes the contract;
- one adjacent product only when it offers a genuinely useful alternative pattern.

Prefer representative behavior archetypes over a long list of near-duplicates.
State why each product is in scope and note important exclusions. For a narrow
implementation question, 2–4 strong OSS comparisons are often enough. For
positioning, a somewhat broader set may be useful.

Stop when the evidence is saturated: additional products repeat an already-seen
behavior and are unlikely to change the recommendation. Do not pad the report to
hit a count.

## 4. Gather evidence at the right depth

Use current primary sources. Search snippets and generated summaries are leads,
not evidence.

For OSS behavior, prefer this order:

1. source at a named commit or release matching the relevant version;
2. tests, schemas, examples, and default configuration;
3. official documentation and release notes;
4. maintainers' issues or discussions when they explain intent or an unresolved
   limitation.

Trace only the code path needed for the active question. When semantics matter,
follow input/configuration through resolution/defaulting to the API or UI, and
check relevant error and ambiguity paths. Search for all obvious call sites before
concluding a behavior is universal.

For product, UX, or positioning, prefer current first-party docs, screenshots,
demos, pricing, and marketing pages. Use source code only when a user-visible
claim depends on behavior the public material leaves unclear.

Record the version, commit, release, and research date when behavior may vary.
Link to exact files/lines or permanent commit URLs when possible. If docs and code
disagree, report the discrepancy and treat the shipped code for the relevant
version as authoritative. Say "not found after checking X and Y," not "unsupported,"
when absence cannot be proved.

Clearly distinguish:

- **Observed:** directly supported by code, docs, or product evidence.
- **Inferred:** a reasonable conclusion from multiple facts.
- **Claimed:** the vendor or project says it, but it was not independently verified.

## 5. Compare choices, not popularity

For each product, explain:

- the behavior relevant to the active axes;
- where that behavior lives and how strong the evidence is;
- the tradeoff it makes and the context in which it is sensible;
- any version, deployment, licensing, or evidence caveat that affects comparison.

Then compare it with the current approach. Do not treat majority behavior as best
practice. Judge which behavior is better for the actual users and constraints:
correctness, predictability, setup burden, operability, compatibility, product
clarity, and implementation complexity. Different contexts may justify different
winners; say so explicitly.

Separate:

- a clearly better change worth adopting now;
- a useful hybrid or small first step;
- an idea that is valid but out of scope;
- a behavior that should not be copied here.

Do not turn uncertain or weakly evidenced differences into implementation work.
If reuse or close adaptation of source is recommended, call out license
compatibility before suggesting copied code.

## Output

Consider `/review-packet` when an open decision depends on comparing substantial
source excerpts, product captures, or competing tradeoffs. Reuse existing evidence
and any packet already prepared; do not research more merely to populate one.
Keep the recommendation in the response and skip the packet for a simple answer.
Prepare local-only output unless publication is already authorized.

Lead with the decision the research informs and the recommended direction. Then
provide:

1. **Scope and method** — altitude, axes, products, versions/date, notable limits.
2. **One summary per product** — behavior, evidence, rationale/tradeoff, and how it
   compares with the current approach.
3. **Compact comparison** — a table when several products map cleanly across the
   same axes; otherwise use concise prose.
4. **Recommendation** — keep, adopt, hybridize, or defer, with confidence and the
   smallest worthwhile next step.
5. **Open questions** — only decisions that evidence cannot settle.

Place citations next to the claims they support. End with a short ledger:

`🔭 competitive-research · <altitude> · <N> products · <N> primary sources · recommendation: <keep|adopt|hybrid|defer>`
