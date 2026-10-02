# Git Pull Rebase Autostash (GPRA)

Perform a "git pull rebase autostash" operation - rebase my current work over the remote default branch.

Resolve the default branch first by asking the remote: `git ls-remote --symref origin HEAD` prints `ref: refs/heads/<default>	HEAD`. Below, `<default>` is that branch name. Don't trust a local `origin/HEAD`, which goes stale when the remote renames its default branch. Fall back to `main` only if the remote can't be reached.

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
   - After a successful rebase, fast-forward the local default branch so `git log <default>..HEAD` stays accurate for PR workflows. Skip this if it is the current branch. Only move it when it has no local-only commits: if `git merge-base --is-ancestor <default> origin/<default>` succeeds, run `git branch -f <default> origin/<default>`; otherwise leave it alone and report that local `<default>` has commits not on `origin/<default>`.

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
