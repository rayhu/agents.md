## Go

Go is the default language for deterministic backend logic. Prefer the standard library; keep the dependency count low.

### Errors

- Handle every error explicitly. Never discard with `_`.
- Do not log an error and continue as though the operation succeeded.
- Wrap with context: `fmt.Errorf("load user %s: %w", id, err)`. Preserve the cause so `errors.Is` / `errors.As` work.
- Do not convert unrelated errors into generic 500s early. Map errors to responses at the transport edge.
- Define sentinel or typed errors for conditions callers must distinguish.

### Context

Any HTTP, database, network, or long-running operation takes and propagates `context.Context` as the first parameter. Do not create `context.Background()` inside request-handling code unless ownership is explicitly transferred.

### Style

- No `panic` for expected failures.
- No `init()` side effects; wire dependencies explicitly in `main`.
- Accept interfaces, return structs; define interfaces at the consumer, and only when there are two implementations or a test seam.
- No global mutable state.
- Concurrency: every goroutine has an owner, a cancellation path, and a defined exit. Prefer `errgroup` over hand-rolled coordination.
- Use `log/slog` for structured logging.

### Verification

```
gofmt -l .        # must print nothing
go vet ./...
golangci-lint run
go test ./... -race
```
