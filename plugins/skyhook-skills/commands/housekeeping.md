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

3. Scan repos for per-project regenerable artifact dirs (these often dominate disk):
   - Recurse each workspace root for these reserved directory names, using `-prune` so nested matches don't double-count:
     `find <root> -type d -name node_modules -prune`
   - Reserved artifact names (never legit source — safe to list as reclaimable):
     - JS/TS: `node_modules`, `.next`, `.nuxt`, `.svelte-kit`, `.turbo`, `.angular`, `.parcel-cache`
     - Python: `.venv`, `__pycache__`, `.pytest_cache`, `.mypy_cache`
     - IaC: `.terraform`
     - JVM: per-repo `.gradle`
   - All Reclaimable now, but regeneration has a cost (see Classification) — state the regen command per type (`npm install`, `terraform init`, `next build`, etc.).

4. Check services/processes only with read-only commands:
   - `ps`, `pgrep`, `lsof`, `brew services list`
   - Explain any daemon/service before recommending a kill/stop.

5. Review package/tool state:
   - Homebrew: `brew doctor`, `brew missing`, `brew outdated --verbose`, `brew leaves`, `brew services list`
   - Docker: `docker system df` only if Docker is running
   - Local model managers: inspect model names/dates before recommending removal

6. For workspaces/backups:
   - List size and modified date.
   - For git repos, inspect status, branch, ahead/behind, untracked files, and recent commits.
   - Before recommending deletion, assess whether work was merged/subsumed. If uncertain, recommend archiving diffs first.

## Classification

- **Reclaimable now (free)**: logs, package caches, old build caches, deleted-tool caches, clearly unused local model files after confirming names/dates.
- **Reclaimable now (regen cost)**: reserved per-project dependency/build dirs (`node_modules`, `.venv`, `.terraform`, `.next`, etc.). Low-risk to delete but reclaiming costs a reinstall/rebuild (network + time) — note the cost alongside the size.
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
- macOS `du` is BSD, not GNU: `du --files0-from=-` and similar GNU-only flags don't exist. Sum sizes with a per-dir loop instead.
- `du -sch $(find ...)` overflows the arg list on large repos and returns blank/0B totals — pipe `find` into a loop or `xargs -0`.
