# Version-sensitive sources

The cgo contract changes with Go releases, with the C toolchain, and with the
target platform. Confirm each reference against the toolchain the target project
actually declares before relying on a detail here.

## cgo core

- cgo command documentation: <https://pkg.go.dev/cmd/cgo>
- cgo introduction: <https://go.dev/blog/cgo>
- C to Go calls and `//export`: <https://pkg.go.dev/cmd/cgo#hdr-C_references_to_Go>
- `#cgo` directives and build constraints: <https://pkg.go.dev/cmd/cgo#hdr-Using_cgo_with_the_go_command>
- Pointer-passing rules: <https://pkg.go.dev/cmd/cgo#hdr-Passing_pointers>
- Special cases and unsupported constructs: <https://pkg.go.dev/cmd/cgo#hdr-Go_references_to_C>

## Runtime and unsafe

- `runtime.Pinner`: <https://pkg.go.dev/runtime#Pinner>
- `runtime/cgo.Handle`: <https://pkg.go.dev/runtime/cgo#Handle>
- `runtime.LockOSThread`: <https://pkg.go.dev/runtime#LockOSThread>
- `runtime.KeepAlive`: <https://pkg.go.dev/runtime#KeepAlive>
- `runtime.SetFinalizer`: <https://pkg.go.dev/runtime#SetFinalizer>
- `runtime.AddCleanup`: <https://pkg.go.dev/runtime#AddCleanup>
- `runtime.SetCgoTraceback`: <https://pkg.go.dev/runtime#SetCgoTraceback>
- `runtime/debug.SetMaxThreads`: <https://pkg.go.dev/runtime/debug#SetMaxThreads>
- `unsafe`: <https://pkg.go.dev/unsafe>
- `unsafe.Slice`: <https://pkg.go.dev/unsafe#Slice>

## Build, environment, and signals

- Environment variables including the `CGO_*` set: <https://pkg.go.dev/cmd/go#hdr-Environment_variables>
- Build constraints: <https://pkg.go.dev/cmd/go#hdr-Build_constraints>
- `GODEBUG` settings: <https://go.dev/doc/godebug>
- Signals in programs that use cgo: <https://pkg.go.dev/os/signal#hdr-Go_programs_that_use_cgo_or_SWIG>
- Diagnostics overview: <https://go.dev/doc/diagnostics>
- Race detector: <https://go.dev/doc/articles/race_detector>

## Version gates

The project's declared Go version gates what may be recommended. Read the
version from the project before proposing a mechanism.

| Mechanism | Available from | Consequence when the project is older |
|---|---|---|
| `unsafe.Slice` over a C pointer | Go 1.17 | Use the array-cast conversion idiom instead |
| `runtime/cgo.Handle` | Go 1.17 | Carry identity through a project-owned registry keyed by an integer |
| `-asan` build mode | Go 1.18 | Rely on the C toolchain's own sanitizer builds outside the Go build |
| `GOEXPERIMENT=cgocheck2` | Go 1.21 | The stronger check is selected with `GODEBUG=cgocheck=2` instead |
| `runtime.Pinner` | Go 1.21 | Copy into C memory or use a handle; pinning is unavailable |
| `runtime.AddCleanup` | Go 1.24 | `runtime.SetFinalizer` remains the backstop, with its hazards |
| Linker `-macos` and `-macsdk` | Go 1.27 | Record the toolchain's observed defaults and report a required deployment target as a limitation; the values are not selectable per build |

## Review cadence

- Re-read the pointer-passing section of the cgo documentation after every
  stable Go release. The rules have gained mechanisms such as pinning, and the
  detection wording changes with them.
- Re-check the sanitizer platform support list per release; the supported
  platform-architecture pairs move.
- Record the Go version, `GOOS`, `GOARCH`, `CGO_ENABLED`, `CC`, and the C
  library versions with every verification result, plus the recorded macOS OS
  and SDK versions for a darwin target, so a later reviewer can reproduce it.
- Re-check the build matrix whenever a target, a compiler, or a linked library
  version changes, because each of those changes the ABI the boundary assumes.

Last verified: 2026-08-31 against a local go1.27.0 toolchain, except the
macOS default OS and SDK versions in `references/build-matrix.md`, which are
release-note documented and not toolchain-observed.
