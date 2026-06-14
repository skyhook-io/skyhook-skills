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

## Install (Claude Code)

```
/plugin marketplace add skyhook-io/skyhook-skills
/plugin install skyhook-skills@skyhook-skills
```

Auto-updates at startup (it's a public marketplace — no token needed).

## Install (Codex companions, optional)

Claude's marketplace only manages the Claude plugin. The Codex-side skills install manually:

```
git clone https://github.com/skyhook-io/skyhook-skills
skyhook-skills/scripts/install-codex.sh   # copies skills -> ~/.codex/skills, then restart Codex
```

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
