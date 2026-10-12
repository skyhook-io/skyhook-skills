import os
import re
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


SOURCE = Path(__file__).resolve().parents[1]


class InstallCodexTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="skyhook installer ")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.repo = self.root / "source checkout"
        self.repo.mkdir()
        for directory in ("scripts", "codex", "plugins"):
            shutil.copytree(SOURCE / directory, self.repo / directory)
        self.git("init", "-q")
        self.git("add", ".")
        self.git("-c", "user.name=Installer test", "-c", "user.email=test@example.invalid",
                 "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null",
                 "commit", "-qm", "Fixture")
        self.revision = self.git("rev-parse", "HEAD").stdout.strip()
        self.user_home = self.root / "user home"
        self.user_home.mkdir()
        self.env = dict(os.environ, HOME=str(self.user_home))
        self.env.pop("CODEX_HOME", None)
        self.skills = self.user_home / ".codex/skills"

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.repo), *args],
                              check=True, text=True, capture_output=True)

    def install(self):
        return subprocess.run(["bash", str(self.repo / "scripts/install-codex.sh")],
                              cwd=self.root, env=self.env, check=True,
                              text=True, capture_output=True)

    def assert_bundle(self):
        for source in (self.repo / "codex/skills").glob("*/SKILL.md"):
            installed = self.skills / source.parent.name / "SKILL.md"
            self.assertEqual(source.read_bytes(), installed.read_bytes())
            references = re.findall(r"`(\.\./skyhook-skills-commands/[^`]+\.md)`",
                                    installed.read_text())
            for reference in references:
                resolved = (installed.parent / reference).resolve()
                canonical = self.repo / "plugins/skyhook-skills/commands" / resolved.name
                self.assertEqual(resolved.read_bytes(), canonical.read_bytes())
        for source in (self.repo / "plugins/skyhook-skills/commands").glob("*.md"):
            installed = self.skills / "skyhook-skills-commands" / source.name
            self.assertEqual(source.read_bytes(), installed.read_bytes())

    def test_fresh_install_and_repeat_preserve_unrelated_skill(self):
        unrelated = self.skills / "personal/SKILL.md"
        unrelated.parent.mkdir(parents=True)
        unrelated.write_text("My personal skill\n")
        first = self.install()
        self.assert_bundle()
        marker = self.skills / "skyhook-skills-commands/.source-revision"
        self.assertEqual(marker.read_text().strip(), self.revision)
        self.assertIn(self.revision, first.stdout)
        self.assertIn("retro -> ../skyhook-skills-commands/retro.md", first.stdout)
        self.assertIn("claude-review -> self-contained skill", first.stdout)
        self.assertIn(str(self.skills / "skyhook-skills-commands"), first.stdout)
        self.assertNotIn("WARNING", first.stderr)
        second = self.install()
        self.assert_bundle()
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(unrelated.read_text(), "My personal skill\n")

    def test_update_refreshes_commands_and_reports_modified_source(self):
        self.install()
        command = self.repo / "plugins/skyhook-skills/commands/retro.md"
        command.write_text(command.read_text() + "\nFixture update\n")
        updated = self.install()
        self.assert_bundle()
        self.assertIn(self.revision + " (modified checkout)", updated.stdout)
        self.assertIn("modified checkout",
                      (self.skills / "skyhook-skills-commands/.source-revision").read_text())

    def test_copied_ignored_command_marks_source_as_modified(self):
        self.git("config", "status.showUntrackedFiles", "no")
        command = self.repo / "plugins/skyhook-skills/commands/local-only.md"
        command.write_text("Local command not in the recorded commit\n")
        (self.repo / ".git/info/exclude").write_text("local-only.md\n")
        result = self.install()
        self.assert_bundle()
        self.assertIn(self.revision + " (modified checkout)", result.stdout)
        self.assertIn("modified checkout",
                      (self.skills / "skyhook-skills-commands/.source-revision").read_text())

    def test_conflicting_adapter_is_reported_and_preserved(self):
        conflict = self.user_home / ".agents/skills/retro/SKILL.md"
        conflict.parent.mkdir(parents=True)
        legacy = "---\nname: retro\n---\nFollow `/old/commands/retro.md`.\n"
        conflict.write_text(legacy)
        result = self.install()
        self.assertIn(str(conflict), result.stderr)
        self.assertIn("/old/commands/retro.md", result.stderr)
        self.assertEqual(conflict.read_text(), legacy)
        self.assert_bundle()

    def test_same_file_symlink_is_not_reported_as_competing_adapter(self):
        self.install()
        linked = self.user_home / ".agents/skills"
        linked.parent.mkdir(parents=True)
        linked.symlink_to(self.skills, target_is_directory=True)
        result = self.install()
        self.assertNotIn("WARNING", result.stderr)
        self.assertTrue(linked.is_symlink())

    def test_custom_install_reports_references_and_preserves_default_copy(self):
        self.install()
        default_adapter = self.skills / "retro/SKILL.md"
        previous = default_adapter.read_bytes()
        self.env["CODEX_HOME"] = str(self.root / "custom codex")
        self.skills = Path(self.env["CODEX_HOME"]) / "skills"
        result = self.install()
        self.assert_bundle()
        self.assertIn(str(default_adapter), result.stderr)
        self.assertIn("references the default ~/.codex/skills command bundle", result.stderr)
        self.assertEqual(default_adapter.read_bytes(), previous)

    def test_archive_install_reports_unavailable_revision_without_failing(self):
        archive = self.root / "source archive"
        archive.mkdir()
        for directory in ("scripts", "codex", "plugins"):
            shutil.copytree(self.repo / directory, archive / directory)
        self.repo = archive
        result = self.install()
        self.assert_bundle()
        self.assertIn("source revision unavailable", result.stderr)
        self.assertIn("unavailable (git metadata could not be read)", result.stdout)
        self.assertEqual(
            (self.skills / "skyhook-skills-commands/.source-revision").read_text().strip(),
            "unavailable (git metadata could not be read)")

    def test_nested_archive_does_not_claim_enclosing_repository_revision(self):
        archive = self.repo / "unpacked archive"
        archive.mkdir()
        for directory in ("scripts", "codex", "plugins"):
            shutil.copytree(self.repo / directory, archive / directory)
        self.repo = archive
        result = self.install()
        self.assert_bundle()
        self.assertNotIn(self.revision, result.stdout)
        self.assertIn("source revision unavailable", result.stderr)
        self.assertIn("unavailable",
                      (self.skills / "skyhook-skills-commands/.source-revision").read_text())

    def test_piped_install_fetches_bundle_and_cleans_temporary_checkout(self):
        shim_dir = self.root / "shim"
        shim_dir.mkdir()
        actual_git = shutil.which("git")
        shim = shim_dir / "git"
        shim.write_text('#!/usr/bin/env python3\n'
                        'import os, sys\n'
                        'args = sys.argv[1:]\n'
                        'if args and args[0] == "clone":\n'
                        '    args[-2] = os.environ["FIXTURE_SOURCE"]\n'
                        '    with open(os.environ["CLONE_LOCATION"], "w") as log:\n'
                        '        log.write(args[-1])\n'
                        '    if os.environ.get("SIMULATE_FETCH_FAILURE") == "1":\n'
                        '        sys.exit(23)\n'
                        'os.execv(os.environ["ACTUAL_GIT"], ["git", *args])\n')
        shim.chmod(0o755)
        location = self.root / "clone location"
        self.env.update(PATH=str(shim_dir) + os.pathsep + self.env["PATH"],
                        FIXTURE_SOURCE=str(self.repo), ACTUAL_GIT=actual_git,
                        CLONE_LOCATION=str(location))
        result = subprocess.run(["bash"],
                                input=(self.repo / "scripts/install-codex.sh").read_text(),
                                cwd=self.root, env=self.env, check=True,
                                text=True, capture_output=True)
        self.assert_bundle()
        self.assertIn("Fetching https://github.com/skyhook-io/skyhook-skills", result.stdout)
        self.assertIn(self.revision, result.stdout)
        clone = Path(location.read_text())
        self.assertFalse(clone.parent.exists())
        self.env["SIMULATE_FETCH_FAILURE"] = "1"
        failure = subprocess.run(["bash"],
                                 input=(self.repo / "scripts/install-codex.sh").read_text(),
                                 cwd=self.root, env=self.env, text=True, capture_output=True)
        self.assertEqual(failure.returncode, 23)
        self.assertNotIn("Installed skills", failure.stdout)
        self.assertFalse(Path(location.read_text()).parent.exists())
        self.assert_bundle()


if __name__ == "__main__":
    unittest.main()
