"""Structural checks only; prose quality is evaluated with real agent trials."""

import importlib.util
from pathlib import Path
import tempfile
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "check_package.py"
TEMP_ROOT = Path(__file__).resolve().parents[1] / ".tmp" / "unit-tests"
TEMP_ROOT.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location("check_package", MODULE_PATH)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class PackageChecks(unittest.TestCase):
    def make_package(self, root):
        for relative in checker.REQUIRED:
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("# Example\n", encoding="utf-8")
        (root / "SKILL.md").write_text(
            "---\nname: personal-voice-polisher\ndescription: Use when polishing prose.\n---\n# Skill\n",
            encoding="utf-8",
        )

    def test_missing_entrypoint_is_actionable(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temp:
            errors = checker.validate(Path(temp))
            self.assertTrue(any("SKILL.md" in error for error in errors))

    def test_complete_portable_package_passes(self):
        with tempfile.TemporaryDirectory(prefix="中文 路径 ", dir=TEMP_ROOT) as temp:
            root = Path(temp)
            self.make_package(root)
            (root / "README.md").write_text(
                "[template](assets/profile-template.md)\n[source](https://example.com)\n",
                encoding="utf-8",
            )
            self.assertEqual(checker.validate(root), [])

    def test_missing_reference_is_reported(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temp:
            root = Path(temp)
            self.make_package(root)
            (root / "SKILL.md").write_text(
                (root / "SKILL.md").read_text(encoding="utf-8")
                + "[details](references/nonexistent.md)\n",
                encoding="utf-8",
            )
            self.assertTrue(any("nonexistent.md" in e for e in checker.validate(root)))

    def test_reference_cannot_escape_package(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temp:
            root = Path(temp) / "skill"
            root.mkdir()
            self.make_package(root)
            (Path(temp) / "private.md").write_text("private", encoding="utf-8")
            (root / "README.md").write_text("[private](../private.md)\n", encoding="utf-8")
            self.assertTrue(any("越界" in e for e in checker.validate(root)))

    def test_wrong_skill_name_is_rejected(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temp:
            root = Path(temp)
            self.make_package(root)
            path = root / "SKILL.md"
            path.write_text(path.read_text(encoding="utf-8").replace(
                "name: personal-voice-polisher", "name: different-skill"
            ), encoding="utf-8")
            self.assertTrue(any("name" in e for e in checker.validate(root)))


if __name__ == "__main__":
    unittest.main()
