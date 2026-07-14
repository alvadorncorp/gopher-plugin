# Concurrency and Performance Lens

Review goroutine ownership/termination, cancellation, channel close/send/receive,
lock/atomic invariants, races, deadlocks, leaks, backpressure, hot paths,
allocations, and evidence for performance claims. Tie every finding to a
specific schedule, blocked path, invariant violation, or measured regression.

Optimization style or an unmeasured suspicion is `MISSING_EVIDENCE`, not a
finding. Route diagnosis and fixes to `gopher:concurrency-performance` and keep
general package architecture in its own selected lens.
