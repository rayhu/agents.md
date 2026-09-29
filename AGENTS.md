# AGENTS.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A library of modular `AGENTS.md` building blocks for AI coding agents, plus a script that composes them into per-repo files. The product is markdown, not code. The rationale (constrain the agent, prefer machine-checkable rules) is in `README.md`; read it before changing the philosophy of a module.

There is no build, lint, or test suite yet. The only executable is the composer.

## Commands

```bash
# Generate the AGENTS.md files for a stack into a scratch dir
scripts/compose.sh stacks/<stack>/manifest.txt "$TMPDIR/out"

# Check every stack still composes (run after editing any module or manifest)
for s in stacks/*/; do scripts/compose.sh "$s/manifest.txt" "$TMPDIR/out-$(basename "$s")"; done
```

`compose.sh` fails on a missing module and warns when an output named `*AGENTS.md` exceeds `AGENTS_MAX_LINES` (default 200). Do not write generated output into the repo.

## Architecture

Three layers, one direction of dependency:

1. `templates/<category>/<name>/AGENTS.md` are the source-of-truth modules. Categories: `base`, `languages`, `layers`, `concerns`, `tasks`. A module id is its path under `templates/` (e.g. `languages/go`).
2. `stacks/<stack>/manifest.txt` maps output paths to lists of modules. Format: `<output-path>: <item> <item> ...`, where an item is a module id, or a `*.md` path relative to the manifest (used for repo-specific text such as `architecture.md` or `routing.md`).
3. `scripts/compose.sh` concatenates the items in order, separated by a blank line.

Constraints that are easy to break:

- Modules are concatenated, so each starts with a `##` heading and has no `#` title. Do not add front matter.
- Manifests deliberately keep root outputs short: the root is a map plus universal rules. Cross-cutting concerns go to `docs/agent-rules/` and task workflows to `docs/agent-tasks/`, loaded on demand. Adding a module to a root output raises its line count; check the warning.
- Put a rule in the most general module that applies. Do not duplicate it across modules.
- Modules must be concrete and short (about 20 to 60 lines). See `docs/authoring-guide.md`.

`enforcement/` holds starter tool configs (tsconfig, eslint, pyproject, golangci). They have not been run against a real project.

`docs/composition.md` explains nesting and manifests; `docs/prior-art.md` records outside `AGENTS.md` examples and which lessons were applied.

## Language

All repo content is English. 
