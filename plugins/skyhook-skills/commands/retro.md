# Session Retrospective

Reflect on the current session and identify concrete improvements to agent configuration (Claude Code or Codex), documentation, and workflows that would prevent friction and improve future sessions.

## Step 1: Gather Context

Read these files to understand the current setup (read in parallel, skip any that don't exist):

**Configuration:**
- `~/.claude/settings.json` - user-level settings, hooks, permissions
- `.claude/settings.json` (in repo root) - project-level settings
- `~/.claude/CLAUDE.md` - user-level instructions
- `CLAUDE.md` (in repo root) - project-level instructions
- Any parent `CLAUDE.md` files (e.g., workspace-level)
- When running in Codex: `AGENTS.md` (repo and parents), `$CODEX_HOME/AGENTS.md`, `$CODEX_HOME/config.toml` (`$CODEX_HOME` defaults to `~/.codex`)

**Custom commands:**
- List files in `~/.claude/commands/` - user-level slash commands
- List files in `.claude/commands/` (in repo root) - project-level slash commands
- When running in Codex: list `$CODEX_HOME/skills/`
- Note which commands/skills come from a plugin (e.g. `/plugin` list, `~/.claude/plugins/`) rather than a local file — they are edited in a different place (see category D)

**Project docs:**
- `README.md` - does it have accurate build/run instructions?
- `DEVELOPMENT.md`, `CONTRIBUTING.md` - if they exist
- `.gitignore` - anything missing?

## Step 2: Analyze the Session

Think carefully about the full conversation history. For each interaction, consider:

### Friction Points
- **Wrong approach**: Did I take a wrong initial approach that required user correction? What information was missing or what assumption was wrong?
- **Repeated corrections**: Did the user have to tell me the same thing more than once? Could a CLAUDE.md rule prevent this?
- **Wasted iterations**: Were there back-and-forth cycles that could have been avoided with better upfront context?
- **Tool/permission friction**: Did the user have to approve tool uses that should be pre-allowed? Did I use the wrong tool for a task?
- **Missing context**: Did I have to ask questions or make wrong assumptions that better documentation would have prevented?
- **Excessive changes**: Did I modify more than requested, reformat unrelated code, or make unnecessary changes?
- **Wrong file/target**: Did I edit the wrong file or miss the right one?

### What Went Well
- What workflows were smooth and efficient?
- What patterns should be reinforced or documented?

### Environment Issues
- Were there build/test/tooling issues that better documentation could prevent?
- Were there missing dependencies, wrong paths, or stale configs?

## Step 3: Propose Improvements

For each finding, propose a **specific, actionable change** in one of these categories:

### A. CLAUDE.md Updates (Repo-Level)
Rules, conventions, or context that would help in this specific repository.
- Project conventions (naming, patterns, architecture decisions)
- Build/test commands and common gotchas
- File organization and where to find things
- Things NOT to do (common mistakes)

### B. CLAUDE.md Updates (User-Level — create `~/.claude/CLAUDE.md` if needed)
Rules that apply across all your projects.
- Personal workflow preferences
- Git/commit conventions
- Communication style preferences
- Things you consistently correct

### C. Settings Changes (`~/.claude/settings.json` or `.claude/settings.json`)
- Permission pre-approvals that would reduce friction
- Hook suggestions (pre-commit checks, post-edit validations)

### D. New or Updated Slash Commands (`~/.claude/commands/` or `.claude/commands/`)
- Repetitive multi-step workflows that should be a single command
- Existing commands that need updating based on session experience

**Where a command change goes depends on where the command comes from:**
- Local file in `~/.claude/commands/` or `.claude/commands/`: edit it there.
- Plugin-provided (namespaced like `/plugin-name:command`, or listed by `/plugin`): propose the change in the **plugin's source repository**, not the installed copy. The installed copy under `~/.claude/plugins/` (or `$CODEX_HOME/skills/`) is overwritten on the next update. Never "fix" a plugin command by adding a same-named file to `~/.claude/commands/` — it silently shadows the plugin and drifts from it.
- For skyhook-skills that repository is `github.com/skyhook-io/skyhook-skills`: commands in `plugins/skyhook-skills/commands/<name>.md` (shared by Claude, Codex and Cursor), Codex/Cursor adapters in `codex/skills/<name>/SKILL.md`. Propose the edit as a PR there.

### E. Documentation Improvements
- README.md updates (build instructions, architecture, setup)
- Missing docs that caused confusion
- Stale docs that led to wrong assumptions

### F. Other Improvements
- `.gitignore` additions
- Build scripts, Makefiles, or dev tooling
- CI/CD or workflow improvements

## Step 4: Present Findings

Output your findings in this format:

```
## Session Retro

### What Went Well
- [Bullet points of smooth workflows and effective patterns]

### Friction Points Found
For each issue:
- **What happened**: [Brief description]
- **Root cause**: [Why it happened]
- **Proposed fix**: [Specific change with exact file path and content]
- **Category**: [A-F from above]

### Proposed Changes (Priority Order)

#### High Impact (would have saved significant time this session)
[List with exact file paths and proposed content]

#### Medium Impact (would improve future sessions)
[List with exact file paths and proposed content]

#### Low Impact (nice to have)
[List with exact file paths and proposed content]
```

## Step 5: Apply Changes

After presenting findings, ask the user which changes they'd like to apply. Then make the approved changes directly — edit the files, don't just suggest.

## Important Guidelines
- Be specific. "Add a CLAUDE.md rule" is not enough — write the exact rule text.
- Prioritize by impact. Lead with changes that would have prevented the most friction in THIS session.
- Don't over-engineer. Only propose changes backed by actual session evidence, not theoretical improvements.
- Keep CLAUDE.md rules concise. One line per rule when possible. Claude reads these every session.
- Consider whether a fix belongs at user-level (all repos) or repo-level (this project only).
- In Codex, map the categories to their equivalents: `AGENTS.md` for CLAUDE.md, `$CODEX_HOME/config.toml` for settings, `$CODEX_HOME/skills/` for commands.
- If you can't find evidence of friction, say so. Not every session needs improvements. A short "everything went smoothly" retro is perfectly fine.
