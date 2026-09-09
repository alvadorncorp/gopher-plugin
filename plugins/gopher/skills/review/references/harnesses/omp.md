# Omp Review Adapter

1. Use omp's `task` tool with one item per selected lens in a single `tasks[]`
   batch, each item dispatched on the bundled read-only `scout` agent.
2. Give every child the immutable bundle, one lens reference, read-only scope,
   and the exact reviewer output schema. Resolve every reference through the
   skill directory the host injected, never through `skill://<name>`, because
   omp resolves a skill by its bare name and another installed plugin can own
   that name.
3. Dispatch the selected lens items together in successive parallel windows of
   at most the bound the controller resolved; omp queues anything past its own
   concurrent-subagent ceiling.
4. Results auto-deliver when a child yields; poll nothing. Drain each window
   before opening the next, and drain the union of all windows before
   consolidation; preserve each lens result verbatim.
5. `gopher-reviewer` is this controller. It is not a lens agent. Lens children
   are `scout`. Every child inherits the session model. A task item carries a
   coarse effort hint only when the host enables `task.enableEffort`, and it
   carries no model selector at all, so report an inherited-model limitation for
   any declared model or effort policy.
6. Degrade to isolated sequential lens execution with
   `degradation: sequential_no_parallel_support` when `task` is unavailable or
   the session spawn policy denies the fan-out. That degradation does not
   substitute a generic `task` child or omp's bundled `reviewer` for a missing
   Gopher role.
7. Retry one failed lens once after adding only the missing bundle context.

The controller performs no lens analysis and reviewers execute no shared
build/test targets. A separate narrow `scout` task adjudicates only submitted
conflicts.

Before dispatching a native Gopher role, confirm that name is present in the
`task` catalog and is not disabled. If it is missing or disabled, stop that
handoff, name the cause, and point at the directed omp install configuration:
`extensions` must include the Gopher `omp` root and `skills.customDirectories`
must include the Gopher `skills` tree. Do not substitute `task` or the bundled
`reviewer`. If the autoloaded `review` skill is unavailable, stop with an
installation block rather than inventing the workflow.
