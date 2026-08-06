# Kimi Refactor Adapter

1. Use Kimi Code's `Agent` subagent tool to delegate each dimension to its
   canonical owner, one distinct child per owner.
2. Give every child the immutable baseline, the dimension scope, the applicable
   authorization gate, and the expected evidence bundle.
3. Launch read-only analysis children in one parallel window when supported
   (`subagent_type: explore`); they mutate nothing.
4. Run mutating phases one at a time, in priority order, draining each phase's
   passing boundary before the next begins.
5. Inherit the session model when per-child model controls are unused and report
   the limitation.
6. Degrade to sequential analysis with
   `degradation: sequential_no_parallel_support` when concurrency is unavailable.
7. Close with a read-only `gopher:review` child over the accumulated diff; the
   orchestrator applies no fixes during review.

The controller performs no owned analysis. Each specialist keeps its gate, and no
two mutating phases run concurrently on intersecting scope.

## Packaged agent fallback

Kimi Code loads plugin skills and discards packaged plugin agents, so the
`developer`, `architect`, and `reviewer` roles the other three harnesses load with
a fixed binding do not exist here. Reproduce each envelope inline in the
delegating prompt:

1. A child delegated to `gopher:developer` stays inside one package, keeps every
   change local and reversible, never edits generated output, runs only project
   commands that already exist, and stops at the first cross-package,
   public-contract, persistence, security-boundary, or ADR-affecting change.
2. A child delegated to `gopher:architecture` states its mode first, creates no
   file, and edits an existing file only when both conditions hold: the effective
   `agents.authorization` is `inherit-session`, and the delegating prompt carries
   the approval explicitly. Either one alone is not enough, and under the default
   `handback` the child never edits. Otherwise it returns
   `authorization_gate: approval-required` with its decided slices.
3. The closing `gopher:review` child is read-only for the whole run: it observes,
   makes no edit, never redirects output into the working tree, and never uses an
   in-place editor.
4. Read the `[agents]` table of `.gopher-plugin.toml` in the controller and
   evaluate this gate before the first mutating phase of step 4 above begins,
   never after one has run. Stop the run when `agents.enabled` is `false`, or
   when `agents.policy_divergence` is `block` and a divergence exists. Apply
   `agents.authorization` to every child's gate, and report `policy_status` with
   the same five values the packaged agents report: `NOT_CONFIGURED`, `ALIGNED`,
   `DIVERGED`, `UNVERIFIABLE`, or `BLOCKED_BY_POLICY`.
5. Report `policy_status: UNVERIFIABLE` for any declared model or effort, because
   this harness binds neither per child.

The declared policy may narrow this run and it can never widen it.
