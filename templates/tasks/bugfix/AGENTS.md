## Task: Fix a Bug

1. **Reproduce first.** Write a failing test that captures the bug. If you cannot reproduce it, say so; do not guess-fix.
2. **Find the root cause,** not the nearest symptom. State it in one sentence before changing code.
3. **Fix at the owning layer.** Do not patch over it in a caller.
4. **Minimal diff.** Change only what the fix requires. No drive-by cleanups.
5. **Confirm** the regression test fails without the fix and passes with it.
6. **Look for siblings.** Search for the same pattern elsewhere; report other instances instead of silently changing them.
7. **Run the full relevant checks.**

Do not: suppress the error, add a broad try/catch, add a retry to mask a race, or weaken an existing assertion to get green.
