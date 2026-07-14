# Benchmarking Protocol

1. Define the user-visible metric and representative workload.
2. Keep environment, inputs, Go version, CPU settings, and benchmark flags stable.
3. Verify correctness before timing.
4. Run enough samples for variance analysis; compare with `benchstat` when adopted.
5. Report `ns/op`, `B/op`, `allocs/op`, throughput, or latency only when relevant.
6. Re-run after the change and state regressions, noise, and trade-offs.

Microbenchmarks do not establish end-to-end value. Optimization claims without
a stable baseline remain hypotheses.

Source: <https://pkg.go.dev/testing#hdr-Benchmarks>.
Last verified: 2026-07-14.
