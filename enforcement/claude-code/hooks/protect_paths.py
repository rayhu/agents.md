#!/usr/bin/env python3
"""PreToolUse hook: block edits to paths that must never be hand-edited.

Claude Code passes the tool call as JSON on stdin. Exit code 2 blocks the
call and feeds stderr back to the agent; exit code 0 allows it.

Extra patterns can be added, one glob per line, in
<project>/.claude/protected-paths.txt (lines starting with # are ignored).
"""

from __future__ import annotations

import fnmatch
import json
import os
import sys
from pathlib import Path

DEFAULT_PATTERNS: tuple[str, ...] = (
    "*.lock",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "go.sum",
    "uv.lock",
    "Cargo.lock",
    "node_modules/*",
    "dist/*",
    ".env",
    ".env.*",
)

EDIT_TOOLS = frozenset({"Write", "Edit", "MultiEdit"})


def load_patterns(project_dir: Path) -> tuple[str, ...]:
    extra_file = project_dir / ".claude" / "protected-paths.txt"
    extra: list[str] = []
    if extra_file.is_file():
        for line in extra_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                extra.append(line)
    return DEFAULT_PATTERNS + tuple(extra)


def matched_pattern(path: str, project_dir: Path, patterns: tuple[str, ...]) -> str | None:
    candidate = Path(path)
    try:
        relative = candidate.resolve().relative_to(project_dir.resolve()).as_posix()
    except ValueError:
        relative = candidate.as_posix()
    for pattern in patterns:
        if fnmatch.fnmatch(relative, pattern) or fnmatch.fnmatch(Path(relative).name, pattern):
            return pattern
    return None


def decide(event: dict[str, object], project_dir: Path) -> str | None:
    """Return a block message, or None to allow."""
    if event.get("tool_name") not in EDIT_TOOLS:
        return None
    tool_input = event.get("tool_input")
    if not isinstance(tool_input, dict):
        return None
    path = tool_input.get("file_path")
    if not isinstance(path, str):
        return None
    pattern = matched_pattern(path, project_dir, load_patterns(project_dir))
    if pattern is None:
        return None
    return (
        f"Blocked: {path} matches protected pattern '{pattern}'. "
        "Generated, lock, and secret files are not hand-edited. "
        "Regenerate with the project's tool, or ask the user to change the protected list."
    )


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        print(f"protect_paths: invalid hook input: {exc}", file=sys.stderr)
        return 1
    if not isinstance(event, dict):
        print("protect_paths: hook input is not a JSON object", file=sys.stderr)
        return 1
    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()))
    message = decide(event, project_dir)
    if message is None:
        return 0
    print(message, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
