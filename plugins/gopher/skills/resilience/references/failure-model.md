# Failure Model

The failure model is the single artifact every mode depends on. It is a finite
table, not a narrative, and it stays finite because the enumeration follows the
system's real surface.

## The eight columns

| Column | What it records | Accepted when |
|---|---|---|
| Trigger | The concrete event that starts the failure: a dependency timeout, a poisoned message, a disk-full write, a deploy, a certificate expiry | It names an observable event, not a feeling ("it gets slow") |
| Affected operation | The specific request path, job, or background loop that stops behaving | It maps to a handler, a consumer, or a named goroutine owner |
| Propagation | How the failure reaches other operations: shared pool exhaustion, shared mutex, retry amplification, queue growth, cache stampede | It names the shared resource or the amplifier |
| Impact | The user-visible or data-visible consequence, and its blast radius | It says who is affected and in what proportion |
| Detection signal | The signal that must distinguish this failure from a healthy state and from its neighbours | It states the discrimination, and `gopher:observability` implements it |
| Containment | The control that stops propagation: budget, bounded attempts, breaker, bulkhead, queue bound, shed rule | It is bounded and it is reachable in code |
| Recovery | How the system returns to healthy: retry, restart, failover, reconciliation, manual runbook step | It states who or what performs it and how completion is confirmed |
| Residual risk | What survives the control: an untested path, an unbounded dependency, an absent objective | It stays explicit and reaches the output bundle |

## Bounding the enumeration

Enumerate by dependency and by operation, never by imagination. Two passes
produce a finite table:

1. **By dependency.** List every outbound edge the process actually has:
   databases, caches, brokers, HTTP and gRPC clients, object storage, DNS, the
   filesystem, the clock, and the configuration source. For each edge, walk the
   fixed failure vocabulary below.
2. **By operation.** List every inbound entry point: HTTP and gRPC handlers,
   consumers, cron jobs, and background loops. For each, record what happens
   when its own resources are exhausted and when it is cancelled mid-flight.

The fixed per-dependency vocabulary keeps the table bounded: unavailable, slow,
partially failing, returning wrong or stale data, rejecting for authorization,
rate limiting, and recovering while the caller is still retrying.

Record what the enumeration deliberately excluded. "Region loss is out of scope
for this iteration" is a bounded model; silence is a hidden gap.

## Worked Go example

An order service writes to PostgreSQL and calls a pricing API.

| Trigger | Affected operation | Propagation | Impact | Detection signal | Containment | Recovery | Residual risk |
|---|---|---|---|---|---|---|---|
| Pricing API latency exceeds the per-call budget | `POST /orders` | Handler goroutines hold database connections while waiting, exhausting the pool | Checkout error rate rises for all customers | A signal separating pricing-call latency from database wait; a saturated-pool signal | Per-call `context.WithTimeout` shorter than the request budget, plus a breaker on the pricing client | Breaker half-opens on a probe; the pool drains as calls fail fast | Cached prices may be stale for the degraded window |
| PostgreSQL primary fails over | every write path | Writes fail while reads succeed, so the health endpoint stays green | Orders are rejected for the failover window | A write-path error signal distinct from the read path | Terminal-vs-retryable classification, bounded attempts, and readiness that reflects write capability | Reconnect and replay unfinished work from the outbox | An in-flight write may have committed before the connection dropped |
| A consumer receives a message it can never process | the settlement consumer | The consumer redelivers forever and starves healthy messages | Settlement lag grows without bound | A redelivery-count signal per message | Bounded redelivery with a dead-letter destination | An operator replays the dead-letter queue after a fix | Dead-lettered messages stay unsettled until replay |

## Ambiguity is a first-class entry

A call that times out has an unknown outcome: the peer may have applied the
effect. Model that as its own row, with idempotency as the containment and
reconciliation as the recovery. `references/runtime-controls.md` covers the
error taxonomy, and `references/lifecycle-recovery.md` covers reconciliation.

## Routing out of the model

A row whose evidence is a leaked goroutine or a contended lock hands its
mechanics to `gopher:concurrency`. A row whose cause is still unknown hands
attribution to `gopher:diagnose`. A row whose impact is throughput or latency
under healthy conditions belongs to `gopher:performance`. The failure model
keeps the row; the neighbouring skill supplies the mechanism.

Sources: <https://pkg.go.dev/context>, <https://go.dev/blog/context>.
Last verified: 2026-08-05.
