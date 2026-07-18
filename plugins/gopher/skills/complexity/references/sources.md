# Version-sensitive sources

These references change with tool releases. Confirm each against the versions
actually installed in the target project before relying on a detail here.

## Official references

- GolangCI-Lint complexity linters and configuration:
  https://golangci-lint.run/docs/linters/configuration/
- Go command and tooling documentation: https://pkg.go.dev/cmd/go
- Go analysis passes (for analyzer behavior and flags):
  https://pkg.go.dev/golang.org/x/tools/go/analysis

## Review cadence

- Re-check the selected analyzer's metric definitions and flags whenever the
  project upgrades the analyzer or the Go toolchain; a version change can shift
  a metric's meaning.
- Keep the pinned analyzer and configuration recorded with each measurement so a
  later reviewer can reproduce it.
- When an official tool deprecates or renames a metric, update the pin and
  restate the baseline before comparing.
