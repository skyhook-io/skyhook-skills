#!/usr/bin/env python3
"""Approve GitHub PRs from Slack: one run checks the approvals channel once.

Each person runs their own copy. It acts only on that person's own "approve"
reply in a request thread, and approves with that person's own `gh` login, so
every approval is recorded under the reviewer who gave it.

Config: ~/.config/pr-approvals-watcher/config.json
  {"slack_user_id": "U...", "channel_id": "C...", "gh_user": "optional-login"}
Slack bot token: macOS Keychain, service "pr-approvals-watcher", account "slack-bot".
"""

import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime

CONFIG_PATH = os.path.expanduser("~/.config/pr-approvals-watcher/config.json")
LOOKBACK_SECONDS = 3 * 24 * 3600
APPROVE_RE = re.compile(r"^\s*approved?\s*[.!]*\s*$", re.IGNORECASE)
PR_URL_RE = re.compile(r"https://github\.com/([\w.-]+)/([\w.-]+)/pull/(\d+)")
DONE = "white_check_mark"
REFUSED = "warning"


def log(msg):
    print(f"{datetime.now().isoformat(timespec='seconds')} {msg}", flush=True)


def keychain_token():
    return subprocess.run(
        ["security", "find-generic-password", "-s", "pr-approvals-watcher", "-a", "slack-bot", "-w"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()


class Slack:
    def __init__(self, token):
        self.token = token

    def call(self, method, **params):
        data = urllib.parse.urlencode(params).encode()
        req = urllib.request.Request(
            f"https://slack.com/api/{method}", data=data,
            headers={"Authorization": f"Bearer {self.token}"},
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = json.load(resp)
        if not body.get("ok"):
            raise RuntimeError(f"slack {method}: {body.get('error')}")
        return body


def gh(args, gh_env):
    out = subprocess.run(["gh", *args], check=True, capture_output=True, text=True, env=gh_env)
    return out.stdout


def is_approve(text):
    return bool(APPROVE_RE.match(text or ""))


def find_pr(text):
    m = PR_URL_RE.search(text or "")
    return (m.group(1), m.group(2), int(m.group(3))) if m else None


def handled_by(reply, bot_user_id):
    return any(
        r.get("name") in (DONE, REFUSED) and bot_user_id in r.get("users", [])
        for r in reply.get("reactions", [])
    )


def ts(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).timestamp() if iso else 0


def decide(pr, me, reply_ts, force_pushes=()):
    """Return (action, reason). action is 'approve', 'skip' or 'refuse'.

    force_pushes: ISO times of head_ref_force_pushed events. A force-push can
    carry old commit dates, so commit dates alone can't show what changed after
    the reply.
    """
    if pr["state"] != "OPEN":
        return "refuse", f"the PR is {pr['state'].lower()}, so there is nothing to approve"
    if pr["author"]["login"].lower() == me.lower():
        return "refuse", "this is your own PR, and GitHub doesn't allow approving your own PR"
    head = pr["headRefOid"]
    for review in pr.get("reviews", []):
        if (review.get("author") or {}).get("login", "").lower() == me.lower() \
                and review.get("state") == "APPROVED" and review.get("commit", {}).get("oid") == head:
            return "skip", "already approved at the current commit"
    commits = pr.get("commits") or []
    changed = [ts(c.get("committedDate")) for c in commits[-1:]] + [ts(t) for t in force_pushes]
    if any(t > float(reply_ts) for t in changed):
        return "refuse", "new commits were pushed after your approve; check them and reply approve again"
    return "approve", ""


def main():
    with open(CONFIG_PATH) as f:
        cfg = json.load(f)
    slack = Slack(keychain_token())
    bot_user_id = slack.call("auth.test")["user_id"]
    gh_env = dict(os.environ)
    if cfg.get("gh_user"):
        gh_env["GH_TOKEN"] = subprocess.run(
            ["gh", "auth", "token", "-u", cfg["gh_user"]], check=True, capture_output=True, text=True,
        ).stdout.strip()
    me = json.loads(gh(["api", "user"], gh_env))
    my_login, my_name = me["login"], me.get("name") or me["login"]

    history = slack.call(
        "conversations.history", channel=cfg["channel_id"],
        oldest=str(time.time() - LOOKBACK_SECONDS), limit=200,
    )
    for msg in history.get("messages", []):
        target = find_pr(msg.get("text"))
        if not target or not msg.get("reply_count"):
            continue
        replies = slack.call("conversations.replies", channel=cfg["channel_id"], ts=msg["ts"], limit=200)
        mine = [r for r in replies["messages"][1:]
                if r.get("user") == cfg["slack_user_id"] and is_approve(r.get("text"))]
        pending = [r for r in mine if not handled_by(r, bot_user_id)]
        if not pending:
            continue
        reply = pending[-1]
        owner, repo, number = target
        pr = json.loads(gh(["pr", "view", str(number), "-R", f"{owner}/{repo}",
                            "--json", "state,author,headRefOid,commits,reviews,url"], gh_env))
        timeline = json.loads(gh(["api", "--paginate", "--slurp",
                                  f"repos/{owner}/{repo}/issues/{number}/timeline"], gh_env))
        force_pushes = [e["created_at"] for page in timeline for e in page
                        if e.get("event") == "head_ref_force_pushed"]
        action, reason = decide(pr, my_login, reply["ts"], force_pushes)
        link = slack.call("chat.getPermalink", channel=cfg["channel_id"], message_ts=reply["ts"])["permalink"]
        if action == "approve":
            gh(["api", "-X", "POST", f"repos/{owner}/{repo}/pulls/{number}/reviews",
                "-f", "event=APPROVE", "-f", f"commit_id={pr['headRefOid']}",
                "-f", f"body=Approved by {my_name} via #pr-approvals: {link}"], gh_env)
            note = f"Approved on GitHub by {my_name} (@{my_login}) at {pr['headRefOid'][:7]}."
            log(f"approved {owner}/{repo}#{number}")
        elif action == "skip":
            note = None
            log(f"skip {owner}/{repo}#{number}: {reason}")
        else:
            note = f"Not approved: {reason}."
            log(f"refused {owner}/{repo}#{number}: {reason}")
        for r in pending:
            slack.call("reactions.add", channel=cfg["channel_id"], timestamp=r["ts"],
                       name=REFUSED if action == "refuse" else DONE)
        if note:
            slack.call("chat.postMessage", channel=cfg["channel_id"], thread_ts=msg["ts"], text=note)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # launchd runs this every minute; log and let the next run retry
        log(f"error: {exc}")
        sys.exit(1)
