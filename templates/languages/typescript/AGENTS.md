## TypeScript

All TypeScript compiles under `strict` (plus `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`).

### Forbidden

- `any`, unless a third-party library makes it unavoidable. Contain it at the boundary and convert to a typed value immediately.
- `as` casts to silence errors. Narrow with a type guard or a Zod parse instead.
- `@ts-ignore`. Use `@ts-expect-error` with a reason, and only when unavoidable.
- Non-null assertions (`!`) on values that can legitimately be absent.
- `enum`. Use string-literal unions or `as const` objects.

### Preferred

- `unknown` followed by explicit validation for anything external.
- Discriminated unions with exhaustive `switch` (end with a `never` check).
- `readonly` and immutable data by default.
- Explicit return types on exported functions.
- Zod schemas as the source of runtime types: `type T = z.infer<typeof T>`.

### Errors

- Return typed results (`{ ok: true, value } | { ok: false, error }`) for expected failures; throw only for programmer errors.
- Never catch and ignore. Never `catch (e)` without narrowing `e` from `unknown`.

### Verification

```
tsc --noEmit
eslint .
vitest run
```
