## Task: Implement a Feature

1. **Restate** the requirement in one or two sentences, including what is out of scope. Ask if it is ambiguous.
2. **Locate the owner.** Find the layer and existing abstraction that owns this behavior. Extend it rather than creating a parallel one.
3. **Types first.** Define input/output types and, for API changes, update `contracts/` before implementation.
4. **Test first or alongside.** Write tests for the normal path and the failure paths (invalid input, boundary values, errors).
5. **Implement the smallest change** that satisfies the tests. No opportunistic refactors.
6. **Verify.** Run the full relevant checks for every layer touched.
7. **Report.** Summarize what changed, what was verified, and anything you could not verify or deliberately left out.

Stop and ask before: adding a dependency, changing a public contract in a breaking way, changing a database schema, or touching code outside the feature's layer.
