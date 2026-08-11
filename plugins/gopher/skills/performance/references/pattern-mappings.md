# Performance Pattern Mappings

| General ID | Go mapping | Direct baseline and selection rule |
|---|---|---|
| `pattern.object-pool` | `go.sync-pool` | allocate normally; select only from allocation and GC evidence and temporary, reusable, independently owned item semantics |

For `sync.Pool`, record these liabilities: nondeterministic eviction, the
absence of a resource lifecycle guarantee, reset requirements, retention of
oversized buffers, and contention. A pool proposed without an allocation
profile that names the object and a before and after benchmark is returned as a
measurement plan. Operational preconditions and failure modes:
`allocation-runtime.md`.

Cancellation and pipeline mappings live in `gopher:concurrency`, because those
decisions rest on lifetime and backpressure rather than on allocation evidence.

Identity interning and canonicalization map as `pattern.flyweight` →
`go.canonical-intern` under `gopher:developer` (with measured memory benefit and
safe identity and lifetime), not as pooling.

Sources: <https://pkg.go.dev/sync#Pool>,
<https://go.dev/doc/gc-guide#Understanding_costs>.
Last verified: 2026-07-28.
