# Signal Contracts

A signal is designed when every field below has an answer. A missing field is an
open design question, not a detail to settle after shipping.

## Contract fields

| Field | What it fixes | Failure when it is left open |
|---|---|---|
| Name | The stable identifier a query targets | Renames break dashboards, alerts, and saved queries |
| Type | Log record, counter, updown counter, gauge, histogram, span, or profile | The consumer cannot aggregate the value correctly |
| Unit | The UCUM unit (`s`, `By`, `1`, `{request}`) | Milliseconds and seconds mix in one panel |
| Lifecycle | When emission starts, how it changes, and when it is retired | Dead signals accrue cost forever |
| Attributes | The exact key set and the allowed value domain per key | Unplanned keys appear and queries stop matching |
| Cardinality | The series budget: product of allowed values per attribute, per target | A single unbounded key saturates the backend |
| Sampling | Head ratio, tail policy, or full fidelity, with the reason | Rare errors vanish or volume explodes |
| Retention | How long the consumer needs it | Alert windows outlive stored data |
| Cost | Series, events per second, or spans per second times retention | Cost surfaces as an invoice rather than a decision |
| Redaction | The fields removed, hashed, or bucketed before emission | Secrets and user content reach a shared backend |
| Correlation | Trace id, span id, resource identity, and shared attribute keys | Signals cannot be joined during an incident |
| Consumer | The person, alert, dashboard, or query that reads it | Nobody notices when the signal breaks |
| Acceptance test | The local assertion that proves emission | Regressions are found during the next incident |

## Worked example: metric

| Field | Value |
|---|---|
| Name | `http.server.request.duration` |
| Type | Histogram |
| Unit | `s` |
| Lifecycle | Emitted per completed server request, for the life of the service |
| Attributes | `http.request.method` (known methods plus `_OTHER`), `http.route` (registered patterns), `http.response.status_code` |
| Cardinality | methods times routes times status classes, per instance; budget stated before rollout |
| Sampling | Full fidelity; aggregation is the reduction |
| Retention | 13 months at reduced resolution for trend comparison |
| Cost | Series count times scrape interval times retention |
| Redaction | Route patterns only; raw paths and query strings stay out |
| Correlation | Exemplars carry trace id; resource attributes match the trace resource |
| Consumer | Latency panel and the burn-rate alert owned by `gopher:resilience` |
| Acceptance test | Manual reader collects one recorded value per path with the expected attributes |

## Worked example: log record

| Field | Value |
|---|---|
| Name | `payment.capture.failed` as the stable message |
| Type | Log record at `ERROR` |
| Unit | Not applicable; count occurrences from the metric, not from log volume |
| Lifecycle | Emitted at the outermost handler that decides the request has failed |
| Attributes | `payment.provider`, `error.kind`, `retryable`, `attempt`, plus trace and span id |
| Cardinality | Bounded by provider and a closed error-kind enumeration |
| Sampling | Full fidelity for `ERROR`; `DEBUG` gated by a level variable |
| Retention | 30 days searchable |
| Cost | Events per second times record size times retention |
| Redaction | Card data, tokens, and provider payloads stay out; only the closed error kind is recorded |
| Correlation | Trace and span id from the request context |
| Consumer | On-call search during a payment incident |
| Acceptance test | Handler capture asserts the message, level, attribute keys, and absence of payload fields |

## Worked example: span

| Field | Value |
|---|---|
| Name | `POST /orders/{id}/capture`, the low-cardinality operation name |
| Type | Span, kind `SERVER` |
| Unit | Not applicable; duration is intrinsic |
| Lifecycle | Starts at request entry, ends after the response is written |
| Attributes | Method, route, status code, and the closed error kind on failure |
| Cardinality | Attribute keys are fixed; span names use route patterns |
| Sampling | Parent-based head sampling with a stated ratio; error paths kept |
| Retention | 7 days |
| Cost | Spans per second times sampled ratio times average span size |
| Redaction | Request bodies, headers carrying authorization, and user identifiers stay out |
| Correlation | Propagated `traceparent`; logs emitted inside carry the same ids |
| Consumer | Latency breakdown and cross-service attribution |
| Acceptance test | In-memory span recorder asserts name, kind, status, and attributes per path |

## Worked example: profile

| Field | Value |
|---|---|
| Name | CPU profile exposed by the service |
| Type | Profile |
| Unit | Samples over a bounded window |
| Lifecycle | Continuous collection at a stated interval, or on-demand capture |
| Attributes | Service, version, instance, and deployment environment |
| Cardinality | Bounded by the instance count |
| Sampling | Collection window and frequency, with the measured overhead |
| Retention | 14 days |
| Cost | Instances times captures per hour times artifact size |
| Redaction | Symbol names can reveal internal structure; access is authorized, not public |
| Correlation | Resource identity shared with metrics and traces |
| Consumer | `gopher:performance` reads the captured profile; this skill owns the exposure decision |
| Acceptance test | The endpoint returns a parsable profile within the collection window under authorization |

Last verified: 2026-08-05.
