# Profiling and Runtime Evidence

Capture exactly one profile per hypothesis, under the same workload as the
benchmark that established magnitude.

## Selecting the view

| Question | Profile |
|---|---|
| Which call path burns on-CPU time? | `cpu` |
| Where does allocation volume come from? | `allocs` |
| What memory stays live? | heap `inuse_space` and `inuse_objects` |
| Which lock is contended? | `mutex` |
| Where does the code block? | `block` |
| How many goroutines exist right now? | `goroutine` (point-in-time handoff evidence for `gopher:concurrency`) |

## Capture from a benchmark

```bash
go test -run '^$' -bench 'BenchmarkTarget' -benchmem \
  -cpuprofile cpu.out ./pkg
go test -run '^$' -bench 'BenchmarkTarget' -benchmem \
  -memprofile mem.out -memprofilerate 1 ./pkg
go tool pprof -top -nodecount 20 cpu.out
go tool pprof -sample_index=alloc_space -top mem.out
go tool pprof -sample_index=inuse_space -top mem.out
```

Block and mutex profiles need their sampling rates enabled first, through
`runtime.SetBlockProfileRate` and `runtime.SetMutexProfileFraction`, or through
the `-blockprofile` and `-mutexprofile` test flags.

## Capture from a running service

```bash
go tool pprof http://<host>/debug/pprof/profile?seconds=30
go tool pprof http://<host>/debug/pprof/allocs
go tool pprof http://<host>/debug/pprof/heap
```

Importing `net/http/pprof` exposes these endpoints. Deciding that a service
exposes them continuously, at what cost and retention, is `gopher:observability`;
who may reach them is `gopher:security`; this skill reads what an authorized
capture produced. Production capture requires explicit authorization, a bounded
collection window, and a plan for the artifact.

## Execution traces

Capture a trace only for a latency, scheduling, utilization, syscall or network
wait, blocking, or GC-timeline question. Official Go diagnostics states a trace
is not the preferred tool for CPU or memory hot spots.

```bash
go test -run '^$' -bench 'BenchmarkTarget' -trace trace.out ./pkg
go tool trace trace.out
go tool trace -pprof=sched trace.out > sched.pprof
```

`go tool trace` can derive `net`, `sync`, `syscall`, and `sched` profiles from
the capture. Modern tracing costs roughly 1 to 2 percent CPU for many
applications, but capture size and analysis memory still grow with duration, so
keep captures bounded and aligned to the incident. A project on Go 1.25 or newer
may use `runtime/trace.FlightRecorder` for an intermittent symptom; an older
declared version needs a bounded direct capture.

From Go 1.27, `-http` with only a port listens on localhost alone. Reaching the
viewer from another host takes an explicit unspecified address:

```bash
go tool trace -http=:6060 trace.out        # localhost only, from Go 1.27
go tool trace -http=0.0.0.0:6060 trace.out # reachable off-box, and an exposure decision
```

## Leaked goroutines

From Go 1.27 the `goroutineleak` profile is generally available in
`runtime/pprof` and at `/debug/pprof/goroutineleak`, reporting stack traces of
goroutines the garbage collector proves cannot be unblocked. It answers "which
goroutines are stuck", not "why they are stuck", and the diagnosis belongs to
`gopher:concurrency`. Its exposure is a decision owned by `gopher:security` like
any other pprof endpoint.

## Symbols do not survive a toolchain upgrade

Go 1.27 generates simpler, inlining-independent names for function literals and
may share code between instances of one literal. Closure frames therefore do not
line up between a Go 1.26 profile and a Go 1.27 profile. Compare profiles across
a toolchain change only after recapturing the baseline.

## Limits to report

- Profiles are sampled or point-in-time views, not exact event counts.
- A profile shows correlation, not causality.
- Diagnostics interfere: precise memory profiling can skew a CPU profile, and
  block profiling can affect a scheduler trace. Capture one at a time.

Sources: <https://pkg.go.dev/runtime/pprof>, <https://pkg.go.dev/net/http/pprof>,
<https://pkg.go.dev/runtime/trace>, <https://go.dev/cmd/trace/>,
<https://go.dev/doc/diagnostics>,
<https://go.dev/blog/execution-traces-2024>,
<https://go.dev/doc/go1.27>.
Last verified: 2026-08-31 against a local go1.27.0 toolchain.
