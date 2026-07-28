# Evidence Matrix

Pick the probe that discriminates between the surviving hypotheses. Collect one
diagnostic at a time: precise memory profiling can skew a CPU profile, and block
profiling can affect a scheduler trace.

## Claim to probe

| Claim under test | Discriminating probe | What it cannot show |
|---|---|---|
| The routine is slower than the workload allows | `testing.B` over the representative input | production impact, end-to-end value |
| Cost grows faster than the input | the same benchmark over small, representative, large, and adversarial sizes | the complexity class; growth is a symptom, static analysis is the proof |
| One call path dominates on-CPU time | CPU profile | off-CPU waiting, retained memory |
| Allocation churn drives the cost | `allocs` profile plus `B/op` and `allocs/op` | GC pause attribution, live-heap growth |
| Memory is retained rather than churned | heap `inuse_space` / `inuse_objects` | which call path allocated it originally |
| The routine waits on a lock | mutex profile | which goroutine held it and for what reason |
| The routine blocks on a channel or syscall | block profile | scheduling order across processors |
| Latency, scheduling, utilization, syscall or network wait, blocking, or GC timing explains the metric | bounded execution trace | CPU or memory hot-spot attribution |
| I/O round trips dominate | request count and payload size at the boundary, plus a CPU profile to exclude local cost | database or remote-service execution cost |

## Stopping rules

Stop collecting when all of the following hold:

- One hypothesis explains the observed metric and the rejected hypotheses have
  a recorded reason.
- The supporting measurement is reproducible under an equivalent workload.
- The proposed change has a stated expected cost model and a verification that
  would falsify it.

Keep collecting when two hypotheses remain viable, when the measurement is not
reproducible, or when the proposed change has no falsifiable verification.

## Reporting evidence strength

Every finding carries:

- `evidence`: the exact command, workload, input sizes, environment, and Go
  version.
- `strength`: `reproduced` (repeated samples, stable environment),
  `observed` (a single capture), or `suspected` (static reasoning only).
- `limits`: sampling rate, capture overhead, point-in-time scope, and the
  schedules or inputs the probe did not cover.

A `suspected` finding is a measurement request, not a recommendation to change
code.

## Owner routing from the evidence

| Dominant evidence | Owner |
|---|---|
| CPU, allocation, GC, cache, parsing, or I/O amplification | `gopher:performance` |
| Blocked goroutine, contended lock, cancellation, or backpressure | `gopher:concurrency` |
| Local reversible edit that applies the accepted plan | `gopher:developer` |
| Package boundary, module topology, or public contract | `gopher:architecture` |

Source: <https://go.dev/doc/diagnostics>.
Last verified: 2026-07-28.
