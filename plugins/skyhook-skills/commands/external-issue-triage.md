---
description: Triage externally reported bugs and feature requests, suggest a fast human acknowledgment, investigate the evidence, and prepare a private recommendation for the maintainer. Use for contributor or user reports, not implementation or internal backlog grooming.
argument-hint: "<GitHub URL> [focus or constraints]"
---

# External contributor issue triage

Use the GitHub issue URL supplied by the user (command arguments in Claude),
with any trailing focus or constraints. Resolve the repository and issue number
before investigating. If no target was supplied, use an unambiguous target from
the session or ask for it; do not guess a different contribution.

Give reporters a timely, honest response and help the maintainer decide what to do. Keep the public reply and private investigation separate. This workflow ends at triage and a recommendation; the maintainer decides what happens next.

## Exact-message approval

Never post any message without the maintainer's explicit approval of its exact text and destination. This includes acknowledgments, clarification questions, comments, and newly filed issues or tickets. A request to triage, agreement with the diagnosis, or approval of an earlier draft does not authorize posting. If the text changes, obtain approval again. Show proposed replies as drafts. Once an exact message is approved, post only that message to the approved destination without requesting approval again.

Do not implement a fix, open a PR, change labels or assignees, close the issue, or create tracking work as part of triage unless separately authorized.

## Fast first response

Read the report and existing conversation first so the proposed response reflects what the reporter already supplied and what maintainers have already said. Do a brief initial check to determine whether the report is clearly valid and well scoped. Do not delay a useful acknowledgment until a deep investigation finishes.

If diagnosis or direction remains uncertain and investigation will take time, suggest a short acknowledgment early in a commentary update for the maintainer to approve, then continue independent investigation. Never send it automatically. Avoid implying that an investigation, fix, or timeline has been committed. For example: "Thanks for reporting this. I don't have a clear explanation yet."

If the initial check establishes a real, needed, narrowly scoped bug or feature, use a slightly more positive response tied to the evidence. For example: "Thanks for reporting this. The namespace filter is getting lost when switching views. Keeping it in the URL looks like a small fix." Only use those specifics if verified. "We'll try to prioritize this soon" is an optional soft commitment for the maintainer to approve when the scope and priority justify it, never a default sign-off.

For a larger request, uncertain cause, or unclear product fit, acknowledge the use case without endorsing the proposed solution or promising work. Follow documented project scope and surface unresolved product decisions privately. Do not invent a restriction or disclose private context in public copy.

Ask the reporter only for information that materially changes the diagnosis and cannot reasonably be obtained from the issue or repository. Draft a focused question if needed; do not prescribe a generic environment/log checklist. If an existing maintainer response already serves as an acknowledgment, avoid proposing a redundant one.

## Voice

Public drafts must read like a real maintainer talking to another person. Be brief, plain, specific, and honest. No canned AI phrasing, inflated warmth, excessive apologies, exaggerated appreciation, or unrequested walls of helpful advice. Avoid formulas such as "Thank you for bringing this to our attention," "rest assured," and "we appreciate your patience." Do not copy example wording mechanically or repeat information the reporter already knows. Never turn a hypothesis into a confident diagnosis for a friendlier response.

## Investigate for the maintainer

Scale the work to the uncertainty. If the initial investigation is enough, proceed directly to the private plan. Otherwise:

- Establish expected versus observed behavior, affected versions and configuration where known, reproduction steps, scope, and user impact. For a feature request, identify the underlying task and assess whether existing functionality already serves it.
- Read relevant repository instructions, docs, implementation paths, related issues, and tests. Trace the behavior instead of assuming the reporter's diagnosis is correct. Check the same pattern at related call sites and reuse existing concepts or helpers in proposed fixes.
- Reproduce or run targeted verification when it will resolve a meaningful uncertainty. State what was observed, what follows from code inspection, and what remains hypothetical. Do not equate "not reproduced" with "invalid." Avoid executing untrusted attachments or scripts blindly.
- Consider a workaround, a smaller fix, an alternative design, deferral, or declining the request when warranted. Research external behavior only if it would materially settle a technical or product question.
- Surface product and architecture decisions early. Use the project's documented scope; ask for the maintainer's direction when ownership or product fit is unresolved. Do not invent a public promise or product boundary.

Do not expand a clear small issue into an exhaustive audit. If progress depends on missing reporter evidence, say exactly what is missing and prepare the smallest useful question while completing independent checks.

## Deliver to the maintainer, then stop

Provide a private recommendation that helps the maintainer choose the next step:

- **Assessment:** validity and confidence, scope and impact, whether the proposed feature is needed and fits, and any open product decision.
- **Evidence:** what was checked, relevant code or discussion links, reproduction/test results, and remaining uncertainty.
- **Proposed plan:** the likely fix or approach, rough effort when supportable, alternatives and their tradeoffs, and additional verification needed before calling it fixed. This plan is for the maintainer, never the reporter-facing response.
- **Next decision:** recommend fix now, request focused information, defer/track, discuss product direction, or decline with a reason. Make clear what needs the maintainer's judgment.
- **Public draft:** the exact suggested acknowledgment or substantive reply, separately labeled. If an acknowledgment draft was already shown, include the current proposed text so it remains reviewable; if already sent with approval, report that and draft another reply only when it adds value.

Do not paste the internal plan, effort estimates, internal deliberations, or commercial positioning into the public draft. Stop after triage; do not autonomously transition into implementation or promise to pursue it.
