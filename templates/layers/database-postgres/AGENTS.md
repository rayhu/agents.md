## Database: PostgreSQL

### Schema changes

- Only through explicit, versioned migrations in `db/migrations/`. Never edit an applied migration; add a new one.
- Application startup never mutates the production schema.
- Every migration is reviewed for: locking behavior on large tables, backfill strategy, and rollback or forward-fix plan.
- Prefer expand/contract for breaking changes: add new, dual-write or backfill, switch reads, then remove old in a later migration.

### Modeling

- Enforce invariants in the database: `NOT NULL`, `CHECK`, `UNIQUE`, foreign keys. Do not rely on application code alone.
- Use `timestamptz`, never `timestamp` without time zone.
- Use closed sets via enum types or lookup tables plus constraints.
- Primary keys are explicit. Name constraints and indexes explicitly.
- Add an index with a stated query it serves.

### Queries

- Statically checked SQL (`sqlc`) only. No string-concatenated SQL. Parameters only via placeholders.
- No `SELECT *` in application queries.
- Multi-statement business operations run in an explicit transaction.

### Verification

- Migrations apply cleanly to an empty database and to a copy of the current schema.
- `sqlc generate` produces no diff.
