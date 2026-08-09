# Go-specific Testing Guidance

`gopher:developer` owns the local test-workflow sequencing below. Keep
test-quality analysis with `gopher:test-quality`; this workflow only establishes
the evidence required to safely make one bounded local change.

## Resolved test-workflow state machines

Before editing production behavior, establish a focused baseline, classify the
change, and apply the resolved `test_workflow` matrix:

| Workflow | Behavior or bug fix | Behavior-preserving refactor | Mechanical change | Test-only change |
|---|---|---|---|---|
| `adaptive-tdd` | Require an attributable red signal before production code. | Require a passing characterization test before refactoring. | Permit a recorded test-first exception when no observable behavior changes. | Add or strengthen tests without production edits. |
| `strict-tdd` | Require an attributable red signal before production code. | Require a passing characterization safety net before refactoring. | Block production edits unless the session explicitly overrides the strict policy. | Add or strengthen tests without production edits. |
| `test-after` | Implement first, then add or update behavior tests. | Require a passing characterization safety net before refactoring. | Validate proportionally after the edit. | Add or strengthen tests without production edits. |

For every matrix row, record the focused baseline, resolved workflow and change
class, applicable first signal, green confirmation, refactor check, and final
validation in the parent output contract. Advance only when the current stage's
evidence is available; record why a stage is skipped or non-applicable.

For `adaptive-tdd` and `strict-tdd`, record the applicable first signal before
writing production behavior. A valid attributable red signal is an assertion failure or compile failure
caused by the requested missing behavior, never an unrelated failure. An existing failing regression test is a
red signal only after the remaining focused baseline passes and the failure is isolated to the requested bug. If
a candidate test passes unexpectedly, add an assertion for
the missing behavior or correct the test/setup while keeping production code
unchanged. When failure is unrelated, correct setup or stop and record it as a
non-signal; it never counts as red evidence.

After implementation, the same focused command must turn green. Refactor only
while that command stays green, then run final validation using the affected-risk
ladder in `references/tooling.md`. For each baseline, first-signal, green,
refactor, and final-validation stage, record the exact command, exit status, and
concise observation. Record an explicit reason for every exception, skipped, or
non-applicable stage. If required evidence is unknown, stop at that gate and
name the exact command or decision needed to continue.

## Go test mechanics

- Assert public behavior and independent expected values.
- Cover success, expected absence, error identity/cause, boundary values, and
  compatibility behavior changed by the implementation.
- Use table tests when cases share setup and assertion shape; name each case.
- Keep helpers deterministic and call `t.Helper()` where failure locations matter.
- Use fakes at consumer-owned seams; prefer real values for local pure behavior.
- Add race tests for shared-state or goroutine changes, fuzzing for parsers and
  serialization boundaries, and integration tests only across real boundaries.
- Keep benchmarks separate from correctness and report `benchstat` comparisons
  for performance claims.

## Specialist boundaries

Keep this reference to local test mechanics and workflow evidence. Route
suite-level coverage, effectiveness, mutation, and technique selection to
`gopher:test-quality`; native fuzz target, invariant, and campaign design to
`gopher:fuzz`; race, deadlock, leak, and synchronization diagnosis to
`gopher:concurrency`; and benchmark, profile, or performance measurement to
`gopher:performance`. Production behavior fixes remain with `gopher:developer`.

Sources: <https://go.dev/doc/tutorial/add-a-test>, <https://go.dev/doc/fuzz>.
Last verified: 2026-07-14.
