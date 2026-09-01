# Version-sensitive sources

These references change with Go and tool releases. Confirm each against the
declared versions in the target project before relying on a detail here.

## Official references

- `go help fix`, `go tool fix help`, and `go tool fix help <analyzer>` —
  authoritative for the toolchain actually in hand, and the source this skill
  uses for the roster. The analyzer set and defaults are version-matched to the
  installed toolchain, unlike any pinned URL.
- The `modernize` analysis pass in `x/tools`:
  https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize
  It documents a **larger** set than the in-toolchain `go fix` registers, and
  it disagrees with the shipped tool on which analyzers exist and which are
  enabled. Treat it as background on the rewrites, never as the roster.
- Go release notes (for version-gated language and API features):
  https://go.dev/doc/devel/release, most recently
  https://go.dev/doc/go1.27
- `GODEBUG` history, including removed settings and the version that removed
  them: https://go.dev/doc/godebug
- Go modules reference (versioning, `go.mod`, `toolchain`):
  https://go.dev/ref/mod

## Review cadence

- Re-check which idioms and APIs are available whenever the declared Go version
  changes; a feature valid at one version may not compile at another.
- Re-check the analyzer roster with `go tool fix help` on every Go release.
  Analyzers are added, removed, and renamed between releases — Go 1.27 did all
  three — and a pinned command naming a withdrawn analyzer fails outright.
- Keep the resolved target version and every tool version recorded with the
  result so a reviewer can reproduce the modernization exactly.
