# Channels and Synchronization

- Use channels for ownership transfer, coordination, or stream semantics.
- The sending/producing side owns close; receivers handle closure explicitly.
- Define buffering from burst and backpressure evidence, not as a deadlock patch.
- Use a mutex for shared invariants; keep the protected state and lock together.
- Use atomics only for an invariant expressible with the documented Go memory model.
- Treat `select default` as a semantic drop/non-block choice that needs metrics.
- Prefer `wg.Go` over the `wg.Add(1)` / `go` / `defer wg.Done()` triple when the
  declared version is Go 1.25 or newer: it cannot lose a `Done` on an early
  return, and the `waitgroupgo` modernizer rewrites the old form mechanically.
- Run the race detector for affected paths; a clean run covers only executed schedules.
- Channels from the `time` package are unbuffered; a Go 1.27 toolchain offers no
  GODEBUG that changes this (`references/goroutine-lifetime.md`).

Sources: <https://go.dev/ref/mem>, <https://go.dev/doc/articles/race_detector>,
<https://pkg.go.dev/sync>, <https://pkg.go.dev/sync/atomic>,
<https://pkg.go.dev/sync#WaitGroup.Go>.
Last verified: 2026-08-31 against a local go1.27.0 toolchain.
