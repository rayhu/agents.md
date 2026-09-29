## Frontend: React + Vite SPA

This is a single-page app. Do not introduce SSR, server components, or a meta-framework. If SSR/SEO becomes a real requirement, that is an architecture decision for a human.

### Fixed choices (do not re-decide per task)

| Concern | Use | Do not introduce |
| --- | --- | --- |
| Server state | TanStack Query | SWR, Redux Toolkit Query, ad hoc `useEffect` fetching |
| Forms | React Hook Form + Zod | Formik, hand-rolled form state |
| Local UI state | `useState` / `useReducer` | MobX, Recoil, Jotai |
| Global client state | none by default; Zustand only with a demonstrated need | Redux, Context as a store |
| Routing | the router already in `package.json` | a second router |
| HTTP | the repository HTTP client | raw `fetch()` / `axios` in components |
| UI | the repository design system | new component libraries, one-off styled primitives |

### Layers

| Layer | Owns | May call | Must not contain |
| --- | --- | --- | --- |
| Components | rendering, interaction | hooks, design system | fetching, business rules |
| Hooks / query layer | server-state access, caching | the HTTP client | JSX |
| HTTP client | transport, auth, validation, errors | network | UI concerns |

Use the existing layering; do not add a new one.

### Components

- Components do presentation and interaction. Business rules do not belong in components.
- No hidden network access inside presentational components. Data comes through the query/API layer.
- Derive state instead of syncing it with `useEffect`. An effect is for synchronizing with the outside world, not for computing values.

### HTTP layer

The single client handles timeout, cancellation (`AbortSignal`), authentication, JSON decoding, schema validation, and structured errors. Use protocol semantics (e.g. `response.ok`, status classes), not magic status numbers.

API types come from `contracts/`; do not hand-write request or response types.

### Verification

```
tsc --noEmit && eslint . && vitest run
```
