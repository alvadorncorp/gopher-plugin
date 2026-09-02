# Omp Review Adapter

1. Use omp's `task` tool with one item per selected lens in a single `tasks[]`
   batch, each item dispatched on the bundled read-only `scout` agent.
2. Give every child the immutable bundle, one lens reference, read-only scope,
   and the exact reviewer output schema. Resolve every reference through the
   skill directory the host injected, never through `skill://<name>`, because
   omp resolves a skill by its bare name and another installed plugin can own
   that name.
3. Dispatch the selected lens items together in successive parallel windows of
   at most the bound item 5 of the fallback below resolves; omp queues anything
   past its own concurrent-subagent ceiling.
4. Results auto-deliver when a child yields; poll nothing. Drain each window
   before opening the next, and drain the union of all windows before
   consolidation; preserve each lens result verbatim.
5. Every child inherits the session model. A task item carries a coarse effort
   hint only when the host enables `task.enableEffort`, and it carries no model
   selector at all, so report an inherited-model limitation for any declared
   model or effort policy.
6. Degrade to isolated sequential lens execution with
   `degradation: sequential_no_parallel_support` when `task` is unavailable or
   the session spawn policy denies the fan-out.

The controller performs no lens analysis and reviewers execute no shared
build/test targets. A separate narrow `scout` task adjudicates only submitted
conflicts.

## Packaged agent fallback

omp discovers the packaged markdown agents but binds no packaged agent model, effort, or tool restriction:
it ignores `disallowedTools`, `skills`, and `effort`, and it matches a `model`
value such as `opus` against no selector, so each role falls back to the session
model and the session's own tools. The `reviewer` role therefore arrives without
its read-only binding. Dispatch bundled read-only `scout` children instead and
reproduce the envelope inline in every dispatch above:

1. State in each child's prompt that it is read-only: it observes, it makes no
   edit of any kind, it never redirects output into the working tree, and it
   never uses an in-place editor.
2. State that the child runs no shared build or test target; it receives the
   controller's verification results inside the bundle.
3. State the exact reviewer output schema in the child's prompt, because no
   packaged agent definition supplies it here.
4. Keep the controller itself read-only for the whole run.
5. Read the `[agents]` table of `.gopher-plugin.toml` in the controller. Bound
   the parallel window by `agents.reviewer_max_parallel`, stop the run when
   `agents.enabled` is `false` or when `agents.policy_divergence` is `block` and
   a divergence exists, and report `policy_status` with the same five values the
   packaged agents report: `NOT_CONFIGURED`, `ALIGNED`, `DIVERGED`,
   `UNVERIFIABLE`, or `BLOCKED_BY_POLICY`.
6. Report `policy_status: UNVERIFIABLE` for any declared model or effort,
   because this harness binds neither per child. A window narrowed by
   `agents.reviewer_max_parallel` is `parallel_window: bounded-by-policy`, never
   `degradation: sequential_no_parallel_support`.

The declared policy may narrow this run and it can never widen it.
