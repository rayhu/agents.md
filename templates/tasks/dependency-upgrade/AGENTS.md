## Task: Upgrade Dependencies

1. **One dependency (or one tightly coupled group) per change.** No feature work mixed in.
2. **Read the changelog** for every version crossed. List breaking changes and deprecations that touch this repo.
3. **Upgrade, then let the tools speak:** compiler, type checker, linter, and the full test suite. Fix what they report.
4. **Fix root causes** of new errors. Do not add `any`, `# type: ignore`, or lint suppressions to get green.
5. **Do not edit lockfiles by hand.** Regenerate with the package manager and commit the result.
6. **Check transitive changes:** review the lockfile diff for surprising additions or removals.
7. **Report** the version range, breaking changes handled, and anything not verifiable locally (e.g. runtime behavior in production).

Stop and ask if an upgrade requires a major rewrite, a new peer dependency, or dropping support for a runtime version.
