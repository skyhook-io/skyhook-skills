# Git Pull Rebase Autostash (GPRA)

Perform a "git pull rebase autostash" operation - rebase my current work over the remote default branch.

Resolve the default branch first (`git symbolic-ref --short refs/remotes/origin/HEAD`, e.g. `origin/main`); below, `<default>` is that branch name without `origin/`. Fall back to `main` if it can't be resolved.

## Instructions

1. **Assess the current state** by running these commands in parallel:
   - `git status` - check for uncommitted changes (staged, unstaged, untracked)
   - `git branch --show-current` - get current branch name
   - `git log origin/<default>..HEAD --oneline` - see commits ahead of the default branch
   - `git stash list` - check existing stashes
   - `gh pr view --json number,state,title 2>/dev/null || echo "No PR"` - check if there's a PR for this branch

2. **Report the current state** to me, including:
   - Current branch name
   - Whether there are uncommitted changes
   - How many commits ahead of origin/<default>
   - Whether a PR exists for this branch

3. **Perform the rebase**:
   - First run `git fetch origin <default>` to update the remote tracking branch
   - Then run `git pull origin <default> --rebase --autostash`
   - After a successful rebase, update the local default branch to match: `git branch -f <default> origin/<default>` (skip if it is the current branch)
     (This keeps it in sync so `git log <default>..HEAD` is accurate for PR workflows)

4. **Handle the outcome**:
   - If successful: report the result and whether any stashed changes were restored
   - If there are conflicts:
     - List the conflicting files
     - Ask me how I want to proceed (resolve manually, abort, etc.)
     - Do NOT automatically resolve conflicts

5. **If a PR exists and rebase succeeded**:
   - Ask me if I want to force-push to update the PR
   - Only force-push if I confirm (use `git push --force-with-lease`)

## Important
- Always use `--force-with-lease` instead of `--force` when pushing
- Never automatically resolve merge conflicts - always ask
- If the rebase fails for any reason, clearly explain what happened and how to recover
