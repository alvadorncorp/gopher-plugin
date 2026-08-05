# Version-sensitive sources

Native fuzzing entered the Go toolchain in Go 1.18. Flag behavior, corpus
handling, and minimization have continued to change since then. Confirm each
detail below against the toolchain the target project actually declares before
relying on it.

## Version gate

| Declared Go version | Recommendation |
|---|---|
| 1.18 and later | Native `testing.F` fuzzing is available; this skill applies as written |
| Below 1.18 | Report `BLOCKED` for a native campaign, and state the version as the reason |

The project's declared version in `go.mod`, together with any `toolchain`
directive, gates the recommendation. A newer local toolchain does not change
what the project supports; record the version that actually ran the campaign.

## Fuzzing documentation

- Go fuzzing reference: <https://go.dev/security/fuzz/>
- Go fuzzing landing page: <https://go.dev/doc/fuzz/>
- Fuzzing tutorial: <https://go.dev/doc/tutorial/fuzz>
- Fuzzing announcement and design notes: <https://go.dev/blog/fuzz-beta>
- Go 1.18 release notes, fuzzing: <https://go.dev/doc/go1.18#fuzzing>

## Testing API

- `testing.F`: <https://pkg.go.dev/testing#F>
- `testing.F.Add`: <https://pkg.go.dev/testing#F.Add>
- `testing.F.Fuzz`: <https://pkg.go.dev/testing#F.Fuzz>
- `testing.F.Skip`: <https://pkg.go.dev/testing#F.Skip>
- `testing.T`: <https://pkg.go.dev/testing#T>
- `testing` package overview: <https://pkg.go.dev/testing>

## Toolchain and flags

- `go test` testing flags: <https://pkg.go.dev/cmd/go#hdr-Testing_flags>
- `go test` command: <https://pkg.go.dev/cmd/go#hdr-Test_packages>
- `go clean` and `-fuzzcache`: <https://pkg.go.dev/cmd/go#hdr-Remove_object_files_and_cached_files>
- `go env` and `GOCACHE`: <https://pkg.go.dev/cmd/go#hdr-Print_Go_environment_information>
- Build and test caching: <https://pkg.go.dev/cmd/go#hdr-Build_and_test_caching>

## Related verification

- Race detector: <https://go.dev/doc/articles/race_detector>
- `go vet`: <https://pkg.go.dev/cmd/vet>
- `govulncheck`: <https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck>
- Go security policy and reporting: <https://go.dev/security/policy>

## Review cadence

- Re-read this file after every stable Go release. Flag semantics, corpus file
  format, and minimization behavior are toolchain details, and a release can
  change a recommendation that was accurate one version earlier.
- Record the Go version, the toolchain directive, the full command line, the
  budget, and the parallelism with every campaign result, so a later reader can
  reproduce both a `PASS` and a `CRASH`.
- Re-verify the corpus file format against the toolchain in use before relying
  on a hand-written seed file. A format change invalidates hand-written seeds
  while leaving engine-written seeds intact.
- When an official source renames or retires a flag, update the command shapes
  in `references/campaigns.md` and `references/triage.md` in the same change.

Last verified: 2026-08-05.
