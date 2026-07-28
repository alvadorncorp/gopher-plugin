# Declared-Go-Version Guards

Resolve every recommendation against the target project's declared Go and
toolchain version in `go.mod`, never against the current stable release. A
technique whose guard the project does not meet is rejected with the guard
stated, not offered with a caveat.

## Guard table

| API or behavior | Available from | Consequence below the guard |
|---|---|---|
| `unsafe.Slice` | Go 1.17 | no supported slice reinterpretation |
| `GOMEMLIMIT` | Go 1.19 | only `GOGC` controls the heap target |
| `unsafe.String`, `unsafe.StringData`, `unsafe.SliceData` | Go 1.20 | zero-copy string conversion is unavailable |
| `slices.BinarySearchFunc`, `slices.DeleteFunc` | Go 1.21 | hand-written search and filter, with explicit tail clearing |
| Profile-guided optimization, generally available with `default.pgo` auto-detection | Go 1.21 (preview in 1.20) | no supported PGO build path |
| Automatic tail clearing in standard-library slice operations | Go 1.22 | clear pointer-containing tails manually to release referents |
| `testing.B.Loop` | Go 1.24 | keep the `b.N` benchmark form |
| `runtime/trace.FlightRecorder` | Go 1.25 | bounded direct trace capture only |
| `GOEXPERIMENT=greenteagc` | Go 1.25 | the experiment cannot be enabled; the previous collector is in use |
| Green Tea GC as the default | Go 1.26 | the previous collector is in use |

## Maintenance

This file is the single place to revisit per Go release. Green Tea GC became the
default in Go 1.26 with a temporary `GOEXPERIMENT=nogreenteagc` opt-out that is
expected to disappear in Go 1.27; its locality and scalability gains remain
workload- and hardware-dependent.

Sources: <https://pkg.go.dev/unsafe>, <https://pkg.go.dev/slices>,
<https://pkg.go.dev/testing#B>, <https://go.dev/doc/pgo>,
<https://go.dev/doc/gc-guide#Memory_limit>, <https://go.dev/doc/go1.26#runtime>,
<https://go.dev/blog/greenteagc>.
Last verified: 2026-07-28.
