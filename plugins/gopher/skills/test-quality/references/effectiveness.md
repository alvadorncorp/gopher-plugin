# Test effectiveness

Coverage shows which lines run, not whether a test would catch a fault. Evaluate
whether the suite actually protects behavior.

## Signals of weak tests

- Assertions that check only that no error occurred, never the returned value.
- Tests that assert on the implementation's own output echoed back, rather than
  an independent expected value.
- Missing cases for error paths, boundary values, empty and nil inputs, and
  concurrency where relevant.
- Snapshot or golden tests that would pass after a silent behavior change.

## Untested behavior

- List behaviors exercised by production code but never asserted.
- Distinguish "covered but unasserted" (a line runs with no meaningful check)
  from "not covered".

## Refactor protection

Before a refactor, confirm the suite pins the behavior the refactor must
preserve. If it does not, recommend strengthening or characterization tests
(`references/refactoring-safety.md`) before production edits begin. A refactor
without a protecting test is unsafe and must be reported as such.
