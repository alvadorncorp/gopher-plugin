# Codex Review Adapter

1. Use the available Codex collaboration/subagent API; create one task per selected lens.
2. Give every task the immutable bundle, one lens reference, read-only scope,
   and the exact reviewer output schema.
3. Dispatch selected lenses together when parallel subagents are available, in
   successive windows of at most the bound the controller resolved.
4. Await/drain each window before opening the next, and drain the union of all
   windows before consolidation; preserve task/lens identity.
5. When model/reasoning controls exist, apply the session's review policy; when
   they do not, inherit the session model and report that limitation.
   The Codex agent dialect carries no model or effort key, so the packaged
   `reviewer` agent binds this controller's sandbox and not its model. The lens
   tasks it dispatches are not packaged agents either, so this limitation applies
   to the controller and to every lens task.
6. When parallelism is unavailable, run isolated lens prompts sequentially and
   add `degradation: sequential_no_parallel_support` to the final report.
7. Retry one failed lens once with corrected missing bundle context.

Reviewer tasks receive read-only instructions and must return findings instead
of modifying files. The controller performs shared commands before dispatch.
