# Goroutine Lifetime

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

On Go 1.27 and newer the `goroutineleak` profile turns the hypothesis into
evidence. The runtime uses garbage-collector reachability to identify goroutines
blocked on a channel, `sync.Mutex`, or `sync.Cond` that can never be unblocked,
and reports their stacks:

```go
pprof.Lookup("goroutineleak").WriteTo(w, 1)
```

It is also served at `/debug/pprof/goroutineleak`, with `debug=2` rendering the
stacks in unrecovered-panic form.

Read the limits with the result. The profile finds goroutines that are *stuck
forever*, so it does not report a goroutine still looping, still waiting on a
live timer, or blocked on a primitive something could still reach. Those remain
leaks in the lifetime sense and still need the record above plus a lifecycle
test. Below Go 1.27 the evidence is a goroutine-count delta across a repeated
lifecycle test or an adopted leak-check helper.

## `time` channels are always unbuffered

The `asynctimerchan` GODEBUG was removed in Go 1.27, so channels created by the
`time` package are unbuffered on every supported setting. Code that pinned
`asynctimerchan=1` to keep the pre-1.23 asynchronous behavior no longer builds
on Go 1.27 — the pin is a blocking upgrade finding owned by `gopher:modernize`,
and the timer-drain logic it protected is a lifetime question for this skill.
