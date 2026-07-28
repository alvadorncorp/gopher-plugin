# Concurrency Pattern Mappings

| General ID | Go mapping | Direct baseline and selection rule |
|---|---|---|
| `pattern.context-cancellation` | `go.context-cancellation` | synchronous call first; select when lifetime and cancellation cross calls |
| `pattern.pipeline` | `go.pipeline` | sequential loop first; select for measured independent stages with explicit backpressure |

For pipelines, specify stage ownership, channel direction, buffer rationale,
ordering, error and cancellation propagation, drain behavior, and fan-out and
fan-in bounds. A buffer size is a backpressure decision supported by burst
evidence, never a patch for a deadlock.

Object pooling maps in `gopher:performance`, because the decision rests on
allocation and GC evidence rather than on lifetime or synchronization.

Sources: <https://go.dev/blog/pipelines>, <https://pkg.go.dev/context>.
Last verified: 2026-07-28.
