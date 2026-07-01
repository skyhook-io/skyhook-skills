---
description: Proactively review the current code (self + cross-model), triage skeptically, fix, update the PR — loop until clean
argument-hint: "[--deep] [--auto] [--base <ref>]  (default: branch vs main, collaborative)"
---

# Review Loop (proactive)

I generate the review and fix the code — the **proactive** counterpart to
`/fix-pr-loop` (which reacts to CI / Bugbot / CodeRabbit). Run this when you're
already far along and want the self + cross-model review → fix → update-PR cycle
to run on its own instead of you invoking `/review`, `/triage`, `/fix-findings`,
`/pr` one at a time.

This command **composes** existing procedures — it does not re-implement them:
- `/review` — self correctness review
- `/simple` — over-engineering / dead-weight audit (honor its "don't ping-pong
  with the reviewer" rule)
- `/cross-review` — cross-model review by the configured secondary reviewer (codex or cursor; nontrivial only)
- `/triage-findings` — validate every finding against the real code
- `/fix-findings` — apply confirmed fixes
- `/pr` — stage only relevant files, commit/amend, push `--force-with-lease`,
  keep the PR title/body accurate

## Modes
- **Default (collaborative):** stop and ask on anything triage marks **Discuss**
  — product/UX calls, ambiguous intent, architecture forks.
- **`--auto`:** decide those within reason and log the call; only hard-stop for
  the autonomy ceiling (prod/deploy/data migrations · external publish/money ·
  security/auth/secrets · breaking public API or deleting files you didn't
  create). You review at the end.

## Caller directives & per-step judgment
The steps below are **defaults you apply with judgment, not a fixed checklist** —
decide each time whether each is warranted: Is a PR wanted right now, or should
this stay local? Is the change nontrivial enough to cross-review, or is a
self-review enough? Does QA need visual-test? Skip what doesn't fit; don't run a
step just because it's listed.

**Honor free-text steering in the invocation as an override** — the caller's
intent beats the heuristic. Examples (generalize beyond them):
- `consult codex` / `consult cursor` / `second opinion` → run the cross-model pass
  (and pick that reviewer for this run) even if the change looks trivial.
  `self-review only` / `skip cross-review` → skip it.
- `no PR` / `local only` → review + fix but don't create/update a PR.
- `review only` / `don't fix` → report findings, skip the fix step.
- `thorough` / `deep` → raise ceremony (deep review, cross-review, more rounds);
  `quick` → lower it.
- `focus on <area>` → narrow the review's *attention* to that area.
- **Scope** (which diff): `whole pr` / `full branch` is the **default**;
  `just my latest` / `--uncommitted`, `since <ref>` / `--base <ref>`, or
  `this commit` / `--commit <sha>` narrow it (see Step 1). Scope = *which commits*;
  focus = *what to look at within them*.

## Loop

Each round:
1. **Scope — default to the WHOLE PR, and announce it.** Unless told otherwise,
   review the **full branch delta** (`git diff main...HEAD` — *all* commits — plus
   any uncommitted changes), **not** just the latest commit or the small local
   delta. A review loop means "is this change good as a whole," not "check what I
   just typed." Announce the resolved scope in the 🔭 banner (e.g.
   `🔭 SCOPE · PR #910 · 14 commits · +656/−121` vs `🔭 SCOPE · 3 uncommitted files`)
   so the user can redirect before you spend a cross-review on the wrong slice.
   Scope overrides (the caller can narrow/redirect):
   - `whole pr` / `full branch` → `main...HEAD` + uncommitted **(default)**
   - `just my latest` / `--uncommitted` / `wip` → only staged+unstaged+untracked
   - `since <ref>` / `--base <ref>` → delta vs that base
   - `this commit` / `--commit <sha>` → just that commit

   If which slice the user wants is genuinely ambiguous **and** it materially
   changes the review, state your assumption in the banner or ask — never silently
   narrow to a convenient small delta.
