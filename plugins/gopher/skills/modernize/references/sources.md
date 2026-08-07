# Version-sensitive sources

These references change with Go and tool releases. Confirm each against the
declared versions in the target project before relying on a detail here.

## Official references

- The `modernize` analysis pass (vendored into `go fix` since Go 1.26):
  https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize
- `go help fix`, `go tool fix help`, and `go tool fix help <analyzer>` —
  authoritative for the toolchain actually in hand: the analyzer roster and
  defaults are version-matched to it, unlike a pinned URL.
- Go release notes (for version-gated language and API features):
  https://go.dev/doc/devel/release
- Go modules reference (versioning, `go.mod`, `toolchain`):
  https://go.dev/ref/mod

## Review cadence

- Re-check which idioms and APIs are available whenever the declared Go version
  changes; a feature valid at one version may not compile at another.
- Re-check the analyzer roster with `go tool fix help` on every Go release;
  analyzers are added and defaults flip between releases.
- Keep the resolved target version and every tool version recorded with the
  result so a reviewer can reproduce the modernization exactly.
