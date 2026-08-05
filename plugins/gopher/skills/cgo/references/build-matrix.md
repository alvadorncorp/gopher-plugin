# Build Matrix, Flags, and Linking

Enabling cgo turns the build into a C build. The Go toolchain alone stops being
sufficient; a target now needs a C compiler, target headers, and target
libraries. Enumerate the matrix explicitly.

## `CGO_ENABLED`

| Value | Effect |
|---|---|
| `1` | cgo files compile; a working C toolchain for the target is required |
| `0` | cgo files are excluded; only the pure-Go build path exists |

The default is `1` when building for the host and a C compiler is present, and
`0` when `GOOS` or `GOARCH` differs from the host. A build that silently drops
to `CGO_ENABLED=0` compiles a different program, so pin the value in the build
command rather than inheriting it.

Keep a pure-Go fallback compiling by guarding the two paths:

```go
//go:build cgo
//go:build !cgo
```

## Environment inputs

| Variable | Role |
|---|---|
| `CC`, `CXX` | The C and C++ compilers used for the target |
| `CGO_CFLAGS`, `CGO_CPPFLAGS`, `CGO_CXXFLAGS` | Compile flags added to every cgo compilation |
| `CGO_LDFLAGS` | Link flags added to the external link step |
| `CGO_CFLAGS_ALLOW`, `CGO_CFLAGS_DISALLOW` | Regular expressions gating which flags may come from `#cgo` directives and `pkg-config` |
| `PKG_CONFIG`, `PKG_CONFIG_PATH` | The `pkg-config` binary and its search path |

Flags that arrive from source or from `pkg-config` pass a security filter before
the toolchain accepts them. A rejected flag is reported as a disallowed flag, and
widening `CGO_CFLAGS_ALLOW` is an approval-gated decision, not a build fix.

## `#cgo` directives

Directives live in the preamble comment and accumulate across files in a
package:

```go
/*
#cgo CFLAGS: -I${SRCDIR}/vendor/include
#cgo linux LDFLAGS: -L${SRCDIR}/lib -lfoo -Wl,-rpath,$ORIGIN
#cgo darwin LDFLAGS: -framework CoreFoundation
#cgo linux,arm64 CFLAGS: -DFOO_NEON=1
#cgo pkg-config: libfoo >= 1.4
*/
import "C"
```

The space-separated words before the flag name are build constraints combined
with a logical AND, and separate directive lines combine with a logical OR.
`${SRCDIR}` expands to the package directory, which keeps a vendored path
relocatable. A `pkg-config` directive delegates flag discovery to the target's
`.pc` files, which means the build now depends on the target's development
packages being installed and discoverable.

## Static and dynamic linking

| Mode | Command shape | Consequence |
|---|---|---|
| Dynamic, internal linking | The default for simple cgo builds | The binary needs the shared libraries at run time |
| Dynamic, external linking | `-ldflags '-linkmode external'` | The system linker resolves symbols; required by some libraries |
| Fully static | `-ldflags '-linkmode external -extldflags "-static"'` | No run-time library dependency, subject to the caveat below |

Static linking against glibc keeps working for most code but leaves the
name-service switch resolving through `dlopen` at run time, so user lookups and
host resolution can fail in a container that lacks the matching libraries.
Building the pure-Go implementations with the `osusergo` and `netgo` tags, or
linking against a libc designed for static linking, removes that class of
failure. Record which choice the project made.

Verify the run-time dependencies of the produced binary with the inspection tool
the project already uses for its platform, and treat an unexpected shared
dependency as a build-matrix finding.

## Cross-compilation

`GOOS` and `GOARCH` select the Go target. With cgo enabled they do not select a
C toolchain, so a cross build additionally needs:

- A cross compiler for the target, set through `CC` and `CXX`.
- Target headers for every library in the preamble.
- Target libraries for the link step, and a sysroot when the compiler needs one.
- A matching `pkg-config` setup when directives use it.

```bash
CGO_ENABLED=1 GOOS=linux GOARCH=arm64 CC=aarch64-linux-gnu-gcc go build ./...
```

Without those pieces the build fails at the C compile or link step. This is the
convenience that cgo trades away: with `CGO_ENABLED=0` the same source
cross-compiles to every supported target from any host, and enabling cgo makes
each target a separate toolchain to provision.

Toolchains outside the project's contract are reported rather than installed.
State the exact requirement, for example the compiler triple, the library
version, and the sysroot, so the target becomes buildable by a deliberate
decision.

## Matrix table

Fill one row per shipped target. This table is the deliverable of the
`build-matrix` mode.

| `GOOS`/`GOARCH` | `CGO_ENABLED` | `CC` | Link mode | Libraries | Verified |
|---|---|---|---|---|---|
| | | | internal / external / static | | yes / unavailable |
