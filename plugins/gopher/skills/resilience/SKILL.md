---
name: resilience
description: Models Go failure behavior and recovery across time budgets, retries, idempotency, backoff and jitter, circuit breakers, bulkheads, overload and load shedding, graceful shutdown, dependency criticality, delivery semantics, degraded modes, failover, disaster recovery, SLO-driven alerting, chaos hypotheses, and residual risk. Use to decide how a Go service fails, degrades, and returns to health, when it falls over because a database is slow, when deploys drop requests, when retries storm a dependency, and to assess how reliable a service is and what evidence backs that. Goroutine, channel, and backpressure propagation mechanics belong to `gopher:concurrency`, causal attribution of an incident to `gopher:diagnose`, telemetry implementation to `gopher:observability`, and cost and throughput tuning to `gopher:performance`.
---

# Go Resilience

## Context and ownership

Own Go failure semantics, runtime reliability, distributed degradation,
recovery, and explicit reliability assessment. Primary owner:
`gopher:resilience`. Model how a service fails, degrades, and returns to
health; state the reliability intent, the controls that carry it, and the
residual risk that survives them. Adjacent concerns keep their canonical owner:

| Adjacent concern | Owner |
|---|---|
| goroutine and synchronization mechanics | `gopher:concurrency` |
| backpressure propagation mechanics (goroutines, channels, permits) | `gopher:concurrency` |
| causal attribution of an incident | `gopher:diagnose` |
| performance tuning | `gopher:performance` |
| telemetry implementation | `gopher:observability` |
| security policy | `gopher:security` |
| general implementation | `gopher:developer` |
| architectural change | `gopher:architecture` |

A goroutine that leaks after cancellation is `gopher:concurrency`; whether a
dependency timeout should shed load or degrade is `gopher:resilience`. This
skill states WHAT signal must detect a failure mode, and
`gopher:observability` designs and implements that signal. On the same split,
`gopher:resilience` chooses where backpressure must be felt and what happens at
that point; `gopher:concurrency` implements the propagation.

## Modes

| Mode | When | Stop condition |
|---|---|---|
| `runtime` | A single process or service needs time budgets, retries, idempotency, backoff and jitter, cancellation, circuit breakers, bulkheads, overload handling, backpressure, graceful shutdown, or recovery | Every failure-model entry has a bounded control, a detection signal, and a recovery path, and each open item is named as residual risk |
| `distributed` | Several services or dependencies interact and the question is dependency criticality, delivery and consistency semantics, failover, degraded modes, disaster recovery, or SLO-driven alerting | Each dependency has a criticality class, a degraded behavior, a restoration path, and an alert tied to a declared objective or a recorded objective gap |
| `assessment` | The user asks how reliable a system is, and evidence produced by other specialists already exists | The bounded synthesis separates proven controls, proposed controls, missing evidence, and residual risk, and every claim cites the specialist that produced its evidence |

Select the mode from the question, not from the topology. A question answered
inside one process or service selects `runtime`. A question that crosses a
service or dependency edge — criticality, delivery or consistency semantics,
failover, disaster recovery, or an objective-tied alert — selects `distributed`,
which runs the same workflow and additionally satisfies the `runtime` stop
condition. A request to judge existing reliability from evidence other
specialists produced selects `assessment`. When a request spans `runtime` and
`distributed`, such as whether a dependency timeout should shed load or degrade,
select `distributed` and report both stop conditions. `runtime` is the default
when no rule above selects a mode.

## State machine

```text
BOUNDARY AND WORKLOAD -> FAILURE MODEL -> RUNTIME CONTROLS -> OVERLOAD AND DEGRADATION -> LIFECYCLE AND RECOVERY -> RESIDUAL RISK
```

| Terminal state | Meaning |
|---|---|
| `COMPLETE` | The failure model is bounded, every entry carries a control, a detection signal, and a recovery path, and the declared objectives are covered |
| `COMPLETE_WITH_RISK` | The honest state when the controls are specified but named residual risk remains, or when the project declares no objective for a modeled failure mode. The gap is reported as a gap |
| `BLOCKED` | The boundary, workload, or dependency set stays unknown, or the requested work needs an authorization that is absent |

