# Tracing and Context Propagation

A trace answers "where did the time go, and across which components". Design the
span set from that question rather than instrumenting every function.

## Span shape

| Element | Rule |
|---|---|
| Name | The low-cardinality operation: a route pattern, an RPC method, a job kind. Identifiers belong in attributes |
| Kind | `SERVER`, `CLIENT`, `PRODUCER`, `CONSUMER`, or `INTERNAL`, matching the relationship to the remote peer |
| Start and end | Both in the same function, with the end deferred so every return path closes the span |
| Attributes | The fixed key set from the signal contract, set at start where known so samplers can see them |
| Status | Left unset on success, set to error only when the operation failed for its caller |
| Events | Bounded, timestamped facts inside the span, never a substitute for logs |

An expected outcome is not an error: a validation rejection or a cache miss is a
normal result, and marking it as an error inflates every error-rate panel built
on span status.

## Errors on a span

Recording an error and setting the status are two separate actions. Record the
error to attach the exception detail; set the status to error so aggregation and
sampling recognize the failure. Doing only the first leaves the span green in
every dashboard.

Keep the recorded detail bounded. A stack trace and a message may carry
identifiers, query text, or user content, so redact per
`references/cardinality-cost-redaction.md` before recording.

## Span kinds across a boundary

| Boundary | Producer side | Consumer side |
|---|---|---|
| HTTP or gRPC call | `CLIENT` span, context injected into request headers | `SERVER` span, context extracted from request headers |
| Message queue | `PRODUCER` span, context injected into message metadata | `CONSUMER` span, context extracted from message metadata |
| In-process stage worth timing | `INTERNAL` span | Not applicable |

An asynchronous consumer often starts a new trace linked to the producing span
rather than continuing it, because a long-lived batch that inherits the
producer's trace distorts that trace's duration. Record which of the two the
design chose.

## W3C Trace Context

Cross-process correlation travels in two headers:

- `traceparent`: version, trace id, parent span id, and trace flags, including
  the sampled flag. This header carries the identity a downstream service joins.
- `tracestate`: an ordered, vendor-keyed list of additional state. Preserve and
  forward entries that the process did not create; dropping the header breaks
  vendor-specific state for every hop downstream.

Configure the propagator once in the composition root, composing trace context
with baggage when the deployment uses baggage. A service that traces internally
but omits propagator configuration produces disconnected single-service traces
that look correct in isolation. Confirm the specification level the propagator
implements before relying on a newer flag or field.

Treat inbound trace context from an untrusted client as attacker-controlled
input: it can force sampling decisions and inject baggage. The decision to
accept, restart, or link is an authorization boundary shared with
`gopher:security`.

## Context inside Go

- Pass `context.Context` as the first parameter and derive spans from it. The
  active span lives in the context, so a function that drops it silently
  orphans every child span.
- Start a goroutine with the caller's context when its work belongs to the
  request, and with a context detached from cancellation when the work must
  outlive the request. In the second case link the new trace to the originating
  span rather than inheriting a context about to be cancelled.
- Keep the context out of struct fields. A stored context freezes one request's
  trace and cancellation into an object reused by others.
- End a span on the cancellation path too, with the status the caller should
  see. Cancellation deserves an explicit outcome rather than a missing span.

## Correlation with logs and metrics

| Direction | Mechanism |
|---|---|
| Log to trace | Read trace id and span id from the context and attach them to every record; see `references/logging-slog.md` |
| Trace to metric | Metric exemplars carry the trace id sampled at recording time, so a latency bucket links to a representative trace |
| Metric to log | Shared resource identity and shared attribute keys let one query span both stores |
| Trace to profile | Shared resource identity plus the collection window; see `references/profiles-runtime.md` |

Correlation is a design constraint, not a later addition: attribute keys,
resource attributes, and id propagation must agree across all four signals from
the first contract.

Last verified: 2026-08-05.
