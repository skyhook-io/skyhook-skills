---
name: handoff
description: Use when the user asks for a handoff, a prompt for another agent, or to delegate a task to a fresh session (Claude, Codex, a teammate). Writes a self-contained discussion prompt or work order and copies it to the clipboard.
---

Read `../skyhook-skills-commands/handoff.md` relative to this skill's installed
directory and follow it. In this repository, the source is
`../../../plugins/skyhook-skills/commands/handoff.md`.

Keep the prompt free of local paths, pair every hard rule with an exit, and grant
no outward actions (push, merge, post) unless the user asked for them.
