# Signal Tests

A signal is a contract, so it gets a test. The test proves that emission happens
with the agreed name, attributes, and level on every path the contract claims to
cover.

## Recorders by signal

| Signal | Local recorder | Assertion |
|---|---|---|
| Log | A handler writing to a buffer, or a recording handler collecting records | Message, level, attribute keys and values, and the absence of redacted fields |
| Log handler conformance | The standard library's handler conformance test | A custom handler obeys grouping, attribute, and level semantics |
| Metric | A manual reader collected on demand | Instrument name, unit, attribute set, data point value, and histogram bucket counts |
| Prometheus exposition | The client library's test helpers | Exposed name, labels, and value against expected exposition text |
| Trace | An in-memory span exporter or span recorder | Span name, kind, status, attributes, events, and parent relationship |
| Propagation | Inject into a carrier, then extract from it | Trace id and span id survive the round trip, and `tracestate` entries are preserved |
| Profile | A request against the exposed endpoint | A parsable profile returns within the collection window |

Collect deterministically. A test that sleeps and hopes the batch exporter
flushed is flaky by construction: use a manual reader, a synchronous span
processor, or an explicit flush before asserting.

## The four paths

| Path | What the test drives | What it asserts |
|---|---|---|
| Success | The operation completes normally | The expected records, data points, and one span with an unset status; no error signal is emitted |
| Error | The dependency or the operation fails | The error is recorded, the span status is error, the error counter increments, and the closed error kind appears |
| Cancellation | The caller cancels the context or the deadline expires | The span ends with the intended outcome, the operation stops promptly, and cancellation is distinguished from a dependency failure |
| Shutdown | Provider shutdown or flush runs with signals still buffered | Buffered records reach the exporter before the process exits, and shutdown returns within its timeout |

The cancellation path is where instrumentation most often leaks: a span started
before a blocking call and ended only on the success return leaves an unfinished
span and a missing data point whenever the deadline fires. The shutdown path is
where the last seconds of an incident are lost, because a batch exporter still
holds them.

## Assertion discipline

- Assert on the contracted fields, not on the whole serialized record. A test
  comparing full JSON breaks whenever an unrelated attribute is added.
- Assert the absence of redacted fields explicitly, since a presence-only
  assertion never detects a leak.
- Assert attribute value domains, not only keys: a route attribute holding a raw
  path passes a key-only check and still breaks cardinality.
- Assert the emission count. A signal emitted twice through doubled middleware
  passes every single-record assertion.
- Keep instrumentation tests next to the behaviour they cover, so a refactor
  that removes a span fails a test in the same package.

## What a local pass proves

A local pass proves that the process emits the contracted signal on the covered
paths. It is not a claim about production operability. These remain unproven
until a backend confirms them:

| Unproven locally | Confirmed by |
|---|---|
| The collector accepts the payload and its schema | An ingestion check against the real pipeline |
| The name survives exporter normalization | Reading the exposed or ingested name |
| Cardinality stays inside budget under real traffic | Series count measured against production attribute distributions |
| The query behind a panel returns the expected shape | Running it against ingested data |
| The alert routes to the intended owner | An end-to-end alert test |
| Retention covers the alert window | Backend retention configuration |

Report the design as `COMPLETE_WITH_LIMITATIONS` and list each unconfirmed item
when local validation is all that was available.

Last verified: 2026-08-05.
