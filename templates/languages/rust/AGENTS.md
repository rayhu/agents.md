## Rust

The compiler is the primary reviewer. Treat every compiler and clippy diagnostic as a required fix, not noise.

### Errors

- Return `Result<T, E>`. No `unwrap()` / `expect()` in non-test code unless the invariant is proven and documented in a comment.
- Libraries define typed errors with `thiserror`; binaries may use `anyhow` at the top level only.
- Propagate with `?`; add context at layer boundaries.

### Types

- Model states with enums; make illegal states unrepresentable.
- Newtypes for IDs and units instead of bare `String` / `u64`.
- Exhaustive `match`. Avoid `_ =>` wildcards on enums you own.

### Unsafe and concurrency

- No `unsafe` without a `// SAFETY:` comment stating the invariant, and only when the task requires it.
- Do not fight the borrow checker with `clone()` or `Rc<RefCell<_>>` as a first resort; restructure ownership.
- Prefer channels or clearly owned state over shared `Mutex` sprawl.

### Dependencies

Keep the dependency tree small; check `cargo tree` before adding a crate.

### Verification

```
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
```
