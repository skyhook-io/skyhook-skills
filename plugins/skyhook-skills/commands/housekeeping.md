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
   - Recurse each workspace root once, matching all names in a single `find` with a shared `-prune` so a matched dir is never descended into. One combined pass (not one per name) is what prevents double-counting — both same-name nesting (`node_modules` in `node_modules`) and cross-name nesting (`__pycache__` in `.venv`):
     `find <root> -type d \( -name node_modules -o -name .next -o -name .venv -o -name .terraform \) -prune`  (extend the `-o -name …` list with the names below)
   - Reserved artifact names (never legit source — safe to list as reclaimable):
     - JS/TS: `node_modules`, `.next`, `.nuxt`, `.svelte-kit`, `.turbo`, `.angular`, `.parcel-cache`
     - Python: `.venv`, `__pycache__`, `.pytest_cache`, `.mypy_cache`
     - IaC: `.terraform`
     - JVM: per-repo `.gradle`
   - All Reclaimable now, but regeneration has a cost (see Classification) — state the regen command per type (`npm install`, `terraform init`, `next build`, etc.).

   - Skip repos with any live process inside them — dev servers, agents (Claude, Codex), Python, anything: `lsof -d cwd 2>/dev/null | grep '<repo path>'`. Deleting files under a running process breaks it.
   - Copy-on-write clones (`cp -c`) and pnpm hard links share blocks, so summed sizes overstate what deleting frees.

4. Temp dirs and side checkouts — usually the biggest forgotten bucket:
   - `/private/tmp`, `$TMPDIR` (`/var/folders/...`), and agent scratch dirs (`/tmp/claude-<uid>/<project>/<session-id>/...`) collect review clones, worktrees, recordings and debug output.
   - Agent scratch dirs belong to sessions, and a running agent's cwd is its project, not its scratchpad, so the `lsof` cwd check misses them. Only consider a session dir with no file modified in the last few days (`find <dir> -type f -mtime -3` prints nothing *and* exits 0 — an error also prints nothing) and whose session id is not a running agent's; never the current session's own scratchpad.
   - **Symlinks first:** these roots hold links into live workspaces. Size with `[ -L "$d" ] && continue`, resolve with `readlink`, and never treat a link as a deletable checkout.
   - Every repo: `git worktree list`, and `git worktree prune -n -v` (dry run) to list registrations whose folder is gone; the real prune is an approved action. Side checkouts in workspace roots (`repo-copy`, `repo-pr123`, `repo-review`) are common.
   - A checkout is **settled** when: no changes or untracked files, no stash (standalone clones only — worktrees share the parent repo's stash, which survives removal), no local-only commits, its branch's PR is merged/closed (`gh pr list --head <branch> --state all`), and no live process has its cwd inside it (same `lsof` check as step 3).
     - Local-only commits: for a worktree, `git log HEAD --not --remotes` (covers detached HEAD; its other branches live on in the parent repo). For a standalone clone, `git log HEAD --branches --not --remotes`, since deleting the clone deletes every branch in it. If local-only commits remain, check whether their content is on main; archive them with `git bundle create <durable path>.bundle HEAD` (add `--branches` for a clone) before deleting — a durable path outside the checkout, such as the workspace root, never `/tmp`. A bundle keeps every commit including merges; restore a clone with `git clone <bundle>`, a worktree's commits with `git fetch <bundle> HEAD:refs/heads/<restored-branch>` (a bare `git fetch` only sets `FETCH_HEAD`).

5. Agent transcripts and tool caches (no retention by default; grow with use):
   - `~/.codex/sessions` — rollout JSONL per session; compaction snapshots, raw tool output and sub-agents can make single files 100 MB–1.5 GB. No age/size setting exists. List by mtime (`find ~/.codex/sessions -name 'rollout-*.jsonl*' -mtime +30`); deleting loses `codex resume` for those sessions.
   - `~/.claude/projects/*/*.jsonl` — same trade-off.
   - `~/Library/Caches/go-build`, `~/.npm/_cacache`, `~/.npm/_npx`, the pnpm store. Once approved, reclaim with `go clean -cache`, `npm cache clean --force`, `npm cache npx rm --force`, `pnpm store prune`.
   - `~/Library/Caches/ms-playwright-mcp/mcp-chrome-*` — one Chrome profile per project, almost all cache. Recommend clearing only `Default/Cache` and `Default/Code Cache` in profiles idle for weeks and not open (`lsof +D`); that keeps logins.

6. Check services/processes only with read-only commands:
   - `ps`, `pgrep`, `lsof`, `brew services list`
   - Explain any daemon/service before recommending a kill/stop.

7. Review package/tool state:
   - Homebrew: `brew doctor`, `brew missing`, `brew outdated --verbose`, `brew leaves`, `brew services list`
   - Docker: `docker system df` only if Docker is running
   - Local model managers: inspect model names/dates before recommending removal

8. For workspaces/backups:
   - List size and modified date.
   - For git repos, inspect status, branch, ahead/behind, untracked files, and recent commits.
   - Before recommending deletion, assess whether work was merged/subsumed. If uncertain, recommend archiving diffs first.

## Classification

- **Reclaimable now (free)**: logs, package caches, old build caches, deleted-tool caches, clearly unused local model files after confirming names/dates.
- **Reclaimable now (regen cost)**: reserved per-project dependency/build dirs (`node_modules`, `.venv`, `.terraform`, `.next`, etc.). Low-risk to delete but reclaiming costs a reinstall/rebuild (network + time) — note the cost alongside the size.
- **Worth reviewing**: Downloads, browser profiles, workspace backups, old branches, local database data, Docker volumes, agent session transcripts (lose resume/search), side checkouts that are not fully settled.
- **Leave alone**: Docker VM disk image, active Chrome profiles, database data directories, app support directories with account/session state, active services, system daemons.

## Output

Report a compact ranked list:

- **Reclaimable now**: path, size, why low-risk, what would be lost.
- **Worth reviewing**: path, size, decision needed, what would be lost.
- **Leave alone**: path, size, reason.
- **Suggested next approvals**: exact commands/actions grouped by risk.

Never perform the suggested approvals until the user explicitly says to do that cleanup.

When approved, delete safely: `cd` to a known root, then one explicit `rm -rf -- <relative path>` per target, each guarded (`[ ! -L path ]`). No `xargs`/`find -delete` unless the exact list was shown first. Remove worktrees with `git -C <parent> worktree remove <real path>` — never via a symlink, since git follows it and deletes the target.

## Notes

- Docker Desktop VM size may not shrink after object pruning; host VM size and Docker logical usage are different.
- Chrome profile data is user state, not just cache.
- Embedded browser profiles lose cookies, local storage, site data, history/session restore, and extension/profile state.
- Homebrew `Cellar` is mostly installed software; separate direct leaf tools from transitive libraries before recommending updates/removals.
- Deprecated running services (old database versions, orphaned daemons) require an explicit migration/removal decision, not a reflexive kill.
- macOS `du` is BSD, not GNU: `du --files0-from=-` and similar GNU-only flags don't exist. Sum sizes with a per-dir loop instead.
- Free space can lag or be eaten by concurrent writers; judge a cleanup by the "used" column of `df`, not "avail".
- `du -sch $(find ...)` overflows the arg list on large repos and returns blank/0B totals — pipe `find` into a loop or `xargs -0`.
