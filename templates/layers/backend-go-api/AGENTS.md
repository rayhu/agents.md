## Backend: Go API

The Go service is the deterministic core: business rules, authorization, persistence, orchestration. It calls the AI service through an explicit typed boundary; it does not embed LLM logic.

### Fixed choices

- HTTP: `net/http` (with the router already in `go.mod`).
- Database: PostgreSQL via `pgx`; queries via `sqlc`. No ORM.
- Contract: handlers implement the OpenAPI spec in `contracts/`; use generated server/types.
- Logging: `log/slog`, structured, with request IDs.
- Config: read env vars once at startup into a validated struct; fail fast if invalid.

### Structure

```
cmd/<service>/main.go     # wiring only
internal/<domain>/        # business logic, no HTTP types
internal/http/            # handlers, request/response mapping
internal/db/              # sqlc generated + thin store wrappers
```

| Layer | Owns | May call | Must not contain |
| --- | --- | --- | --- |
| `internal/http` | routing, request/response models, protocol validation, authentication, error-to-status mapping | `internal/<domain>` | business rules, SQL |
| `internal/<domain>` | business rules, authorization, orchestration | `internal/db`, outbound clients | `net/http` types, status codes |
| `internal/db` | generated queries, transactions | database | business decisions |

Do not push HTTP semantics into domain code, or business rules into handlers. Dependencies point inward only: `http → domain → db`.

### Rules

- Validate every request body, query, and path parameter before use.
- Authorization is checked in domain code, never trusted from the client.
- Map domain errors to HTTP status in one place.
- Timeouts on every server and every outbound client. No default `http.Client`.
- Migrations are the only way schema changes; the service never mutates schema on startup.

### Verification

```
go vet ./... && golangci-lint run && go test ./... -race
sqlc generate && git diff --exit-code   # generated code is committed and current
```
