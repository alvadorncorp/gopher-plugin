# Runtime Controls

Every control here is grounded in the standard library first. A third-party
breaker, limiter, or retry package is a project decision: name it as a proposed
control, record the dependency it adds, and leave the adoption to the user.

## Time budgets

A request carries one budget. Each downstream call receives a slice of what
remains, never a fresh independent timeout.

- Derive the budget once at the entry point with `context.WithTimeout`, and
  call the returned cancel function.
- Derive each downstream call from that context so cancellation propagates.
- Keep the sum of attempt budgets plus backoff inside the parent budget; a
  retry that outlives its parent context is wasted work.
- Set server-side limits too: `http.Server` `ReadHeaderTimeout`,
  `ReadTimeout`, `WriteTimeout`, and `IdleTimeout` bound what a slow or hostile
  peer can hold.

```go
ctx, cancel := context.WithTimeout(r.Context(), 800*time.Millisecond)
defer cancel()
```

## Error taxonomy

Classification decides behavior. Three classes are enough, and each call site
maps its errors into exactly one.

| Class | Meaning | Behavior |
|---|---|---|
| Retryable | The effect certainly did not apply: connection refused, HTTP 503, HTTP 429 with a retry hint | Retry within the budget and the attempt bound |
| Terminal | The effect will never apply: HTTP 400, a validation failure, `context.Canceled` from the caller | Fail fast and report |
| Ambiguous | The outcome is unknown: timeout, connection reset mid-response, `context.DeadlineExceeded` on a write | Retry only when the operation is idempotent; otherwise reconcile |

Use `errors.Is` and `errors.As` over string matching, and wrap with `%w` so the
class survives the call chain. `net.Error` and the `context` sentinel errors
carry most of the signal a Go client needs.

## Idempotency

A retry is safe when the operation is idempotent or carries an idempotency key.

- Reads and pure computations are naturally idempotent.
- Writes need a client-generated key persisted with the effect, so a replay
  returns the first result rather than applying a second effect.
- The key belongs to the logical operation, not to the attempt: every retry of
  one operation reuses one key.
- Without a key, an ambiguous result becomes a reconciliation task rather than
  a retry.

## Bounded attempts, backoff, and jitter

- Bound attempts by both a count and the remaining budget, and stop at whichever
  arrives first.
- Use exponential backoff with full jitter: sleep a uniform random duration in
  `[0, min(cap, base*2^attempt))`. Full jitter is what breaks the synchronized
  wave that fixed or equal backoff creates.
- Honour a server's `Retry-After` when it sends one; a stated wait beats a
  computed one.
- Sleep with a cancellable timer so a cancelled parent stops the wait
  immediately.

```go
select {
case <-ctx.Done():
    return ctx.Err()
case <-time.After(jittered):
}
```

## Retry storms

Retries multiply: three layers of three attempts is twenty-seven calls for one
request. Controls that keep the multiplication bounded:

- Retry at exactly one layer per hop, and let the other layers pass the error
  through.
- Keep a retry budget as a fraction of successful traffic, and stop retrying
  when the fraction is exceeded.
- Propagate a deadline so a downstream service knows the caller has already
  given up.
- Pair every retry policy with the breaker that turns sustained failure into
  fast rejection.

## Circuit breakers

A breaker converts repeated failure into immediate, cheap rejection, which frees
the resources that propagation feeds on.

- Closed: calls pass and outcomes are counted over a rolling window.
- Open: calls fail immediately for a cool-down; the failure-model row that
  depends on this call moves to its degraded behavior.
- Half-open: a bounded number of probes decides the next state.
- Count only the classes that indicate dependency health. Terminal client errors
  are the caller's fault and keep the breaker closed.
- Scope one breaker per dependency and per operation class; one global breaker
  hides which dependency is unhealthy.

## Bulkheads

A bulkhead limits how much of a shared resource one workload can hold, so one
failure keeps its blast radius.

- Give each dependency its own client, connection pool, and concurrency limit.
  Sizing `http.Transport` `MaxIdleConnsPerHost` per dependency is the simplest
  Go form.
- Use a buffered channel or `golang.org/x/sync/semaphore` as an explicit
  concurrency permit around each dependency call.
- Separate critical and best-effort work onto distinct pools so a best-effort
  flood leaves the critical path intact.
- Keep goroutine ownership and termination in `gopher:concurrency`; this skill
  chooses the limit and its failure behavior.

## Cancellation

- Treat `ctx.Err()` as a first-class outcome and report it as terminal for the
  caller, distinct from a dependency failure.
- Release every resource on cancellation: close bodies, return permits, and
  stop timers.
- Confirm that cancellation actually reaches the blocking call; a call that
  ignores the context turns a bounded budget into an unbounded wait.

Sources: <https://pkg.go.dev/context>, <https://pkg.go.dev/net/http#Server>,
<https://pkg.go.dev/errors>.
Last verified: 2026-08-05.
