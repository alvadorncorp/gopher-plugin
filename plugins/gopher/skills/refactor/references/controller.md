# Refactor controller

The controller drives the bounded flow and enforces sequencing. It coordinates
specialist owners; it performs no owned-elsewhere analysis or mutation itself.

## Sequencing

0. Scope preflight (cheap): resolve config presence, dirty tree, package patterns,
   and whether more than one dimension applies. If exactly one dimension applies,
   hand off to that specialist and do not open multidimensional orchestration.
   In `plan` mode, a failing test baseline is recorded but does not block analysis.
1. Resolve configuration, then capture the immutable baseline
   (`references/baseline.md`).
2. Gather read-only analysis per dimension. Analysis may run in parallel because
   it mutates nothing.
3. Order the work with `references/prioritization.md`.
4. In `plan` mode, stop after prioritization with `PLAN_READY`.
5. In `remediate` mode, run mutating phases strictly one at a time. Each phase
   starts from a passing state, records its evidence bundle, and ends by
   restoring a passing state.
6. Re-measure each dimension by the baseline method, then run the fresh review
   (remediate only).

## Handoff discipline

- For every dimension, request the analysis or change from its canonical owner
  and record the handoff (`references/handoffs.md`).
- When a specialist reports a change is out of its scope (a public contract, a
  module boundary, a security boundary), record the escalation to the correct
  owner rather than performing it here.
- Never collapse two owners into one phase; each specialist keeps its gate.

## Fresh final review

- The final review runs `gopher:review` read-only over the accumulated diff.
- The controller applies no fixes during review; a review finding becomes a new,
  separately owned change with its own baseline.
- A changed diff invalidates a prior approval.
- Fresh final review runs only in `remediate` mode, never in `plan` mode.
