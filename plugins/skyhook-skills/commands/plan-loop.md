---
description: Draft a detailed plan, cross-review it with the other agent, triage skeptically, iterate until settled, then gate for sign-off
argument-hint: "[--auto] <task>"
---

# Plan Loop

Turn a task into a settled implementation plan **before** any code — draft →
cross-review with the other agent → skeptic-triage the critique → revise → gate.

The steps are defaults applied with judgment. **Honor free-text steering in the
invocation as an override** — e.g. `skip cross-review` (trust the draft),
`two cycles min` (iterate harder), `focus on the data model`, `no gate` (proceed
without sign-off). Caller intent beats the defaults below.

## Step 1 — Draft a real plan

**First, challenge the premise, not just the execution:** is this the right thing
to build, and the right approach? If a fundamentally simpler or different design
serves the goal better — or if the idea itself is questionable — say so *before*
planning the build. Don't produce a polished plan for the wrong thing. **For
product / UI-facing work, run `/product-review` here** (premise + top user journeys
+ scope decision) — the cheapest place to catch "wrong thing" or "wrong UX."

Then read the relevant code first; anchor every claim in evidence. Follow your
plan conventions:
- **Cite `file:line`** for every factual claim about how things work today.
- **Split by confidence:** **Certain** / **Confident** / **Needs-input** — don't
  blur them.
- **Give real opinions** — recommend an approach and say why; name the tradeoffs
  and the things that *won't* compress. Don't rubber-stamp.
- Lay out the build sequence: files to add/modify, key decisions, risks, test
  strategy.

## Step 2 — Cross-review with the other agent (nontrivial plans)

Hand the plan to Codex for an independent critique — it has no stake in your
draft. Foreground, long timeout:

```bash
codex exec "Critique this implementation plan as a skeptical senior engineer. FIRST challenge the premise: is this the right thing to build and the right approach, or is there a fundamentally simpler/different design? Then find flawed assumptions, missing steps, hidden complexity, and risks. Don't just check internal consistency — question whether the whole direction is correct. Be specific; challenge it, don't rewrite it. PLAN:\n\n<the full plan>"
```

(Trivial plans skip this. This is Claude→Codex, which has no export gate.)

## Step 3 — Triage the critique skeptically

**Do not auto-accept Codex's feedback** — apply `/triage-findings`: verify each
point against the actual code/reality, integrate the valid ones, reject the weak
ones **with a stated reason**. A cross-model reviewer is often right about blind
spots and often wrong about things already handled. You decide, with evidence.

## Step 4 — Revise & iterate

Fold confirmed points into the plan. Repeat Steps 2–3 until the critique stops
surfacing substantive issues — **cap at 2 cross-review cycles**, then move on and
note any residual disagreement.

## Step 5 — Gate

- **Default:** present the settled plan + every **Needs-input** question, then
  **STOP for sign-off**. This is the highest-leverage checkpoint — do not start
  coding until the user approves direction and resolves the open questions.
- **`--auto`:** resolve **Needs-input** with your best judgment, **record each
  call in `NOTES.md`** (Assumptions/Decisions), and proceed — *unless* a decision
  hits the autonomy ceiling (prod/deploy/data migrations · external publish/money
  · security/auth/secrets · breaking public API or destructive file ops), in
  which case stop and ask regardless of mode.

## Progress output + summary (make it scannable)
Announce phases with scannable headers carrying the headline inline — same glyphs
every run: 🧭 plan · 🤝 cross-review · ⚖️ triage · 🚦 gate. Close with a short
ledger:

```
📋 plan-loop · <task>
 🧭 plan          drafted · <n> open (Needs-input) questions
 🤝 cross-review  2 cycles · 5 raised → 3 folded · 2 rejected (cited)
 🚦 gate          awaiting sign-off   (or: assumptions logged → NOTES.md)
 open for you:
   • <Needs-input question>
```

When invoked standalone, end after the gate. When invoked by `/autodev`, the
approved/assumed plan flows straight into implementation.
