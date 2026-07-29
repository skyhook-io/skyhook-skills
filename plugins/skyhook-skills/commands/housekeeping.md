# Housekeeping

Scan local cleanup targets and recommend actions. Do not delete, kill, uninstall, prune, reset, update, or otherwise mutate anything until the user explicitly approves a specific action.

## Scope

Inventory disk usage, stale developer tools, caches, old services/processes, Homebrew/Docker/Chrome/workspace bloat, and other local housekeeping targets.

## Read-Only Workflow

1. Establish disk pressure:
   - `df -h /System/Volumes/Data /`
   - top-level `du -hd 1` scans for home, Library, workspace roots (detect where the user's repos actually live — e.g. `~/workspace`, `~/dev`, `~/src` — or ask), `/opt/homebrew`, `/Applications`, `/usr/local`

2. Drill into large buckets:
   - `~/Library/Application Support`
   - `~/Library/Containers`
   - `~/Library/Caches`
   - workspace roots and `~/Downloads`
   - large dot-directories, e.g.: `.config`, `.cache`, `.local`, `.gradle`, `.nvm`, `.vscode`, `.cursor`, `.codex`, `.claude`, `.gemini`, `.ollama`

3. Check services/processes only with read-only commands:
   - `ps`, `pgrep`, `lsof`, `brew services list`
   - Explain any daemon/service before recommending a kill/stop.

4. Review package/tool state:
   - Homebrew: `brew doctor`, `brew missing`, `brew outdated --verbose`, `brew leaves`, `brew services list`
   - Docker: `docker system df` only if Docker is running
   - Local model managers: inspect model names/dates before recommending removal

5. For workspaces/backups:
   - List size and modified date.
   - For git repos, inspect status, branch, ahead/behind, untracked files, and recent commits.
   - Before recommending deletion, assess whether work was merged/subsumed. If uncertain, recommend archiving diffs first.

## Classification

- **Reclaimable now**: logs, package caches, old build caches, deleted-tool caches, clearly unused local model files after confirming names/dates.
- **Worth reviewing**: Downloads, browser profiles, workspace backups, old branches, local database data, Docker volumes.
- **Leave alone**: Docker VM disk image, active Chrome profiles, database data directories, app support directories with account/session state, active services, system daemons.

## Output

Report a compact ranked list:

- **Reclaimable now**: path, size, why low-risk, what would be lost.
- **Worth reviewing**: path, size, decision needed, what would be lost.
- **Leave alone**: path, size, reason.
- **Suggested next approvals**: exact commands/actions grouped by risk.

Never perform the suggested approvals until the user explicitly says to do that cleanup.

## Notes

- Docker Desktop VM size may not shrink after object pruning; host VM size and Docker logical usage are different.
- Chrome profile data is user state, not just cache.
- Embedded browser profiles lose cookies, local storage, site data, history/session restore, and extension/profile state.
- Homebrew `Cellar` is mostly installed software; separate direct leaf tools from transitive libraries before recommending updates/removals.
- Deprecated running services (old database versions, orphaned daemons) require an explicit migration/removal decision, not a reflexive kill.
