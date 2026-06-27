# Simple

Audit a PR for code that isn't earning its keep — over-engineering, speculative abstractions, useless tests, dead exports. **Not** bug-hunting, **not** style, **not** "should add tests." The bar is *"is this actually right and clearly better?"*

## Mission

Most AI-assisted PRs ship code that compiles, passes tests, and is structurally plausible — but contains scaffolding for a future that may never arrive. Options no caller sets. Interfaces with one implementation. Helpers with one call site. Tests that assert what the implementation literally writes. This skill finds that surplus.

**"Nothing to cut" is the expected, normal outcome on a well-shaped PR.** Plenty of PRs are already simple. If you scan the inventory and nothing meets the bar below, the answer is `0 findings — PR is in good shape`, period. Don't dig harder until you find something to say; don't downgrade the bar to justify having flagged something.

The bar for flagging anything: **delete this — what regresses?** If the answer is "a test that exercises only this code" or "nothing", flag it. If the answer is "a user-visible behavior" or "an actually-called code path", don't flag it.

**Prefer no finding over a weak finding.** Weak findings burn the user's time and credibility for the next real one.

### Don't ping-pong with the reviewer

A common failure mode: a reviewer asks for an addition (extra option, defensive check, abstraction), the author adds it, then `/simple` silently flags it as over-engineering and removes it. The PR thrashes between reviewers and cleanup with no net progress.

Before flagging, check whether the symbol was **added in response to a specific review comment, ticket, or stated requirement on this PR** (look at PR comments, recent commit messages, conversation context). When the answer is yes:

- **Raise the bar.** A reviewer who explicitly asked for X is the second caller. Don't flag a borderline case just because it would otherwise look speculative.
- **But reviewers do go overboard** — especially AI bots that demand null checks for non-null params, abstract every helper "for testability," or pile on speculative options. If a reviewer-requested item is genuinely over-engineered, you may still flag it. The bar is "I'd argue with the reviewer about this," not "I'd silently remove it."
- **When you do flag a reviewer-requested item, surface the tension.** Note who asked for it and why, name your disagreement, and let the user decide. Don't auto-remove things a reviewer asked for — that's how the thrash starts.

When you can't tell whether something was reviewer-requested vs speculatively added, ask the user before flagging.

## Inputs (collect first, anchor everything in evidence)

```bash
git log <base>..HEAD --oneline       # commits in scope
git diff --stat <base>...HEAD        # files + line counts
git diff <base>...HEAD               # full diff
gh pr view --json title,body         # what the PR *claims* to do
```

Before judging, list:
1. **New exported symbols** (functions, types, constants, interfaces) added by this PR.
2. **New options/flags** (struct fields on Option types, CLI flags, config keys).
3. **New interfaces** and their implementations *in this repo*.
4. **New test files** and what each one targets.
5. **Net LOC delta** and what % is moved code vs new functionality vs tests.

Then run the smell checklist below against that inventory.

## Smell Checklist

For each finding, cite `file:line`, name the smell, show the detector evidence, and propose the action (almost always *delete* or *inline*).

### 1. Speculative options struct
**Detector:** A field on an Options/Config struct has zero call sites that set it to a non-default value.
**Action:** Delete the field. If the entire struct has 0–1 fields actually used, replace with a plain parameter.
**Don't flag** if: the field is documented as part of a stable public API and the PR is explicitly publishing that API.

### 2. Ghost interface / concrete abstraction
**Detector:** An interface has exactly one implementation in the repo, no test seam needs it, and no external consumer is named in the PR.
**Diagnostic question (matklad):** *Is this abstraction used exclusively concretely?* If `x.Foo()` is always called with `x` being a known specific type, the interface earns nothing.
**Action:** Inline the concrete type. Delete the interface.
**Don't flag** if: the package is explicitly a library with documented consumers, OR a test substitutes a fake that satisfies the interface.

### 3. Future-proofing helper
**Detector:** A new function/method has exactly one caller and no plausible second caller named in the PR description or nearby code.
**Action:** Inline at the call site.
**Don't flag** if: extracting the helper makes the one call site significantly more readable (e.g., names a tricky calculation).

### 4. Phantom export
**Detector:** A symbol is exported (capitalized in Go, public in TS/Python) but no code outside its package references it.
**Action:** Unexport. If the symbol is genuinely unreachable, delete.
**Don't flag** if: the symbol is part of a published library API surface that external consumers (outside this repo) plausibly need.

### 5. Tautological test
**Detector:** The expected value in the assertion is computed by the same code path as the actual value. Or the test mirrors the implementation: read the test without the impl, you can't tell what behavior is being verified.
**Action:** Delete or rewrite from the user-observable behavior, not from the implementation.
**Don't flag** if: the test asserts a behavior described in a spec/contract independent of how it's implemented.

