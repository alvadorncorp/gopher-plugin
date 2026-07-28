# Concurrency Diagnostics

| Symptom | First safe evidence | Limit |
|---|---|---|
| Data race | targeted `go test -race` and shared-state trace | only executed schedules are covered |
| Deadlock/hang | goroutine dump, blocked stack, timeout reproduction | dump is a point-in-time view |
| Leak | repeated lifecycle test plus goroutine/profile delta | background runtime goroutines need filtering |
| Contention | mutex/block profile under representative load | profiling changes timing |
| Backpressure failure | queue depth, latency, drop/block metrics | synthetic load must match workload |

Keep at most three hypotheses. Use one discriminating probe at a time and
record the exact command, workload, environment, and observed result.
