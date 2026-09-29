## API Contracts

`contracts/` is the source of truth for every cross-service interface. OpenAPI (HTTP) and JSON Schema (shared payloads) live here.

### Rules

- Change the contract first, then regenerate code, then implement. Never hand-edit generated files.
- Do not define the same request or response shape independently in two services.
- Schemas are closed: `additionalProperties: false`, explicit `required`, explicit enums for closed sets, bounded strings and arrays (`maxLength`, `maxItems`).
- Errors have a documented, typed shape shared by all endpoints.
- Breaking changes (removing a field, tightening a type, changing meaning) need a new version or an expand/contract rollout. Additive changes are preferred.
- Every endpoint documents auth requirements and all non-2xx responses.

### Generation

TypeScript types and Zod schemas, Go server/types, and Pydantic models are generated from these files. The generation command is in the repository `Makefile`; run it after any contract change and commit the output.

### Verification

```
# lint the spec (e.g. spectral / redocly), regenerate, and require a clean tree
git diff --exit-code
```
