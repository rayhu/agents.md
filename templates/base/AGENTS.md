## Purpose

This repository is designed for AI-assisted development. The goal is not maximum flexibility. It is to keep the valid implementation space narrow, explicit, typed, deterministic, and mechanically verifiable.

Prefer boring, explicit code over clever abstractions. If two implementations are equally correct, choose the one with:

1. fewer concepts,
2. fewer dependencies,
3. stronger static guarantees,
4. fewer implicit behaviors,
5. easier automated verification.

## Deterministic First

Use normal code for anything that can be expressed deterministically. Do not use an LLM for arithmetic, date calculations, schema transformation, deterministic classification, database filtering, authorization, or business rules that can be written explicitly.

## Validate Every External Boundary

Never trust unvalidated external data. Boundaries include HTTP requests and responses, environment variables, files, user input, third-party APIs, message queues, database data crossing service boundaries, and LLM output.

Do not propagate raw dictionaries or untyped JSON into application logic. Parse into a typed representation at the boundary.

## One Source of Truth

Do not define the same contract, constant, or rule in two places. Generate or derive instead of copying.

## No Speculative Abstraction

Do not create an abstraction because it might be useful later. Do not introduce generic repository layers, service frameworks, plugin systems, event buses, factories, DI frameworks, or custom DSLs unless the current task demonstrably requires them. Three explicit implementations beat one premature abstraction.

## Fail Loudly

- Fail when an invariant is violated.
- Do not substitute placeholder values.
- Do not turn programming errors into valid-looking results.
- Fallback behavior must be intentional and documented.

## Scope Discipline

- Keep diffs small.
- Do not combine refactoring with a feature or bug fix.
- Do not rename or reorganize unrelated files.
- Preserve existing behavior unless changing it is the task.

## Do Not Invent Structure

Use the naming, layering, and patterns the repository already has. Do not create a new architectural layer, directory convention, or cross-cutting mechanism. If the existing structure cannot express the change, stop and ask.

## Boundaries

**Always:**

- read the code you are changing and its tests first,
- say what you could not verify.

**Ask first:**

- adding a dependency, or upgrading one across a major version,
- changing a public contract or a database schema,
- changing CI, permissions, or security configuration,
- anything that contradicts an existing design decision or ADR.

**Never** without explicit instruction in the current task:

- bump a package or release version,
- publish, deploy, or tag a release,
- run migrations against a shared or production database,
- delete data, force-push, or rewrite history,
- push or open a PR because a task mentioned it; the mention is intent, not permission.

Existing violations of these rules are debt, not precedent. Do not copy them or widen them; if a task requires it, propose a fix first.

## Comments

Explain why a constraint exists, why an unusual implementation is needed, or why a tempting alternative is unsafe. Do not comment obvious syntax.

## Before Writing Code

Determine first:

1. which layer owns the behavior,
2. the input and output types,
3. the invariants that must hold,
4. which external boundaries need validation,
5. which existing abstraction already owns this responsibility.

Do not start implementing until these are clear. If the task is ambiguous, ask rather than guess.

## Definition of Done

A task is complete only when the relevant machine checks pass, not when the code looks right. Run the smallest relevant checks while iterating and the full relevant suite before finishing. Report any check you could not run.

If a machine-checkable rule can replace a prose convention, prefer the machine-checkable rule.
