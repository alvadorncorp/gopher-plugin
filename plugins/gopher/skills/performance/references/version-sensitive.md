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
| `goroutineleak` profile in `runtime/pprof` and `net/http/pprof` | Go 1.27 (experiment in 1.26) | leak evidence comes from a lifecycle test or goroutine-count delta only |
| Size-specialized allocation as the default | Go 1.27 | small allocations take the general path; no opt-out to reason about |
| `encoding/json/v2` and `encoding/json/jsontext` | Go 1.27 | `encoding/json` v1 only, with its own decode cost |
| `hash/maphash.Hasher` and `ComparableHasher` | Go 1.27 | hand-rolled hash and equality contract per structure |
| `simd` and `simd/archsimd` under `GOEXPERIMENT=simd` | Go 1.26 for amd64; Go 1.27 revises amd64 and adds arm64 Neon and wasm 128-bit | no portable vector API; hand-written assembly or nothing |

## Go 1.27 runtime and library shifts worth measuring

- **Size-specialized allocation.** The compiler emits size-specialized
  allocation routines, cutting the cost of small allocations (under 80 bytes)
  by up to 30% and moving allocation-heavy programs about 1%, for roughly 60 KB
  of extra binary. `GOEXPERIMENT=nosizespecializedmalloc` restores the previous
  path and is expected to be removed in Go 1.28, so treat it as a bisection
  tool for a regression, not a setting to ship.
- **`encoding/json` v1 is backed by v2.** Marshal and unmarshal behavior is
  preserved and unmarshal is materially faster, but error strings differ.
  `GOEXPERIMENT=nojsonv2` restores the v1 implementation and is likewise a
  bisection tool. A decode-bound profile taken on Go 1.26 does not predict the
  same profile on 1.27.
- **`compress/flate` compresses faster and its encoded output can differ from
  Go 1.26.** Size and ratio baselines captured before the upgrade are not
  comparable across it (`references/benchmarking.md`).
- **Symbol names for closures changed.** The compiler generates simpler,
  inlining-independent names for function literals and may share code between
  instances, so profile symbols for closures do not line up across the 1.26 to
  1.27 boundary.

## Maintenance

This file is the single place to revisit per Go release.

Green Tea GC became the default in Go 1.26; its locality and scalability gains
remain workload- and hardware-dependent. The `GOEXPERIMENT=nogreenteagc`
opt-out was expected to disappear in Go 1.27 and **did not** — the Go 1.27
toolchain still accepts it (`GOEXPERIMENT=nogreenteagc go env GOEXPERIMENT`
echoes it back). Verify an opt-out against the toolchain in hand before
recording it as gone; a removal forecast in a release note is not a removal.

Sources: <https://pkg.go.dev/unsafe>, <https://pkg.go.dev/slices>,
<https://pkg.go.dev/testing#B>, <https://go.dev/doc/pgo>,
<https://go.dev/doc/gc-guide#Memory_limit>, <https://go.dev/doc/go1.26#runtime>,
<https://go.dev/doc/go1.27>, <https://go.dev/blog/greenteagc>.
Last verified: 2026-08-31 against a local go1.27.0 toolchain.
