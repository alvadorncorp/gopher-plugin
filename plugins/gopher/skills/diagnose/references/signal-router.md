# Evidence-based Signal Router

## When to route

Use this table only after evidence identifies a dominant supported signal. A
keyword alone is not attribution. On a match, set `primary_owner` to exactly
one table owner and status to `ATTRIBUTED`. When no row is supported by the
evidence, keep status `UNKNOWN` and `primary_owner` null.

## Owner table

| Dominant supported signal | Primary owner |
|---|---|
| Local API, types, errors, modules, tooling, tests, or reversible implementation | `gopher:developer` |
| Cross-package dependency, package boundary, interface seam, module/workspace, or public contract | `gopher:architecture` |
| Goroutine lifetime, channel, synchronization, context, race, deadlock, goroutine leak, or backpressure | `gopher:concurrency` |
| Algorithmic or asymptotic cost, allocation, GC, memory growth, cache behavior, parsing, I/O amplification, benchmark, profile, latency, or throughput | `gopher:performance` |
| Explicit pattern forces and selection/rejection | `gopher:design-patterns` |
| Speculative interface or abstraction without a demonstrated consumer seam, framed as design choice rather than a crash | `gopher:design-patterns` |
| Global access, service locator, or registry convenience without process-wide identity or plugin-ecosystem evidence | `gopher:design-patterns` |
| Clone, snapshot/undo, interning/canonicalization, or expression/AST-eval design without an implementation request | `gopher:design-patterns` |
| Language-agnostic internal application boundary or dependency direction | `gopher:application-architecture` |
| Threat, trust boundary, exploit path, vulnerable dependency/symbol, or security control | `gopher:security` |
| Diff/PR review intent rather than diagnosis | `gopher:review` |
| Project configuration bootstrap, validation, or explanation | `gopher:config` |
| Cyclomatic/cognitive complexity, hotspots, or complexity thresholds | `gopher:complexity` |
| Coverage, mutation score, or whether tests detect behavioral faults | `gopher:test-quality` |
| Go version, API, module, dependency, or toolchain modernization | `gopher:modernize` |
| Repository-wide or multidimensional remediation across two or more dimensions | `gopher:refactor` |
| A known project, configuration, toolchain, module-state, or generated-output invariant that a written rule already covers | `gopher:doctor` |
| Failure semantics, retry and idempotency behavior, overload, degradation, or recovery under dependency failure | `gopher:resilience` |
| A missing, ambiguous, or costly telemetry signal, or a correlation, cardinality, sampling, or redaction question | `gopher:observability` |
| Generated output that is stale, nondeterministic, or of unclear provenance | `gopher:codegen` |
| An attributed defect at a Go/C boundary — pointer, ownership, lifetime, callback, thread affinity, or linking | `gopher:cgo` |
| An input-driven defect in a parser, decoder, or state machine that a falsifiable invariant can expose | `gopher:fuzz` |

## Boundary gates

A crash or hang at a Go/C boundary that has not been attributed stays in
`gopher:diagnose` until the evidence supports the boundary as the dominant
signal. The presence of `import "C"` is a keyword, not attribution; route to
`gopher:cgo` once a probe ties the observed failure to the boundary itself.

`gopher:doctor` owns a signal only while the request is still a readiness check
against an already-written rule. Once evidence attributes a cause, set
`primary_owner` to the specialist that performs the remedy —
`gopher:codegen` for a stale artifact, `gopher:config` for an invalid project
contract, `gopher:architecture` for a module or workspace inconsistency,
`gopher:modernize` for a toolchain or declared-version issue — and record the
readiness rule in `recommended_next_step`.

## One-owner rule

Mixed symptoms still receive one owner: choose the domain whose risk and
evidence explain the observed failure. Assign exactly one primary owner; put
secondary constraints in `recommended_next_step`.
