# Review

Comprehensive code review with startup-appropriate priorities. Choose depth based on context.

## IMPORTANT: Announce Mode
**First line of output MUST state which mode you're using:**
- "Running QUICK review..."
- "Running DEEP review..."

## Modes

### Quick Mode (default)
Fast review focusing on real problems only. Use when:
- Checking work before commit/PR
- Sanity check before merge
- Want to catch obvious issues fast

### Deep Mode (add `--deep` or request explicitly)
Thorough review including design quality. Use when:
- Major feature implementation
- Refactoring or architectural changes
- Uncertain about approach
- Want comprehensive feedback

---

## Scope: What to Review

### 1. Determine the work scope
```bash
# Check current branch and changes
git status
git log main..HEAD --oneline

# See all changes in branch vs main
git diff main..HEAD

# See uncommitted changes
git diff
```

- **Review ALL commits** in this branch that aren't in main/master
- **Review pending changes**: Unstaged and staged changes
- **Ignore unrelated changes**: Skip files modified locally but unrelated to current work
  - Look at file modification times if unsure
  - Check if changes are in `.gitignore` or build artifacts
  - When in doubt, list them and ask before including

---

## What to Flag

### Philosophy
Early-stage startup. Ship working code fast, not perfect code slowly.

### Critical (Always flag - blocks shipping):
- Logic errors (wrong algorithm, off-by-one, etc.)
- Realistic security vulnerabilities (auth bypass, injection, XSS, secrets exposure)
- Data corruption risks
- Race conditions that will happen in practice
- Silent failures that hide real errors
- Breaking API changes without migration path
- LLM trust boundary violations (unsanitized LLM output used in SQL, shell, or code execution)
- Enum/discriminated union exhaustiveness gaps (missing switch cases TypeScript won't catch at runtime)

### Important (Flag if easy to fix):
- Confusing error messages users will actually see
- Resource leaks (connections, files, goroutines)
- Performance issues with clear impact (N+1 queries, O(n²) where n is large)
- Error handling that makes debugging hard

### Quick Fixes (Just do them - < 30 seconds each):
- Typos in user-facing messages or docs
- Style/lint issues (unused imports, formatting)
- Minor naming improvements (if truly confusing)
- Comment typos or formatting
- Missing error checks that are 1-line fixes
- Debug prints, commented-out code

### Deprioritize (High bar to mention):
- **Missing tests** - only flag if regression-prone or genuinely hard to verify manually
- **Theoretical issues** - only if realistic and likely to occur in practice
- **Theoretical security** - only if realistic attack vector exists
- **Complex refactoring** - only if current code will clearly cause problems soon
- **Over-engineering** - YAGNI applies
- **Documentation gaps** - only for public APIs

---

## Deep Mode: Additional Checks

When in deep mode, also examine:

### Design Quality
- Is the implementation effective for the original goal?
- Sometimes we start with one idea, realize it's suboptimal, but forget to refactor
- Step back: Is this the right approach?
- Are there architectural concerns?

### Design-system / theme compliance (frontend changes only)
- If the project has a design system, scan changed `.tsx`/`.css` files for raw hardcoded styling (e.g. raw Tailwind color classes like `bg-white` / `bg-gray-*` / `text-gray-*`, inline hex) that should use the project's design tokens instead.
- Check for hand-written badge/color strings or hand-rolled brand buttons that should use the project's shared components/utilities.
- See the project's design doc (e.g. `DESIGN.md`) for its token reference, if it has one.

### Completeness
- Leftovers: Temporary hacks still in code
- Unused code: Dead imports, functions, variables
- Documentation: Missing or outdated docs, comments, README updates
- TODOs: Unfinished work, missing error handling

### Validation
- **Build**: Ensure everything compiles/builds
- **Lint**: Must pass linter according to current repo rules
- **Tests**: If tests exist, they should pass (run them if practical)

---

## Process

### Quick Mode:
1. **Announce**: "Running QUICK review..."
2. Run `git diff main..HEAD` to see all changes
3. Scan for critical issues
4. Make quick fixes automatically
5. Flag important issues if easy to fix
6. Skip deprioritized items unless exceptional
7. **Batch all questions into ONE block at the end** — never ask mid-review

### Deep Mode:
1. **Announce**: "Running DEEP review..."
2. Run `git diff main..HEAD` to see all changes
3. Review each commit in the branch individually for context
4. Check all categories (critical, important, quick fixes, deprioritized + design/completeness)
5. Think methodically about each file
6. Consider the original goal and current implementation
7. Run build/lint/tests if applicable
8. **Batch all questions into ONE block at the end** — never ask mid-review

---

## Output Format

### Quick Mode:
```
Quick fixes applied:
- Fixed 3 typos in error messages
- Removed unused import
- Fixed formatting in comments

[If any critical/important issues:]
[File:Line] - [What will actually break]
Fix: [Specific suggestion]

[File:Line] - [What will be annoying]
Fix: [Specific suggestion] or defer to later

[Otherwise:]
No blocking issues. Ship it!
```

### Deep Mode:
Summarize findings in categories:
1. **Critical**: Must fix - breaks, bugs, security, data loss
2. **Design Concerns**: Effectiveness questions, architectural issues
3. **Important**: Error handling, resource leaks, UX issues
4. **Quality Improvements**: Leftovers, cleanup, documentation (already applied)
5. **Questions**: Things you're uncertain about (ask before changing)

---

## Guidelines

- **Quick fixes are free** - Just do style/typo fixes without overthinking
- **Don't guess** - If unsure about something, collect it and ask at the end in one batch
- **Don't be destructive** - Don't remove code unless you're certain it's unused
- **Context matters** - Consider what problem we were solving originally
- **Deprioritized ≠ ignored** - Note if something genuinely matters despite being in that category
- **Focus on changed code** - Don't review unrelated existing code unless it's directly affected
- **Never commit or push** - Applying fixes is in scope; committing is /pr's job

Remember: The goal is to ship working code fast, not perfect code slowly.
