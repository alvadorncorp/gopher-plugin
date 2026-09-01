# Profiles and Runtime Metrics

This file covers the exposure decision for profiles and runtime metrics, the
exposure surface it creates, the discovery rule for `runtime/metrics`, and the
profile-adjacent runtime knobs telemetry reports.

## The exposure decision

| Question | What the answer fixes |
|---|---|
| Which operational question needs a profile that a metric leaves open | Whether continuous collection earns its cost at all |
| Which profile kinds are collected | CPU, heap, goroutine, mutex, and block each carry a different overhead and a different enabling step |
| At what frequency and window | Sampling cost, artifact volume, and how often a transient event is caught |
| Where the artifacts are stored, and for how long | Storage cost and the exposure window of symbol data |
| Who may fetch a profile | An authorization boundary owned by `gopher:security` |
| What overhead was measured, not assumed | Whether the collection can run in production |

Mutex and block profiles stay inert until their sampling rates are enabled, so
"the endpoint is exposed" and "the profile has data" are separate states. Enable
a rate deliberately, since both add per-event cost on contended paths.

From Go 1.27 a sixth kind is generally available: `goroutineleak`, served at
`/debug/pprof/goroutineleak`, reporting stacks of goroutines the collector
proves can never be unblocked. It is computed during garbage collection rather
than sampled, so it carries no steady-state cost, and its content is the same
class of internal detail as a goroutine dump. Interpreting one is
`gopher:concurrency` work; deciding who may fetch it is not.

## Goroutine labels reach tracebacks from Go 1.27

The `tracebacklabels` GODEBUG arrived in Go 1.26 defaulting to off. Go 1.27
changes the default to on, so `runtime/pprof` goroutine labels appear in the
goroutine status header of runtime tracebacks and of `debug=2` stack dumps —
including the traceback printed by an unrecovered panic, which usually lands in
ordinary application logs.

This widens the blast radius of a label. A label chosen for profile
dimensionality now also becomes crash-log content, so a label carrying a tenant
id, an account identifier, or a request attribute changes what an incident log
contains. Go documents `tracebacklabels=0` as an opt-out expected to be kept
indefinitely for exactly this case.

Two consequences for signal design:

- Label keys and values fall under the redaction rules in
  `references/cardinality-cost-redaction.md`, not only the cardinality rules.
- A project that cannot redact its labels sets `tracebacklabels=0` deliberately
  and records why, rather than discovering the exposure from a log.

A continuous-profiling pipeline is a signal like any other: it needs a contract
in `references/signal-contracts.md`, a named consumer, a retention period, and a
cost line. A profiler running because it was easy to enable is cost without a
consumer.

## Exposure surface

`net/http/pprof` registers its handlers on the default multiplexer as an import
side effect. Two consequences follow:

- The endpoint set must be served on an interface reachable only by authorized
  operators, with the authorization decision owned by `gopher:security`.
- Profile artifacts expose internal package and function names, and a heap
  profile can reveal allocation shapes tied to customer workloads. Treat them as
  sensitive artifacts with a retention policy.

Capture windows stay bounded and aligned to the incident. An unbounded capture
inflates both artifact size and the memory needed to analyze it.

## Runtime metrics are discovered, not assumed

The `runtime/metrics` package exposes a versioned catalog: metric names, kinds,
and semantics change between Go releases, and names carry an explicit unit
suffix. The rule is discovery.

| Step | Action |
|---|---|
| Enumerate | Read the supported descriptions from the running toolchain rather than a hard-coded list |
| Filter | Keep the metrics whose descriptions exist for the declared Go version |
| Read | Sample the selected set through a single read call, reusing the sample slice |
| Guard | Treat an unsupported name as absent and report the gap, rather than exporting a zero |
| Re-check | Repeat the enumeration on every Go upgrade, since a name may be added, renamed, or removed |

A dashboard built on a runtime metric that the project's Go version does not
supply shows a flat zero, which reads as healthy. Discovery converts that silent
failure into an explicit limitation.

Telemetry modules that ship a runtime-instrumentation package follow the same
rule: the metric set they emit tracks both their own version and the Go version,
so resolve both before promising a panel.

## Profile-adjacent runtime knobs

| Knob | Observability position |
|---|---|
| `GOMAXPROCS` | Report the effective value as a resource attribute; changing it is a performance decision |
| `GOMEMLIMIT` | Report it alongside heap metrics so a limit-driven collection cycle is legible |
| `GOGC` | Same; a heap panel without the target is hard to read |
| Profile-guided optimization | Consumes collected profiles; the build decision belongs to `gopher:performance` |

Exporting the effective value of each knob as a resource attribute is
observability work. Choosing the value is not.

## Handoff

| Situation | Owner |
|---|---|
| Deciding to collect profiles continuously, at what cost, retention, and access | `gopher:observability` |
| Reading a captured profile to find the hot path or the retained allocation | `gopher:performance` |
| Authorizing who reaches the profiling endpoints | `gopher:security` |
| Attributing a specific incident to a change or component | `gopher:diagnose` |

Deliver the captured artifact together with the workload, Go version, capture
window, and sampling rate, so the receiving skill can reproduce the measurement.

Last verified: 2026-08-31 against a local go1.27.0 toolchain.
