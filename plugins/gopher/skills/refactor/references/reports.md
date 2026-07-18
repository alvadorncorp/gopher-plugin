# Evidence and output contract

Every refactor records enough evidence to reproduce and compare its result. The
report is the durable record of what changed, what was skipped, and why.

## Evidence bundle

- Source commit, working-tree diff, configuration path/state/hash, and the
  effective values used.
- Selected packages and modules and the dimension scope.
- Exact commands, tool names and versions, the baseline test result, and each
  metric collection result.
- Before/after values measured by the same method as the baseline.
- Applied changes, skipped work, handoffs, blockers, limitations, and every
  authorization decision.

## Terminal states

The three terminal states (`COMPLETE`, `COMPLETE_WITH_LIMITATIONS`, `BLOCKED`)
are defined in the `## Terminal states` section of `SKILL.md`. Report exactly one
of them with the evidence bundle below.

## Reporting rules

- A failed or skipped dimension is always visible; it is never reported as
  success.
- Ephemeral defaults are labeled ephemeral, with a note that no project policy
  was persisted.
- The final read-only review verdict and its diff range are included in the
  report.
