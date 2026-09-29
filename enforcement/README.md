# Enforcement

`AGENTS.md` is a prompt. These configs make its rules machine-checked, so an agent cannot "forget" them.

| Rule in AGENTS.md | Enforced by |
| --- | --- |
| No `any`, strict null checks | `typescript/tsconfig.strict.json` |
| No `as` casts, no floating promises, exhaustive switches | `typescript/eslint.config.js` |
| No `Any`, complete annotations | `python/pyproject.toml` (pyright strict) |
| No bare except, no mutable defaults, no wildcard imports | `python/pyproject.toml` (ruff) |
| No ignored errors, no `panic` for control flow | `go/.golangci.yml` |
| Generated code is current | CI step: regenerate, then `git diff --exit-code` |
| Tests and types pass before done | CI + a single `make check` per layer |

Rule of thumb: when you catch an agent violating a prose rule twice, turn it into a lint rule or a test.

These are starting points. Copy them into your repo and tighten over time.
