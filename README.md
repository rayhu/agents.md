# agents.md

A curated library of `AGENTS.md` files for AI coding agents, organized by scenario.

Not "write clean code" prompts. Each file is a **narrow, checkable specification** that shrinks the space of valid implementations, and points at the tools that enforce it.

## Why this repo exists

### 1. The bottleneck is no longer agent intelligence

Agents are smart enough to write almost anything. The failure mode is different: they have too much freedom. Given a bare repo, a shell, and an instruction, an agent can pick any of seven ways to do a thing, invent an abstraction, add a dependency, or swallow an error and move on.

Handing an agent a bare repo and letting it improvise is the equivalent of handing someone a bare machine and asking for assembly. It works, but the freedom is the problem.

The engineering-quality formula we believe in:

```
AI intelligence  ×  strong constraints  ×  fast feedback
```

not

```
AI intelligence  ×  maximum flexibility
```

### 2. High-level languages took freedom away, and systems got more reliable

Assembly allowed self-modifying code, arbitrary jumps, and hand-managed stacks. High-level languages did not make those tricks impossible for their own sake. They removed them, and the whole system became more reliable.

AI-assisted development is going through the same shift:

```
Before:  machine code ← assembly ← high-level language ← framework
Now:     general language ← constrained subset ← schema / types / contracts ← agent policy / verifier
```

Go, TypeScript, Rust and strict Python become a stable, uniform, verifiable intermediate layer. The real "high-level language" for agents is the **set of constraints**: allowed APIs, allowed side effects, input/output schemas, error types, resource limits, invariants, required tests.

`AGENTS.md` is where those constraints are declared to the agent.

### 3. Most existing AGENTS.md files have no constraining power

```
Write clean code.
Follow best practices.
Add tests.
Keep functions small.
```

An agent cannot act on this. A useful `AGENTS.md` reads like **language spec + architecture rules + verifier configuration**:

- names the exact libraries and forbids the alternatives (so "Redux? Zustand? Context? SWR?" is never an open question),
- lists forbidden patterns (`Any`, `dict[str, Any]`, raw `fetch()`, string-built SQL),
- states what "done" means as commands that must pass,
- says which layer owns which behavior.

### 4. One AGENTS.md does not fit every situation

A React frontend, a Go API, a Python LLM service, a database migration, and a bug fix need different rules. A single 10,000-line file is noise for every task. So this repo provides **small, single-purpose modules** that you compose for your repo and place close to the code they govern.

### 5. Prose is the weakest enforcement

`AGENTS.md` is still just a prompt. The design principle across every file here:

> If a machine-checkable rule can replace a prose convention, prefer the machine-checkable rule.

```
AGENTS.md                → tells the agent what the rules are
compiler / type checker  → forces part of them
linter                   → narrows the valid space further
schema                   → constrains the boundaries
tests                    → verify behavior
runtime permissions      → limit actual capability
```

Keep `AGENTS.md` short; back every important rule with a tool. The [`enforcement/`](enforcement/) directory holds the tool configs that make the rules real.

## Design principles

The language and stack choices in these modules follow this priority order:

```
constraint strength > verifiability > ecosystem maturity > development speed > expressiveness
```

Properties we favor, because they are easy for agents and easy to check:

1. **Strong static types.** No `Any`, no dynamic bags, no magic coercion.
2. **Explicit semantics.** `Result<T, E>` or explicit `(T, error)` over "sometimes `None`, sometimes throws".
3. **Small, uniform standard library.** One obvious way to do it.
4. **Schema at every boundary.** Zod, Pydantic, Protobuf, JSON Schema, OpenAPI.
5. **Machine-checkable constraints.** Compiler, type checker, linter, tests, contracts.
6. **Little implicit behavior.** No hidden side effects, no framework magic where a plain alternative exists.

Rough AI-friendliness of languages under this lens:

| Language | AI-friendliness | Why |
| --- | --- | --- |
| Rust | Very high | Compiler constraints are extremely strong; errors are useful feedback |
| TypeScript (strict) | Very high | Fast type feedback, huge ecosystem |
| Go | Very high | Small language, one way to write things; "boring" is a feature |
| Kotlin / Swift | High | Strong types, null safety, explicit semantics |
| Python + strict tooling | High | Ecosystem is irreplaceable, but must be constrained |
| Bare Python | Medium | Too free |
| JavaScript | Medium-low | Too much dynamic behavior |
| Bash | Low | String semantics, weak error model |

## Repository layout

