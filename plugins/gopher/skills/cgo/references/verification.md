# Verification

Verify with the tools the project has already adopted. Each entry below states
what a clean result proves and what it leaves untested, because a boundary
finding is only as strong as the coverage behind it. A tool the project does not
declare is reported as a limitation with its exact requirement.

## Tool coverage

| Tool | Proves | Leaves untested |
|---|---|---|
| `go build` with the target's `CC` | The preamble, headers, and link step resolve for that target | Every other target in the matrix |
| `go vet` | Static cgo findings, including a Go type with an embedded pointer passed to C through an `unsafe.Pointer` conversion | Anything the analyzer cannot see through a conversion or an indirection |
| `go test` | The boundary behaves as the tests exercise it | Inputs, sizes, and error paths no test covers |
| `go test -race` | Data races between Go accesses, on the schedules that executed | Races inside C code, and schedules that did not execute |
| `GODEBUG=cgocheck=1` (default) | Rule violations observable at the crossing | Pointer writes into C memory away from a crossing |
| `GOEXPERIMENT=cgocheck2` build | Go pointers stored into non-Go memory anywhere in the run | Paths the run did not execute; it also changes performance materially |
| `go build -asan` | C-side heap overflow, use-after-free, and double free on the executed paths | Uninstrumented libraries, and platforms where the mode is unsupported |
| `go build -msan` | Reads of uninitialized memory on the executed paths | Correctness of uninstrumented C, which produces false reports |
| `go build -x` | The exact compiler and linker invocations and their flags | Whether the resulting binary behaves correctly |
| `go tool cgo` | The generated bindings for inspection | Runtime behavior of those bindings |

## Race detection at the boundary

The race detector instruments Go memory accesses. C code compiled without
`-fsanitize=thread` is invisible to it, so a clean run says nothing about a race
between two C threads or between C code and Go code through a shared buffer.
Report that bound with every clean result, and state which schedules the run
covered.

The detector needs cgo enabled on most platforms, so a `CGO_ENABLED=0` build
cannot be race-tested. That makes a pure-Go fallback path a separate
verification question from the cgo path.

## Sanitizers

`-asan` and `-msan` require a supported compiler and a supported
platform-architecture pair; both are considerably narrower than the full Go
target list. Confirm support for the specific target before recommending them,
and treat an unsupported combination as a limitation rather than as a gap in the
boundary.

`-msan` reports uninitialized reads only when every C translation unit in the
link is instrumented. A prebuilt system library in the link produces reports
that are artifacts of the missing instrumentation. Either instrument the whole
dependency chain or record `-msan` as unavailable for that boundary.

A sanitizer confirms nothing about a path it did not execute. Pair a sanitizer
run with the tests or the workload that exercises the crossing under audit, and
name that workload in the result.

## `cgocheck` levels

The default level runs on every cgo call and is inexpensive enough to leave on
everywhere, including production. The stronger mode checks every pointer write in
the program and costs enough that it belongs in a dedicated verification build.
Its form is version-dependent: a build experiment from Go 1.21 onward, and a
`GODEBUG` value before that, so confirm against the project's declared Go
version.

A detection from either level is a defect in ownership or lifetime. The result to
record is the message, the crossing it names, and the ownership or lifetime
change that resolves it.

## Linker and dependency inspection

`go build -x` prints the compile and link commands, which answers what the
build actually passed to the C toolchain when a `#cgo` directive, a
`pkg-config` result, or an environment variable is in doubt. Combine it with
`go env` to see the effective cgo variables for the target.

Inspect the produced binary's run-time dependencies with the platform tool the
project already uses, and compare the result against the intended link mode. An
unexpected shared dependency in a build intended to be static is a build-matrix
finding.

## Reporting a result

Every verification entry in the output bundle carries:

- The exact command, including `GOOS`, `GOARCH`, `CGO_ENABLED`, `CC`, and the
  Go version.
- The workload or test set that executed.
- What the clean or failing result proves.
- What it leaves untested, in the terms of the table above.
