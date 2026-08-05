# Distributed Degradation

`distributed` mode reasons about edges between services. The unit of analysis is
the dependency, and every dependency gets a criticality class, a degraded
behavior, and a restoration path.

## Dependency criticality

| Class | Definition | Required design |
|---|---|---|
| Critical | The core operation is impossible without it | A stated recovery objective, a tested failover or queue-and-replay path, and an alert tied to a declared objective |
| Degradable | The operation continues with reduced value | A named degraded tier, a staleness bound, and a signal showing the tier is active |
| Optional | The operation is unaffected in substance | A short budget, a breaker, and a failure that is logged rather than surfaced |

Classification is read from the product, not assumed. A dependency called on
every request is not automatically critical: if the call has a usable fallback,
it is degradable, and saying so is what makes the degraded tier real.

Every dependency also records its own dependencies where they are known. A
"degradable" cache that fronts a critical datastore inherits the datastore's
consequences on a miss storm.

## Delivery semantics

| Semantics | Guarantee | Cost | Fits |
|---|---|---|---|
| At-most-once | Never applied twice, possibly never applied | Silent loss | Telemetry samples, best-effort notifications |
| At-least-once | Applied at least once, possibly repeated | Consumers must be idempotent | Most work queues and event pipelines |
| Effectively-once | Observably applied once, built from at-least-once delivery plus deduplication or idempotent application | A durable dedup key store with a retention window | Payments, ledger entries, provisioning |

Effectively-once is an application property, not a transport promise. Its parts
are a stable idempotency key, a durable record of applied keys, and a retention
window at least as long as the maximum redelivery horizon. State the retention
window explicitly; an expired key turns a late redelivery into a duplicate
effect.

Pair the choice with a durability decision at the boundary: a write that must
survive the process uses the transactional outbox pattern, so the state change
and the intent to publish commit together and a relay publishes afterwards.

## Consistency expectations

- State which reads tolerate staleness and how much. "Eventually consistent"
  without a bound is an unmeasurable promise.
- Name the operations that require read-your-writes, and record how they get it:
  primary reads, session tokens, or a version check.
- Record what a replica lag spike does to each operation, and treat that as a
  failure-model row with its own detection signal.
- Clock-derived ordering is a hazard: prefer sequence numbers or versions over
  wall-clock comparisons across hosts.

## Failover and degraded modes

- Define the failover unit: a connection, an instance, a zone, or a region.
- State detection, decision, and execution separately. Who or what declares the
  failover, and how long each step takes, is the bulk of the real recovery time.
- Prefer failover paths that are exercised by normal traffic. A standby that is
  never read is an untested control and stays in residual risk.
- Define the failback path with the same rigor, including how divergent writes
  are reconciled.
- Guard against flapping: require a stable signal before failing over, and a
  longer stable signal before failing back.

## Disaster recovery

- Record the recovery objectives the project declares for time to restore and
  for tolerable data loss, and the date of the last restore exercise.
- Record what a restore actually reproduces: schema, data, secrets,
  configuration, and the order in which dependencies must return.
- A backup whose restore has never been exercised is a proposed control.

## SLO-driven alerting

An SLO is read from the project's declared objectives; it is never invented
here. When the project declares none, report the absence as a gap, carry it as
residual risk, and return `COMPLETE_WITH_RISK`.

Given a declared objective:

- Alert on symptoms that map to the objective — the user-visible failure and
  latency of a named journey — rather than on individual resource readings.
- Derive burn-rate alerting from the declared error budget: a fast burn signals
  an urgent page, a slow burn signals a ticket.
- Give every failure-model row a signal that distinguishes it from its
  neighbours, and hand the metric, trace, and log implementation to
  `gopher:observability`.
- Record what each alert cannot see, so an untested failure mode stays visible
  as residual risk instead of hiding behind a green dashboard.

Sources: <https://pkg.go.dev/context>, <https://go.dev/blog/context>,
<https://go.dev/doc/database/execute-transactions>.
Last verified: 2026-08-05.
