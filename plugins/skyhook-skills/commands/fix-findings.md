# Fix Review Findings

Process the review findings from the conversation above and fix valid issues.

## Step 1: List All Issues
Extract all issues mentioned (critical, important, suggestions) into a numbered list.

## Step 2: Triage Each Issue

For each issue, work through this checklist:

### Understanding
- What exactly is the issue claiming?
- Read the actual code at the referenced location
- Do I fully understand the problem being described?

### Validity Check
- Is this a real issue or a false positive?
- Does the reviewer's understanding of the code match reality?
- Are there mitigating factors the reviewer missed (e.g., caller guarantees, existing validation elsewhere)?

### Severity Assessment
- Is this a practical concern or purely theoretical?
- What's the actual likelihood of this causing problems?
- Has this pattern worked fine elsewhere in the codebase?
- **Default to Skip** for: defensive programming against things that can't happen today, guards redundant with framework behavior (e.g., chi routing already enforces HTTP method), "sync.Once on a function nothing calls twice", missing tests for trivial/obvious code, theoretical future concerns
- **Do fix** small issues that are genuinely correct improvements — the bar is "is this actually right and clearly better?", not "is this important enough?" A 1-line fix that removes real confusion or a misleading log message is worth shipping. Size doesn't matter; correctness does.

### Fix Evaluation
- If valid, what's the right fix?
- Is the suggested fix appropriate, or is there a better approach?
- Does fixing this introduce other issues or unnecessary complexity?

## Step 3: Produce Triage Summary

Output a table with columns:
| # | Issue | Verdict | Reasoning | Action |

Verdicts:
- **Fix**: Valid issue, will fix
- **Skip**: False positive or not worth fixing

## Step 4: Apply Fixes

Immediately proceed to fix all issues marked as "Fix" in the triage summary. Do not ask for confirmation - just make the changes.

**Bugs of-a-kind cluster — fix the pattern, not just the reported site.** When a finding is a *kind* of bug (a wrong call shape, a missing guard, an unsafe unwrap), grep the codebase for the same pattern before calling it fixed. Patching only the flagged line leaves the same bug at the sibling sites — the next reviewer just re-flags them. Fix every instance; if you deliberately leave one, say why.

After fixing, verify the changes compile and tests pass using whatever build/test commands are appropriate for the project.
