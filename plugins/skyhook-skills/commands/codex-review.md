---
description: Run the native Codex review (codex plugin), print findings verbatim, then triage them skeptically
argument-hint: "[--base <ref>] [--scope auto|working-tree|branch]  (default: auto)"
allowed-tools: Bash(node:*), Bash(ls:*), Bash(git status:*), Bash(git log:*), Bash(git diff:*), Bash(git rev-parse:*), Read, Grep, Glob
---

# Cross-Review: Codex reviews (native plugin), you triage

This is a **thin wrapper over the official `codex` plugin's native reviewer**
(`/codex:review`). The plugin does the actual Codex run through its shared
runtime (`codex-companion.mjs` + structured output); this command's *only*
addition is the final step — stress-testing Codex's findings with a skeptic lens
instead of rubber-stamping them. Don't re-implement the review; reuse the plugin.

The point is an adversarial second opinion: Codex is the reviewer, you are the
skeptic. Don't assume Codex is right or wrong — verify against the code.

---

## Step 1 — Locate the plugin's companion script

The codex plugin runs every review through `codex-companion.mjs`. Resolve the
newest installed copy (don't hardcode the version):

```bash
SCRIPT="$(ls -t ~/.claude/plugins/cache/openai-codex/codex/*/scripts/codex-companion.mjs 2>/dev/null | head -1)"
echo "$SCRIPT"
```

If that's empty, the `codex` plugin isn't installed — tell the user to add it
(`/plugin` → `openai-codex` marketplace → install `codex`). **Do not** fall back
to a hand-rolled `codex exec review`; the whole point is to use the plugin.

## Step 2 — Run the native Codex review (foreground)

The companion has two review modes — pick by whether you have **focus text**:

- **Plain review** takes **scope flags only** (`--base <ref>` / `--commit <sha>`
  / `--scope auto|working-tree|branch`) and **rejects prose** ("does not support
  custom focus text"):
  ```bash
  node "$SCRIPT" review --base <ref>
  ```
- **Focused review** — when you want to direct attention to specific areas — uses
  `adversarial-review`, which **does** take trailing focus text plus scope flags:
  ```bash
  node "$SCRIPT" adversarial-review --base <ref> "Focus on: <areas>. Flag correctness bugs, silent failures, races, logic errors."
  ```

Map the caller's intent: scope-only ⇒ `review`; any focus/instructions ⇒
`adversarial-review`. **Never pass prose to `review`** — that's the failure mode.
Default `--base main` for a branch review. Run in the **foreground** (we triage
the output this turn).

**For the design / intent lens — "is this the right thing, well-designed?" — use
`adversarial-review`.** It challenges the approach, tradeoffs, and assumptions;
plain `review` only hunts defects. For substantive changes prefer it (or run both:
`adversarial-review` for the design pass, `review` for the defect sweep) — a clean
implementation of the wrong design is still wrong, and the cross-model voice is
most valuable challenging direction, not just nitpicking lines.

- **Use a 10-minute Bash timeout (`timeout: 600000`)** — the default 2 min will
  kill the review mid-run.
- This is foreground-only by design, because Step 4 triages the output now. If
  the user just wants an async review with no triage, point them at the plugin
  directly: `/codex:review --background` then `/codex:result`.
- If the script reports Codex isn't set up, run `node "$SCRIPT" setup` once (or
  tell the user to run `/codex:setup`), then retry.
- On any error, surface it verbatim and stop — don't fabricate findings.

## Step 3 — Print Codex's findings **as-is**

Reproduce the script's stdout **verbatim** inside a fenced block — do not
summarize, reword, re-rank, or drop anything. The user wants the raw second
opinion before your take.

```
## 🔵 Codex's review (verbatim)

<exact stdout from codex-companion.mjs>
```

Verbatim means verbatim, even if long.

## Step 4 — Triage skeptically (do NOT auto-agree)

Apply the `/triage-findings` discipline to each finding, skeptic lens up:

1. **Understand the claim** — restate what Codex is actually asserting.
2. **Read the real code** at the referenced `file:line` (Read/Grep — don't trust
   the snippet Codex pasted; it may be stale or out of context).
3. **Validity** — real, or a false positive? Did Codex misread control flow, miss
   a caller-side guarantee, miss validation elsewhere, or misunderstand the
   framework? Cross-model reviewers frequently flag things already handled.
4. **Severity** — practical or theoretical? Default to **Skip** for defensive
   guards against impossible states, redundant-with-framework checks, missing
   tests for trivial code, and speculative future concerns. Default to **Fix**
   when it's genuinely correct and clearly better — correctness matters, size
   doesn't.
5. **Fix** — if valid, the right fix (which may differ from Codex's suggestion).

Then emit the triage table:

| # | Codex finding | Verdict | Why (verified against code) | Action |
|---|---------------|---------|-----------------------------|--------|

Verdicts: **Fix** · **Skip** · **Discuss**.

For every **Skip**, name specifically what Codex missed (cite the file:line of
the mitigating code). A bare "disagree" is not acceptable — show the evidence.

## Step 5 — Confirm before changing anything

End with a one-line scoreboard ("Codex raised N · Fix X · Skip Y · Discuss Z")
and ask: **"Want me to apply the confirmed fixes?"**

Do not edit, commit, or push as part of this command — fixes happen only after
the user says go.
