import json
from pathlib import Path
import re
import unittest

REPO = Path(__file__).resolve().parent.parent


class AntigravityPluginTest(unittest.TestCase):
    def test_manifest_and_version_match_claude_plugin(self):
        ag_manifest = json.loads((REPO / ".antigravity-plugin/plugin.json").read_text())
        claude_manifest = json.loads(
            (REPO / "plugins/skyhook-skills/.claude-plugin/plugin.json").read_text()
        )
        self.assertEqual(ag_manifest["name"], "skyhook-skills")
        self.assertEqual(ag_manifest["version"], claude_manifest["version"])
        skills_rel = ag_manifest["skills"]
        self.assertTrue((REPO / skills_rel).is_dir())

    def test_every_skill_has_matching_frontmatter_and_valid_command_refs(self):
        skills_root = REPO / "antigravity/skills"
        skill_dirs = sorted(p for p in skills_root.iterdir() if p.is_dir())
        self.assertGreaterEqual(len(skill_dirs), 20)

        for skill_dir in skill_dirs:
            skill_md = skill_dir / "SKILL.md"
            self.assertTrue(skill_md.is_file(), f"Missing {skill_md}")
            text = skill_md.read_text()
            match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
            self.assertIsNotNone(match, f"Missing YAML frontmatter in {skill_md}")
            frontmatter = match.group(1)
            name_match = re.search(r"^name:\s*(\S+)\s*$", frontmatter, re.MULTILINE)
            desc_match = re.search(r"^description:\s*.+$", frontmatter, re.MULTILINE)
            self.assertIsNotNone(name_match, f"Missing name in {skill_md}")
            self.assertIsNotNone(desc_match, f"Missing description in {skill_md}")
            self.assertEqual(
                name_match.group(1),
                skill_dir.name,
                f"Skill frontmatter name must match folder in {skill_md}",
            )

            refs = re.findall(r"`(\.\./\.\./\.\./plugins/skyhook-skills/commands/[^`]+\.md)`", text)
            self.assertTrue(refs, f"No canonical command reference in {skill_md}")
            for ref in refs:
                target = (skill_dir / ref).resolve()
                self.assertTrue(target.is_file(), f"Broken reference {ref} in {skill_md}")


if __name__ == "__main__":
    unittest.main()
