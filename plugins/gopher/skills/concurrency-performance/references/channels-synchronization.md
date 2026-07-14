# Channels and Synchronization

- Use channels for ownership transfer, coordination, or stream semantics.
- The sending/producing side owns close; receivers handle closure explicitly.
- Define buffering from burst and backpressure evidence, not as a deadlock patch.
- Use a mutex for shared invariants; keep the protected state and lock together.
- Use atomics only for an invariant expressible with the documented Go memory model.
- Treat `select default` as a semantic drop/non-block choice that needs metrics.
- Run the race detector for affected paths; a clean run covers only executed schedules.

Sources: <https://go.dev/ref/mem>, <https://go.dev/doc/articles/race_detector>,
<https://pkg.go.dev/sync>, <https://pkg.go.dev/sync/atomic>.
Last verified: 2026-07-14.
