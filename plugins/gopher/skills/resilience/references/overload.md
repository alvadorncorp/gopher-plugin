# Overload and Degradation

Overload is the state where arrival rate exceeds service capacity. The goal is
never to accept everything; it is to keep the accepted work correct and fast
while the surplus is rejected early and honestly.

## The queue rule

**An unbounded queue converts an overload into a memory failure.** An unbuffered
or bounded channel makes the producer wait, which is backpressure. An unbounded
slice, an unbounded worker backlog, or a goroutine spawned per request turns
excess arrivals into resident memory, and the process dies from the surplus
instead of rejecting it.

Every queue in the design therefore carries three declared properties:

| Property | Question it answers |
|---|---|
| Bound | How many items may wait at once |
| Behavior at the bound | Block the producer, reject the arrival, or drop the oldest item |
| Maximum wait | How long an item may sit before it is worthless |

An item whose deadline has already passed is discarded on dequeue rather than
processed; serving expired work is the classic path from a latency spike to a
sustained collapse.

## Admission control

Admission decides what enters the system, at the cheapest possible point.

- Reject before allocation: check the limit before parsing a body, opening a
  connection, or starting a goroutine.
- Bound the request itself: `http.MaxBytesReader` and a header timeout keep one
  client from consuming the budget of many.
- Rate-limit per tenant or per key with `golang.org/x/time/rate`, so one caller
  cannot claim the whole capacity.
- Return a truthful rejection: HTTP 429 with a retry hint for a rate decision,
  HTTP 503 for a capacity decision. A rejection that looks like a server bug
  invites the client to retry harder.

## Concurrency limits

- Cap in-flight work per dependency with a semaphore or a fixed worker pool,
  sized from measured service time and the target latency rather than from a
  round number.
- Prefer a fixed pool consuming a bounded channel over one goroutine per
  arrival; the pool makes the limit visible and the memory bounded.
- Size the limit so that queue wait plus service time stays inside the request
  budget. A limit that admits more work than the budget allows produces
  timeouts, not throughput.

## Backpressure

Backpressure is the signal that travels from a saturated stage back to its
producer.

- In-process, a bounded channel is the signal: the producer blocks, and the
  blocking is the message.
- Across a network, the signal is an explicit rejection or a flow-control
  window; a peer that cannot see saturation keeps sending.
- Propagate the signal to the true source. Backpressure that stops at an
  internal stage moves the queue rather than bounding it.
- Goroutine and channel mechanics for the propagation belong to
  `gopher:concurrency`; this reference chooses where the pressure must be felt.

## Load shedding

Shedding is the deliberate rejection of work the system cannot serve.

| Decision | Guidance |
|---|---|
| Trigger | A measured saturation signal: queue depth, in-flight count, or latency against the budget |
| Selection | Shed by declared priority — best-effort before critical, anonymous before authenticated, retries before first attempts |
| Rate | Shed enough to return inside the budget, and restore admission gradually |
| Honesty | Report the shed rate as its own signal so shedding is never mistaken for a dependency failure |

Shedding retries before first attempts is what stops a retry storm from
consuming the capacity that would have ended it.

## Degraded service tiers

A degraded tier is a named, tested, lower-value behavior that keeps the core
promise while a dependency is impaired.

| Tier | Behavior | Example |
|---|---|---|
| Full | Every feature at the declared objective | Live prices, personalized ranking |
| Degraded | Core operation with a stated loss of freshness or richness | Cached prices with an explicit staleness bound, default ranking |
| Minimal | The single invariant the product cannot lose | Accept and durably record the order for later processing |
| Rejecting | Fast, truthful rejection with a retry hint | HTTP 503 while the datastore is unwritable |

Each tier declares its entry condition, its exit condition, its user-visible
effect, and the signal that shows which tier is active. A degraded tier that
has never been exercised is a proposed control, not a proven one, and it stays
in the residual-risk list until an exercise or a real incident proves it.

Sources: <https://pkg.go.dev/golang.org/x/time/rate>,
<https://pkg.go.dev/net/http#MaxBytesReader>,
<https://pkg.go.dev/golang.org/x/sync/semaphore>.
Last verified: 2026-08-05.
