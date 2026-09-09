# Omp Refactor Adapter

1. Use omp's `task` tool to delegate each dimension to its canonical owner, one
   distinct child per owner.
2. Give every child the immutable baseline, the dimension scope, the applicable
   authorization gate, and the expected evidence bundle. Resolve every reference
   through the skill directory the host injected, never through `skill://<name>`.
3. Launch read-only analysis on bundled `scout` children in one parallel window;
   they mutate nothing.
4. Run mutating phases strictly one at a time, in priority order, draining each
   phase's passing boundary before the next begins. Dispatch local reversible
   work on `gopher-developer`. Route structural work to `gopher-architect`; it
   returns decided slices for the delegating session to apply unless both
   `agents.authorization` is `inherit-session` and the prompt carries explicit
   approval. Other canonical owners keep their own skill and gate on `task`;
   this adapter does not absorb their work into the three Gopher roles.
5. All children inherit the session model. Report that limitation when project
   policy declares a model or effort.
6. Degrade to sequential analysis with
   `degradation: sequential_no_parallel_support` when `task` is unavailable or
   the session spawn policy denies the fan-out. That degradation does not
   substitute a generic `task` child or omp's bundled `reviewer` for a missing
   Gopher role.
7. Close with a read-only `gopher-reviewer` run over the accumulated diff; the
   orchestrator applies no fixes during review.

The controller performs no owned analysis. Each specialist keeps its gate, and
no two mutating phases run concurrently on intersecting scope.

Before dispatching `gopher-developer`, `gopher-architect`, or `gopher-reviewer`,
confirm that name is present in the `task` catalog and is not disabled. If it is
missing or disabled, stop that handoff, name the cause, and point at the
directed omp install configuration: `extensions` must include the Gopher `omp`
root and `skills.customDirectories` must include the Gopher `skills` tree. Do
not substitute `task` or the bundled `reviewer`. If the autoloaded skill for
that role is unavailable, stop with an installation block rather than inventing
the workflow.
