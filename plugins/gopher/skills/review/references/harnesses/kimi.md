# Kimi Review Adapter

1. Use Kimi Code's `Agent` subagent tool with one distinct child per selected
   lens (`subagent_type: explore` for read-only dispatch).
2. Give every child the immutable bundle, one lens reference, read-only scope,
   and the exact reviewer output schema.
3. Launch the selected lens children in successive parallel windows of at most
   the bound item 5 of the fallback below resolves; use `AgentSwarm` when the
   lens children share one prompt template.
4. Drain each window before opening the next, and drain the union of all windows
   before consolidation; preserve each lens result verbatim.
5. Inherit the session model when per-child model controls are unused and report
   that limitation.
6. Degrade to isolated sequential lens execution with
   `degradation: sequential_no_parallel_support` when concurrency is unavailable.
7. Retry one failed lens once after adding only the missing bundle context.

The controller performs no lens analysis and reviewers execute no shared
build/test targets. A separate narrow child adjudicates only submitted conflicts.

## Packaged agent fallback

Kimi Code loads plugin skills and discards packaged plugin agents, so the
`reviewer` role that Claude Code, Grok Build, and Codex load with a fixed binding
does not exist in this harness. Reproduce its envelope inline in every dispatch
above rather than assuming it:

1. State in each child's prompt that it is read-only: it observes, it makes no
   edit of any kind, it never redirects output into the working tree, and it never
   uses an in-place editor.
2. State that the child runs no shared build or test target; it receives the
   controller's verification results inside the bundle.
3. State the exact reviewer output schema in the child's prompt, because no
   packaged agent definition supplies it here.
4. Keep the controller itself read-only for the whole run.
5. Read the `[agents]` table of `.gopher-plugin.toml` in the controller. Bound the
   parallel window by `agents.reviewer_max_parallel`, stop the run when
   `agents.enabled` is `false` or when `agents.policy_divergence` is `block` and a
   divergence exists, and report `policy_status` with the same five values the
   packaged agents report: `NOT_CONFIGURED`, `ALIGNED`, `DIVERGED`, `UNVERIFIABLE`,
   or `BLOCKED_BY_POLICY`.
6. Report `policy_status: UNVERIFIABLE` for any declared model or effort, because
   this harness binds neither per child. A window narrowed by
   `agents.reviewer_max_parallel` is `parallel_window: bounded-by-policy`, never
   `degradation: sequential_no_parallel_support`.

The declared policy may narrow this run and it can never widen it.
