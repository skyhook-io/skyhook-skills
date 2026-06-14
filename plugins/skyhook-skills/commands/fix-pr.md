# Fix PR Issues

Review PR feedback, triage by priority, and address legitimate issues.

## Context
Early-stage startup codebase. Apply pragmatic judgment focusing on velocity and real impact.

## Process

### Step 1: Fetch and Analyze Reviews
1. Fetch PR comments: `gh pr view --json comments,reviews`
2. Filter for all reviewers (AI bots like "claude", "coderabbit", "github-actions" AND human reviewers)
3. **Prioritize the latest review from each reviewer** - Earlier reviews may be obsolete after code changes
   - If multiple AI reviews exist from the same bot, focus primarily on the MOST RECENT one
   - Earlier reviews can provide context but don't need deep consideration of each item
   - Look for patterns across reviews but don't duplicate work on issues already addressed
4. Read the changed files to understand actual code context

### Step 2: Categorize All Feedback
Sort every suggestion into priority buckets:

#### 🔴 Must Fix (Always address):
- Actual bugs, logic errors, race conditions, data corruption
- Realistic security vulnerabilities (with actual attack vector)
- Production-breaking changes
- Silent failures that hide errors

#### 🟡 Worth Considering (Fix if easy):
- Confusing error messages users will see
- Resource leaks (connections, files, goroutines)
- Error handling that makes debugging hard
- Performance issues with clear, measurable impact

#### 🟢 Quick Wins (Just do them - < 30 seconds each):
- Typos in user-facing messages or docs
- Style/lint issues (unused imports, formatting)
- Minor naming improvements (if truly confusing)

#### ⚪ Deprioritized (High bar to address):
- **Test coverage** - Only add if:
  - Regression-prone area (has broken multiple times)
  - Complex business logic genuinely hard to verify manually
  - Critical path expensive to break in production
  - **Skip**: Generic "should add tests" without specific risk
- **Theoretical issues** - Only if realistic and likely to occur
- **Theoretical security** - Only if realistic attack vector exists
- **Complex refactoring** - Only if current code will clearly cause problems soon
- **Over-engineering** - YAGNI applies

### Step 3: Present Summary
Before making any changes, show:
```
## PR Review Triage

### 🔴 Must Fix (X items)
1. [File:Line] [Brief description] - [Why it's critical]

### 🟡 Worth Considering (X items)
1. [File:Line] [Brief description]

### 🟢 Quick Wins (X items)
- [List of quick fixes]

### ⚪ Deprioritized (X items - skipping)
- X test suggestions (note any that seem genuinely valuable)
- X theoretical concerns (note any with realistic risk)

**Plan**: Fix 🔴 must-fix items + 🟢 quick wins. Address 🟡 if straightforward.
```

### Step 4: Ask for Confirmation
"Proceed with fixes? Or would you like me to adjust the plan?"

### Step 5: Make Fixes
Once confirmed:
- **🔴 Must-fix**: Explain why + minimal change needed
- **🟡 Worth considering**: Fix if genuinely easy (< 5 min)
- **🟢 Quick wins**: Just fix, group in output ("Fixed 8 style/lint issues")
- **⚪ Deprioritized**: Skip (already noted in summary)

## Output Format

### Summary First (before fixes):
Show triage summary (see Step 3)

### Then Fixes:
```
### Fixes Applied

#### 🔴 Critical Fixes:
**[File:Line] - [Issue]**
- Why this matters: [Real-world impact]
- Fix: [What changed]

#### 🟡 Important Fixes:
[Same format]

#### 🟢 Quick Wins:
- Fixed 3 typos in error messages
- Removed 2 unused imports
- Fixed formatting in 4 files

### Skipped (as planned):
- 12 test suggestions (none met high bar)
- 5 theoretical concerns (no realistic risk)
```

## Key Principles
- **Triage first, fix second** - Always show the summary before making changes
- **Quick wins are free** - Just do style/typo fixes without overthinking
- **Deprioritized ≠ ignored** - Note if something genuinely matters despite being in that category
- **When in doubt, ask** - Better to confirm than guess