### 6. Mirror test / test theater
**Detector:** Test asserts what the implementation literally writes, not what callers depend on. Mocks echo back the SUT's own assumptions. Test name describes an implementation detail ("calls helper X") rather than behavior ("returns sorted results when input is unsorted").
**Action:** Delete. Replace only if there's a real behavior worth pinning.

### 7. Speculative hierarchy / one-child abstract type
**Detector:** A new abstract type, base class, or generic interface has exactly one concrete implementation.
**Action:** Collapse to the concrete type.

### 8. Defensive fallback for nonexistent legacy
**Detector:** Code like `resp?.field ?? resp` or `if oldShape { ... } else { newShape }` with no versioned producer that emits the old shape in the current repo.
**Action:** Delete the fallback. Trust the producer's type.
**Don't flag** if: the codebase actually has multiple producers emitting different shapes (e.g., during a documented migration).

### 9. Phantom dependency / disconnected pipeline
**Detector:** New imports/code paths that aren't reached from any entry point. Setup that no runtime caller invokes.
**Action:** Delete.

### 10. Inflated documentation
**Detector:** Docstrings/comments that restate the function name or describe **what** the code does instead of **why**. Or comments that reference tickets, PR numbers, "previously", "used to", etc.
**Action:** Delete the comment, or rewrite to capture a non-obvious *why* (a constraint, an invariant, a workaround for a specific cause).

### 11. Duplicate left after extraction
**Detector:** A PR extracts logic into a new function/component/hook but the original inline copy is still there — now two definitions of the same thing (the extraction was added, the original never deleted). Greppable: the extracted name AND a near-identical inline block both present; callers still hitting the old copy.
**Action:** Replace the original with a call to the extraction; delete the inline copy. An extraction that doesn't remove what it replaced is incomplete, not additive — the duplicate will silently diverge.
**Don't flag** if: the two copies are deliberately distinct (different behavior) and only superficially similar.

## Diagnostic questions (apply to every new symbol)

1. **Who is the second caller?** If "nobody yet," it's suspect.
2. **Is this abstraction used exclusively concretely?** (matklad)
3. **If I deleted this, what test fails or what user-visible behavior regresses?** If "only its own test," delete both.
4. **Does the PR description justify this scope, or did scope creep during implementation?**

## Test-specific lens (run separately; tests are usually >50% of AI surplus)

For each new test file or test:
- **Same-algorithm expected value?** Expected is computed by calling the same code or reimplementing the same logic → tautological.
- **Asserts a language guarantee?** Tests that `append` appends, that JSON serialization round-trips a struct, that a getter returns what was set → delete.
- **Mocks echo SUT?** The mock returns a value derived from inputs the SUT just passed it → mirror test.
- **Name = implementation detail?** "Test_calls_validateBefore_save" → likely brittle. "Test_rejects_invalid_email" → behavioral, keep.
- **Coverage cargo-culting?** Test added because a tool flagged missing coverage on a trivial getter/setter → delete.

## What NOT to flag

- Style, formatting, naming preferences (unless a name actively misleads).
- "Could use a more idiomatic X" without a concrete bug.
- Missing coverage on areas that already have adequate test coverage.
- Architectural opinions about layering or directory structure.
- Anything pre-existing on the base branch (call it out as out-of-scope, don't fix).
- Intentional scope-expanding changes the PR description names.
- Trivial wrappers that exist to give a stable name to a one-liner (e.g., `func IsAdmin(u User) bool { return u.Role == "admin" }` — leave it).

## Output format

```
## Right-Shape Audit — <PR title>

**Inventory:** N new exported symbols, N new option fields, N new interfaces, N new test files. Net +X / -Y LOC.

### Findings (N)

| # | file:line | Smell | Evidence | Action |
|---|-----------|-------|----------|--------|
| 1 | pkg/foo/bar.go:42 | Speculative options struct | `Opts.Timeout` field added; 0 callers set it (grep'd all callers) | Delete field |
| 2 | pkg/foo/iface.go:10 | Ghost interface | `Storer` interface, 1 impl (`memStore`), used concretely everywhere | Inline `memStore`, delete interface |
| ... |

### Out of scope (noted, not flagged)
- <pre-existing issues>

### Clean
- <areas audited that passed>
```

End with one line:
- **0 findings:** `PR is in good shape — nothing to cut.` Stop there. Don't add caveats, don't list "things you considered." Just the one line.
- **N>0 findings:** `N findings to address. Estimated cleanup: -K LOC.`

## Calibration footer

The bar isn't "could this be cleaner" — it's *"is this actually right and clearly better, and would deleting it regress observable behavior or a real test?"* If you're not sure, don't flag.

A clean result is a feature, not a failure. PRs that are already simple shouldn't be churned to justify the audit happening. Don't auto-apply fixes — present findings first, then ask. And if there's nothing to flag, say so and stop.
