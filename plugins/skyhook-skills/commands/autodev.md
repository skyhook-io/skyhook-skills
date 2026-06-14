---
description: Autopilot — plan → implement → review → PR → converge, running the whole chain end-to-end and stopping only at real decisions
argument-hint: "[--auto] <task>"
---

# Autodev (autopilot)

Run the **entire** development chain in one invocation instead of you running
`/plan-loop` → `/review-loop` → `/pr` → `/fix-pr-loop` by hand and waiting
between each. This is a **thin conductor** — every phase is an existing command;
your edits to those commands flow through here automatically.

## Prime directive
**Do not hand control back between phases.** Execute the chain to completion in
one run. The whole point is one command, not six. Pause **only** where the mode
below says to — otherwise keep going.

## Modes
- **Default (collaborative):** make progress autonomously, but **stop and ask**
  at genuine decision points — ambiguous intent, product/UX calls, architecture
  forks, scope changes, and anything triage marks **Discuss**. The plan is
  **gated** (you sign off before code).
- **`--auto`:** make those product/direction calls yourself, **log each in
  `NOTES.md`** (Assumptions/Decisions), and keep going. You review once, at the
  end. The plan gate is **skipped** (assumptions logged instead).

  **Hard ceiling — always stop and ask, even in `--auto`:**
  1. Prod / deploy / DB schema or data migrations
  2. External publish or money (npm publish, emails, public-facing, billing, spend)
  3. Security, auth, secrets, crypto, RBAC posture
  4. Breaking a public/library API (your published package exports, e.g. `@your-scope/*`) or deleting/
     overwriting files not created in this run

## Caller directives & per-step judgment
The chain is **defaults applied with judgment, not a fixed sequence** — decide
which phases are warranted: Does this need a full plan loop or is it small enough
to implement directly? Cross-review, or self-review enough? PR now, or more work
first? Skip what doesn't fit.

**Honor free-text steering in the invocation as an override** — caller intent wins:
- `consult codex` / `cross-review` → force the cross-model pass; `no codex` /
  `self-review only` → skip it.
- `plan only` → stop after the plan gate; `skip planning` / `just build it` → go
  straight to implement (small tasks).
- `no PR` / `local only` → stop before opening a PR; `don't converge` → skip the
  reactive bot loop.
- `thorough` / `deep` vs `quick` → scale ceremony; `focus on <area>` → scope it.

Generalize — read the directive and adjust which phases run and how.

## The chain

1. **Frame & size.** Restate the task. If it's **trivial**, skip planning — go
   straight to a light `/review-loop` and finish. Scale ceremony to the work;
   don't over-orchestrate a small change.
2. **Plan** — run `/plan-loop` (pass `--auto` through). Default: it gates for
   sign-off; `--auto`: it logs assumptions and proceeds. Ceiling decisions stop
   regardless.
3. **Implement.** Build per the approved/assumed plan. Make progress; stop on
   genuine decisions (default) or decide-and-log within the ceiling (`--auto`).
4. **Review** — run `/review-loop` (pass `--auto`): self + cross-model review →
   skeptic-triage → fix, looping until clean. Never auto-accepts a reviewer.
   For a **UI / product-facing feature** (new rendered surfaces), **lean toward
   running `/visual-test` + `/product-review` here, before opening the PR** — that's
   where "does it render, read, and serve the user" gets caught. Recommended, not
   required; a skip is fine when the change is small or non-visual, but it must be a
   **stated decision** (see hand-back), never silent. Don't open the PR blind to its
   own rendered result on a feature whose value *is* the UI.
5. **PR** — verify with the repo's `/qa` (type-check/tests, and visual-test only
   if a UI change warrants it; falls back to plain build/test detection if no
   `/qa`). Skip if `/review-loop` just ran `/qa` green this round. If green, open
   the PR with `/pr`. Stop on failing checks. **Never merge.**
6. **Converge** — run `/fix-pr-loop`: wait for CI + Bugbot/CodeRabbit/AI
   reviewers, triage each comment skeptically, fix the real ones, push, repeat
   until settled or capped.
