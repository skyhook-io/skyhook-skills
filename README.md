# skyhook-skills

Composable AI **dev-workflow and research** commands for [Claude Code](https://claude.com/claude-code), [Codex](https://github.com/openai/codex), and [Cursor Agent](https://cursor.com/docs/skills). An autonomous plan → implement → review → PR → converge loop, cross-model review, product/design/UX critique, and decision-focused competitive research.

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
- **`/cross-review`** — runs a review by the configured secondary model — **Codex or Cursor** — prints it verbatim, then triages it skeptically (never auto-accepts). Pick the reviewer via `~/.claude/skyhook-skills.json` (`{"reviewer":"codex|cursor","model":"…"}`), the `SKYHOOK_REVIEWER` env var, or a `consult cursor` / `consult codex` directive. `/codex-review` forces Codex.

**PR**
- **`/pr`**, **`/fix-pr`**, **`/fix-pr-loop`** (reacts to CI + bot reviewers until converged).

**Hand it over**
- **`/review-packet [pr|set|design|research] [focus]`** — packages work for guided review: a document that leads with the decisions the reviewer has to make and puts the evidence for every claim right beside it. Claude publishes an artifact; Codex publishes through Sites. Ask for local-only output to get self-contained HTML with embedded evidence (no PDF). If publishing is unavailable, the skill hands over HTML and explains the gap. Cursor defaults to local HTML. Built for large PRs, PR *sets*, rendered UI, and design or research proposals — the cases where review otherwise means scrolling a diff and taking your word for it.

**Research**
- **`/competitive-research [implementation|product|positioning|hybrid] [focus]`** — investigates how comparable products handle the active decision using primary evidence: OSS source and tests for implementation details, official product material for UX/features, or current first-party pages for positioning. Compares the tradeoffs with the current approach and recommends what to keep, adopt, hybridize, or defer.

**Utilities**
- **`/housekeeping`** — read-only audit of a dev machine's disk, caches, stale tools, and services; triages findings into reclaimable / worth-reviewing / leave-alone and never mutates anything without explicit approval.

Cross-cutting: **never auto-accept a reviewer** (your own, the cross-model pass, or PR bots) — every finding is triaged with evidence; cross-review only when nontrivial; every loop caps and reports; review at altitude (a clean implementation of the wrong thing is still wrong).

## Concepts

A few principles run through every command:

- **Review at altitude, intent before details.** Before judging whether code is *correct*, judge whether it's the *right thing to build* and the *right design* — approach, architecture, UX, user journey. A clean implementation of the wrong thing is still wrong. `/product-review` is the dedicated pass for this.
- **Research at the task's altitude.** Competitive work should answer the decision in front of you: source-level evidence for implementation semantics, product evidence for UX and features, market evidence for positioning. Prefer representative patterns over exhaustive feature grids.
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

## Install and update

Claude Code uses the plugin marketplace. Codex and Cursor Agent use the same
Agent Skill adapters and canonical command bundle under `~/.codex/skills`;
Cursor discovers that directory for compatibility, so installing for both does
not create two copies.

The Claude plugin exposes the full command catalog. Codex and Cursor expose the
companion entry points `autodev`, `plan-loop`, `review-loop`, `product-review`,
`claude-review`, `competitive-research`, and `review-packet`; those skills use the shared
canonical commands internally.

| Agent | Distribution | Invoke a skill |
|---|---|---|
| Claude Code | `skyhook-skills` marketplace plugin | `/skyhook-skills:competitive-research` |
| Codex | User-level Agent Skills | `$competitive-research` |
| Cursor Agent | The same Agent Skills as Codex | `/competitive-research` |

### Claude Code

First install — run these **inside Claude Code**:

```text
/plugin marketplace add skyhook-io/skyhook-skills
/plugin install skyhook-skills@skyhook-skills
```

Update — run these in a terminal:

```bash
claude plugin marketplace update skyhook-skills
claude plugin update skyhook-skills@skyhook-skills
```

Then apply the update to an already-running Claude Code session:

```text
/reload-plugins
```

Use `/plugin` to browse installed commands or enable marketplace auto-update.
Third-party marketplace auto-update may be disabled, so the explicit update
commands above are the reliable path. See the
[Claude Code plugin documentation](https://code.claude.com/docs/en/discover-plugins).

### Codex

First install **and every update** use the same idempotent command:

```bash
curl -fsSL https://raw.githubusercontent.com/skyhook-io/skyhook-skills/main/scripts/install-codex.sh | bash
```

The installer fetches `main`, updates the Skyhook adapters and canonical
commands, and leaves unrelated skills alone. Codex normally detects skill changes
automatically; if the update does not appear, restart Codex. Verify with
`/skills`, then invoke a skill with `$competitive-research`. See the
[OpenAI Agent Skills documentation](https://developers.openai.com/codex/skills).

If you prefer a checkout over piping from the network, clone this repository,
`git pull --ff-only` for each update, then run
`bash scripts/install-codex.sh` from the repository root.

### Cursor Agent

Cursor Agent discovers `~/.codex/skills`, so it uses the **same install and
update command as Codex**:

```bash
curl -fsSL https://raw.githubusercontent.com/skyhook-io/skyhook-skills/main/scripts/install-codex.sh | bash
```

If you already ran that command for Codex, there is nothing else to install.
Start a new Cursor Agent session (or restart Cursor) after an update. Verify under
**Customize → Skills** or invoke `/competitive-research` in Agent chat.
Updating the Cursor binary with `cursor-agent update` is separate and does not
update these skills. See the [Cursor Agent Skills documentation](https://cursor.com/docs/skills).

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

- **`/cross-review` reviewers** (pick via `~/.claude/skyhook-skills.json`, `SKYHOOK_REVIEWER`, or a `consult <x>` directive):
  - **codex** — needs the official [`codex` plugin](https://github.com/openai/codex-plugin-cc) (`/plugin marketplace add openai/codex-plugin-cc`).
  - **cursor** — needs the [Cursor CLI](https://cursor.com) (`cursor-agent`) logged in, or `CURSOR_API_KEY` set; defaults to the `gpt-5.6-high` model. For a genuine second opinion when driving from Claude, keep it on a non-Claude model.
- **Codex → Claude** (the `claude-review` Codex skill) needs the `claude` CLI. On macOS, run it un-sandboxed so it can read Keychain auth, and (if Codex's guardian blocks the export) add a narrow `[auto_review]` allowance in `~/.codex/config.toml`. Long reviews should use streamed JSON and the final `result` field; plain `claude -p` can look idle while it is still reading/thinking.
- **`/review --deep`** uses the [`pr-review-toolkit`](https://github.com/anthropics/claude-plugins-official) plugin if installed (optional).

## License

MIT — see [LICENSE](LICENSE).
