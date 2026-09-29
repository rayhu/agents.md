## Repository Architecture

```
apps/web/          TypeScript + React (Vite) frontend
services/api/      Go deterministic backend
services/ai/       Python AI / LLM service
contracts/         Shared API and schema definitions (source of truth)
db/migrations/     Database migrations
```

Respect these boundaries. Do not move logic between layers because it is convenient.

```
UI (TypeScript)
   ↓ typed API contract
Go deterministic core
   ↓ explicit AI boundary
Python / LLM service
```

## Repository Invariants

- `apps/web` talks only to `services/api`, never to `services/ai` or the database.
- `services/ai` never writes to the database and never authorizes anything.
- `services/api` and `services/ai` do not import each other's code; they share only `contracts/`.
- Request/response types are generated from `contracts/`, never hand-written twice.
- Schema changes go only through `db/migrations/`.

If a change seems to require breaking one of these, stop and ask.

Each directory has its own `AGENTS.md` with the rules for that layer. Read the one for the layer you are editing, in addition to this file: `apps/web/AGENTS.md`, `services/api/AGENTS.md`, `services/ai/AGENTS.md`, `contracts/AGENTS.md`, `db/migrations/AGENTS.md`. Step-by-step workflows for common jobs (feature, bug fix, refactor, review, dependency upgrade, DB migration) are in `docs/agent-tasks/`. Read the matching one before starting.

Cross-cutting rules (security, testing, dependencies, observability) are in `docs/agent-rules/`. Read the ones relevant to the change.

Verification per layer:

- `apps/web`: `tsc --noEmit`, `eslint .`, `vitest run`
- `services/api`: `go vet ./...`, `go test ./...`
- `services/ai`: `ruff check .`, `pyright`, `pytest`
