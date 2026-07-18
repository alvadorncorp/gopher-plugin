# Codex Refactor Adapter

1. Use the available Codex collaboration/subagent API to delegate each dimension
   to its canonical owner, one owner per task.
2. Give every task the immutable baseline, the dimension scope, the applicable
   authorization gate, and the expected evidence bundle.
3. Run read-only analysis tasks together when parallel subagents are available;
   analysis mutates nothing.
4. Run mutating phases strictly one at a time, in priority order; await each
   phase's passing boundary before dispatching the next.
5. When model/reasoning controls exist, apply the session's policy per owner;
   otherwise inherit the session model and report that limitation.
6. When parallelism is unavailable, run analysis sequentially and add
   `degradation: sequential_no_parallel_support` to the final report.
7. Close with a read-only `gopher:review` task over the accumulated diff; apply
   no fixes during review.

The controller performs no owned analysis. Specialists keep their gates, and a
mutating phase never overlaps another on intersecting scope.
