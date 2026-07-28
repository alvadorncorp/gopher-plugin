# Concurrency Lens

Review goroutine ownership and termination, cancellation, channel close, send,
and receive semantics, lock and atomic invariants, races, deadlocks, leaks, and
backpressure. Tie every finding to a specific schedule, blocked path, or
invariant violation.

An unmeasured suspicion or a style preference about primitives is
`MISSING_EVIDENCE`, not a finding. A clean race-detector run covers only the
schedules that executed; say so when citing one.

Route diagnosis and fixes to `gopher:concurrency`. Keep cost, allocation, GC,
and throughput claims in the `performance` lens and general package
architecture in the `architecture` lens.
