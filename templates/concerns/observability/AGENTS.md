## Observability

- Logs are structured (key/value or JSON), never string-concatenated prose.
- Every request carries a request/trace ID through logs, outbound calls, and error responses.
- Log at the point an error is handled, once. Do not log and rethrow the same error at every layer.
- Never log secrets, tokens, full request bodies, or personal data.
- Use levels consistently: `error` means someone should look; expected failures (validation, not-found) are not `error`.
- New external calls and background jobs emit duration and outcome metrics.
- Agent runs record each step, tool call, and result so a run can be replayed and audited.
