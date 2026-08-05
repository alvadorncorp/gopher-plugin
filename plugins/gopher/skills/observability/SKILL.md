---
name: observability
description: Designs, instruments, and audits Go telemetry across logs, metrics, traces, profiles, dashboards, alerts, correlation, sampling, cardinality, cost, and redaction, using `log/slog`, OpenTelemetry, W3C Trace Context, and Prometheus conventions. Use to choose the signals that answer an operational question, place instrumentation at the correct boundary, or audit telemetry coverage, safety, and cost. Route reliability objectives to `gopher:resilience`, incident attribution to `gopher:diagnose`, profile interpretation to `gopher:performance`, and debug-endpoint exposure to `gopher:security`.
---

# Go Observability

## Context and ownership

Own the design, instrumentation, and audit of Go telemetry: signal contracts for
logs, metrics, traces, and profiles, plus dashboards, alerts, correlation,
sampling, cardinality, cost, redaction application and verification, and signal
tests. Primary owner: `gopher:observability`. `gopher:security` rules on whether
a value class may be carried at all; this skill applies that ruling at the
emission site, states the bounded replacement, and proves it with an absence
assertion. Recommendations stay vendor-neutral and follow the
conventions of OpenTelemetry, W3C Trace Context propagation, Prometheus, and
`log/slog`. Route by intent:

| Question | Owner |
|---|---|
| Which reliability objective applies, and what happens when it is missed | `gopher:resilience` |
| Which change, component, or dependency caused this incident | `gopher:diagnose` |
| What does this already-captured profile say about the hot path | `gopher:performance` |
| Who may reach the debug and profiling endpoints | `gopher:security` |
| Whether an attribute may carry a secret, credential, authorization material, or personal data | `gopher:security` |

The split with `gopher:performance` is concrete: reading an already-captured CPU
profile to find the hot path is `gopher:performance`; deciding that the service
must continuously expose profiles, and at what cost, is `gopher:observability`;
who may reach them is `gopher:security`. Package boundaries stay with `gopher:architecture`,
local reversible edits that apply an accepted instrumentation plan go to
`gopher:developer`, and backpressure remedies stay with `gopher:concurrency`.

## Modes

| Mode | When | Stop condition |
|---|---|---|
| `design` | An operational question exists and the signals that answer it are undecided, absent, or disputed | Every stated question maps to a complete signal contract with a named consumer and an acceptance test |
| `instrument` | The contracts are agreed and the code needs the signals emitted | Each contracted signal is emitted at its declared boundary and covered by a local signal test |
| `audit` | Telemetry already exists and its coverage, safety, cost, correlation, or operability is in question | Each existing signal is classified as answering a question, cost-bearing without a consumer, or unsafe, with a remedy and an owner |

## Workflow

1. **Start from the operational question.** Record the question, who asks it,
   the decision it drives, and the response window. A signal that answers no
   stated question is not designed; it is either retired or given a question.
2. **Define the signal contract.** Fix name, type, unit, lifecycle, attributes,
   cardinality budget, sampling, retention, cost, redaction, correlation keys,
   consumer, and acceptance test per `references/signal-contracts.md`. Resolve
   the Go version, the telemetry modules in use, and the applicable
   semantic-convention version before committing to an API or an attribute name.
3. **Place instrumentation at the correct boundary.** Apply
   `references/instrumentation-boundaries.md`: a library exposes hooks and
   accepts providers; the composition root configures exporters, samplers,
   propagators, and shutdown. Emit through `references/logging-slog.md`,
   `references/metrics.md`, `references/tracing-context.md`, and
   `references/profiles-runtime.md`.
4. **Validate locally.** Prove each signal on the success, error, cancellation,
   and shutdown paths with the recorders in `references/signal-tests.md`, and
   record what a local pass leaves unproven.
5. **Tie every dashboard and alert to a declared decision or objective.** Apply
   `references/dashboards-alerts.md`, hand the objective itself to
   `gopher:resilience`, and close with the review in
   `references/cardinality-cost-redaction.md`.

## Output format

```yaml
selected_skill: gopher:observability
primary_owner: gopher:observability
mode: design | instrument | audit
status: COMPLETE | COMPLETE_WITH_LIMITATIONS | BLOCKED
operational_questions:
signal_contracts:
instrumentation_boundaries:
validated_paths:
limitations:
authorization_gate: none | approval-required | blocked
handoff: gopher:<skill> | null
```

Terminal states:

- `COMPLETE`: every stated question has a contracted signal, the instrumentation
  sits at its declared boundary, and the local validation passed.
- `COMPLETE_WITH_LIMITATIONS`: the design is sound while backend validation, a
  runtime capability, or a semantic-convention stability guarantee stayed
  unconfirmed locally. Name each unverified item in `limitations`.
- `BLOCKED`: the operational question, an authorization gate, or the Go and
  telemetry module versions stayed unresolved, so a recommendation would be a
  guess.

## Authorization boundaries

- Local design, reading existing instrumentation, and running project-adopted
  tests may proceed on request.
- Changing exporter endpoints, sampling ratios, retention, or ingestion volume
  affects cost and a shared backend; carry an explicit approval gate and state
  the expected volume delta.
- Keep secrets, credentials, tokens, prompts, authorization material, and
  unbounded user-controlled values out of every log, attribute, span, metric
  label, and exemplar. Telemetry egress is irreversible once shipped.
- Exposing `net/http/pprof`, `/debug/vars`, or a continuous-profiling endpoint
  requires an authorization decision owned by `gopher:security`.
- Production access, live traffic capture, and backend configuration changes
  require explicit authorization; report the blind spot when it is withheld.
- Report operability as validated locally until a backend confirms ingestion,
  query, and alert routing.

## Quality checklist

- Every signal names the operational question and the consumer it serves.
- Every attribute has a bounded value set and a stated cardinality budget.
- Resolve the Go version, the telemetry module versions, and the applicable
  semantic-convention version before recommending an API or an attribute name.
- Discover runtime-metric support for the declared Go version rather than
  assuming a metric name exists.
- Keep library instrumentation free of global providers, exporters, and default
  handlers; the composition root owns those.
- Correlate the four signals through trace and span ids plus a shared resource
  identity.
- Cover the success, error, cancellation, and shutdown paths locally.
- State cost, retention, and redaction alongside every proposed signal.

## References

- `references/signal-contracts.md` — the full signal contract table with a worked example per signal kind.
- `references/logging-slog.md` — `log/slog` handler selection, level policy, and attribute discipline.
- `references/metrics.md` — instrument selection, units, buckets, and Prometheus naming and labels.
- `references/tracing-context.md` — spans, status, W3C propagation, and log and metric correlation.
- `references/profiles-runtime.md` — continuous profiling exposure and discovered `runtime/metrics` support.
- `references/instrumentation-boundaries.md` — library versus composition-root ownership and middleware placement.
- `references/dashboards-alerts.md` — panels and alerts traced to a declared decision or objective.
- `references/cardinality-cost-redaction.md` — cardinality budgets, cost estimation, and redaction rules.
- `references/signal-tests.md` — in-memory recorders and the four paths a signal must survive.
- `references/sources.md` — version-sensitive official references and review cadence.