## Workflow

Steps 1, 2, and 6 run in every mode; steps 3, 4, and 5 specify controls in
`runtime` and `distributed`, and in `assessment` they are read as evidence
checks against existing artifacts under the read-only contract in
`references/assessment.md`.

1. Define the boundary, workload, dependencies, objectives, invariants, and
   recovery assumptions, plus the project's declared Go version.
2. Build a finite failure model with `references/failure-model.md`. Each entry
   carries a trigger, the affected operation, propagation, impact, detection
   signal, containment, recovery, and residual risk.
3. Verify the time budget, error taxonomy, idempotency, bounded attempts,
   backoff and jitter, cancellation, and retry-storm controls using
   `references/runtime-controls.md`.
4. Evaluate admission, queues, backpressure, load shedding, concurrency limits,
   and degraded service with `references/overload.md`, continuing into
   `references/distributed.md` in `distributed` mode.
5. Specify startup, readiness, shutdown, failover, restoration, and
   reconciliation with `references/lifecycle-recovery.md`.
6. Separate proven controls, proposed controls, missing evidence, and residual
   risk. Plan chaos with `references/chaos.md`; run `assessment` mode through
   `references/assessment.md`.

## Output format

```yaml
selected_skill: gopher:resilience
primary_owner: gopher:resilience
mode: runtime | distributed | assessment
status: COMPLETE | COMPLETE_WITH_RISK | BLOCKED
failure_model:
dependencies:
proven_controls:
proposed_controls:
missing_evidence:
residual_risk:
authorization_gate: none | approval-required | blocked
handoff: gopher:<skill> | null
```

## Authorization boundaries

- An SLO is read from the objectives the project declares. A failure mode with
  no declared objective is reported as a gap, carried as residual risk, and
  returned as `COMPLETE_WITH_RISK`.
- Chaos work starts plan-only. Never run a chaos experiment against production
  without explicit authorization naming the environment, the blast radius, the
  abort condition, and the owner.
- `assessment` mode reads and synthesizes. It implements nothing, configures
  nothing, deploys nothing, and runs no production probe; it hands every change
  to the owning skill, and widening its scope requires an explicit user request.
- Use the tests, load generators, and telemetry the project already adopted.
  Tool installation, destructive load generation, failover drills against live
  traffic, and secret access require explicit authorization.
- A local reversible implementation of an approved control goes to
  `gopher:developer`; a package boundary or public-contract change retains
  `gopher:architecture` and its approval gate.

## Quality checklist

- Bound the failure model by dependency and by operation, and state what the
  enumeration deliberately excluded.
- Give every entry a detection signal, implemented by `gopher:observability`.
- Pair every retry with an idempotency claim, a bounded attempt count, a
  budget, and jitter.
- Give every queue an explicit bound and a stated behavior at that bound.
- Name the degraded behavior of each dependency, not only its failure.
- Keep proven controls separate from proposed ones, and cite the evidence
  behind each proven one.
- Report residual risk explicitly rather than resolving it by assumption.

## References

- `references/failure-model.md` — the eight-column failure-model table and how to bound the enumeration.
- `references/runtime-controls.md` — time budgets, error taxonomy, idempotency, retries, breakers, and bulkheads.
- `references/overload.md` — admission, queue bounding, backpressure, shedding, and degraded tiers.
- `references/distributed.md` — dependency criticality, delivery semantics, failover, disaster recovery, and SLO-driven alerting.
- `references/lifecycle-recovery.md` — startup, readiness, graceful shutdown, restoration, and reconciliation.
- `references/chaos.md` — chaos as a falsifiable hypothesis with a blast radius, an abort condition, and an owner.
- `references/assessment.md` — the read-only bounded synthesis contract and its evidence-citation rule.
- `references/sources.md` — version-sensitive official references and review cadence.
