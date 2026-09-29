## Testing

Test behavior, not implementation details.

### Coverage of cases

Tests cover, where relevant: normal behavior, boundary values, malformed external input, invalid schema, network failure, timeout, authorization failure, and expected retry behavior.

### Bug fixes

Write a regression test first and confirm it fails without the fix.

### Rules

- Tests are deterministic: no real network, no wall-clock sleeps, no shared mutable state, no ordering dependence. Inject clocks and randomness.
- Do not weaken, skip, or delete a failing test to make a change pass. If a test is wrong, say so and fix it deliberately.
- Do not assert on incidental output (log text, internal call counts) unless that is the behavior.
- Prefer real implementations over mocks for code you own; fake only at external boundaries (network, LLM, clock).
- Property-based tests for parsers, serializers, and invariants where cheap.
- Keep test names as sentences describing behavior.

### Running

Run the smallest relevant test set while iterating. Run the full relevant suite before declaring done, and report the actual result.
