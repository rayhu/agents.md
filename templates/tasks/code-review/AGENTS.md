## Task: Review Code

You are reviewing, not rewriting. Do not modify files unless asked.

### What to check, in priority order

1. **Correctness:** does it do what the task says, including edge cases and error paths?
2. **Boundaries:** is every external input validated? Is LLM output treated as untrusted?
3. **Errors:** any swallowed, unwrapped, or misclassified errors?
4. **Security:** injection, authz gaps, secrets, unsafe deserialization.
5. **Contracts:** does it change a public interface or schema without updating `contracts/`?
6. **Tests:** do they cover failure paths, and would they fail without the change?
7. **Scope:** unrelated changes, unnecessary dependencies, speculative abstraction.
8. **Architecture:** does the change respect layer boundaries?

### Output format

- Lead with a verdict: approve, approve with nits, or request changes.
- List findings most severe first. Each: file and line, the problem, a concrete failure scenario, and a suggested fix.
- Separate blocking issues from optional suggestions.
- Do not pad with praise or restate the diff. Do not report style issues a linter already enforces.
- If you could not verify something (did not run tests, lacked context), say so explicitly.
