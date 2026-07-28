---
name: concurrency
description: Diagnoses and fixes Go concurrency defects across goroutine lifetime, channels, mutexes, atomics, context cancellation, races, deadlocks, goroutine leaks, and backpressure. Use for hangs, leaked goroutines, race detector output, unclear ownership, or synchronization design. Route asymptotic cost, allocation, GC, and throughput analysis to `gopher:performance`.
---

# Go Concurrency

## Context and ownership

Own goroutine lifetime, channels, synchronization, atomics, context, races,
deadlocks, goroutine leaks, and backpressure. Primary owner: `gopher:concurrency`.

Route asymptotic cost, allocation, GC, cache behavior, parsing, I/O
amplification, benchmark, profile, latency, and throughput analysis to
`gopher:performance`. Route local reversible implementation to
`gopher:developer`, cross-package or public-contract work to
`gopher:architecture`, and an unattributed symptom to `gopher:diagnose`.

A symptom with both a concurrency defect and a cost component keeps one primary
owner: choose the domain whose evidence explains the observed failure and record
the other as a handoff.

## State machine

```text
CAPTURE SYMPTOM -> REPRODUCE -> HYPOTHESES -> ONE DISCRIMINATING PROBE -> EXPLICIT OWNERSHIP -> SMALLEST CHANGE -> RE-VERIFY
```

## Workflow

1. Capture expected behavior, observed symptom, workload, environment, the
   project's declared Go version, recent changes, and current measurements.
2. Reproduce safely and separate correctness and liveness from latency and
   throughput. A cost question with no lifetime, synchronization, or
   backpressure defect belongs to `gopher:performance`.
3. Build at most three hypotheses and choose one discriminating probe from
   `references/diagnostics.md`.
4. Make ownership, lifetime, cancellation, blocking, and backpressure explicit
   before changing any primitive, using `references/goroutine-lifetime.md`,
   `references/channels-synchronization.md`, and
   `references/context-cancellation.md`.
5. Recommend or hand off the smallest change the evidence supports.
6. Re-run correctness plus the same probe, and state which schedules the
   evidence covered.

## Output format

```yaml
selected_skill: gopher:concurrency
primary_owner: gopher:concurrency
problem_and_evidence:
workload_and_environment:
hypotheses_and_probes:
ownership_lifetime_backpressure:
change_or_recommendation:
after_verification:
limitations:
authorization_gate: none | approval-required | blocked
handoff: gopher:developer | gopher:performance | gopher:architecture | gopher:diagnose | null
```

## Authorization boundaries

- Use local tests, the race detector, goroutine dumps, and block or mutex
  profiles already adopted by the project.
- Tool installation, production profiling, destructive load generation, and
  broad security probes require explicit authorization.
- Hand a local reversible fix to `gopher:developer`. A package boundary,
  public-contract, or module-topology change retains `gopher:architecture` and
  its approval gate.
- A clean race-detector run covers only the schedules that executed; report that
  bound with every clean result.

## Quality checklist

- Separate safety, liveness, and progress claims from cost claims.
- Name the owner and the termination path of every changed goroutine.
- Specify close, send, receive, cancellation, error, and backpressure semantics.
- Match the synchronization primitive to the invariant, and justify an atomic
  with the memory ordering it relies on.
- State which schedules the evidence covered and which remain untested.
- Keep correctness tests alongside every concurrency change.

## References

- `references/goroutine-lifetime.md` — ownership and termination.
- `references/channels-synchronization.md` — channels, locks, atomics, races.
- `references/context-cancellation.md` — context ownership and propagation.
- `references/diagnostics.md` — race, deadlock, leak, and contention probes.
- `references/pattern-mappings.md` — cancellation and pipeline mappings.