2. **Review at two altitudes — intent before details.**
   - **Right thing / right design FIRST:** does this serve the real goal, is the
     approach/architecture sound, and (for UI) does the layout + user journey hold
     together end-to-end (per the project's design doc) — or is it a clean solution to the wrong
     problem? **A clean implementation of the wrong thing is still wrong:** if
     intent or design is off, raise THAT first and loudest and surface it for the
     user — don't polish details inside a design that shouldn't ship. **For UI /
     product-facing changes, run `/product-review`** as this altitude pass
     (journeys, comprehension, UX shape, AI-slop).
   - **Risk / blast radius:** for nontrivial changes, briefly assess what can
     break, who or what is affected, and whether the tests, live checks,
     guardrails, or rollback path actually cover that risk. Keep it proportional:
     one line is enough for low-risk copy/test-only changes.
   - **Then line-level:** run `/review` (`--deep` ⇒ `/pr-review-toolkit:review-pr
     all`) and `/simple` for correctness, bugs, and dead weight.
   - **Cross-model pass** (nontrivial only): run `/cross-review` — the configured
     secondary reviewer (codex or cursor; set in `~/.claude/skyhook-skills.json` or
     `consult <x>`). Have it *challenge the approach/design*, not just hunt defects
     (codex: use its adversarial mode). Trivial diffs skip it — don't ceremony-ize a typo.
   - **Scenario ledger for scenario-sensitive work:** if the change affects
     user-facing copy, diagnostics, remediation guidance, detector precision,
     error classification, permissions/security posture, or UI states, first
     derive the scenario list from the ticket + code paths + tests. The review is
     not complete until each scenario has a row with scenario, expected final
     behavior/copy, evidence source, self-review verdict, cross-review status,
     tests/proof, and open decision. Cross-review status is either the verdict or
     `skipped: <reason>` when the cross-model pass was intentionally skipped. A
     blanket "review loop ran" is invalid for these PRs.
3. **Triage skeptically** — pool every finding (self, `/simple`, Codex) and apply
   `/triage-findings`: read the real code at each `file:line`, **never
   auto-accept**, cite evidence on every Skip. Surface reviewer-requested items
   as tension rather than silently removing them (`/simple`'s rule).
4. **Fix** the confirmed **Fix** verdicts via `/fix-findings`.
5. **Update the PR** if one exists — `/pr` (relevant files only,
   `--force-with-lease`, accurate title/body). No PR yet ⇒ leave commits local
   and say so; do not open one here (that's `/autodev`'s job).
6. **Repeat** until a round yields **no new valid Fix verdicts** and all
   required review artifacts for this scope are complete (for example, the
   scenario ledger for scenario-sensitive work and the risk/blast-radius note for
   nontrivial changes).

## Stop / caps
- **Converged:** a clean round (only Skips) **and required review artifacts
  complete** → stop, summarize.
- **Cap:** default **3 rounds**; report and stop rather than looping silently.
- **Stuck:** the same finding survives **2 fix attempts** → stop and surface the
  blocker.
- **Decision:** a genuine product/scope question → ask (default) or log + proceed
  within the ceiling (`--auto`).

## Repo-aware verification — `/qa`
Repos own their verification via a `/qa` command (`.claude/commands/qa.md`). When
a change is substantial enough to be worth verifying, run `/qa` and let it pick
the checks that fit the *delta* — most rounds that's just type-check/tests (or
nothing for a trivial fix). Heavier checks like a repo's `/visual-test` are
**reserved for self-contained UI changes worth a capture and skipped by default**
otherwise (logic, utils, server, Go-only, refactors, types, copy → no
visual-test). When in doubt whether a UI change warrants it, ask rather than
auto-run. No repo `/qa` ⇒ fall back to plain build/test detection.

## Safety
Never on `main`/`master` (ask for a feature branch). Never merge. Never resolve
conflicts automatically. `--force-with-lease` only. Stage only relevant files;
preserve unrelated untracked files.

## Progress output (make the run scannable)
Announce each phase with a header line that carries its **headline number inline**,
so scrolling back reads the story without expanding anything. Same greppable glyph
set every run: 🔭 scope · 🔎 self-review · 🔵 Codex review · 🟣 Claude review ·
⚖️ triage · 🔧 fix · ✅ qa · 📤 PR · 🤖 converge/bots · 📋 summary. E.g.:

`### 🔵 CODEX REVIEW · 8m · 13 findings`
`### ⚖️ TRIAGE · 5 fix · 7 skip · 1 discuss`
`### 🔧 FIX · 5 applied · history.go, meaningfulchanges.go (+2)`

## End with — run-summary ledger (audit trail)
Close the run with a compact ledger so the user can scan what happened and audit it
later — one line per step, headline metric inline, grouped by round:

```
📋 review-loop · <branch>
 🔗 PR [#910](https://github.com/your-org/your-repo/pull/910) · OPEN
            checks 4 ✓ · 2 pending (Backend, Cursor Bugbot) · mergeable
 round 1
   🔎 self-review     6 findings
   🔵 codex review    8m · 13 findings
   ⚖️ triage          5 fix · 7 skip · 1 discuss
   🔧 fix             5 applied · history.go, meaningfulchanges.go (+2)
   ✅ qa              tsc ✓ · test ✓ · visual-test skipped (no UI delta)
   risk              low · copy-only UI labels · mitigated by renderer tests
   scenarios         4/4 covered · table posted in Linear
   📤 PR              pushed b083fbd9 + body
 round 2             clean — no new valid findings
 result: converged locally · 2 rounds · 8 fixed · 7 skipped · 1 open · CI pending
 open for you:
   • [discuss] <one-line question that needs your call>
```

Always include: per-step counts, the **triage breakdown** (the signal you didn't
auto-accept), files/PR touched, the **result line**
(`converged|capped|blocked · rounds · fixed/skipped/open`), and open items. In
`--auto`, add an `assumptions:` block. Show durations only where they matter
(cross-review, CI waits).

For nontrivial changes, include a compact risk/blast-radius note: affected
surface, likely failure mode, mitigation/test proof, and any residual risk. Do
not overbuild this for harmless mechanical edits, but do not leave it implicit
for behavior, UI, auth/security, data, or diagnosis/remediation changes.

For scenario-sensitive work, include the scenario ledger in the summary or link
to where it was posted. Minimum columns: scenario, expected final behavior/copy,
evidence source (`file:line`, fixture, screenshot, live cluster/API proof),
self-review verdict, cross-review status, tests/proof, and open decision.
Cross-review status is either the verdict or `skipped: <reason>` when the
cross-model pass was intentionally skipped. If the cross-review happened before
fixes, explicitly say whether the final post-fix head was re-reviewed; don't let
"Claude reviewed it" imply a later commit was covered when it was not.

**The `✅ qa` line must state visual-test explicitly** — never ambiguous. If it
ran, include the screenshot directory as an **absolute path** (or `file://` URL —
not relative, not `~`, so the terminal linkifies it) and the shot count; if not,
`visual-test: skipped (<reason>)`. A QA line with no visual-test entry is a bug —
the reader can't tell whether it happened.

**When a PR is open, lead the ledger with a clickable `🔗 PR` line** — render the
number as a **markdown link** `PR [#910](url)` (the summaries render as markdown in
the Claude/Codex TUI, so it shows a clean clickable "#910"; a bare absolute URL is
the plain-terminal fallback). Include state (`OPEN`/`DRAFT`), the checks rollup
(counts + **names of any pending/failing**), and mergeable/`CONFLICTS`. Pull it with `gh pr view <n> --json
url,state,isDraft,mergeable,statusCheckRollup`. If the loop converged locally but
remote checks are still running, say `converged locally · … · CI pending` on the
result line and keep the link visible so the user can watch it land.
