# Instrumentation Boundaries

Telemetry has two owners in a Go program, and mixing them is the most common
structural defect in an instrumentation review.

## The two roles

| Concern | Library | Composition root |
|---|---|---|
| Tracer, meter, and logger acquisition | Accepts a provider through an option, falling back to the documented global | Constructs and installs the providers |
| Exporters and endpoints | Leaves them to the caller | Configures OTLP, Prometheus, or file exporters |
| Sampler and resource | Leaves them to the caller | Chooses the sampler and builds the resource identity |
| Propagators | Uses the configured propagator | Sets the propagator, composing trace context and baggage |
| Shutdown and flush | Exposes a close for its own goroutines | Registers provider shutdown with a bounded timeout |
| Default `slog` handler | Accepts a `*slog.Logger`, defaults to no output | Calls `slog.SetDefault` once |
| Instrumentation scope | Names its own scope, versioned with the module | Leaves scope naming to each library |

A library that installs a global provider decides format, destination, sampling,
and cost for an application it cannot see, from an import side effect. A library
that accepts providers leaves every one of those decisions where the operator
can make them.

## Library checklist

- Take `context.Context` as the first parameter on every exported operation that
  can be traced or cancelled.
- Offer `WithTracerProvider`, `WithMeterProvider`, and a logger option, each
  defaulting to a no-output or global value that the caller can override.
- Acquire the tracer and meter once at construction, keyed by a scope name that
  matches the module path and carries the module version.
- Document the emitted span names, metric names, attribute keys, and log levels,
  so an application can budget cardinality and cost.
- Keep instrumentation optional in cost: when no provider is supplied, the code
  path stays free of exporters, background goroutines, and per-call allocation.

## Composition-root checklist

- Build the resource once: service name, version, instance id, and deployment
  environment. Every signal inherits this identity, and correlation depends on
  it matching across signals.
- Configure exporters, readers, and the sampler from configuration rather than
  from constants compiled into the binary.
- Set the propagator explicitly. A service that traces internally without a
  configured propagator produces disconnected single-service traces.
- Register shutdown for every provider, with a bounded timeout, so buffered
  spans, metrics, and log records flush before exit. Wire it to the same signal
  handling that drains the server.
- Install the `slog` default handler once, with the level variable that runtime
  verbosity changes will target.

## Middleware and wrapper placement

| Surface | Placement | Reason |
|---|---|---|
| HTTP server | Wrap the server handler so the span starts before routing and ends after the response is written | Time spent in other middleware and in routing belongs inside the request span |
| HTTP server route naming | Set the route pattern after the router resolves it, or read the matched pattern the standard multiplexer records for the declared Go version | The raw path carries identifiers and destroys cardinality |
| Panic recovery | Recovery inside the telemetry wrapper | The span records the failure and still ends with an error status |
| HTTP client | Wrap the transport, not each call site | Every request through that client is covered, including retries and redirects |
| gRPC | Register the instrumentation stats handler on the server and the client | Stats handlers see stream events that interceptors miss; the interceptor form is superseded in current instrumentation modules |
| Database | Wrap the driver or install the driver's tracer hook, and name spans by the statement kind | Query text is high-cardinality and can carry user data |
| Message consumer | Extract context from message metadata at the outermost consume loop | The consumer span then covers deserialization and handling |
| Background job | Start the span in the scheduler entry point, with a context detached from the request that enqueued it | A job outliving its enqueuer must not inherit a cancelled context |

## Review questions

1. Does any library package call a global setter for a provider, propagator, or
   default logger? Move it to the composition root.
2. Does the composition root register shutdown for every provider it creates?
3. Does the resource identity match across traces, metrics, logs, and profiles?
4. Is any instrumentation applied twice — a wrapped transport inside a wrapped
   client — producing duplicate spans and doubled counters?
5. Does an operation that can be cancelled accept a context and end its span on
   the cancellation path?

Last verified: 2026-08-05.
