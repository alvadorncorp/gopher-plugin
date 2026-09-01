# Declared-Go-Version Guards

Resolve every recommendation against the target project's versions, never
against the current stable release. A technique whose guard the project does not
meet is rejected with the guard stated, not offered with a caveat.

Two different guards apply, and confusing them rejects working techniques:

- **Declared version** — the `go` directive in `go.mod` (and `toolchain` when
  present). It gates anything the source must name: a standard-library symbol, a
  language feature, an import. The compiler enforces it, so a violation fails
  the build rather than reaching review.
- **Active toolchain** — the version that builds the binary, from `go version`.
  It gates runtime, garbage-collector, compiler-output, and profile behavior,
  none of which the source names. A module declaring an older version still gets
  this behavior when a newer toolchain builds it.

State which guard a recommendation was resolved against whenever the two differ.

## Declared-version guards

The source names the API, so the declared version is the ceiling.

| API | Available from | Consequence below the guard |
|---|---|---|
| `unsafe.Slice` | Go 1.17 | no supported slice reinterpretation |
| `unsafe.String`, `unsafe.StringData`, `unsafe.SliceData` | Go 1.20 | zero-copy string conversion is unavailable |
| `slices.BinarySearchFunc`, `slices.DeleteFunc` | Go 1.21 | hand-written search and filter, with explicit tail clearing |
| `testing.B.Loop` | Go 1.24 | keep the `b.N` benchmark form |
| `runtime/trace.FlightRecorder` | Go 1.25 | bounded direct trace capture only |
| `encoding/json/v2` and `encoding/json/jsontext` | Go 1.27 | `encoding/json` v1 only, with its own decode cost |
| `hash/maphash.Hasher` and `ComparableHasher` | Go 1.27 | hand-rolled hash and equality contract per structure |
| `simd` and `simd/archsimd`, which also need `GOEXPERIMENT=simd` at build time | Go 1.26 for amd64; Go 1.27 revises amd64 and adds arm64 Neon and wasm 128-bit | no portable vector API; hand-written assembly or nothing |

## Active-toolchain guards

The source names nothing, so the building toolchain decides. Read it from
`go version`, not from `go.mod`.

| Behavior | Available from | Consequence below the guard |
|---|---|---|
| `GOMEMLIMIT` | Go 1.19 | only `GOGC` controls the heap target |
| Profile-guided optimization, generally available with `default.pgo` auto-detection | Go 1.21 (preview in 1.20) | no supported PGO build path |
| Automatic tail clearing in standard-library slice operations | Go 1.22 | clear pointer-containing tails manually to release referents |
| `GOEXPERIMENT=greenteagc` | Go 1.25 | the experiment cannot be enabled; the previous collector is in use |
| Green Tea GC as the default | Go 1.26 | the previous collector is in use |
| `goroutineleak` profile in `runtime/pprof` and `net/http/pprof` | Go 1.27 (experiment in 1.26) | leak evidence comes from a lifecycle test or goroutine-count delta only |
| Size-specialized allocation as the default | Go 1.27 | small allocations take the general path |

A module declaring `go 1.24` built with a Go 1.27 toolchain does get the
`goroutineleak` profile. Rejecting it on the declared version is the error this
split exists to prevent.

The one Go 1.27 behavior that keys off the *declared* version instead is the
`tracebacklabels` default, because a GODEBUG default is selected by the `go`
directive. `gopher:observability` owns it.

## Go 1.27 shifts worth measuring on the path under analysis

Measure the shift that touches the code being analyzed; the rest are context.

- **Size-specialized allocation.** The compiler emits size-specialized
  allocation routines, cutting the cost of small allocations (under 80 bytes)
  by up to 30% and moving allocation-heavy programs about 1%, for roughly 60 KB
  of extra binary. The gain needs no code change, so on a Go 1.27 build it is
  already in the baseline.
- **`encoding/json` v1 is backed by v2.** Marshal and unmarshal behavior is
  preserved and unmarshal is materially faster, but error strings differ. A
  decode-bound profile taken on Go 1.26 does not predict the same profile on
  1.27.
- **`compress/flate` compresses faster and its encoded output can differ from
  Go 1.26.** Size and ratio baselines captured before the upgrade are not
  comparable across it (`references/benchmarking.md`).
- **Symbol names for closures changed.** The compiler generates simpler,
  inlining-independent names for function literals and may share code between
  instances, so profile symbols for closures do not line up across the 1.26 to
  1.27 boundary.

`GOEXPERIMENT=nosizespecializedmalloc` and `GOEXPERIMENT=nojsonv2` restore the
previous behavior. Each exists to bisect a suspected regression, which is what
an experiment knob is for; neither is a setting to ship.

## Maintenance

This file is the single place to revisit per Go release.

Verify an opt-out against the toolchain in hand before recording it as gone. The
`GOEXPERIMENT=nogreenteagc` opt-out was expected to disappear in Go 1.27 and did
not — `GOEXPERIMENT=nogreenteagc go env GOEXPERIMENT` still echoes it back. A
removal forecast in a release note is not a removal.

Past the newest row verified here, report a guard as unverified for that release
rather than assuming the behavior continues.

Sources: <https://pkg.go.dev/unsafe>, <https://pkg.go.dev/slices>,
<https://pkg.go.dev/testing#B>, <https://go.dev/doc/pgo>,
<https://go.dev/doc/gc-guide#Memory_limit>, <https://go.dev/doc/go1.26#runtime>,
<https://go.dev/doc/go1.27>, <https://go.dev/blog/greenteagc>.
Last verified: 2026-08-31 against a local go1.27.0 toolchain.
