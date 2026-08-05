# Lifecycle and Recovery

A process is reliable across its whole lifetime, not only while it is serving.
Startup, readiness, shutdown, failover, restoration, and reconciliation each
carry their own failure modes.

## Startup ordering

- Acquire configuration and secrets first, and fail fast with a clear message
  when a required value is absent. A process that starts with half a
  configuration fails later and more confusingly.
- Open the resources whose absence makes the service useless, and treat a
  failure there as a startup failure rather than a background retry.
- Start background loops after the resources they use exist, and give each one
  an owner and a termination path; the mechanics belong to
  `gopher:concurrency`.
- Begin accepting traffic last, once warmup — connection pools, caches,
  compiled templates — has reached the state the first request assumes.
- Bound startup itself. A startup that hangs on a dependency looks identical to
  a crash loop from the outside; a bounded startup that reports why is
  diagnosable.

## Readiness and liveness intent

The two probes answer different questions, and conflating them is the most
common self-inflicted outage in this area.

| Probe | Question | Correct reaction |
|---|---|---|
| Liveness | Is this process unrecoverably stuck? | Restart it |
| Readiness | Should this instance receive traffic right now? | Remove it from rotation, keep it running |

- Keep liveness narrow and local. A liveness probe that calls a shared
  dependency restarts every instance at once when that dependency fails.
- Let readiness reflect what this instance can actually serve, including write
  capability when writes are part of the promise.
- Fail readiness first during shutdown, so traffic drains before serving stops.
- Bound both probes with their own timeouts so a slow probe is not read as a
  dead process.

## Graceful shutdown

The sequence is: stop accepting, drain in flight, release resources, exit.

```go
ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
defer stop()

go func() {
    if err := srv.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
        log.Error("serve", "err", err)
    }
}()

<-ctx.Done()
stop() // restore default handling so a second signal terminates immediately

shutdownCtx, cancel := context.WithTimeout(context.Background(), 20*time.Second)
defer cancel()
if err := srv.Shutdown(shutdownCtx); err != nil {
    // deadline exceeded: in-flight work was cut short — record it
}
```

Details that decide whether this works:

- `signal.NotifyContext` gives one cancellable context for the whole process;
  every background loop derives from it and reports when it has stopped.
- `http.Server.Shutdown` stops listeners, closes idle connections, and waits for
  active requests. It returns `http.ErrServerClosed` from `ListenAndServe`, so
  that error is the expected outcome rather than a failure.
- The drain deadline is shorter than the platform's termination grace period.
  A drain deadline that outlives the grace period is a hard kill wearing the
  costume of a graceful shutdown.
- Fail readiness and wait one propagation interval before calling `Shutdown`, so
  the load balancer stops sending new requests to a closing listener.
- Hijacked and long-lived connections (WebSocket, streaming) are not waited on
  by `Shutdown`. Cancel them explicitly through the process context and count
  them as their own drain step.
- Shut background workers down after the server, so in-flight requests can
  finish the work they enqueued.
- Record what the deadline cut short; a truncated drain is residual risk, not a
  clean exit.

## Failover and restoration

- State what the instance does when its primary dependency moves: reconnect,
  re-resolve DNS, refresh credentials, and rebuild pooled connections.
- Treat restoration as its own hazard. A recovered dependency meets the full
  backlog at once, so restore admission gradually and keep the breaker's
  half-open probe bounded.
- Warm the caches a restored instance assumes, or accept the miss storm as a
  modeled failure with its own control.
- Expect a thundering herd of clients reconnecting simultaneously, and jitter
  the reconnect just as retries are jittered.

## Reconciliation after partial failure

Any ambiguous outcome leaves the system with work of unknown status. Recovery
is a reconciliation loop, not a guess.

- Persist intent before the effect, so a restart can find unfinished work: an
  outbox row, a job record, or a state machine with an explicit in-progress
  state.
- Make the reconciler idempotent and repeatable, keyed on the same idempotency
  key the original attempt used.
- Bound the reconciler's own work: batch size, rate, and a maximum age after
  which an item is escalated to an operator rather than retried forever.
- Give the backlog its own signal, since a reconciler that silently falls
  behind hides the original failure.
- Record items the reconciler cannot resolve; they are residual risk with a
  named owner.

Sources: <https://pkg.go.dev/os/signal#NotifyContext>,
<https://pkg.go.dev/net/http#Server.Shutdown>,
<https://pkg.go.dev/net/http#ErrServerClosed>.
Last verified: 2026-08-05.
