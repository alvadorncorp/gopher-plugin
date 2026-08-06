# Claude Review Adapter

1. Use Claude Code's native subagent/task capability with one distinct task per lens.
2. Give every task the immutable bundle, one lens reference, read-only scope,
   and the exact reviewer output schema.
3. Launch the selected lens tasks in successive parallel windows of at most the
   bound the controller resolved, when supported.
4. Drain each window before opening the next, and drain the union of all windows
   before consolidation; preserve each lens result verbatim.
5. Inherit the session model when per-task model controls are unavailable and
   report the limitation.
   The packaged `reviewer` agent pins only this controller; the lens tasks
   it dispatches are not packaged agents and stay on the session model, so
   this limitation still applies to them.
6. Degrade to isolated sequential lens execution with
   `degradation: sequential_no_parallel_support` when concurrency is unavailable.
7. Retry one failed lens once after adding only the missing bundle context.

The controller performs no lens analysis and reviewers execute no shared
build/test targets. A separate narrow task adjudicates only submitted conflicts.
