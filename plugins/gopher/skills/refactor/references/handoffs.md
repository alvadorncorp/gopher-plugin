# Handoffs

The orchestrator delegates every owned change and records the handoff. It never
performs work that belongs to a specialist.

## Owners

| Dimension or change | Canonical owner |
|---|---|
| Local reversible refactor | `gopher:developer` |
| Complexity measurement and reduction | `gopher:complexity` |
| Coverage, effectiveness, mutation, safety nets | `gopher:test-quality` |
| Language, API, module, toolchain modernization | `gopher:modernize` |
| Public API, module topology, cross-package contract | `gopher:architecture` |
| Security exposure and boundaries | `gopher:security` |
| Goroutine lifetime, synchronization, cancellation, backpressure | `gopher:concurrency` |
| Algorithmic cost, allocation, GC, memory growth, latency, throughput | `gopher:performance` |
| Readiness against known project, toolchain, module, and generated-output invariants | `gopher:doctor` |
| Failure semantics, retries and idempotency, overload and degradation, recovery | `gopher:resilience` |
| Telemetry signal design, instrumentation, and audit | `gopher:observability` |
| Generated-output freshness, determinism, and provenance | `gopher:codegen` |
| Go/C boundary ownership, lifetime, pointers, callbacks, and build matrix | `gopher:cgo` |
| Native fuzz targets, corpora, bounded campaigns, and triage of campaign-produced crashes | `gopher:fuzz` |
| Read-only multi-lens review | `gopher:review` |

## Recording a handoff

For each handoff record: the target owner, the requested outcome, the input
evidence (baseline, diff range, scope), the authorization gate that applies, and
the returned result or blocker.

## Following a handoff

- Wait for the specialist's passing boundary before advancing to the next
  mutating phase.
- When a specialist escalates (a change exceeds its scope), route the escalation
  to the correct owner and record it; do not absorb the work.
- Keep every handoff visible in the final report, including declined or blocked
  ones.

A finding and its fix can have different owners. `gopher:fuzz` can return a
minimized crash whose production fix belongs to `gopher:developer`, and
`gopher:doctor` can return a stale-artifact finding whose remediation belongs to
`gopher:codegen`. Record both the finding's owner and the fix's owner, open a
second handoff to the fix owner with the returned evidence as its input, and
leave both sides of the pair with their specialists.
