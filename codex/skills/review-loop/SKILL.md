---
name: review-loop
description: Use when the user wants the current code proactively reviewed and fixed (e.g. "review-loop", "/review-loop", "review what I have and fix it"). Self + cross-model review → triage → fix → update PR, loop until clean.
metadata:
  short-description: Proactive self + Claude review → triage → fix → update PR
---

# Review Loop (Codex)

Proactively review the current code and fix it, Codex-side — the proactive
counterpart to reacting to CI/Bugbot on a PR. Same workflow as Claude's
`/review-loop`.

**Canonical procedure:** read `~/.codex/skills/skyhook-skills-commands/review-loop.md` and follow it
(scope → review → triage → fix → update PR → loop; caps; safety). **Codex
translations:**

- **Self review** ("/review", "/simple") → YOU review your own diff hard:
  correctness bugs, security, silent failures, races, logic errors, breaking API
  — and over-engineering / dead weight (options no caller sets, one-impl
  interfaces, tests that assert the implementation). Don't ping-pong with prior
  reviewers.
- **Cross-model review** ("/cross-review") → the **claude-review** skill — from
  Codex the secondary reviewer stays Claude (it reviews your work). Nontrivial
  changes only — don't ceremony-ize a typo.
- **Scenario-sensitive work** (copy, diagnostics/remediation, detector precision,
  error classification, security/permissions, UI states) → build a scenario
  ledger before calling the review complete: scenario, expected final behavior or
  copy, source-of-truth evidence, self-review verdict, Claude status, tests/live
  proof, open decision. Claude status is either the verdict or `skipped:
  <reason>` when cross-review was intentionally skipped. "Review loop ran" is not
  a completion claim.
- **Risk / blast radius** → for nontrivial changes, include a practical risk note:
  affected surface, likely failure mode, mitigation/test proof, and residual
  risk. Keep it proportional; don't add boilerplate for harmless edits.
- **Triage** ("/triage-findings") → inline: read the real code at each
  `file:line`, **never auto-accept**, cite evidence on every skip.
- **Fix** ("/fix-findings") → apply the confirmed Fix verdicts.
- **`/qa`** → read the repo's `.claude/commands/qa.md` and follow it (type-check
  + tests; visual-test default-skip, only warranted self-contained UI changes).
- **Update PR** ("/pr") → via `git` + `gh`: stage relevant files only, commit/
  amend, push `--force-with-lease`. **Write the body per
  `~/.codex/skills/skyhook-skills-commands/pr.md`** — depth proportional to the change, motivation +
  design, **no review-fix trivia; re-derive the narrative, don't append fix bullets
  each round.** No PR yet ⇒ leave commits local and say so.

**Invariants:** triage skeptically and never auto-accept; cross-review only when
nontrivial; cap at 3 rounds and report (stop if the same finding survives 2 fix
attempts); never on `main`, never merge, `--force-with-lease` only. Narrate phases
with the glyph-tagged banners and **end with the run-summary ledger** (per-step
counts, triage breakdown, result line, open items) defined in the canonical file.

Steps are judgment calls — decide which apply, and **honor free-text steering in
the invocation** (e.g. `consult claude`, `no PR`, `review only`, `thorough`,
`focus on <area>`) as an override, per the canonical file's directives section.
