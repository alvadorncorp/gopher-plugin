# Performance Lens

Review asymptotic and algorithmic cost, data structure choice, allocation and
GC pressure, cache behavior, parsing, I/O amplification, latency, and
throughput. Trace the changed path over the workload it actually serves and name
the input shape that makes the cost visible.

Require evidence for every claim: a benchmark for magnitude, a profile for
attribution, and an input-size series for growth. Optimization style, an
unmeasured suspicion, and a speedup asserted without a measurement are
`MISSING_EVIDENCE`, not findings. A regression is a finding only when the diff
changes the cost model or the measurement shows it.

Route diagnosis and the optimization plan to `gopher:performance`, and the local
edit that applies it to `gopher:developer`. Keep goroutine lifetime,
synchronization, and backpressure in the `concurrency` lens, and cyclomatic or
cognitive complexity in the `complexity` lens.
