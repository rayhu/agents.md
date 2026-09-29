## Task: Database Migration

1. **New migration file only.** Never modify an already-applied migration.
2. **State the plan** before writing: what changes, expected table sizes, lock behavior, and rollback or forward-fix.
3. **Make it safe for zero-downtime:** add nullable columns or defaults that do not rewrite the table; create indexes concurrently; use expand/contract for renames and type changes.
4. **Backfills** are batched, idempotent, and separate from the schema change when the table is large.
5. **Update the code layer:** SQL queries, `sqlc` generation, and contracts if the API shape changes. Commit regenerated output.
6. **Test:** apply to an empty database and to a snapshot of the current schema; run the affected test suite.
7. **Never** run migrations against a shared or production database yourself. Provide the command and let a human run it.

Destructive changes (drop table/column, data deletion) require explicit human confirmation and must land in a later release than the code that stops using them.
