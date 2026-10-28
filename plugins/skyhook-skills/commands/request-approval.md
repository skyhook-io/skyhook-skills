---
description: Ask the team for a PR approval in the approvals Slack channel, with an urgency level (NOW, 1H, 1D)
argument-hint: "[now|1h|1d] [PR number or URL]"
---

# Request approval

When a PR can't merge without a human approval, post one line to the team's
approvals channel so a reviewer picks it up at the right speed. The channel is
how approvals get routed: a PR nobody announces waits until someone happens to
look.

## When to post

Post only when all of these hold:

1. **The PR needs a human approval to merge.**
   `gh pr view <pr> --json reviewDecision,isDraft,state,url,title,number,headRepository`
   returns `reviewDecision: "REVIEW_REQUIRED"`. Any other value means no
   approval is required, or it is already approved or has changes requested:
   don't post. An empty `reviewDecision` means the base branch doesn't require
   reviews.
2. **It is open and not a draft.**
3. **It is ready for a human.** Your own loop is finished: the automated
   reviewers have settled and their findings are handled, and CI is green or
   only slow scanners are still pending. Don't ask a person to review code you
   are still changing. When the user asks for a review request directly, post
   now.
4. **It hasn't been posted already.** Search the channel for the PR URL first.
   If it is already there, don't post again. To raise the urgency of a PR that
   is already posted, reply in its existing thread with the new level and why.

## Urgency

| Level | Meaning | Use when |
|---|---|---|
| `NOW` | Blocking, approve right away | Fixing a live production incident or outage, or the user says it blocks them right now |
| `1H` | Approve within the hour | The user is waiting on it to continue today, or it unblocks another PR |
| `1D` | Approve within the day | Everything else. This is the default |

An explicit level from the caller (`now`, `1h`, `1d`, or an invocation
directive like `approval now`) wins. Otherwise pick a level from the table,
default to `1D`, and say in your report which level you chose and why. Never
use `NOW` without a concrete reason, and put that reason in the line.

## The message

Exactly one line, in this format:

```
[NOW|1H|1D] <repo>#<number> <PR title> <PR link> - <one line on what it changes and the risk>
```

For example:

```
[1D] radar-hub#412 Retry webhook delivery on 5xx https://github.com/org/radar-hub/pull/412 - retries failed webhook sends up to 3 times; low risk, delivery path only
```

- `<repo>` is the repository name without the owner.
- The last part is for the reviewer: what the change does and how risky it is,
  in plain words. Name the risky part when there is one ("touches auth
  middleware", "changes the DB schema").
- No @-mentions unless the user asks for a specific reviewer.
- Nothing sensitive: no secrets, customer names, or internal URLs other than the
  PR link.

## Where and how

- **Channel:** `SKYHOOK_APPROVAL_CHANNEL` env var, else `approvalChannel` in
  `~/.claude/skyhook-skills.json` (`cat ~/.claude/skyhook-skills.json
  2>/dev/null`), else `#pr-approvals`.
- **Send** with the Slack integration available to you (for example, a Slack
  MCP `slack_send_message` tool). Find the channel by name first if the tool
  needs an ID.
- **If your instructions require approval before sending messages**, show the
  exact line and wait for the user's go-ahead. Those instructions win over this
  command.
- **No Slack integration, or the channel doesn't exist?** Don't fail the run.
  Print the exact line, tell the user to post it in the channel, and list it as
  an open item in your report.

## After posting

Reviewers who run `/approval-watcher` can approve by replying `approve` in the
message's thread; their watcher approves on GitHub under their own login.


- Report the level, the line you posted, and a link to the message when the
  tool returns one.
- Never merge, and never use an admin bypass (`gh pr merge --admin`, disabling
  branch protection) to skip the approval. Those are the user's calls, even in
  an emergency.
- If you push new commits after an approval and the approval is dismissed,
  reply in the PR's existing thread in the channel instead of posting a new
  line.
