# skyhook-skills

Composable AI **dev-workflow** commands for [Claude Code](https://claude.com/claude-code) — with [Codex](https://github.com/openai/codex) companions. An autonomous plan → implement → review → PR → converge loop, cross-model (Claude ↔ Codex) review, and a product/design/UX critique pass.

Built by [Skyhook](https://skyhook.io) for building [Radar](https://github.com/skyhook-io/radar); generic enough to use anywhere.

## What you get

**The loop**
- **`/autodev [--auto] <task>`** — full autopilot: plan → implement → review → PR → converge, end-to-end, stopping only at real decisions. Default mode gates on the plan before coding; `--auto` makes product calls itself (logging assumptions) and stops only for an irreversible-action ceiling.
- **`/plan-loop`** — draft a plan, cross-review it with the *other* model, triage the critique skeptically, iterate, gate.
- **`/review-loop`** — proactively review the current code (self + cross-model), triage, fix, update the PR — loop until clean.

**Review & critique** (three altitudes — *right thing* → *earning its keep* → *correct*)
- **`/product-review`** — questions *what* to build and *how* users perceive it: premise, top user journeys (ranked 0–10), UX shape, comprehension, states, AI-slop. Borrows forcing-function patterns from [gstack](https://github.com/garrytan/gstack) and [OneRedOak](https://github.com/OneRedOak/claude-code-workflows) + a journey-ranking + non-expert-comprehension lens.
- **`/review`**, **`/simple`** (anti-over-engineering), **`/triage-findings`**, **`/fix-findings`**.

**Cross-model review**
- **`/codex-review`** — runs a [Codex](https://github.com/openai/codex-plugin-cc) review of your branch, prints it verbatim, then triages it skeptically (never auto-accepts).

**PR**
- **`/pr`**, **`/fix-pr`**, **`/fix-pr-loop`** (reacts to CI + bot reviewers until converged).

Cross-cutting: **never auto-accept a reviewer** (your own, the cross-model pass, or PR bots) — every finding is triaged with evidence; cross-review only when nontrivial; every loop caps and reports; review at altitude (a clean implementation of the wrong thing is still wrong).

## Concepts

A few principles run through every command:

- **Review at altitude, intent before details.** Before judging whether code is *correct*, judge whether it's the *right thing to build* and the *right design* — approach, architecture, UX, user journey. A clean implementation of the wrong thing is still wrong. `/product-review` is the dedicated pass for this.
- **Never auto-accept a reviewer.** Every finding — your own, the cross-model pass, or a PR bot — is triaged against the real code, with evidence cited on every skip. Cross-model reviewers are often right about blind spots and often wrong about things already handled; you decide.
- **Compose, don't rebuild.** The loops are thin conductors over small, single-purpose commands. Edit one (e.g. `/triage-findings`) and every loop that uses it inherits the change.
- **Scale ceremony to the task.** Trivial changes skip the loop; nontrivial work gets cross-review + product critique. Steps are judgment calls, and you can steer them inline (`/review-loop consult codex`, `/autodev no PR`, `quick`, `focus on auth`).
- **Bring-your-own verification (`/qa`).** The loops call `/qa`, but each repo defines what verification means there — type-check, tests, and optionally a `/visual-test`. The workflow stays repo-agnostic.

### Example run-summary

Every loop narrates itself and closes with a scannable audit ledger:

```
📋 review-loop · feature/bulk-actions
 🔗 PR [#910](https://github.com/your-org/your-repo/pull/910) · OPEN · checks 4 ✓ · 2 pending (Backend, Bugbot)
 round 1
   🔎 self-review     6 findings
   🔵 codex review    8m · 13 findings
   ⚖️ triage          5 fix · 7 skip · 1 discuss
   🔧 fix             5 applied
   ✅ qa              tsc ✓ · test ✓ · visual-test skipped (no UI delta)
   📤 PR              pushed + body
 result: converged locally · 1 round · 5 fixed · 7 skipped · 1 open · CI pending
 open for you:
   • [discuss] <the one question that needs your call>
```

## Install (Claude Code)

Run these **inside Claude Code** (they're slash commands, not shell commands):

```
/plugin marketplace add skyhook-io/skyhook-skills
/plugin install skyhook-skills@skyhook-skills
```

The commands then appear **namespaced under the plugin** — `/skyhook-skills:autodev`, `/skyhook-skills:review-loop`, `/skyhook-skills:product-review`, etc. (`/plugin` to browse them). Auto-updates at startup — it's a public marketplace, no token needed.

## Install (Codex companions, optional)

Claude's marketplace only manages the Claude plugin; the Codex-side skills install with one line:

```bash
curl -fsSL https://raw.githubusercontent.com/skyhook-io/skyhook-skills/main/scripts/install-codex.sh | bash
```

Then **restart Codex**. (Rather not pipe curl to bash? `git clone https://github.com/skyhook-io/skyhook-skills && bash skyhook-skills/scripts/install-codex.sh` does the same.) The companions call the `claude` CLI for cross-model review — see Prerequisites.

## The `/qa` seam — bring your own verification

The loops call **`/qa`** to verify a change, but `/qa` is **repo-provided**: each repo defines what verification means there (type-check, tests, and optionally a `/visual-test`). Drop a `.claude/commands/qa.md` in your repo, e.g.:

```markdown
---
description: Verify this change — type-check, tests, and visual-test when a UI change warrants it
---
# QA
- Code changed → run your type-check + tests (e.g. `make tsc` / `make test`, `npm run tsc`, `go test ./...`).
- UI changed → lean toward `/visual-test` for feature-scale rendered changes; skip for small/non-visual. Report status (ran → link the screenshot dir; skipped → why).
```

No `/qa`? The loops fall back to plain build/test detection.

## Prerequisites & optional integrations

- **`/codex-review`** needs the official [`codex` plugin](https://github.com/openai/codex-plugin-cc) installed (`/plugin marketplace add openai/codex-plugin-cc`).
- **Codex → Claude** (the `claude-review` Codex skill) needs the `claude` CLI. On macOS, run it un-sandboxed so it can read Keychain auth, and (if Codex's guardian blocks the export) add a narrow `[auto_review]` allowance in `~/.codex/config.toml`.
- **`/review --deep`** uses the [`pr-review-toolkit`](https://github.com/anthropics/claude-plugins-official) plugin if installed (optional).

## License

MIT — see [LICENSE](LICENSE).