7. **Hand back.** Summarize: what was built, decisions made, **assumptions taken
   (`--auto`, from `NOTES.md`)**, reviewer verdicts (Fix/Skip with evidence),
   anything still **open**, and the PR link.

## Cross-cutting rules (inherited, restated)
- **Triage every reviewer — self, Codex, bots — skeptically. Never auto-accept;
  cite evidence on Skips.** Don't ping-pong with reviewers (`/simple`'s rule).
- **Review at altitude before details.** At the plan gate and every review pass,
  judge whether this is the right thing to build and well-designed (approach,
  architecture, UI layout, user journey) — not just whether the code is correct.
  A clean implementation of the wrong thing is still wrong: surface intent/design
  problems to the user instead of optimizing within a design that shouldn't ship.
- **Cross-review only when nontrivial.** Agents are smart about tools — be smart
  about when to spend a reviewer.
- **Every loop caps and reports at the cap.** Never loop silently; never proceed
  silently past a blocker — surface it.
- **Never** merge, deploy, push to `main`, hard-`--force`, or stage unrelated
  files. PRs are fine; shipping is the user's call.

## Progress output + run summary (narrate the autopilot)
Make the run scannable: announce each phase with a header line carrying its
headline number inline — same greppable glyph set every run: 🔭 scope · 🧭 plan ·
🤝 plan cross-review · 🔎 self-review · 🔵 Codex review · 🟣 Claude review ·
⚖️ triage · 🔧 fix · ✅ qa · 📤 PR · 🤖 converge/bots · 📋 summary
(e.g. `### ⚖️ TRIAGE · 5 fix · 7 skip · 1 discuss`).

Close (step 7) with one run-summary ledger spanning the whole chain, so the user
can audit the autopilot at a glance:

```
📋 autodev · <branch>
 🔗 PR [#910](https://github.com/your-org/your-repo/pull/910) · OPEN · checks 5 ✓ · 1 pending (Backend) · mergeable
 🧭 plan          settled in 2 cycles · 🤝 codex 4 raised → 2 folded · 2 rejected · gate: approved
 🔧 implement     <n> files · <one-line what was built>
 review · round 1   🔎 self 4 · 🟣 claude 6m · 9 → ⚖️ 7 fix · 6 skip · 1 discuss → 🔧 5 applied
 review · round 2   clean
 ✅ qa            tsc ✓ · test ✓ · visual-test skipped
 📤 PR            #<n> opened
 🤖 converge      bugbot 4 → ⚖️ 3 fix · 1 skip → 🔧 3 applied · pushed · CI ✓
 result: shipped-to-PR · plan 2 cycles · review 2 rounds · 11 fixed · 7 skipped · 1 open
 assumptions (--auto):
   • <decision you made on your own + why>
 open for you:
   • [discuss] <question needing your call>
```

Always include the **triage breakdowns** (your skepticism signal), the **result
line**, **assumptions** (in `--auto`), and **open items**. Durations only where
they matter (cross-review, CI waits). **The `✅ qa` line must state visual-test
explicitly** — ran ⇒ link the screenshot directory as an **absolute path** (or
`file://`, not relative/`~`, so it linkifies); skipped ⇒ `visual-test: skipped
(<reason>)`. **Likewise state `product-review` status** for UI/product-facing work
(ran ⇒ key verdicts; skipped ⇒ why). Never leave either ambiguous — a silent skip
is the bug.

**When a PR is open, lead with a clickable `🔗 PR` line** — render the number as a
**markdown link** `PR [#910](url)` (clean clickable "#910" in the Claude/Codex
markdown TUI; bare absolute URL is the plain-terminal fallback), plus state
(`OPEN`/`DRAFT`), checks rollup (counts + names of any pending/failing), and
mergeable/`CONFLICTS` (`gh pr view <n> --json
url,state,isDraft,mergeable,statusCheckRollup`). If checks are still running, say
`CI pending` on the result line and keep the link visible.
