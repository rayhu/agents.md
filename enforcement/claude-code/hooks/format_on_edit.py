#!/usr/bin/env python3
"""PostToolUse hook: format the file the agent just wrote.

Formatting is enforced by the harness, not requested in prose. The formatter
is chosen by file extension. If the formatter binary is missing the hook does
nothing; if it fails, stderr is fed back to the agent (exit code 2).
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

EDIT_TOOLS = frozenset({"Write", "Edit", "MultiEdit"})

# suffix -> argv prefix; the file path is appended.
FORMATTERS: dict[str, tuple[str, ...]] = {
    ".go": ("gofmt", "-w"),
    ".py": ("ruff", "format"),
    ".ts": ("prettier", "--write"),
    ".tsx": ("prettier", "--write"),
    ".json": ("prettier", "--write"),
}


def formatter_for(path: Path) -> tuple[str, ...] | None:
    argv = FORMATTERS.get(path.suffix)
    if argv is None or shutil.which(argv[0]) is None:
        return None
    return argv


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        print(f"format_on_edit: invalid hook input: {exc}", file=sys.stderr)
        return 1
    if not isinstance(event, dict) or event.get("tool_name") not in EDIT_TOOLS:
        return 0
    tool_input = event.get("tool_input")
    path_value = tool_input.get("file_path") if isinstance(tool_input, dict) else None
    if not isinstance(path_value, str):
        return 0
    path = Path(path_value)
    argv = formatter_for(path)
    if argv is None or not path.is_file():
        return 0
    result = subprocess.run([*argv, str(path)], capture_output=True, text=True, check=False)
    if result.returncode != 0:
        print(f"{' '.join(argv)} failed on {path}:\n{result.stderr}{result.stdout}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
