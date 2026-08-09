# Go-specific Testing Guidance

`gopher:developer` owns the local test-workflow sequencing below. Keep
test-quality analysis with `gopher:test-quality`; this workflow only establishes
the evidence required to safely make one bounded local change.

## Resolved test-workflow state machines

Establish a focused baseline, classify the change, and apply the resolved
`test_workflow` matrix before a production edit:

| Workflow | Behavior or bug fix | Behavior-preserving refactor | Mechanical change | Test-only change |
|---|---|---|---|---|
| `adaptive-tdd` | Require an attributable red signal before production code. | Require a passing characterization test before refactoring. | Permit a recorded test-first exception when no observable behavior changes. | Add or strengthen tests without production edits. |
| `strict-tdd` | Require an attributable red signal before production code. | Require a passing characterization safety net before refactoring. | Block production edits unless the session explicitly overrides the strict policy. | Add or strengthen tests without production edits. |
| `test-after` | Implement first, then add or update behavior tests. | Require a passing characterization safety net before refactoring. | Validate proportionally after the edit. | Add or strengthen tests without production edits. |

For `adaptive-tdd` and `strict-tdd`, production behavior code cannot be written
until its applicable first signal is recorded. A valid attributable red signal
is an assertion failure or compile failure caused by the requested missing
behavior, never an unrelated failure. An existing failing regression test is a
red signal only after the remaining focused baseline passes and the failure is
isolated to the requested bug. If a candidate test passes unexpectedly,
strengthen or correct it without editing production code. If it fails for an
unrelated reason, correct setup or stop; do not count it as red evidence.

After implementation, the same focused command must turn green. Refactor only
while that command stays green, then run proportional final validation. Record
an explicit reason for every exception, skipped, or non-applicable stage.

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

Source: <https://go.dev/doc/tutorial/add-a-test>, <https://go.dev/doc/fuzz>.
Last verified: 2026-07-14.
