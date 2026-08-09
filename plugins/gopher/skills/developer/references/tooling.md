# Proportional Go Validation

Use commands already adopted by the project. Escalate by affected risk:

| Change | Minimum gate | Additional gate when justified |
|---|---|---|
| Local formatting/API implementation | `gofmt` + relevant package tests | `go vet` or adopted lint |
| Module/dependency change | relevant tests + `go mod tidy` diff review | full `go test ./...` |
| Shared-state/concurrency touch | relevant tests | `go test -race` for affected packages |
| Parser/decoder boundary | tests | targeted fuzz run |
| Performance claim | correctness tests | benchmark before/after + profile |
| Security-sensitive dependency/symbol | tests | adopted `govulncheck`/SAST |

For the focused baseline, first signal, green confirmation, refactor check, and
final validation, record the exact command, exit status, and concise observation
when a command runs. Give an explicit skip reason for every skipped or
non-applicable stage. Existing tool absence is a limitation or approval request,
never an implicit installation instruction.
