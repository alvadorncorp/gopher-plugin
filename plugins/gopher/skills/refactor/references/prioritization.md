# Prioritization

Order remediation so the highest-risk, safety-establishing work happens before
lower-risk polish. Apply the dimensions in this fixed order:

1. Correctness and security risk. Fix defects and security exposure first; they
   dominate every other concern.
2. Test safety. Establish or strengthen the tests that protect the remaining
   work before changing production code.
3. Complexity reduction. Reduce the ranked hotspots that make later change risky.
4. Concurrency and performance dimensions. Resolve goroutine lifetime,
   synchronization, backpressure, latency, throughput, allocation, and
   asymptotic-cost work after the safety net is established and before broad API
   modernization.
5. Modernization. Adopt declared-version-safe idioms and API updates, preview
   first.
6. Whole-scope validation and a fresh review. Re-measure every dimension and run
   the read-only `gopher:review`.

## Applying the order

- Skip a dimension that has no applicable work, and record it as skipped rather
  than silently dropping it.
- When a higher-priority dimension is blocked, resolve or explicitly defer it
  before starting a lower-priority one; do not reorder to avoid a blocker.
- Test safety precedes complexity, concurrency, performance, and modernization
  because those dimensions can all change code the tests must already protect.
