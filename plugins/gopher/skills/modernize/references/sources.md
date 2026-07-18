# Version-sensitive sources

These references change with Go and tool releases. Confirm each against the
declared versions in the target project before relying on a detail here.

## Official references

- The `modernize` analysis pass:
  https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize
- Go release notes (for version-gated language and API features):
  https://go.dev/doc/devel/release
- Go modules reference (versioning, `go.mod`, `toolchain`):
  https://go.dev/ref/mod

## Review cadence

- Re-check which idioms and APIs are available whenever the declared Go version
  changes; a feature valid at one version may not compile at another.
- Re-check the `modernize` pass's proposed rewrites whenever its version changes.
- Keep the resolved target version and every tool version recorded with the
  result so a reviewer can reproduce the modernization exactly.
