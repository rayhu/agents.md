## Dependencies

Before adding a dependency:

1. Check whether the standard library solves it.
2. Check whether an existing repository dependency solves it.
3. Prefer mature packages with narrow scope.
4. Avoid packages that duplicate existing infrastructure.

Do not add a dependency to save a few lines of straightforward code.

Do add a mature dependency when it replaces subtle protocol or standards logic: HTTP behavior, date/time and timezones, cryptography, parsers, schema validation, retry policies. Do not reimplement standards.

### Use the popular library; do not hand-roll it

When a well-known, widely used package already solves the problem, adding it is the correct default, not a cost to avoid. Hand-written regular expressions and ad hoc parsing are the most common way agents reinvent these badly.

Do not write your own regex, string splitting, or manual type checks to do any of the following. Use the established library:

| Task | Use (examples) | Not |
| --- | --- | --- |
| Validate or parse structured data | Zod (TS), Pydantic (Python), typed structs + validator (Go) | regex or `if` chains over raw JSON / dicts |
| Validate emails, URLs, UUIDs, IPs | the schema library's built-in validators, `net/url`, `net/mail`, `netip` | hand-written patterns |
| Parse JSON, YAML, TOML, CSV, HTML, Markdown | the standard or mature parser | regex or `split` |
| Parse or format dates, times, durations, timezones | `Temporal`/`date-fns`/`luxon`, `zoneinfo`, `time` | string slicing, manual offset math |
| Parse CLI args, env vars, config | `commander`/`zod`, `pydantic-settings`, `flag`/`envconfig` | manual `os.Getenv` parsing scattered around |
| URLs and query strings | `URL` / `URLSearchParams`, `urllib.parse`, `net/url` | string concatenation |
| Semver, MIME types, cron expressions, locale/number/currency formatting | the dedicated library | regex |
| Retries, backoff, rate limiting | a mature retry/limiter library | hand-written loops with `sleep` |

Regular expressions are acceptable for genuinely simple, local text matching (e.g. a log line filter or a one-off identifier pattern in a test) where no library models the format. If you find yourself writing a regex longer than a line, or one that tries to validate a standard format, stop and look for the library.

Introduce the dependency in the same change that needs it, follow the requirements below, and do not treat "it adds a package" as a reason to write fragile code instead.

### Requirements for a new dependency

- State in the PR description why it is needed and what alternatives were considered.
- Pin via the lockfile; commit the lockfile change.
- Check license, maintenance activity, and transitive dependency count.
- Never add a package based on a name you have not verified exists on the registry.

### Forbidden

- Vendoring or copy-pasting library code to avoid adding a dependency.
- Adding a second library for a concern that already has a fixed choice in this repo.
- Adding a dependency and changing unrelated code in the same change.
