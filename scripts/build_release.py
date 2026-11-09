"""Build a reproducible, public-only ZIP. Python 3.10+, standard library only.

Usage: python -X utf8 -B scripts/build_release.py [skill_directory]
The archive is written to that skill's outputs/ directory, never to a remote.
"""
from pathlib import Path
import re
import stat
import sys
import tempfile
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


PUBLIC_FILES = (
    ".gitignore", ".github/workflows/validate.yml", "SKILL.md", "README.md",
    "LICENSE", "CHANGELOG.md", "CONTRIBUTING.md", "agents/openai.yaml",
    "assets/profile-template.md", "references/onboarding.md", "references/editing.md",
    "references/sources.md", "examples/quickstart.md", "scripts/check_package.py",
    "scripts/build_release.py", "tests/test_check_package.py", "tests/test_build_release.py",
    "tests/scenarios.md",
)


def reject_link_components(root: Path, path: Path) -> None:
    current = root
    for component in path.relative_to(root).parts:
        current = current / component
        try:
            info = current.lstat()
        except FileNotFoundError:
            break
        reparse = getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
        if stat.S_ISLNK(info.st_mode) or reparse:
            raise ValueError(f"Linked package path: {path.relative_to(root)}")


def build_release(root: Path) -> Path:
    root = root.resolve()
    sources = []
    for relative in PUBLIC_FILES:
        source = root / relative
        reject_link_components(root, source)
        if not source.resolve().is_relative_to(root):
            raise ValueError(f"Linked or escaped package input: {relative}")
        if not source.is_file():
            raise ValueError(f"Missing public file: {relative}")
        sources.append((relative, source.read_bytes()))
    entry = dict(sources)["SKILL.md"].decode("utf-8")
    front = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", entry, re.S)
    number = r"(?:0|[1-9][0-9]*)"
    version = re.search(rf'(?m)^  version: "({number}\.{number}\.{number})"\s*$', front[1]) if front else None
    if version is None:
        raise ValueError("SKILL.md metadata.version must be a quoted semantic version (x.y.z)")
    output_dir = root / "outputs"
    reject_link_components(root, output_dir)
    if not output_dir.resolve().is_relative_to(root):
        raise ValueError("Output directory escapes the skill directory")
    output_dir.mkdir(exist_ok=True)
    output = output_dir / f"personal-voice-polisher-{version[1]}.zip"
    with tempfile.NamedTemporaryFile(dir=output_dir, suffix=".part", delete=False) as temp:
        temporary = Path(temp.name)
    try:
        with ZipFile(temporary, "w", compression=ZIP_DEFLATED) as archive:
            for relative, content in sources:
                info = ZipInfo(f"personal-voice-polisher/{relative}", date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                info.compress_type = ZIP_DEFLATED
                archive.writestr(info, content)
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
    return output


def main() -> int:
    if len(sys.argv) > 2:
        print("Usage: python scripts/build_release.py [skill_directory]", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).resolve().parents[1]
    try:
        output = build_release(root)
    except (OSError, ValueError, UnicodeError) as exc:
        print(f"Release build failed: {exc}", file=sys.stderr)
        return 1
    print(f"Built {output.name} with {len(PUBLIC_FILES)} public files in {output.parent}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
