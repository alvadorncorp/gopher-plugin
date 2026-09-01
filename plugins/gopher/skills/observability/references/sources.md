# Version-sensitive sources

Telemetry advice ages faster than the Go standard library. The Go release, the
OpenTelemetry API and SDK modules, the instrumentation modules, and the semantic
conventions all version independently. Resolve each against the target project
before relying on a detail here.

## The semantic-convention warning

OpenTelemetry semantic conventions are versioned, and the Go module encodes that
version in its import path (`.../semconv/v1.X.Y`). A convention can change
between releases, and an attribute can move between experimental and stable
status, be renamed, or be replaced. Two consequences:

- Resolve the semantic-convention version the project imports before
  recommending an attribute or metric name. A name that is correct in one
  version is absent in another.
- Report the stability of each attribute used. An experimental attribute may
  change in a later convention release, which is a `COMPLETE_WITH_LIMITATIONS`
  condition rather than a silent assumption.

Pin one convention version per service and migrate deliberately. Mixing versions
in one process produces two names for the same measurement, and dashboards see
a metric that halves.

## Go standard library

- `log/slog`: <https://pkg.go.dev/log/slog>
- `slog.Handler` contract: <https://pkg.go.dev/log/slog#Handler>
- Structured logging guide: <https://go.dev/blog/slog>
- Handler writing guide: <https://github.com/golang/example/blob/master/slog-handler-guide/README.md>
- `testing/slogtest`: <https://pkg.go.dev/testing/slogtest>
- `context`: <https://pkg.go.dev/context>
- `runtime/metrics`: <https://pkg.go.dev/runtime/metrics>
- `runtime/pprof`: <https://pkg.go.dev/runtime/pprof>
- `net/http/pprof`: <https://pkg.go.dev/net/http/pprof>
- `GODEBUG` history, including `tracebacklabels`: <https://go.dev/doc/godebug>
- `expvar`: <https://pkg.go.dev/expvar>
- Go diagnostics overview: <https://go.dev/doc/diagnostics>

## OpenTelemetry

- Go documentation: <https://opentelemetry.io/docs/languages/go/>
- API and SDK modules: <https://pkg.go.dev/go.opentelemetry.io/otel>
- Trace API: <https://pkg.go.dev/go.opentelemetry.io/otel/trace>
- Metric API: <https://pkg.go.dev/go.opentelemetry.io/otel/metric>
- Trace SDK and test recorders: <https://pkg.go.dev/go.opentelemetry.io/otel/sdk/trace/tracetest>
- Metric SDK readers: <https://pkg.go.dev/go.opentelemetry.io/otel/sdk/metric>
- Instrumentation modules: <https://pkg.go.dev/go.opentelemetry.io/contrib>
- Semantic conventions: <https://opentelemetry.io/docs/specs/semconv/>
- Specification status and stability: <https://opentelemetry.io/docs/specs/otel/versioning-and-stability/>
- OTLP protocol: <https://opentelemetry.io/docs/specs/otlp/>

## Propagation

- W3C Trace Context: <https://www.w3.org/TR/trace-context/>
- W3C Baggage: <https://www.w3.org/TR/baggage/>
- Propagator configuration: <https://opentelemetry.io/docs/languages/go/instrumentation/#propagators-and-context>

## Prometheus

- Metric and label naming: <https://prometheus.io/docs/practices/naming/>
- Instrumentation practices: <https://prometheus.io/docs/practices/instrumentation/>
- Histograms and summaries: <https://prometheus.io/docs/practices/histograms/>
- Alerting practices: <https://prometheus.io/docs/practices/alerting/>
- Go client library: <https://pkg.go.dev/github.com/prometheus/client_golang/prometheus>
- Test helpers: <https://pkg.go.dev/github.com/prometheus/client_golang/prometheus/testutil>
- Cardinality guidance: <https://prometheus.io/docs/practices/naming/#labels>

## Review cadence

- Re-resolve the Go version, the telemetry module versions, and the
  semantic-convention version at the start of every engagement; a recommendation
  that was correct one release earlier can be absent in the version in use.
- Re-run runtime-metric discovery after every Go upgrade, since names can be
  added, renamed, or removed between releases.
- Re-check instrumentation modules after each release for superseded entry
  points, since middleware and interceptor forms are replaced over time.
- Re-read the alerting and coverage review in `references/dashboards-alerts.md`
  each quarter, and retire signals whose consumers disappeared.
- Record the resolved versions with every recommendation so a later reviewer can
  tell whether the advice still applies.

Last verified: 2026-08-31.
