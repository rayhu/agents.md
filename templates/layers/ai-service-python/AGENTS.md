## AI Service: Python

This service holds LLM, embedding, and ML functionality. It exists because the Python ecosystem is irreplaceable here, not because Python is the default. Anything deterministic belongs in the Go core.

### Fixed choices

- API: FastAPI with Pydantic models for every request and response.
- Packaging and tooling: `uv`, `ruff`, `pyright --strict`, `pytest`.
- HTTP client: HTTPX through the repository abstraction.
- Settings: `pydantic-settings`, validated at startup.

### Boundary rules

- The service only exposes typed endpoints defined in `contracts/`. No `dict` in or out.
- Inputs are validated by Pydantic before any model call.
- Model output is validated against a closed schema before it is returned or used. See the LLM and agents module.
- The service holds no business authority: it does not authorize users, write to the primary database, or trigger side effects. It returns validated results; the Go core decides what to do with them.

### Ownership

| Layer | Owns | May call | Must not contain |
| --- | --- | --- | --- |
| `app/api` | routing, request/response models, error mapping | `app/agents` | model calls, prompt text |
| `app/agents` | prompts, tools, budgets, output schemas | `app/clients` | HTTP framework types |
| `app/clients` | LLM and third-party adapters | network | business decisions |

### Structure

```
services/ai/
  app/api/        # FastAPI routes, thin
  app/agents/     # agent definitions: tools, schema, budget
  app/models/     # Pydantic models
  app/clients/    # LLM and HTTP adapters (only place `Any` may appear)
  tests/
```

### Testing

LLM calls are behind an interface and faked in unit tests. Provide recorded or fixture-based tests for parsing and schema validation, including malformed model output.
