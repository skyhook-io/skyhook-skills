import importlib.util
import pathlib
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "plugins/skyhook-skills/scripts/pr-approvals-watcher.py"
spec = importlib.util.spec_from_file_location("watcher", SCRIPT)
watcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(watcher)

REPLY_TS = "1793176200.000100"  # 2026-10-28T08:30:00Z


def pr(**over):
    base = {
        "state": "OPEN",
        "author": {"login": "nadaverell"},
        "headRefOid": "abc123",
        "commits": [{"committedDate": "2026-10-28T08:00:00Z"}],
        "reviews": [],
    }
    base.update(over)
    return base


class ApproveText(unittest.TestCase):
    def test_accepts_approve_variants(self):
        for text in ["approve", "Approved", " APPROVE! ", "approved."]:
            self.assertTrue(watcher.is_approve(text), text)

    def test_rejects_anything_else(self):
        for text in ["don't approve", "approve after CI", "lgtm", "", None, "approved?"]:
            self.assertFalse(watcher.is_approve(text), text)


class FindPR(unittest.TestCase):
    def test_parses_request_line(self):
        line = "[1D] radar-hub#412 Retry webhook https://github.com/skyhook-dev/radar-hub/pull/412 - low risk"
        self.assertEqual(watcher.find_pr(line), ("skyhook-dev", "radar-hub", 412))

    def test_slack_link_markup(self):
        line = "[NOW] <https://github.com/skyhook-dev/radar-hub-web/pull/9|radar-hub-web#9>"
        self.assertEqual(watcher.find_pr(line), ("skyhook-dev", "radar-hub-web", 9))

    def test_no_pr(self):
        self.assertIsNone(watcher.find_pr("hello"))


class Handled(unittest.TestCase):
    def test_only_the_bots_reaction_counts(self):
        reply = {"reactions": [{"name": "white_check_mark", "users": ["UPERSON"]}]}
        self.assertFalse(watcher.handled_by(reply, "UBOT"))
        reply["reactions"][0]["users"].append("UBOT")
        self.assertTrue(watcher.handled_by(reply, "UBOT"))


class Decide(unittest.TestCase):
    def test_approves_open_pr_from_someone_else(self):
        self.assertEqual(watcher.decide(pr(), "roylibman", REPLY_TS)[0], "approve")

    def test_refuses_own_pr(self):
        self.assertEqual(watcher.decide(pr(author={"login": "RoyLibman"}), "roylibman", REPLY_TS)[0], "refuse")

    def test_refuses_closed_pr(self):
        self.assertEqual(watcher.decide(pr(state="MERGED"), "roylibman", REPLY_TS)[0], "refuse")

    def test_refuses_commits_after_reply(self):
        late = pr(commits=[{"committedDate": "2026-10-28T09:00:00Z"}])
        self.assertEqual(watcher.decide(late, "roylibman", REPLY_TS)[0], "refuse")

    def test_refuses_force_push_after_reply_even_with_old_commit_dates(self):
        action, _ = watcher.decide(pr(), "roylibman", REPLY_TS, ["2026-10-28T09:00:00Z"])
        self.assertEqual(action, "refuse")

    def test_skips_when_already_approved_at_head(self):
        done = pr(reviews=[{"author": {"login": "roylibman"}, "state": "APPROVED", "commit": {"oid": "abc123"}}])
        self.assertEqual(watcher.decide(done, "roylibman", REPLY_TS)[0], "skip")

    def test_old_approval_on_previous_commit_does_not_skip(self):
        old = pr(reviews=[{"author": {"login": "roylibman"}, "state": "APPROVED", "commit": {"oid": "old"}}])
        self.assertEqual(watcher.decide(old, "roylibman", REPLY_TS)[0], "approve")


if __name__ == "__main__":
    unittest.main()
