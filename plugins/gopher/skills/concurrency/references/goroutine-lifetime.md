# Goroutine Lifetime

## Lifetime record

For every goroutine, record:

```yaml
owner:
start_condition:
termination_conditions:
cancellation_source:
blocked_operations:
error_delivery:
join_or_drain:
```

Prefer synchronous code until concurrency provides measured latency/throughput
or required independent progress. Ensure every path terminates on success,
error, cancellation, and peer failure. A goroutine without an owner or bounded
termination is a leak hypothesis.

## Confirming a leak hypothesis

A Go 1.27 toolchain turns the hypothesis into evidence through the
`goroutineleak` profile, which uses garbage-collector reachability to identify
goroutines blocked on a channel, `sync.Mutex`, or `sync.Cond` that can never be
unblocked, and reports their stacks through `pprof.Lookup("goroutineleak")` or
`/debug/pprof/goroutineleak`, where `debug=2` renders them in unrecovered-panic
form.

The guard is the toolchain that builds the binary, not the declared version: a
module declaring `go 1.24` built with Go 1.27 has the profile.

Read the limits with the result. The profile finds goroutines that are *stuck
forever*, so it does not report a goroutine still looping, still waiting on a
live timer, or blocked on a primitive something could still reach. Those remain
leaks in the lifetime sense and still need the lifetime record above plus a
lifecycle test. An empty profile is not a clean bill. Below Go 1.27 the evidence
is the lifecycle-test delta in `references/diagnostics.md` or an adopted
leak-check helper.

## `time` channels are always unbuffered

The `asynctimerchan` GODEBUG was removed in Go 1.27, so channels created by the
`time` package are unbuffered on every supported setting. Code that pinned
`asynctimerchan=1` to keep the pre-1.23 asynchronous behavior no longer builds
on Go 1.27.

Record the pin in `limitations` as a blocking upgrade finding for
`gopher:modernize`, which owns the `go.mod` and `//go:debug` audit. What stays
here is the lifetime consequence: re-derive the drain, `Stop`, and `Reset`
termination paths that the asynchronous behavior was protecting, and put them in
the lifetime record.

Last verified: 2026-08-31 against a local go1.27.0 toolchain.
