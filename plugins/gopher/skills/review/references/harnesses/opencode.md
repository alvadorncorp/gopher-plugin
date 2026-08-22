# OpenCode Review Adapter

1. Use OpenCode's `task` tool with `subagent_type: explore`, one distinct task
   per selected lens.
2. Give every child the immutable bundle, one lens reference, read-only scope,
   and the exact reviewer output schema.
3. Dispatch the selected lens tasks together in successive parallel windows of
   at most the bound the controller resolved.
4. Drain each window before opening the next, and drain the union of all windows
   before consolidation; preserve each lens result verbatim.
5. The `gopher-reviewer` primary agent binds this controller to `edit: deny`.
   Each `explore` child is read-only. Both inherit the session model and variant,
   so report an inherited-model limitation for declared model or effort policy.
6. Degrade to isolated sequential lens execution with
   `degradation: sequential_no_parallel_support` when task concurrency is
   unavailable.
7. Retry one failed lens once after adding only the missing bundle context.

The controller performs no lens analysis and reviewers execute no shared
build/test targets. A separate narrow `explore` task adjudicates only submitted
conflicts.
