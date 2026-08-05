# Metrics

Pick the instrument from the question, then fix the unit, the attributes, and
the aggregation before writing the first recording call.

## Instrument selection

| Question | Instrument | Property |
|---|---|---|
| How many times did this happen | Counter | Monotonic; the consumer reads a rate |
| How many are in flight or currently held | UpDown counter | Increases and decreases; the consumer reads the level |
| What is the current value of something measured, not accumulated | Gauge | Last value wins; the asynchronous form observes on collection |
| How is this value distributed, and what share crosses a threshold | Histogram | Buckets answer percentile and threshold questions |

Two clarifications that decide most disputes:

- A counter plus a duration sum answers "average latency"; only a histogram
  answers "what share of requests exceeded the threshold". Objectives phrased as
  a threshold need a histogram whose buckets contain that threshold.
- An asynchronous gauge callback runs during collection. Keep it cheap and free
  of blocking work, since the collection cycle waits for it.

The synchronous gauge and other instruments arrived across successive releases
of the OpenTelemetry Go metric API. Resolve the module version in `go.mod`
before recommending one.

## Units and naming

- Record base units: seconds, not milliseconds; bytes, not kilobytes. Convert
  for display, never at the recording site.
- Use UCUM annotations in the OpenTelemetry unit field: `s`, `By`, `1` for a
  dimensionless ratio, and `{request}` for a counted item.
- Name by the measured subject and keep the name stable, since a rename breaks
  every dashboard and alert that references it.
- Keep the unit out of the OpenTelemetry instrument name; the exporter appends
  the unit suffix when the target exposition format requires it.

## Bucket choice

| Situation | Boundaries |
|---|---|
| A threshold-based objective exists | Include the exact threshold as a boundary, plus neighbours on each side |
| Latency across orders of magnitude | Exponential boundaries covering the observed range |
| Sizes with a known cap | Boundaries clustered where decisions change, plus one above the cap |
| The range is unknown | Start with the default view, measure, then narrow |

Bucket count multiplies series count: a histogram with `n` boundaries produces
`n + 3` series per attribute combination in a Prometheus exposition. Budget that
before adding boundaries, and check the result against
`references/cardinality-cost-redaction.md`. An exponential or native histogram
representation, where the backend supports it, trades fixed boundaries for a
bounded relative error.

## Prometheus naming and labels

| Rule | Form |
|---|---|
| Metric name | `snake_case`, prefixed by the subsystem, suffixed by the base unit: `http_server_request_duration_seconds` |
| Counter suffix | `_total` on the accumulated series |
| Histogram series | `_bucket` with the `le` label, plus `_sum` and `_count` |
| Label names | `snake_case`, stable across releases |
| Label values | A closed, bounded set; identifiers and free text stay out |
| Reserved | `le` for histogram buckets and `quantile` for summaries stay for their built-in meaning |

Every distinct label-value combination is one time series. Adding one label with
`k` values multiplies the series count for that metric by `k`, per target.

## OpenTelemetry metric versus Prometheus exposition

| Aspect | OpenTelemetry metric | Prometheus exposition |
|---|---|---|
| Model | Instrument plus attributes, exported through a reader | A text or protobuf endpoint scraped by a server |
| Temporality | Delta or cumulative, chosen by the exporter configuration | Cumulative, with counter resets detected by the server |
| Naming | Dotted, unit carried in a separate field | Underscored, unit encoded in the name suffix |
| Identity | Resource attributes carry service identity | Target labels supplied by service discovery, plus scope labels added by the exporter |
| Transport | Push over OTLP, or pull through a Prometheus exporter | Pull by scrape |

The Prometheus exporter normalizes names, appends unit and `_total` suffixes,
and adds scope labels. Design the OpenTelemetry name and unit correctly and let
the exporter perform the translation, rather than pre-encoding Prometheus
conventions in the instrument name and receiving a doubled suffix.

Instrumenting directly with a Prometheus client library remains valid for a
service that exposes only a scrape endpoint. Mixing both in one process is a
decision to record, since it produces two identity models and two naming rules
in the same exposition.

Last verified: 2026-08-05.
