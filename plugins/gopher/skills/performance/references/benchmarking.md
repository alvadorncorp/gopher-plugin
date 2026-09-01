# Benchmarking Protocol

## Protocol

1. Verify correctness before timing. A benchmark over broken behavior measures
   nothing useful.
2. Define the user-visible metric and the representative workload, then hold
   inputs, Go version, compiler flags, CPU settings, and machine state fixed.
3. Write a `testing.B` benchmark. Use `b.Loop` only when the project's declared
   Go version is 1.24 or newer; keep the `b.N` form otherwise.
4. Report allocation metrics with `-benchmem` or `b.ReportAllocs()`. Use
   `b.SetBytes` for throughput, or a custom metric via `b.ReportMetric` for an
   algorithm-specific count.
5. Predeclare the sample count before running. Interleave baseline and candidate
   runs; do not rerun until a difference appears.
6. Compare with `benchstat` when the project has already adopted it. Current
   guidance is at least 10 and ideally 20 runs per configuration. When it is not
   adopted, report the per-run distribution and state that no statistical
   comparison was made; installing a tool needs the authorization gate in
   `SKILL.md`.

## Capture commands

```bash
go test -run '^$' -bench 'BenchmarkTarget' -benchmem -count 10 ./pkg > base.txt
# apply the candidate change, then:
go test -run '^$' -bench 'BenchmarkTarget' -benchmem -count 10 ./pkg > new.txt
benchstat base.txt new.txt
```

## The input-size matrix

Run the same benchmark over four classes and record the metric for each:

| Class | Purpose |
|---|---|
| small | shows fixed overhead and the setup cost of an index or a sort |
| representative | the production shape, the number that decides value |
| large | exposes growth and memory pressure |
| adversarial | worst-case ordering, duplicates, collisions, or skew |

Growth across these points is a scaling symptom. It does not establish a
complexity class: cache thresholds, GC, input shape, an internal algorithm
switch, and setup cost all distort the ratios. Pair the measurements with a
static analysis of the algorithm.

## Limits

- A microbenchmark does not establish end-to-end value.
- A single run is weak evidence; thermal state, battery mode, and host load move
  the numbers.
- Recapture the baseline on the new toolchain before attributing any delta to a
  code change: time, allocation, and size baselines all cross a toolchain change
  unreliably. Go 1.27 alone moved all three
  (`references/version-sensitive.md`).
- An optimization claim without a stable baseline stays a hypothesis.

Sources: <https://pkg.go.dev/testing#B>,
<https://pkg.go.dev/testing#B.ReportAllocs>,
<https://pkg.go.dev/golang.org/x/perf/cmd/benchstat>,
<https://go.dev/doc/go1.27>.
Last verified: 2026-08-31.
