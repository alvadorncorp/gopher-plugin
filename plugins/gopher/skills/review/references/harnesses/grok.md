# Grok Review Adapter

1. Use Grok Build's `spawn_subagent` tool with one distinct child per selected
   lens.
2. Give every child the immutable bundle, one lens reference, read-only scope,
   and the exact reviewer output schema.
3. Launch all selected lens children in one parallel window when supported.
4. Drain all children before consolidation and preserve each lens result
   verbatim.
5. Prefer `capability_mode: read-only` (or an explore-equivalent agent type) so
   reviewers cannot edit files. Inherit the session model when per-child model
   controls are unused and report that limitation.
6. Degrade to isolated sequential lens execution with
   `degradation: sequential_no_parallel_support` when concurrency is unavailable.
7. Retry one failed lens once after adding only the missing bundle context.

The controller performs no lens analysis and reviewers execute no shared
build/test targets. A separate narrow child adjudicates only submitted conflicts.
