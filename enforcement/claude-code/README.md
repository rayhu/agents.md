# Claude Code enforcement

Turns prose rules from `AGENTS.md` into checks the harness runs. A rule the agent can forget in prose cannot be forgotten in a hook.

| Rule in AGENTS.md | Enforced by |
| --- | --- |
| Do not hand-edit generated, lock, or secret files | `hooks/protect_paths.py` (PreToolUse, blocks the edit) |
| Formatting is not a judgment call | `hooks/format_on_edit.py` (PostToolUse, formats every written file) |
| No force-push, no destructive deletes, no reading `.env` | `permissions.deny` in `settings.json` |
| Human approval for publishing, pushing, adding dependencies | `permissions.ask` in `settings.json` |

## Install

```bash
mkdir -p .claude/hooks
cp enforcement/claude-code/hooks/protect_paths.py enforcement/claude-code/hooks/format_on_edit.py .claude/hooks/
cp enforcement/claude-code/settings.json .claude/settings.json   # or merge into an existing one
```

Add project-specific protected globs, one per line, to `.claude/protected-paths.txt` (for example `*.gen.ts`, `internal/db/*.sql.go`, `db/migrations/*` for migrations already applied).

## Behavior

- Hooks read the tool call as JSON on stdin. Exit code 2 blocks a PreToolUse call, or sends stderr back to the agent after a PostToolUse; exit code 0 allows.
- `format_on_edit.py` picks a formatter by extension (`gofmt`, `ruff format`, `prettier`) and does nothing if the binary is not installed. If the formatter fails, the error goes back to the agent.
- Invalid hook input fails loudly (exit 1) rather than silently allowing.

## Status and limits

- Tested: the two hooks, with `python3 -m unittest discover -s enforcement/claude-code/hooks`. `format_on_edit.py` was also run against real `gofmt` and `ruff`.
- Not tested: `prettier`, and the `settings.json` in a live Claude Code session. Check the permission pattern syntax against the current Claude Code docs before relying on it.
- Permissions are a safety net, not a sandbox. A determined command can be phrased to avoid a prefix pattern.
- Other agents (Codex, Cursor) have their own hook and permission mechanisms; these files are Claude Code only.

## Not enforceable by hooks

Judgment rules (choose the right layer, keep the diff small) stay in `AGENTS.md`. Convert any rule you catch an agent breaking twice into a hook, lint rule, or test.
