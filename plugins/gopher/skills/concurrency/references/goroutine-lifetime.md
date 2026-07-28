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
