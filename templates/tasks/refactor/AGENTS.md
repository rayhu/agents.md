## Task: Refactor

A refactor changes structure, not behavior.

1. **Confirm test coverage** of the behavior being preserved. If it is thin, add characterization tests first, in a separate commit.
2. **State the goal** concretely (e.g. "extract X so Y no longer imports Z"). Refactoring without a goal is churn.
3. **Small, mechanical steps.** Keep the tests green after each step.
4. **No behavior change,** no feature work, no dependency changes in the same change.
5. **No new abstractions** beyond what the stated goal needs. Removing duplication is not a reason by itself when the copies may diverge.
6. **Public contracts stay intact** unless the task says otherwise.
7. **Verify** with the full relevant checks and confirm the test diff is empty or purely additive.

If you discover a bug during a refactor, do not fix it inline. Report it and fix it separately.
