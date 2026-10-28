---
description: Set up (or check, or remove) your own watcher that approves a PR when you reply "approve" in its #pr-approvals thread
argument-hint: "[setup|status|uninstall]"
---

# Approval watcher

Lets a reviewer approve a PR from Slack. When **you** reply `approve` (or
`approved`) in the thread of a `/request-approval` message, your watcher
approves that PR on GitHub **with your own `gh` login**. The review comment
names you and links your Slack reply, and the watcher confirms in the thread.

Each person runs their own watcher on their own Mac. It reacts only to its
owner's replies, so an approval is always recorded under the person who gave
it. It is a plain script on a one-minute schedule, with no model calls.

The watcher acts on your word, so read the PR before you reply `approve`: your
name is on the approval.

**Guards.** It does not approve:
- your own PR (GitHub doesn't allow it),
- a PR that is merged or closed,
- a PR with commits or a force-push after your reply. You get a thread reply
  asking you to check the new commits and reply `approve` again.

Each reply is handled once: the watcher reacts ✅ (approved) or ⚠️ (not
approved, with the reason in the thread).

## Arguments

- `setup` (default): install for the current user.
- `status`: show whether it's loaded and the last log lines.
- `uninstall`: unload and remove it. The Keychain token stays until the user
  deletes it.

## One-time workspace setup (a Slack admin does this once)

Skip this when the team already has the **PR Approvals** Slack app and its bot
token in the team password manager.

1. Create the app at api.slack.com/apps → **Create New App** → **From a
   manifest**, pick the workspace, and paste:

   ```yaml
   display_information:
     name: PR Approvals
     description: Approves PRs when a reviewer replies "approve" in #pr-approvals
   features:
     bot_user:
       display_name: PR Approvals
   oauth_config:
     scopes:
       bot:
         - channels:history
         - groups:history
         - chat:write
         - reactions:write
   settings:
     org_deploy_enabled: false
     socket_mode_enabled: false
   ```
2. **Install to Workspace**, then copy the **Bot User OAuth Token**
   (`xoxb-…`) into the team password manager.
3. In the approvals channel, run `/invite @PR Approvals`.

The token lets the app read that channel and post in it. Treat it as a secret.

## Setup (each person)

Run these steps for the user. Never ask the user to paste the Slack token into
the chat, and never type or echo it yourself: the user enters it in step 2.

1. **Check prerequisites.** `gh auth status` shows the account that should
   approve; `/usr/bin/python3 --version` works (it comes with the Xcode command
   line tools). If `gh` has several accounts, note the right login for
   `gh_user`.
2. **Store the Slack token in the Keychain.** Ask the user to run this in their
   own terminal; it prompts for the token so it never appears in the chat or in
   shell history:

   ```bash
   security add-generic-password -U -s pr-approvals-watcher -a slack-bot -w
   ```
3. **Install the script.** Find the copy shipped with the plugin, and fall back
   to the repo's `main` when the plugin isn't installed (Codex, Cursor):

   ```bash
   mkdir -p ~/.local/share/pr-approvals-watcher ~/.config/pr-approvals-watcher
   src=$(find ~/.claude/plugins -path '*skyhook-skills*/scripts/pr-approvals-watcher.py' 2>/dev/null | head -1)
   if [ -n "$src" ]; then cp "$src" ~/.local/share/pr-approvals-watcher/
   else curl -fsSL https://raw.githubusercontent.com/skyhook-io/skyhook-skills/main/plugins/skyhook-skills/scripts/pr-approvals-watcher.py \
     -o ~/.local/share/pr-approvals-watcher/pr-approvals-watcher.py; fi
   ```
4. **Write the config** at `~/.config/pr-approvals-watcher/config.json`:

   ```json
   {"slack_user_id": "U…", "channel_id": "C…", "gh_user": "optional-login"}
   ```

   - `slack_user_id`: the user's Slack member ID. Look it up with a Slack
     integration if you have one, or have the user copy it from their Slack
     profile (⋮ → Copy member ID).
   - `channel_id`: the approvals channel's ID, from a Slack integration or the
     channel's details in Slack (bottom of the About tab).
   - `gh_user`: only when `gh` has several accounts. Omit it otherwise.
5. **Schedule it with launchd** to run every minute:

   ```bash
   cat > ~/Library/LaunchAgents/io.skyhook.pr-approvals-watcher.plist <<EOF
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0"><dict>
     <key>Label</key><string>io.skyhook.pr-approvals-watcher</string>
     <key>ProgramArguments</key><array>
       <string>/usr/bin/python3</string>
       <string>$HOME/.local/share/pr-approvals-watcher/pr-approvals-watcher.py</string>
     </array>
     <key>EnvironmentVariables</key><dict>
       <key>PATH</key><string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
     </dict>
     <key>StartInterval</key><integer>60</integer>
     <key>RunAtLoad</key><true/>
     <key>StandardOutPath</key><string>$HOME/Library/Logs/pr-approvals-watcher.log</string>
     <key>StandardErrorPath</key><string>$HOME/Library/Logs/pr-approvals-watcher.log</string>
   </dict></plist>
   EOF
   launchctl bootout gui/$(id -u)/io.skyhook.pr-approvals-watcher 2>/dev/null
   launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/io.skyhook.pr-approvals-watcher.plist
   ```
6. **Verify.** Run it once by hand:
   `/usr/bin/python3 ~/.local/share/pr-approvals-watcher/pr-approvals-watcher.py`.
   No output means it ran and found nothing to do. An error names the problem:
   `not_in_channel` means the app isn't in the channel yet, `invalid_auth`
   means the token is wrong, and a Keychain error means step 2 didn't run. Then
   check that `launchctl print gui/$(id -u)/io.skyhook.pr-approvals-watcher`
   shows it loaded.

Report what you installed, the account it approves as (`gh api user --jq
.login`), and how to use it: reply `approve` in a request thread, and expect
✅ plus a confirmation within about a minute.

## Status

```bash
launchctl print gui/$(id -u)/io.skyhook.pr-approvals-watcher | grep -E 'state|last exit'
tail -n 20 ~/Library/Logs/pr-approvals-watcher.log
```

## Uninstall

```bash
launchctl bootout gui/$(id -u)/io.skyhook.pr-approvals-watcher
rm ~/Library/LaunchAgents/io.skyhook.pr-approvals-watcher.plist
rm -r ~/.local/share/pr-approvals-watcher ~/.config/pr-approvals-watcher
```

To remove the token too: `security delete-generic-password -s
pr-approvals-watcher -a slack-bot`.

## Limits

- It runs only while the Mac is awake. A reply sent from your phone while the
  laptop sleeps is handled when it wakes.
- It looks back three days. An `approve` older than that is ignored; reply
  again.
- macOS only (launchd and the Keychain).
