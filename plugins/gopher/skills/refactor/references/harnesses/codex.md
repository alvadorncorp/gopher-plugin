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
   The Codex agent dialect carries no model or effort key, so the packaged
   `developer` and `architect` agents bind those two roles' sandbox and not their
   model. Every owner task here stays on the session model.
6. When parallelism is unavailable, run analysis sequentially and add
   `degradation: sequential_no_parallel_support` to the final report.
7. Close with a read-only `gopher:review` task over the accumulated diff; apply
   no fixes during review. That closing task invokes the skill and is not the
   packaged `reviewer` agent, so it carries no packaged binding; the sandbox
   binding in step 5 covers `developer` and `architect` only.

The controller performs no owned analysis. Specialists keep their gates, and a
mutating phase never overlaps another on intersecting scope.
