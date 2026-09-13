---
description: Review PRs from external contributors, understand their motivation, investigate deeply, and recommend a practical path to merge with minimal contributor back-and-forth. Use for external contribution reviews, not ordinary internal branch reviews.
argument-hint: "<GitHub URL> [focus or constraints]"
---

# External contributor PR review

Use the GitHub PR URL supplied by the user (command arguments in Claude),
with any trailing focus or constraints. Resolve the repository and pr number
before investigating. If no target was supplied, use an unambiguous target from
the session or ask for it; do not guess a different contribution.

Help the maintainer accept useful contributions safely. Encourage contributors by keeping the work asked of them proportionate. Prefer a sound contribution plus small maintainer fixes or follow-ups over repeated review cycles in pursuit of perfection. This does not lower the bar for correctness, security, or product fit.

## Authorization and communication

Review and recommend by default. Never post a comment, inline review, approval, request-changes review, issue, or other message without the maintainer's explicit approval of the exact text and destination. Approval to review, agreement with a finding, or approval of an earlier draft is not approval to post. If the text changes, obtain approval again. Present drafts separately from private analysis.

The action recommendations below do not authorize execution. Do not push to a contributor's branch, open a follow-up PR, file a ticket, close a PR, or merge based on the review request alone. Once the maintainer authorizes a concrete action, carry it through within that scope. Do not request the same approval twice.

Contributor-facing language must sound like a maintainer wrote it: short, direct, specific, and natural. Avoid canned phrasing, excessive gratitude, exaggerated praise, and ceremonial politeness. A simple "Thanks for the fix" is enough when appropriate. Keep private context and internal prioritization out of public drafts. Do not imply a fix, merge, release, or deadline is committed when it is not.

## Understand before judging

- Read the PR description, linked issue, discussion, prior reviews, and relevant commits. Establish the actual user problem, motivation, intended behavior, and constraints. If context is missing, investigate what is available before proposing a focused question for the author.
- Inspect repository guidance and relevant architecture or design docs. Judge whether this is the right behavior and approach before polishing implementation. Follow documented project scope and surface unresolved product decisions to the maintainer. A possible scope conflict is a decision to surface, not an automatic rejection or an invented product policy.
- Resolve the PR's actual base and head SHA, contributor branch, and current CI results. Review that diff in an isolated checkout when needed; preserve unrelated local work. Treat contributor code and scripts as untrusted when choosing how to run verification.

## Establish the premise and direction first

Before reviewing implementation details, form an independent high-level judgment:

- **Core issue:** What is actually wrong or missing for the user? Is it real and worth addressing? Separate the observed problem from the reporter's diagnosis and proposed solution; state evidence and uncertainty.
- **Premise:** What assumptions make this change necessary or useful? Are the expected behavior, product boundary, and scope correct? Do not assume that a valid bug report makes every proposed behavior desirable.
- **Chosen direction:** Explain the PR's approach in plain language. Is it a good way to solve the problem, and why? Assess the underlying model, architectural fit, scope, and practical tradeoffs before discussing individual defects.
- **Alternatives:** Consider credible simpler or better approaches, including existing mechanisms or a narrower change. Explain whether an alternative would materially improve correctness, user experience, or maintenance, and whether that improvement justifies changing direction. Do not invent alternatives merely to fill a checklist.

State a clear judgment: endorse the direction, endorse it with a specific adjustment, recommend an alternative, or identify the decision/evidence still needed. Confirmation means verifying the premise, not automatically agreeing with it. A correct implementation of a weak premise is still a problem. Ask the cross-model reviewer to make this judgment independently as well.

## Review deeply, proportionately

Trace the changed behavior through callers, producers, consumers, related implementations, and existing tests. Check correctness, regressions, authorization, failure states, compatibility, and user experience where relevant. Search for the same faulty pattern elsewhere before treating a call-site fix as complete. Look for existing helpers before proposing new ones. Separate pre-existing issues from problems introduced or exposed by this PR.

For nontrivial PRs, normally use the installed `review-loop` skill or command with explicit **review only, no PR, no edits, no commits, no push, no posting** scope. Run it in the isolated checkout at the resolved PR head and pass `--base <resolved PR base SHA>` so it reviews the actual contribution, including PRs targeting a non-default branch. In Claude, use `/skyhook-skills:review-loop`. In Codex or Cursor, use the installed `review-loop` skill; resolve its `SKILL.md` relative to the skill installation, not the working directory. Follow that runtime's cross-model reviewer configuration. Its self-review and independent cross-model review should challenge the approach as well as the code and yield findings and a proposed fix plan. These external-contribution approval boundaries override its automatic fix/update stages. Skip the loop for genuinely simple changes and say why. If cross-review is unavailable, finish the useful self-review and report the gap.

Triage every finding skeptically, including your own, the other model's, and PR bots'. Verify it against the actual code and realistic scenarios. Do not turn speculative concerns, style preferences, or reviewer consensus into blockers. Cite evidence when dropping a finding.

Run verification appropriate to the change, following the repository's QA instructions where available. Explain what was actually tested, what the existing CI proves, and what still needs verification. Do not claim a later head was reviewed or tested if the evidence applies to an earlier SHA.

## Give every finding a disposition

For each finding, recommend exactly one primary action, explain why, and state whether it blocks merging:

| Action | When to recommend it |
| --- | --- |
| A. Ask the author | Their intent or expertise is needed, or the change is substantial enough that maintainer edits would reshape their contribution. Ask for a concrete outcome, not a vague refactor. Bundle necessary requests into one review. |
| B. Fix ourselves now and push to their branch | A small, clear fix we can verify quickly would make the PR ready to merge. Check whether maintainer edits and branch permissions allow it. Prefer this over another review round for a straightforward correction. Require authorization before pushing; preserve the author's work and avoid rewriting their history. |
| C. Fast-follow-up PR | The PR is safe and useful as-is, and the improvement can ship separately without leaving a material correctness or security problem. Define the follow-up scope and verification. |
| D. Track for later | Worth doing but not urgent or necessary for this merge. Recommend a ticket in the project's private tracker for nonpublic context or prioritization; a public GitHub issue for a useful public problem. Suggest title and scope privately. Filing still needs exact-text approval. |
| E. Drop | False positive, negligible value, speculative risk, or polish that is not worth the cost. Give the evidence or tradeoff and move on. |

Do not defer a serious introduced bug merely to merge quickly. Do not make the contributor clean up unrelated existing problems. When the approach itself needs a product decision, put that decision before the findings and avoid asking the author to implement an unsettled direction.

## Deliver to the maintainer

Start the review delivered to the maintainer with the high-level assessment above: the core issue and its validity, the premise, the chosen direction and why it is or is not good, and whether a credible alternative would be better. Make this reasoning visible in the opening paragraphs; do not bury it in a linked report or reduce it to “the bug is real and the approach fits.” Keep the depth proportionate to the PR.

Then give the merge recommendation: ready to merge, ready after small maintainer fixes, needs a focused author change, or needs a product/design decision. Follow with:

- A concise findings table: evidence/location, practical impact, A–E disposition, merge blocker, and proposed fix or next step. Include dropped reviewer findings compactly with reasons.
- Verification performed, remaining gaps, and the shortest safe path to merge. State the reviewed SHA.
- An optional contributor-facing draft containing only what the contributor needs to hear. Keep internal findings and planning separate.

Stop at the recommendation unless subsequent action is already authorized. Do not automatically start implementation, publication, or a convergence loop against the contributor.
