# Grok Review Adapter

1. Use Grok Build's `spawn_subagent` tool with one distinct child per selected
   lens.
2. Give every child the immutable bundle, one lens reference, read-only scope,
   and the exact reviewer output schema.
3. Launch the selected lens children in successive parallel windows of at most
   the bound the controller resolved, when supported.
4. Drain each window before opening the next, and drain the union of all windows
   before consolidation; preserve each lens result verbatim.
5. Prefer `capability_mode: read-only` (or an explore-equivalent agent type) so
   reviewers cannot edit files. Inherit the session model when per-child model
   controls are unused and report that limitation.
   The packaged `reviewer` agent pins only this controller; the lens children
   it dispatches are not packaged agents and stay on the session model, so
   this limitation still applies to them.
6. Degrade to isolated sequential lens execution with
   `degradation: sequential_no_parallel_support` when concurrency is unavailable.
7. Retry one failed lens once after adding only the missing bundle context.

The controller performs no lens analysis and reviewers execute no shared
build/test targets. A separate narrow child adjudicates only submitted conflicts.
