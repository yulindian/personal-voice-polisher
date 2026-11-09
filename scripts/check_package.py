"""Validate this skill's structure and local references; not its prose quality.

Usage: python -B scripts/check_package.py [skill_directory]
Python 3.10+ standard library only. Does not write files or contact services.
"""

from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


REQUIRED = (
    "SKILL.md", "README.md", "LICENSE", "agents/openai.yaml",
    "assets/profile-template.md", "references/onboarding.md",
    "references/editing.md", "references/sources.md", "examples/quickstart.md",
    "scripts/check_package.py",
)


def validate(root: Path) -> list[str]:
    root = root.resolve()
    errors = []
    for relative in REQUIRED:
        if not (root / relative).is_file():
            errors.append(f"缺少文件：{relative}")
    entry = root / "SKILL.md"
    if entry.is_file():
        try:
            text = entry.read_text(encoding="utf-8")
            front = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
            if not front:
                errors.append("SKILL.md 缺少 YAML front matter")
            else:
                if not re.search(r"(?m)^name: personal-voice-polisher\s*$", front[1]):
                    errors.append("SKILL.md name 必须为 personal-voice-polisher")
                if not re.search(r"(?m)^description:\s*\S", front[1]):
                    errors.append("SKILL.md 缺少 description")
        except (OSError, UnicodeError) as exc:
            errors.append(f"无法读取 SKILL.md：{exc}")

    for relative in REQUIRED:
        path = root / relative
        if path.suffix != ".md" or not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"无法读取 {relative}：{exc}")
            continue
        for raw in re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", text):
            target = raw.strip().strip("<>")
            url = urlsplit(target)
            if url.scheme or target.startswith("#"):
                continue
            linked = (path.parent / unquote(url.path)).resolve()
            if not linked.is_relative_to(root):
                errors.append(f"引用越界：{relative} -> {target}")
            elif not linked.exists():
                errors.append(f"引用不存在：{relative} -> {target}")
    return errors


def main() -> int:
    if len(sys.argv) > 2:
        print("用法：python -B scripts/check_package.py [skill_directory]", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).resolve().parents[1]
    if not root.is_dir():
        print(f"目录不可读或不存在：{root}", file=sys.stderr)
        return 1
    errors = validate(root)
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        return 1
    print(f"PASS：{len(REQUIRED)} 个必需文件及其本地引用有效（不代表文风效果已验证）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
