"""Regression checks for the public-file export boundary."""
import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
TEMP_ROOT = ROOT / ".tmp" / "release-tests"
TEMP_ROOT.mkdir(parents=True, exist_ok=True)
script = ROOT / "scripts" / "build_release.py"
builder = None
if script.is_file():
    spec = importlib.util.spec_from_file_location("build_release", script)
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)


class ReleaseChecks(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(builder, "release builder has not been implemented")
        self.temp = tempfile.TemporaryDirectory(prefix="中文 项目 ", dir=TEMP_ROOT)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for relative in builder.PUBLIC_FILES:
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("# Public example\n", encoding="utf-8")
        (self.root / "SKILL.md").write_text(
            '---\nname: personal-voice-polisher\ndescription: Example\nmetadata:\n  version: "0.1.1"\n---\n# Skill\n',
            encoding="utf-8",
        )

    def test_only_allowlisted_files_are_exported(self):
        for relative in (".voice-polisher/profiles/me/profile.md", ".env", ".tmp/debug.txt", "PLAN.md"):
            private = self.root / relative
            private.parent.mkdir(parents=True, exist_ok=True)
            private.write_text("PRIVATE_FIXTURE_DO_NOT_EXPORT", encoding="utf-8")
        output = builder.build_release(self.root)
        with ZipFile(output) as archive:
            expected = {f"personal-voice-polisher/{p}" for p in builder.PUBLIC_FILES}
            self.assertEqual(set(archive.namelist()), expected)
            self.assertNotIn(b"PRIVATE_FIXTURE_DO_NOT_EXPORT", b"".join(
                archive.read(name) for name in archive.namelist()
            ))

    def test_same_inputs_produce_same_archive(self):
        output = builder.build_release(self.root)
        first = output.read_bytes()
        self.assertEqual(builder.build_release(self.root).read_bytes(), first)

    def test_missing_public_file_fails_before_export(self):
        (self.root / "assets/profile-template.md").unlink()
        with self.assertRaisesRegex(ValueError, "profile-template"):
            builder.build_release(self.root)
        self.assertFalse((self.root / "outputs").exists())

    def test_invalid_version_cannot_control_output_path(self):
        path = self.root / "SKILL.md"
        path.write_text(path.read_text(encoding="utf-8").replace("0.1.1", "../../private"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "version"):
            builder.build_release(self.root)

    def test_nonsemantic_versions_are_rejected(self):
        path = self.root / "SKILL.md"
        original = path.read_text(encoding="utf-8")
        for invalid in ("01.2.3", "１.２.３"):
            with self.subTest(version=invalid):
                path.write_text(original.replace("0.1.1", invalid), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "version"):
                    builder.build_release(self.root)

    def test_parent_directory_link_cannot_export_private_data(self):
        private = self.root / ".voice-polisher"
        private.mkdir()
        (private / "profile-template.md").write_text("PRIVATE_DIRECTORY_FIXTURE", encoding="utf-8")
        assets = self.root / "assets"
        (assets / "profile-template.md").unlink()
        assets.rmdir()
        if os.name == "nt":
            result = subprocess.run(
                ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
                 "$ErrorActionPreference='Stop'; New-Item -ItemType Junction -Path $env:PVP_TEST_LINK -Target $env:PVP_TEST_TARGET | Out-Null"],
                env=dict(os.environ, PVP_TEST_LINK=str(assets), PVP_TEST_TARGET=str(private)),
                capture_output=True, text=True, timeout=20,
            )
            self.assertEqual(result.returncode, 0, "Test directory junction could not be created")
        else:
            assets.symlink_to(private, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "[Ll]ink|[Ee]scape"):
            builder.build_release(self.root)

    def test_linked_public_file_cannot_export_external_data(self):
        outside = self.root.parent / (self.root.name + "-private.txt")
        outside.write_text("PRIVATE_FIXTURE_DO_NOT_EXPORT", encoding="utf-8")
        self.addCleanup(outside.unlink)
        target = self.root / "assets/profile-template.md"
        target.unlink()
        try:
            target.symlink_to(outside)
        except OSError:
            self.skipTest("This environment does not permit file symlinks")
        with self.assertRaisesRegex(ValueError, "[Ll]ink|[Ee]scape"):
            builder.build_release(self.root)


if __name__ == "__main__":
    unittest.main()
