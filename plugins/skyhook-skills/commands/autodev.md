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

**"The chain ran" is not "done."** A run finishes when the PR meets the
[Definition of done](#definition-of-done) on its final head — or when you hand
back with every unmet item named. If the user's obvious next question ("does
this pass `/product-review`?", "any open PR comments?") would expose a gap, you
stopped early.

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
- `consult codex` / `consult cursor` / `cross-review` → force the cross-model pass
  (and pick that reviewer); `no cross-review` / `self-review only` → skip it.
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
   If you hand pieces to workers (subagents, `codex exec`), follow
   [Delegating to workers](#delegating-to-workers).
4. **Review** — run `/review-loop` (pass `--auto`): self + cross-model review →
   skeptic-triage → fix, looping until clean. Never auto-accepts a reviewer.
   For scenario-sensitive changes — user-facing copy, diagnostics/remediation,
   detector precision, error classification, permissions/security posture, or UI
   states — require the review-loop scenario ledger before treating the PR as
   reviewed: scenario, expected final behavior/copy, source-of-truth evidence,
   self-review verdict, cross-review status, test/live proof, and open decision.
   Cross-review status can be `skipped: <reason>` when the cross-model pass was
   intentionally skipped. "Review loop ran" is not enough.
   For **user-visible changes** (UI, copy, CLI output, errors, diagnostics,
   workflows), **run `/product-review` here, before opening the PR**, and triage
   its findings like any other reviewer's. It is part of the Definition of done,
   not an optional extra: if the surface changes after it ran, re-check the
   changed parts before calling the PR done. Scale it to the change: a wording
   fix or single-state change gets a focused pass on the affected copy, journey,
   and states, not the full journey ranking. Run `/visual-test` when the rendered
   result is worth capturing. Don't open the PR blind to its own rendered result
   on a feature whose value *is* the UI. Non-user-visible work records
   `product-review: n/a (<why>)`.
5. **PR** — verify with the repo's `/qa` (type-check/tests, and visual-test only
   if a UI change warrants it; falls back to plain build/test detection if no
   `/qa`). Skip if `/review-loop` just ran `/qa` green this round. If green, open
   the PR with `/pr`. Stop on failing checks. **Never merge.**
6. **Converge** — run `/fix-pr-loop`: wait for Bugbot/CodeRabbit/AI reviewers,
   triage each comment skeptically, fix the real ones, push, repeat until settled
   or capped. Check CI as you go and act on failures, but don't wait for slow
   checks while known work remains; full CI is waited on once, at the end.
7. **Consider a review packet.** When the work would be hard for the reviewer to
   judge from the PR alone — a large or multi-PR change, a rendered UI surface,
   captured screenshots or live output worth showing, or open product calls you
   are handing back — run `/review-packet`. It is a judgement call, not a step:
   skip it for ordinary changes a diff explains on its own, and say you skipped it.
8. **Done audit.** Check every item of the
   [Definition of done](#definition-of-done) against the **final head SHA**,
   with evidence. Fix any gap you can close yourself — that is more work in this
   run, not a hand-back item — then push, let the reviewers settle, and
   re-audit. Batch the audit's fixes into one push. Cap: 2 audit rounds; after
   that, hand back as `not done` with the gaps named. Waiting for CI on the final
   head is the audit's last step, after everything else is done.
9. **Hand back.** Summarize: what was built, decisions made, **assumptions taken
   (`--auto`, from `NOTES.md`)**, reviewer verdicts (Fix/Skip with evidence),
   scenario ledgers for scenario-sensitive work, practical risk/blast radius plus
   mitigation/test proof for nontrivial changes, the done-audit result, anything
   still **open**, and the PR link. Do not call an item complete if the final
   head has not been reviewed and verified at the level implied by the task; say
   exactly which proof is missing and keep moving to other independent items when
   appropriate.

## Definition of done
A PR is **done** only when every item holds **on the final head SHA** — not on
an earlier commit that later fixes changed. Mark each item `✓` with its evidence,
`n/a` with a reason, `⏸` when it waits only on a named user decision, or `✗`.
Any `✗` you can fix is work, not a report.
Scale it to the task: for a trivial change most items are a one-line `✓` or
`n/a`. With `no PR` / `local only`, items 7–9 are `n/a` and item 8's inventory
is skipped; say so.

1. **The ask is fully delivered.** Re-read the original request and the plan.
   `✓` means every requirement and plan item is built, or its removal was
   approved by the user (at the plan gate or later). A deferral you chose
   yourself — including one logged as an `--auto` assumption — is not `✓`: mark
   it `⏸` and name the deferral for the user to approve or reject. No stubs or
   unmentioned "phase 2".
2. **The final code was reviewed.** `/review-loop` (self + cross-model when
   nontrivial) covered the final state. Commits after the last review — bot
   fixes, audit fixes — got at least a self-review of that delta; substantive
   ones get the full loop.
3. **User-visible work passes `/product-review`** on its final state, with its
   findings triaged (Fix/Skip with evidence). Scenario-sensitive work also has
   its scenario ledger complete.
4. **It works when used, not just when tested.** Exercise the change through
   the surface a user or operator touches (UI, CLI, API, generated output) and
   probe for fake success: vary the input, refresh or re-run to confirm it
   persisted, try empty and error states, and confirm each action does real work
   rather than showing a success message. Record what you ran and saw. When the
   surface can't be exercised locally, say so and name the missing proof.
5. **Tests and docs follow the change.** Bug fixes have a regression test where
   one fits; new behavior is covered at a meaningful seam; user-visible changes
   update the relevant docs, README, config reference, or help text.
6. **No leftovers in the diff.** No TODO/FIXME placeholders, debug output,
   commented-out code, or dead old paths added by this PR. Old paths are deleted
   unless a named contract needs them (see `/simple` #8).
7. **CI is green on the final head.** Every required check passed on that SHA.
   A slow scanner still pending (per `/fix-pr-loop`'s cap) is named, not hidden.
   This is checked at the end: don't stall earlier work waiting for CI.
8. **Zero unaddressed PR feedback.** After the final push, reviewers have
   settled on the final head and every item from every source in `/fix-pr-loop`'s
   feedback inventory — review threads, review bodies, PR conversation comments
   (including ones bots edit in place), check-run output, human comments — is
   closed: fixed, answered with a reason, or listed as a decision for the user.
   An unresolved bot thread that still looks open is not done.
9. **The PR explains the final state.** Title and body match the full diff (per
   `/pr`); UI changes show the result — a few before/after images or a short
   video, uploaded per `/pr`'s "Screenshots and video" — or say why no capture
   was safe to upload. The PR contains no local paths and nothing sensitive;
   local paths belong in your hand-back summary, and the full evidence set in a
   review packet. The branch merges cleanly into its base and contains no
   unrelated files.
10. **Loose ends are visible.** Deferred work, follow-ups, and open decisions
    appear in the hand-back, not only in commit messages or `NOTES.md`.

**Honest-answer test.** Before declaring done, answer the questions the user is
likely to ask next, with evidence: *Does this pass `/product-review`? Are there
open PR comments? Would `/review-loop` on the final head find anything? Is every
part of what I asked done? Is CI green on the last commit? Does it actually work
when I use it?* "Probably" or "I think so" is a `✗`: go find out.

**Result states** (for the run summary's result line):
- `done` — every item `✓` or `n/a`.
- `waiting on you` — no `✗`, and at least one `⏸` naming the decision needed.
- `not done` — one or more `✗`, each named with what is missing.
- `blocked` — a ceiling item or external blocker stopped the run.

## Delegating to workers
When you hand implementation, fixes, or read-heavy exploration to a worker (a
subagent or `codex exec`), you stay responsible for the result:

- **Write a complete work order.** The worker starts with no context. Give it
  the goal, repo and key paths, constraints, non-goals, the exact proof command,
  and the report shape. `/handoff` has a template.
- **Pair every hard rule with an exit.** A worker boxed in by a rule it can't
  meet will satisfy its letter — weakening a test, editing a baseline, renaming
  identifiers to shrink a bundle — and still report green. For each hard rule,
  add: "if you can't meet this honestly, stop and report the numbers and why; do
  not work around it." Treat that stop report as a successful run.
- **Verify the code, not the report.** Worker summaries are accurate but
  incomplete. Read the diff; check files it was told not to touch, test-helper
  and baseline edits, and commits you didn't ask for.
- **One work order per fresh session.** Don't feed a new task to a long-lived
  worker session; resume only to continue the same order.
- **One writer at a time.** Before editing or committing, confirm no worker is
  still running against the same files (`pgrep -fl "codex exec"`, running
  subagents). A worker that keeps looping can overwrite your fixes.

## Optional tools — use when warranted
Beyond the chain's phases, reach for these when they would change a decision,
not by default:

- **`/competitive-research`** — when a design, UX, or implementation choice
  depends on how comparable products handle it: a new surface, an unfamiliar
  domain, a convention you'd otherwise guess at, or a positioning question.
  Scope it to the specific decision. It fits at planning, but also mid-run when
  a question comes up that planning didn't anticipate. Skip it for
  well-understood, mechanical, or internal-pattern work. If it ran, note what it
  changed in the hand-back.

## Cross-cutting rules (inherited, restated)
- **Triage every reviewer — self, Codex, bots — skeptically. Never auto-accept;
  cite evidence on Skips.** Don't ping-pong with reviewers (`/simple`'s rule).
- **Review at altitude before details.** At the plan gate and every review pass,
  judge whether this is the right thing to build and well-designed (approach,
  architecture, UI layout, user journey) — not just whether the code is correct.
  A clean implementation of the wrong thing is still wrong: surface intent/design
  problems to the user instead of optimizing within a design that shouldn't ship.
- **Assess risk / blast radius proportionally.** For nontrivial changes, identify
  affected surfaces, likely failure modes, mitigation/test proof, and residual
  risk. A low-risk copy/test-only change can be one sentence; behavior, UI,
  auth/security, data, or diagnosis/remediation changes need explicit coverage.
- **Cross-review only when nontrivial.** Agents are smart about tools — be smart
  about when to spend a reviewer.
- **Every loop caps and reports at the cap.** Never loop silently; never proceed
  silently past a blocker — surface it.
- **Never pass a gate by gaming it.** The same rule applies to you as to workers:
  no weakening or skipping tests, no loosening thresholds, no lint suppressions,
  no editing snapshots, baselines, or golden files to hide a failure, no
  resolving a PR thread you didn't address. Updating an expectation because the
  behavior intentionally changed is fine: say so in the PR and review that diff
  like code. When a gate can't be met honestly, stop and report it.
- **Changes you didn't make belong to someone else.** Unexpected edits in the
  tree come from the user or another agent: don't revert or stage them; work
  around them in your own scope, and stop and ask if they conflict.
- **Never** merge, deploy, push to `main`, hard-`--force`, or stage unrelated
  files. PRs are fine; shipping is the user's call.

## Progress output + run summary (narrate the autopilot)
Make the run scannable: announce each phase with a header line carrying its
headline number inline — same greppable glyph set every run: 🔭 scope · 🧭 plan ·
🤝 plan cross-review · 🔎 self-review · 🔵 Codex review · 🟣 Claude review ·
⚖️ triage · 🔧 fix · ✅ qa · 📤 PR · 🤖 converge/bots · 🏁 done audit · 📋 summary
(e.g. `### ⚖️ TRIAGE · 5 fix · 7 skip · 1 discuss`).

Close the **Hand back** step with one run-summary ledger spanning the whole chain, so the user
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
 🏁 done audit    8 ✓ · 1 n/a · 1 ⏸ · 0 ✗ · threads 0 open · product-review ✓ · head a1b2c3d
 result: waiting on you · plan 2 cycles · review 2 rounds · 11 fixed · 7 skipped · 1 open
 assumptions (--auto):
   • <decision you made on your own + why>
 open for you:
   • [discuss] <question needing your call>
```

Always include the **triage breakdowns** (your skepticism signal), the **done
audit** line, the **result line** (`done` · `waiting on you` · `not done` ·
`blocked`), **assumptions** (in `--auto`), and **open items**. Any `✗` in the
audit must appear under open items with what is missing, and every `⏸` with
the decision it needs. Durations only where
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
