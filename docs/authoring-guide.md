# Authoring Guide

## A module is a narrow spec

One module, one topic. Roughly 20 to 60 lines. If it needs more, split it.

Start with a level-2 heading (`## Name`). Modules are concatenated into larger files, so they must not carry a top-level title.

## Test each rule

For every line, ask:

| Question | If "no" |
| --- | --- |
| Could an agent act differently because of this line? | Delete it. "Write clean code" fails here. |
| Is it specific (a tool, library, pattern, command)? | Make it specific. |
| Can a tool check it? | Add the check to `enforcement/`, or note the command in a Verification section. |
| Is it true for every file the module is placed with? | Move it to a narrower module. |

## Size and placement

- The root `AGENTS.md` is a map: architecture, repository invariants, universal rules, and pointers. In a monorepo aim for about 100 lines; warns above 200 for any output.
- Every token should change agent behavior. Delete what a linter already enforces and what `CONTRIBUTING.md` already says; point to it instead.
- Push detail down (nested files) or aside (`docs/agent-rules/`, `docs/agent-tasks/`). The root says where to look.
- Do not copy a template wholesale. Inspect the repo, keep what applies, delete the rest.

## Layer and invariant patterns

Describe layers as: **owns / may call / must not contain**. Describe repository invariants as dependency directions and things that must never happen ("`apps/web` never talks to `services/ai`"). These define the legal space of code and are worth more than style rules.

## Prefer

- Closed lists of allowed and forbidden things over general advice.
- Stating the escape hatch: "unless X; contain it at the boundary".
- Fixed choices in a table, so the agent never picks between five state libraries.
- Verification as commands, so "done" is a fact rather than an opinion.
- The reason for a rule only when knowing it changes what an agent does at the edges.

## Avoid

- Generic virtues ("clean", "maintainable", "best practices").
- Duplicating a rule across modules. Put it in the most general module that applies and rely on composition.
- Long examples. One short snippet at most.
- Rules for tools the repo does not use.

## Checklist before adding a module

- [ ] One topic, under about 60 lines
- [ ] Starts with `## `
- [ ] Every rule is concrete and actionable
- [ ] Verification commands listed where applicable
- [ ] Referenced from at least one stack manifest
- [ ] `scripts/compose.sh` still runs for every stack
