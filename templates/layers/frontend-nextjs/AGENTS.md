## Frontend: Next.js

Next.js is used here only because SSR / SEO / RSC is required. Every Next feature you use adds state space; use the minimum.

### Boundaries to keep explicit

- Every component is server or client on purpose. Add `"use client"` only where interactivity requires it, as low in the tree as possible.
- Data fetching happens in server components or route handlers through the repository API client, never ad hoc in client components.
- Do not import server-only modules (DB, secrets) into client components. Mark such modules with `server-only`.
- Server actions: only for mutations that have an equivalent typed contract; validate input with Zod, authorize inside the action.
- Caching: never rely on default caching behavior. Set `cache` / `revalidate` explicitly on each fetch and document why.
- Rendering mode (static, dynamic, ISR) is chosen per route and stated in a comment at the top of the route file.
- Middleware only for cross-cutting concerns (auth redirect, locale). No business logic.
- Avoid edge runtime unless required; note the reason.

### Fixed choices

Same as the React + Vite module: TanStack Query for client-side server state, React Hook Form + Zod for forms, repository HTTP client, repository design system.

### Verification

```
tsc --noEmit && eslint . && vitest run && next build
```
