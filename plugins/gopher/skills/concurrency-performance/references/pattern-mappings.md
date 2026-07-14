# Concurrency and Performance Pattern Mappings

| General ID | Go mapping | Direct baseline and selection rule |
|---|---|---|
| `pattern.context-cancellation` | `go.context-cancellation` | synchronous call first; select when lifetime and cancellation cross calls |
| `pattern.pipeline` | `go.pipeline` | sequential loop first; select for measured independent stages with explicit backpressure |
| `pattern.object-pool` | `go.sync-pool` | allocate normally; select only from allocation/GC evidence and disposable-item semantics |

For pipelines, specify stage ownership, channel direction, buffer rationale,
ordering, error/cancellation propagation, drain behavior, and fan-out/fan-in
bounds. For `sync.Pool`, account for nondeterministic eviction, no resource
lifecycle guarantee, reset requirements, retention, and contention.

Sources: <https://go.dev/blog/pipelines>, <https://pkg.go.dev/sync#Pool>.
Last verified: 2026-07-14.
