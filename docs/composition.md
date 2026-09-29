# Composition

## The model

An `AGENTS.md` for a repo is assembled from modules:

```
base                      always
+ layers/<layer>          the part of the system this directory is
+ languages/<language>    how code in this directory is written
+ concerns/<topic>        cross-cutting rules that apply here
tasks/<workflow>          on demand, not always loaded
```

`templates/` holds the modules. `stacks/<name>/manifest.txt` says which modules go in which directory. `scripts/compose.sh` builds the files.

## Nesting

Most agents read the `AGENTS.md` closest to the file they are editing, plus ancestors. Use this:

- **Root:** universal rules and a map of the repo. Keep it short; it is loaded for every task.
- **Per directory:** layer and language rules for that directory only. A frontend rule in the root is noise when editing Go.
- **Do not rely on discovery.** How nested files are found differs by agent. Codex concatenates files from the repo root down to the working directory, closer ones last, up to a size cap (32 KiB by default). OpenMeter's maintainers warn not to assume a root-started agent will find descendant files. Make the root list every nested file and say when to read it.
- **Conflicts:** the nearer file wins. Avoid conflicts; if a nested file must override the root, say so explicitly.

## Tasks are not always-on

Workflow modules (feature, bugfix, refactor, review, upgrade, migration) are placed in `docs/agent-tasks/` and referenced from the root. Loading every workflow into every session dilutes attention. The root tells the agent to read the matching one before starting.

## Manifest format

```
<output-path>: <item> <item> ...
```

An item is a module id under `templates/` (`base`, `languages/go`) or a path ending in `.md` relative to the manifest (for repo-specific text such as an architecture map). Lines starting with `#` are comments.

## Adding a stack

1. Create `stacks/<name>/manifest.txt`.
2. If the repo has a shape worth describing, add `architecture.md` next to it and list it first for the root output.
3. Run `scripts/compose.sh stacks/<name>/manifest.txt /tmp/out` and read the result as the agent would.

## One source of truth across tools

Claude Code reads `CLAUDE.md`; Codex, Copilot and Cursor read `AGENTS.md`. Do not maintain two files. Keep everything in `AGENTS.md` and make `CLAUDE.md` a single line:

```text
@AGENTS.md
```

Every stack manifest emits this file (`stacks/shared/claude-import.md`). Put Claude-only material (hooks, permissions, skills) under `.claude/`, not in the shared file.

## What goes where: AGENTS.md, skills, hooks

| Kind of content | Put it in | Why |
| --- | --- | --- |
| One-line guardrails, invariants, commands, boundaries | `AGENTS.md` | Always loaded; must be short |
| Detailed procedures needed only for some tasks | A skill, or `docs/agent-tasks/` | Loaded on demand, keeps the always-on file small |
| A rule that must never be skipped (formatting, protected files, dangerous commands) | A hook or permission rule, see `enforcement/claude-code/` | The harness runs it; the agent cannot forget it |
| A rule a linter, type checker, or test can check | The tool's config | Prose is the weakest enforcement |

If a skill or hook exists for something, the `AGENTS.md` line can be one sentence pointing to it.
