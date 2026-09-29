"""Tests for the hooks. Run: python3 -m unittest discover -s enforcement/claude-code/hooks"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).parent


def run(script: str, event: dict[str, object], project: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(HERE / script)],
        input=json.dumps(event),
        capture_output=True,
        text=True,
        env={"CLAUDE_PROJECT_DIR": str(project), "PATH": "/usr/bin:/bin"},
        check=False,
    )


def edit(path: str) -> dict[str, object]:
    return {"tool_name": "Edit", "tool_input": {"file_path": path}}


class ProtectPathsTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.project = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_blocks_lockfile(self) -> None:
        result = run("protect_paths.py", edit(str(self.project / "pnpm-lock.yaml")), self.project)
        self.assertEqual(result.returncode, 2)
        self.assertIn("protected", result.stderr)

    def test_blocks_env_file(self) -> None:
        result = run("protect_paths.py", edit(str(self.project / ".env.local")), self.project)
        self.assertEqual(result.returncode, 2)

    def test_allows_source_file(self) -> None:
        result = run("protect_paths.py", edit(str(self.project / "src" / "main.go")), self.project)
        self.assertEqual(result.returncode, 0)

    def test_ignores_non_edit_tools(self) -> None:
        event = {"tool_name": "Bash", "tool_input": {"command": "ls"}}
        self.assertEqual(run("protect_paths.py", event, self.project).returncode, 0)

    def test_project_patterns_extend_defaults(self) -> None:
        (self.project / ".claude").mkdir()
        (self.project / ".claude" / "protected-paths.txt").write_text("# generated\n*.gen.ts\n")
        result = run("protect_paths.py", edit(str(self.project / "api.gen.ts")), self.project)
        self.assertEqual(result.returncode, 2)

    def test_invalid_json_fails_loudly(self) -> None:
        result = subprocess.run(
            [sys.executable, str(HERE / "protect_paths.py")],
            input="not json",
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 1)


class FormatOnEditTest(unittest.TestCase):
    def test_unknown_extension_is_a_noop(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "notes.txt"
            path.write_text("x")
            self.assertEqual(run("format_on_edit.py", edit(str(path)), Path(tmp)).returncode, 0)

    def test_missing_file_is_a_noop(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run("format_on_edit.py", edit(str(Path(tmp) / "gone.go")), Path(tmp))
            self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
