# Performance Pattern Mappings

| General ID | Go mapping | Direct baseline and selection rule |
|---|---|---|
| `pattern.object-pool` | `go.sync-pool` | allocate normally; select only from allocation and GC evidence and disposable-item semantics |

For `sync.Pool`, account for nondeterministic eviction, the absence of a
resource lifecycle guarantee, reset requirements, retention of oversized
buffers, and contention. A pool proposed without an allocation profile and a
before and after benchmark is returned as a measurement plan.

Cancellation and pipeline mappings live in `gopher:concurrency`, because those
decisions rest on lifetime and backpressure rather than on allocation evidence.

Sources: <https://pkg.go.dev/sync#Pool>,
<https://go.dev/doc/gc-guide#Understanding_costs>.
Last verified: 2026-07-28.
