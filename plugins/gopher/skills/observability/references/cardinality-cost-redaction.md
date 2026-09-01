# Cardinality, Cost, and Redaction

Three properties decide whether telemetry survives contact with production: how
many series it creates, what it costs, and what it must never carry.

## How cardinality breaks a backend

A metrics backend stores one time series per distinct combination of metric name
and attribute values, per reporting target. The series count for one instrument
is the product of the distinct value counts of its attributes, multiplied by the
number of instances:

```text
series = instances * product(distinct values per attribute) * histogram factor
```

Every series holds an index entry and a sample stream in memory. One attribute
with unbounded values — a user id, a request id, a full URL — turns a bounded
instrument into one series per event. The observed failure mode is not a wrong
graph: ingestion memory grows, the index degrades, queries slow, and the backend
begins dropping samples for unrelated metrics. The damage lands on every tenant
of that backend, not only on the offending service.

Traces and logs tolerate high-cardinality attributes because they store events
rather than pre-aggregated series. That is exactly why an identifier belongs on
a span or a log record and not on a metric.

## Attribute triage

| Risky attribute | Why | Bounded replacement |
|---|---|---|
| User, account, or session id | Unbounded, and personal data | Tier or plan; keep the id on the span |
| Request or correlation id | One value per event | Keep it on the log record and the span |
| Full URL or raw path | Unbounded through path parameters and query strings | Registered route pattern |
| SQL or query text | Unbounded, and can carry user data | Statement kind plus table |
| Raw error message | Unbounded through embedded values | Closed `error.kind` enumeration |
| Exact status code across a wide space | Wide, sometimes unbounded upstream | Status class, keeping exact codes for a known set |
| Timestamp, epoch, or duration value | Unbounded by construction | Histogram bucket |
| Free-form user input | Attacker-controlled | Validated enumeration, otherwise omitted |
| Container, pod, or build id | Grows with every deployment | Resource attribute with a retention plan, kept off per-request instruments |

Set a budget per instrument before rollout, verify it against real traffic, and
add an enforcement layer — an allowed-value list, a transformation, or a drop
rule — for attributes derived from external input.

## Cost estimation

| Signal | Estimate |
|---|---|
| Metric | series times samples per second times retention times bytes per sample |
| Log | events per second times average record size times retention, plus index overhead |
| Trace | spans per second times sampled ratio times average span size times retention |
| Profile | instances times captures per hour times artifact size times retention |

Produce the estimate before the change, state the delta against current volume,
and treat a change to sampling ratio, retention, or attribute set as a cost
decision that carries an approval gate. Two levers reduce cost without losing
the answer: aggregate at the source, and sample events while keeping counts
exact in a metric.

## Redaction

Keep the following out of every log record, span attribute, span event, metric
label, exemplar, and profile label:

- Credentials of any kind: passwords, API keys, tokens, session cookies,
  signing keys, and connection strings containing them.
- Authorization material: bearer tokens, assertions, and the headers carrying
  them.
- Model prompts, completions, and any user-authored content, which carry both
  personal data and unbounded size.
- Personal data beyond what the declared retention and jurisdiction allow.
- Raw user-controlled values, which are simultaneously a cardinality risk and an
  injection vector into log and query parsers.

Telemetry egress is irreversible: once a record reaches a shared backend it has
been copied, indexed, replicated, and possibly forwarded, and deletion is a
request rather than a guarantee. Redact at the emission site, and add a second
layer in the pipeline. Verify redaction with a test that asserts the absence of
the forbidden field, since an assertion on presence never catches a leak.

A profile label has a second egress path from Go 1.27. Modules declaring
`go 1.27` carry `runtime/pprof` goroutine labels into runtime tracebacks and
`debug=2` stack dumps, including the traceback an unrecovered panic prints into
ordinary application logs — a different retention regime and a different
jurisdiction question than the telemetry backend. The absence assertion above
covers that surface too. When a label the project needs cannot lose the forbidden
field, `tracebacklabels=0` is the recorded alternative
(`references/profiles-runtime.md`).

Structured attributes with typed values also reduce the injection surface,
because a value is carried as data rather than concatenated into a message a
downstream parser will re-split.

## Handoff

Deciding who may reach `net/http/pprof`, `/debug/vars`, a metrics endpoint, or a
trace-debug endpoint is an authorization boundary owned by `gopher:security`.
This skill states what each endpoint reveals, its cost, and applies the
redaction `gopher:security` rules on; `gopher:security` decides the exposure and
the controls.

Last verified: 2026-08-31 against a local go1.27.0 toolchain.
