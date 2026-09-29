## LLM and Agents

### LLM output is untrusted external input

Raw model output must never directly execute commands, update a database, authorize a user, move money, delete data, change permissions, or call privileged tools. It crosses a typed validation boundary first; deterministic code then decides.

```
deterministic code → typed request → LLM → schema validation → deterministic code
```

### Structured output

- Use structured output with a closed schema.
- Do not extract application state from free-form prose with regexes.
- On validation failure: bounded retry with the error fed back, then fail explicitly. Never silently accept partial output.

### Agent loops

Every agent has all of:

- a maximum step count,
- a timeout or token/cost budget,
- an explicit allowlist of tools,
- a defined output schema,
- an observable execution history (each step, tool call, and result recorded).

No unconstrained `while True` loops. Termination conditions are code, not a hope that the model stops.

### Tools

- Each tool has a typed input and output schema and the least privilege it needs.
- Side-effecting tools require an explicit approval or policy check outside the model.
- Tool arguments are validated before execution, as with any external input.

### Prompts

- Prompts live in versioned files, not inline strings scattered through code.
- Untrusted content (user text, web pages, documents) is delimited and treated as data, never as instructions.

### Testing

Test with fake models: valid output, malformed output, schema violations, refusals, timeouts, and tool errors.