```
agents.md/
├── README.md
├── templates/                 # Modular AGENTS.md building blocks (source of truth)
│   ├── base/                  # Universal rules; every stack includes this
│   ├── languages/             # Per-language rules: typescript, go, python-strict, rust
│   ├── layers/                # Per-architecture-layer rules: frontend, api, ai-service, db, contracts
│   ├── concerns/              # Cross-cutting: llm-and-agents, testing, dependencies, security, ...
│   └── tasks/                 # Per-workflow: feature, bugfix, refactor, code-review, upgrade, migration
├── stacks/                    # Ready-made compositions: which modules go where in a repo
│   ├── fullstack-ts-go-py/
│   ├── typescript-web-app/
│   ├── go-service/
│   └── python-ai-service/
├── enforcement/               # Tool configs that turn prose rules into machine checks
│   ├── typescript/
│   ├── go/
│   ├── python/
│   └── claude-code/           # Hooks and permissions (protected paths, format-on-edit, deny/ask lists)
├── scripts/
│   └── compose.sh             # Builds AGENTS.md files from a stack manifest
└── docs/
    ├── composition.md         # How nesting and composition work
    ├── prior-art.md           # Public AGENTS.md files worth studying, and what we took from them
    └── authoring-guide.md     # How to write a good module
```

### The five module categories

| Category | Question it answers | Examples |
| --- | --- | --- |
| `base` | What holds for every repo and every agent? | deterministic-first, validate boundaries, no speculative abstraction, definition of done |
| `languages` | What is the allowed subset of this language? | strict TS, Go, strict Python, Rust |
| `layers` | Which part of the system am I in, and what does it own? | React+Vite, Next.js, Go API, Python AI service, Postgres, API contracts |
| `concerns` | What rules apply wherever this topic appears? | LLM/agent safety, testing, dependencies, security |
| `tasks` | What process do I follow for this kind of work? | feature, bugfix, refactor, review, dependency upgrade, DB migration |

Layers say *where* code lives. Languages say *how* it is written. Concerns say *what must never be violated*. Tasks say *how to do this specific job*.

## How to use

**Pick a stack** and generate the files:

```bash
scripts/compose.sh stacks/fullstack-ts-go-py/manifest.txt ./out
# writes ./out/AGENTS.md, ./out/apps/web/AGENTS.md, ./out/services/api/AGENTS.md, ...
```

Copy the output into your repo. Agents that support nested `AGENTS.md` use the closest one to the file being edited, so the root stays short and each directory carries only its own rules.

**Or hand-pick modules:** open `templates/<category>/<name>/AGENTS.md` and copy what you need.

**Then wire up enforcement.** For every rule in your `AGENTS.md`, ask whether a tool can enforce it. Start from [`enforcement/`](enforcement/).

## What a good module looks like

- **Short.** A module is one topic, roughly 20 to 60 lines.
- **Concrete.** Names tools, libraries and commands. "Use TanStack Query for server state" beats "manage state sensibly".
- **Forbids specific things.** A closed list of banned patterns, with the escape hatch stated (where the exception must be contained).
- **Checkable.** Where possible, says which command or linter rule verifies it.
- **Explains the "why" only when it changes behavior.**

See [docs/authoring-guide.md](docs/authoring-guide.md).

## Opinionated defaults

The default full-stack architecture assumed by the `fullstack-ts-go-py` stack:

| Layer | Default | Reason |
| --- | --- | --- |
| Frontend | TypeScript strict + React + Vite | Strong types, mature ecosystem, few moving parts |
| SSR / SEO | Next.js, only when SSR/RSC is actually needed | Server/client components, caching, and rendering modes add state space |
| API contract | OpenAPI / JSON Schema | Types are derived, not hand-duplicated |
| Core backend | Go + Postgres + pgx + sqlc | Small language, explicit behavior, statically checked SQL |
| AI / LLM service | Python strict (uv, ruff, pyright strict, pytest) + FastAPI + Pydantic | Ecosystem is irreplaceable; isolate and constrain it |
| Validation | Zod (TS), Pydantic (Python), typed structs (Go) | Runtime check at every boundary |

The architecture principle: **different degrees of freedom live in different places.**

```
UI (TypeScript)
   ↓ typed API contract
Go deterministic core
   ↓ explicit AI boundary
Python / LLM
```

and around every LLM call:

```
deterministic code → typed request → LLM → schema validation → deterministic code
```

These are defaults, not dogma. Fork the modules and swap in your own stack; keep the principles.

## Status

Early. Modules are drafts; expect the structure to settle as they get used in real repos. Contributions that make a rule more concrete or more checkable are the most valuable ones.
