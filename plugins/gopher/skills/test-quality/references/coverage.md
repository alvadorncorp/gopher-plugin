# Coverage

Measure coverage with the Go toolchain's supported profile workflow. Report
both package coverage and coverage of the relevant scope for the current change.

## Workflow

1. Collect a profile: `go test -coverprofile=<file> <packages>`.
2. Summarize: `go tool cover -func=<file>` for per-function and total numbers;
   `go tool cover -html=<file>` when a reviewer wants line-level detail.
3. Scope the report to the packages the change touches, and separately to the
   whole configured scope, so a small change is not judged only by a repo-wide
   number.

## Targets and regression

- Compare package and scope coverage against `test-quality.coverage_target`.
- Apply `test-quality.coverage_regression_max` as the allowed drop versus the
  recorded baseline. A default of `0` means coverage of the measured scope must
  not fall.
- A legacy package below target does not automatically fail when the measured
  scope maintains or improves its baseline.

## Integration and build tags

For binaries and integration tests, use the Go coverage workflow for whole
programs so integration paths are counted, not only unit tests. See
`references/sources.md`.
