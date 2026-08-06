# Grok Refactor Adapter

1. Use Grok Build's `spawn_subagent` tool to delegate each dimension to its
   canonical owner, one distinct child per owner.
2. Give every child the immutable baseline, the dimension scope, the applicable
   authorization gate, and the expected evidence bundle.
3. Launch read-only analysis children in one parallel window when supported;
   they mutate nothing.
4. Run mutating phases one at a time, in priority order, draining each phase's
   passing boundary before the next begins.
5. Inherit the session model when per-child model controls are unused and report
   the limitation.
   The packaged `developer` and `architect` agents pin those two roles; every
   other owner child stays on the session model.
6. Degrade to sequential analysis with
   `degradation: sequential_no_parallel_support` when concurrency is unavailable.
7. Close with a read-only `gopher:review` child over the accumulated diff; the
   orchestrator applies no fixes during review. That closing child invokes the
   skill and is not the packaged `reviewer` agent, so it carries no packaged
   binding; the pin in step 5 covers `developer` and `architect` only.

The controller performs no owned analysis. Each specialist keeps its gate, and no
two mutating phases run concurrently on intersecting scope.
