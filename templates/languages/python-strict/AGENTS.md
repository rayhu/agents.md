## Strict Python

Python in this repository is **Strict Python**, not ordinary Python.

Required tooling: `uv`, `ruff`, `pyright --strict` (or `mypy --strict`), `pytest`.

### Typing

- Every public function has complete type annotations, including the return type.
- No untyped `def run(data): ...`. Write `def run(request: AgentRequest) -> AgentResponse: ...`.

### Forbidden (outside a documented integration boundary)

- `Any` and `dict[str, Any]`
- untyped decorators
- monkey patching and runtime attribute injection
- wildcard imports
- mutable default arguments
- bare `except:` and `except Exception: pass`
- `# type: ignore` without an error code and a reason

If an external library forces one of these, isolate it in a single adapter module and convert to typed values immediately.

### Data structures

- Pydantic models for external data (requests, responses, config, LLM output).
- `dataclass(frozen=True, slots=True)` for internal structured data.
- `Enum` / `Literal` for closed sets.
- Do not pass arbitrary dicts between layers when the structure is known.

### Time

- Use timezone-aware `datetime` only. Never use naive datetimes.
- Use IANA identifiers (`America/Los_Angeles`) via `zoneinfo`. Never hand-compute DST or represent civil time as a fixed UTC offset.

### HTTP

- Use the repository HTTP abstraction (HTTPX). Do not parse raw status lines.
- Do not hard-code `200` as "success" unless exactly 200 is part of the protocol. Distinguish informational, success, redirect, client error, server error, and transport failure.
- Retries are explicit and bounded. Never blindly retry every failure.

### Verification

```
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run pytest
```
