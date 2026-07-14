---
name: concurrency-performance
description: Diagnoses and improves Go concurrency and measured performance across goroutine lifetimes, channels, synchronization, context, races, leaks, backpressure, benchmarks, profiling, and GC. Use for lifecycle, synchronization, memory, or throughput work. Route general architecture and unmeasured optimization requests to evidence gathering or their canonical owners.
---

# Go Concurrency and Performance

## Context and ownership

Own goroutine lifetime, channels, synchronization, atomics, context, races,
deadlocks, leaks, backpressure, benchmarks, profiles, allocations, GC, and
measured optimization. Primary owner: `gopher:concurrency-performance`.

## Workflow

1. Capture expected behavior, observed symptom, workload, environment, Go
   version, recent change, and current measurements.
2. Reproduce safely; separate correctness/liveness from throughput/latency.
3. Build up to three hypotheses and choose a discriminating race/profile/trace/test probe.
4. For concurrency, make ownership, lifetime, cancellation, blocking, and
   backpressure explicit before changing primitives.
5. For performance, establish a repeatable baseline before optimization.
6. Apply the smallest change supported by evidence.
7. Re-run correctness plus the same measurement; report variance and limitations.

## Output format

```yaml
primary_owner: gopher:concurrency-performance
problem_and_evidence:
workload_and_environment:
hypotheses_and_probes:
ownership_lifetime_backpressure:
baseline:
change_or_recommendation:
after_measurement:
validation:
limitations:
handoff:
```

## Authorization

Use safe local tests, race detection, benchmarks, profiles, and traces already
adopted by the project. Tool installation, production profiling, destructive
load, secret access, or broad security probes require explicit authorization.
An optimization without a stable baseline returns a measurement plan first.

## Quality checklist

- Distinguish safety, liveness, latency, throughput, allocation, and GC claims.
- Name the owner and termination path of every changed goroutine.
- Specify close, send, receive, cancellation, error, and backpressure semantics.
- Use synchronization that matches the invariant; justify atomics with memory ordering.
- Compare before/after under the same workload and report noise.
- Preserve correctness tests alongside performance evidence.

## References

- `references/goroutine-lifetime.md` — ownership and termination.
- `references/channels-synchronization.md` — channels, locks, atomics, races.
- `references/context-cancellation.md` — context ownership and propagation.
- `references/diagnostics.md` — race, deadlock, leak, and contention probes.
- `references/benchmarking.md` — repeatable benchmark protocol.
- `references/profiling.md` — CPU, heap, allocation, trace, and GC evidence.
- `references/pattern-mappings.md` — cancellation, pipeline, and pooling mappings.
