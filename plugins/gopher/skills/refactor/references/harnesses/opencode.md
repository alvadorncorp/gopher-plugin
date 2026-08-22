# OpenCode Refactor Adapter

1. Use OpenCode's `task` tool to delegate each dimension to its canonical owner,
   one distinct child per owner.
2. Give every child the immutable baseline, the dimension scope, the applicable
   authorization gate, and the expected evidence bundle.
3. Launch read-only analysis through `explore` children in one parallel window;
   they mutate nothing.
4. Run mutating phases through `gopher-developer` strictly one at a time, in
   priority order, draining each phase's passing boundary before the next begins.
   Route structural work to `gopher-architect`; its edit permission remains
   denied, so it returns decided slices for the delegating session to apply.
5. All children inherit the session model and variant. Report that limitation
   when project policy declares a model or effort.
6. Degrade to sequential analysis with
   `degradation: sequential_no_parallel_support` when task concurrency is
   unavailable.
7. Close with a read-only `gopher-reviewer` run over the accumulated diff; the
   orchestrator applies no fixes during review.

The controller performs no owned analysis. Each specialist keeps its gate, and no
two mutating phases run concurrently on intersecting scope.
