# Generation Inventory

Discover every surface that produces checked-in Go source before judging any
artifact. An artifact with no discoverable producer is itself a finding.

## Surfaces and discovery

| Surface | Signal | Discovery command |
|---|---|---|
| `go:generate` directives | `//go:generate` at column zero in a `.go` file | `grep -rn '^//go:generate' --include='*.go' .` |
| Declared command set | The commands `go generate` would run | `go generate -n ./...` |
| Build-tag-guarded generators | `//go:build ignore` or `//go:build tools` | `grep -rn '//go:build \(ignore\|tools\)' --include='*.go' .` |
| Pinned tool dependencies | `tool` directives in `go.mod` (Go 1.24 and newer) | `grep -n '^\s*tool ' go.mod` and `go tool` |
| Legacy `tools.go` pattern | Blank imports under a `tools` build tag | `grep -rln 'go:build tools' --include='*.go' .` |
| Make and script targets | `generate`, `proto`, `mocks`, `wire`, `sqlc` targets | `grep -n '^[A-Za-z0-9_.-]*:' Makefile` |
| Generator registries | `buf.gen.yaml`, `sqlc.yaml`, `.mockery.yaml`, `gqlgen.yml`, `oapi-codegen` config, `ent` schema dirs | `ls` the repository root and `grep -rn 'gen' --include='*.y*ml' .` |
| Generated artifacts themselves | The code generation header | `grep -rln '^// Code generated .* DO NOT EDIT\.$' --include='*.go' .` |

Reconcile the two ends: every artifact carrying the header should trace back to
a producer, and every producer should account for its artifacts. A header with
no producer, or a producer with no artifact, is a limitation worth reporting.

## `go:generate` directive syntax

The directive is a line comment that the Go toolchain treats specially:

```go
//go:generate command argument...
```

The precise requirements are:

- The line begins at column zero, with no space between `//` and `go:generate`.
- The line is a comment inside a Go source file; it may appear anywhere in the
  file, and multiple directives run in file order.
- `go generate` runs directives only when invoked directly. It never runs as
  part of `go build`, `go test`, or module loading, so a checked-in artifact can
  drift silently until something reproduces it.
- `//go:generate -command alias name args...` defines a shorthand used by later
  directives in the same file.

The toolchain expands a fixed set of variables inside a directive: `$GOARCH`,
`$GOOS`, `$GOFILE`, `$GOLINE`, `$GOPACKAGE`, `$GOROOT`, `$DOLLAR`, and `$PATH`.
Record any expanded value that reaches the output, because it becomes part of
the artifact's provenance.

Useful read-only flags:

| Flag | Effect |
|---|---|
| `-n` | Print the commands without running them |
| `-x` | Print each command as it runs |
| `-run <regexp>` | Run only directives whose command line matches |
| `-skip <regexp>` | Skip directives whose command line matches |

`go generate -n ./...` is the safest first call: it enumerates the effective
command set for the whole module without executing anything.

## The tools patterns

Two patterns pin generator binaries to the module graph:

- The `tool` directive in `go.mod`, managed with `go get -tool <module>` and
  invoked with `go tool <name>`. This is the current mechanism from Go 1.24 on.
- The older `tools.go` file, guarded by `//go:build tools`, holding blank
  imports of generator packages so the module graph keeps their versions.

A generator that appears in neither, and is instead expected on `PATH`, is
unpinned. Record it as unpinned rather than resolving whatever binary happens to
be installed on the current machine.

## Recording the inventory

For each discovered generator, record the producer, the artifacts it claims, the
declaring surface, and the pin state:

| Field | Example |
|---|---|
| `generator` | `golang.org/x/tools/cmd/stringer` |
| `declared_in` | `internal/pill/pill.go:12` |
| `command` | `stringer -type=Pill` |
| `artifacts` | `internal/pill/pill_string.go` |
| `pin_state` | `pinned` via `tool` directive, or `unpinned` |

Carry this table into `references/provenance.md`, which turns each row into a
reproducible record.
