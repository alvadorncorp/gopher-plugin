# Go-specific Testing Guidance

Own Go mechanics while leaving generic TDD/test-generation workflow ownership
to their dedicated skills.

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
