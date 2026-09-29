# Prior Art

Public `AGENTS.md` files and harnesses worth studying, then the research on them. Files were read directly (2026-09-29, default branch), not taken from summaries; star counts are from the same day. Papers were checked by title and abstract only unless noted.

## Examples

Ratings are about what each file teaches us, not about the project. **Strong**: copy patterns from it. **Partial**: one or two ideas worth taking. **Weak**: included to show a pattern or a limit. Line counts and quoted rules were checked against the files.

| Repo | Stars | Lines | Rating | Take this | Leave this |
| --- | --- | --- | --- | --- | --- |
| [StarRocks/starrocks](https://github.com/StarRocks/starrocks/blob/main/AGENTS.md) | 12k | 87 | Strong | Opens with a numbered Read Order (handbook, nearest nested guide, domain handbook per area), then a repo map, quick commands and invariants an agent cannot guess: protobuf/thrift fields stay optional/repeated, never `required`, ordinals never reused; `gensrc/` is not hand-edited; config or metric changes update both `docs/en/` and `docs/zh/`. | Nothing notable. |
| [openkruise/agents](https://github.com/openkruise/agents/blob/master/AGENTS.md) | 295 | 135 | Strong | Clearest layering: each layer says what it owns and must not contain, with a direction (`API -> Manager -> Infra`) and a rule that the controller's dependency closure excludes the manager packages. Says existing cross-layer imports are "legacy debt, not architectural precedent", and gates a risky call (`APIReader` `Get`) behind explicit user approval. | Long; assumes a large layered Go codebase. |
| [openmeterio/openmeter](https://github.com/openmeterio/openmeter/blob/main/AGENTS.md) | 2.3k | 142 | Strong on gotchas | Non-discoverable facts: Postgres tests silently skip unless `POSTGRES_HOST=127.0.0.1`; Kafka tests need `-tags=dynamic`; root `go test ./...` excludes the `e2e` module; the root module must never require `api/v3/client`. Warns not to assume root-started agents discover nested files, and has a "Maintaining agent guidance" section (merge, remove duplicates). | The section titled "Repository invariants" is only three bullets; much of the rest is Go and test style. |
| [astral-sh/uv](https://github.com/astral-sh/uv/blob/main/AGENTS.md) | 90k | 33 | Strong | Terse rules, each with a reason and pointing at the lint that backs it ("NEVER suppress the `dangerous-triggers` security lint"; "NEVER assume clippy warnings or test failures are pre-existing"). | A few bullets are style preferences. |
| [openai/codex](https://github.com/openai/codex/blob/main/AGENTS.md) | 127k | 320 | Strong | Non-inferable invariants ("No history rewrite" for model-visible context), rules tied to checks (`argument-comment-lint`, CI lockfile drift), a module-size budget. | Rust-only; code-review rules are mixed into a coding file. Its `docs/agents_md.md` is a 3-line link, not an example. |
| [grafana/grafana](https://github.com/grafana/grafana/blob/main/AGENTS.md) | 77k | 172 | Strong | A "Human Review Gates" section ("Open a PR" is intent, not permission to push); directory-scoped nested files; `CLAUDE.md` contains only `@AGENTS.md` for one source of truth. | Commands partly duplicate the Makefile. |
| [vercel/ai](https://github.com/vercel/ai/blob/main/AGENTS.md) | 27k | 320 | Strong on enforcement | A `PostToolUse` hook on `Write\|Edit` runs `pnpm fix`, so formatting is enforced by the harness; an ADR gate (stop and ask if work contradicts an accepted ADR). | Some tables restate README content. |
| [facebook/react](https://github.com/facebook/react/blob/main/CLAUDE.md) | 250k | 13 | Strong harness, thin file | Almost no prose; the harness does the work. A `SessionStart` hook injects instructions except under `compiler/`; permissions allow `yarn test/lint/flow` and deny other package managers. | "Current Active Work" will go stale. |
| [github/spec-kit](https://github.com/github/spec-kit/blob/main/AGENTS.md) | 139k | 58 | Strong on routing | A pointer table ("Before adding CLI commands, read `design/cli.md`"); separate disclosure for agent-authored commits and PRs. | Only as good as the design docs it points to (not audited). |
| [vercel/next.js](https://github.com/vercel/next.js/blob/canary/AGENTS.md) | 143k | 527 | Strong layering, too long | States a policy: skills hold what is too detailed for `AGENTS.md`, one-line guardrails stay in `AGENTS.md`; operational lore ("TS2307 errors in a fresh worktree are artifacts, do not fix them"). | 527 lines; some monorepo-tree content `ls` would show. |
| [TanStack/query](https://github.com/TanStack/query/blob/main/AGENTS.md) | 50k | 10 | Strong, with a caveat | Read and follow `CONTRIBUTING.md`, one topic per change, understand generated code, run required checks, follow the PR template. Not repeating yourself, taken to the limit. | Works only because `CONTRIBUTING.md` is thorough. |
| [cloudflare/agents](https://github.com/cloudflare/agents/blob/main/AGENTS.md) | 5.7k | 196 | Partial | A table of five nested `AGENTS.md` files and their scopes; exact commands; a Boundaries section split into Always / Ask first / Never; some rules name their enforcer ("Oxlint will reject it"). | Not a short map (196 lines); "Learned" sections accumulate. |
| [livekit/agents](https://github.com/livekit/agents/blob/main/AGENTS.md) | 14k | 134 | Partial | Version changes only in release PRs; default to a patch bump; minor or major needs explicit human confirmation. | Env vars, style and commands mostly restate the Makefile and config. |
| [oracle/agent-spec](https://github.com/oracle/agent-spec/blob/main/AGENTS.md) | 430 | 70 | Partial | Nested files take precedence; routes Python SDK, evaluation and TypeScript SDK to their own files; a security section that names trust-boundary surfaces and points to a doc. | Working Rules and Handoff are generic advice. |
| [jetyu/Snaptium](https://github.com/jetyu/Snaptium/blob/main/AGENTS.md) | 63 | 103 | Partial | Renderer to Preload/Bridge to Main, no Node APIs in the renderer, IPC channels centralized and validated at the boundary, and a hard rule not to invent file types or layers. | Generic behavior maxims; a long skill catalogue. |
| [langchain-ai/langchain](https://github.com/langchain-ai/langchain/blob/master/AGENTS.md) | 147k | 390 | Partial | "Preserve function signatures; warn on changes"; "do not cite line numbers, they go stale". | Long, repeats release process, carries a vendor block that is noise. |
| [microsoft/vscode](https://github.com/microsoft/vscode/blob/main/AGENTS.md) | 193k | 5 | Weak alone | The pointer pattern at its extreme: defers to `.github/copilot-instructions.md`. | Nothing to learn beyond the pattern. |

Beyond repos: [Anthropic, Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) (a JSON feature list with a `passes` flag, a progress file, `init.sh`, "unacceptable to remove or edit tests") and [HumanLayer, Writing a good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md) (claims frontier models follow roughly 150 to 200 instructions consistently, so budget them; opinionated, not benchmarked). Not assessed: OpenAI's "Harness engineering" post (403), OpenSpec (its root `AGENTS.md` came back empty), and the curated collections (awesome-cursorrules, awesome-claude-code).

## How Codex finds files

Per the official [AGENTS.md guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md): Codex starts at the project root and walks down to the working directory, checking `AGENTS.override.md`, then `AGENTS.md`, in each directory; it concatenates files root-first, so closer files override earlier guidance; and it stops adding files once the combined size reaches `project_doc_max_bytes` (32 KiB by default). Other agents may discover files differently.

## Research

| Paper | Finding | Implication |
| --- | --- | --- |
| [Evaluating AGENTS.md](https://arxiv.org/abs/2602.11988) | Context files did not generally improve success and raised cost, for human-written and generated files alike (from a search summary) | Prove value with tasks; keep files minimal |
| [Impact on efficiency](https://arxiv.org/abs/2601.20404) | Median runtime down 28.6%, output tokens down 16.6%, comparable completion (from a search summary) | The benefit may be cost, not correctness |
| [Agent READMEs](https://arxiv.org/abs/2511.12884) | 2,303 files: testing in 75.9%, architecture 68.1%, security 14.8%, performance 14.5%; files grow like config code | Real files skimp on constraints; give security its own enforced section |
| [Claude Code manifests](https://arxiv.org/abs/2509.14744) | 253 files: shallow structure, mostly commands, implementation notes, architecture | Descriptive only |
| [Cursor Rules](https://arxiv.org/abs/2512.18925) | 401 repos: five content categories (conventions, guidelines, project info, LLM directives, examples) | A grounded taxonomy for modules. The "28.7% duplicate lines" figure is unverified |
| [Cursorrules at scale](https://arxiv.org/abs/2608.10622) | 12,110 files, mostly small single-maintainer projects; security rare | Confirms the gap |
| [Harness Engineering](https://arxiv.org/abs/2602.14690) | 2,853 repos: context files dominate, `AGENTS.md` is the interoperable standard, skills and subagents are rare; no performance measured | Use `AGENTS.md` as the portable base |
| [Stop comparing agents without disclosing the harness](https://arxiv.org/abs/2605.23950) | Position paper: harness can matter more than the model (specific numbers unverified) | Evaluate an instruction file inside a fixed harness |
| [Coding Agents Have Converged](https://arxiv.org/abs/2609.17394) | Top SWE-bench entries statistically indistinguishable; scaffold choice varies results by up to 29.8 points | Use paired tests; small gaps are noise |
| [SWE-agent](https://arxiv.org/abs/2405.15793), [Agentless](https://arxiv.org/abs/2407.01489) | Tool interface and simple structured workflows drive results | Give exact runnable commands and enforce rules with tools, not prose |

No controlled study found in this survey shows that `AGENTS.md` improves task success beyond the first two rows. Also seen, lower relevance: [Terminal-Bench](https://arxiv.org/abs/2601.11868), [Codified Context](https://arxiv.org/abs/2602.20478) (single-author case study), [OpenHands](https://arxiv.org/abs/2407.16741).

## Lessons, and where they landed here

| Lesson | Evidence | Where it landed |
| --- | --- | --- |
| Invariants an agent cannot infer beat style rules | StarRocks, OpenMeter, Codex | `stacks/fullstack-ts-go-py/architecture.md`; `docs/authoring-guide.md` |
| Layers: owns, may call, must not contain, plus a dependency direction | OpenKruise | Go API, React and Python AI layer modules |
| Human gates for irreversible or risky actions | LiveKit, OpenKruise, Cloudflare, Grafana, vercel/ai (ADR) | "Boundaries" in `templates/base`; `permissions.ask` in `enforcement/claude-code/settings.json` |
| Do not invent a new layer or file type | Snaptium | "Do Not Invent Structure" in `templates/base` |
| Enforce mechanically with hooks, lints, permissions, not prose | vercel/ai, React, uv, Codex; HumanLayer | `enforcement/claude-code/` (hooks and permissions), `enforcement/` (linters) |
| One source of truth across tools: `CLAUDE.md` is just `@AGENTS.md` | Grafana | `stacks/shared/claude-import.md`, emitted by every stack |
| Skills hold detail; `AGENTS.md` holds one-line guardrails | Next.js | "What goes where" table in `docs/composition.md` |
| Always / Ask first / Never; existing violations are debt, not precedent | Cloudflare, OpenKruise | "Boundaries" in `templates/base` |
| Root must list nested files, do not rely on discovery | OpenMeter, Cloudflare, StarRocks | `docs/composition.md`; fullstack `architecture.md` |
| Point to existing docs instead of repeating | TanStack, spec-kit, vscode | Routing text in single-service stacks |
| Delete what the repo already says; avoid stale sections | LiveKit, React (counter-examples) | `docs/authoring-guide.md` |

## Caution

These are examples, not evidence that their files work. The research above finds no controlled result showing that context files raise task success, and one study finds extra cost. That is why this project tests its output against tasks rather than trusting the prose. Most of the large files here (300 to 500 lines) are also longer than the instruction budgets discussed in the research suggest.
