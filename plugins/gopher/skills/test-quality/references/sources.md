# Version-sensitive sources

These references change with tool releases. Confirm each against the versions
installed in the target project before relying on a detail here.

## Official references

- Go coverage for whole programs and integration tests:
  https://go.dev/doc/build-cover
- Go command and `cover` tool: https://pkg.go.dev/cmd/go and
  https://pkg.go.dev/cmd/cover
- Gremlins mutation testing for Go: https://github.com/go-gremlins/gremlins

- `go test -json` event stream: <https://pkg.go.dev/cmd/test2json>

## Review cadence

- Re-check the coverage workflow and flags when the project upgrades the Go
  toolchain.
- Re-check mutation behavior and result-class names whenever the pinned mutation
  binary changes; a version change can rename or re-bucket outcomes.
- Because the mutation tool is pre-1.0, keep mutation advisory unless the project
  explicitly configures it as required, and record the exact version with every
  score.
