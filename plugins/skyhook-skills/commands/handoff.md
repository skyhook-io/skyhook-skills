---
description: Write a self-contained prompt that hands a task to a fresh agent (Claude, Codex, a teammate's session) — a discussion by default, or a work order for delegation
argument-hint: "[work order] <task or short label>"
---

# Handoff — a prompt for a fresh agent

Write a prompt another agent can start from with **zero context**: a new Claude
or Codex session, a teammate's agent, or a worker you are delegating to. Use it
to switch tools mid-task, hand work to someone else, or turn a triaged issue
into something an agent can pick up.

## Pick the shape

- **Discussion (default).** The receiving agent should form its own view before
  changing anything. Use this when the direction isn't settled, the task came
  from an issue or a hunch, or someone else will own the decision.
- **Work order** (`work order` in the arguments, or `/autodev` delegating a
  settled piece). The spec is decided; the worker builds it and proves it. Use
  this only when writing the prompt forced no new decisions — if it did, those
  decisions come first.

## Gather just enough context

Infer the task from the arguments, the conversation, the branch, and linked
issues or PRs. Collect what a fresh agent needs to orient: repo, relevant
issue/PR/branch, likely modules, constraints, known symptoms, and what has
already been tried or ruled out. Don't do the receiving agent's review for it,
and mark anything you haven't verified as unverified.

## Rules for the prompt

- **Portable anchors, not local paths.** Use repo owner/name, issue and PR URLs,
  branch names, package names, public symbols, commands, config keys, exact
  error text, and search terms. No absolute or home-directory paths; the
  receiving agent may run on another machine or checkout.
- **Say what's known and how you know it.** Separate verified facts from
  hypotheses. Include what was tried and ruled out, so the next agent doesn't
  repeat it.
- **Constraints and non-goals, explicitly.** Name what not to touch, and what is
  out of scope.
- **Every hard rule gets an exit.** For each "must" or "never", add: "if you
  can't meet this honestly, stop and report what blocked you and the numbers;
  don't work around it." A cornered agent otherwise satisfies the letter of the
  rule — a weakened test, an edited baseline — and reports success.
- **Exact proof.** Name the commands or checks that show it works, and what
  evidence to report.
- **Re-check live state.** Tell the agent to verify current repo, PR, and CI
  state rather than trusting the handoff.
- **No outward actions unless granted.** No pushing, merging, closing, labeling,
  or posting comments unless the prompt explicitly allows it.

## Templates

**Discussion**

```text
I want to discuss and possibly work on: <short task title>

Context:
- <repo and product context>
- <what triggered this: issue/PR URL, report, observation>
- <current state: branch, PR, what's done, what was tried and ruled out>
- <constraints and ownership boundaries>

Before implementing anything:
- Read the repo's agent instructions and relevant docs.
- Inspect the relevant code, tests, recent commits, and live issue/PR/CI state.
- Decide whether this is still real, already solved, over-scoped, or better
  handled differently, and whether a smaller or better fix exists.
- Call out stale assumptions and anything that should stop the work.

Task (if your review supports it):
- <what to investigate or build>
- <expected behavior or decision criteria>
- Non-goals: <...>

Validation:
- <checks or live proof expected, and the evidence to include>

Output:
- Start with your findings and recommendation, then the plan or patch summary.
- Report the exact proof you ran.
- Don't push, merge, close, label, or post comments unless told to.
```

**Work order**

```text
Goal: <one sentence, the outcome>

Repo: <owner/name>, branch <name> (verify it's current before starting).
Where: <modules, symbols, entrypoints>

Spec:
- <decided behavior, as concrete as possible>
- <precedent to imitate: "follow the shape of PR #NNN">

Constraints:
- <must / must not> — if you can't meet this honestly, stop and report why.
- Don't touch: <files, APIs, baselines, thresholds>.
- Non-goals: <...>

Proof: <exact commands that must pass>, plus <live check if relevant>.

Report: files changed, commands run with results, anything you stopped on and
why, and anything you were unsure about. Do exactly this; don't start adjacent
work.
```

## Deliver

Write the prompt to a temp file and copy it to the clipboard (`pbcopy <
"$file"` on macOS; `wl-copy`, `xclip`, or `clip.exe` elsewhere). Use a quoted
heredoc to write it, so backticks and `$` survive. Reply with the task title,
the shape used, and anything you marked unverified; paste the full prompt only
if asked or if the clipboard is unavailable.
