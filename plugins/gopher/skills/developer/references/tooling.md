# Proportional Go Validation

Before selecting a gate, complete `references/project-detection.md`. Use its
recorded config status, effective `idiom_policy` and `test_workflow`, declared Go
version, and discovered adopted commands and tooling. `ABSENT` and
`MIGRATION_AVAILABLE` use effective defaults without persisting them;
`INVALID` and `UNSUPPORTED_VERSION` permit read-only diagnosis only, block
production edits, and hand recovery to `gopher:config`. If command or policy
evidence is `unknown`, stop the affected gate and report the exact evidence or
owner decision required.

Use commands already adopted by the project. Apply every row whose change or
risk condition matches; when multiple rows match, run the union of their gates.
Escalate by affected risk:

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
in the parent workflow's evidence fields when a command runs. Give an explicit
skip reason for every skipped or non-applicable stage; record `command: not run`,
`observed: exit status: n/a`, and `reason: ...`. Existing tool absence is a
limitation or approval request, never an implicit installation instruction.
Run these stages in parent-workflow order; advance only after the current
stage's evidence is recorded, and run final validation after green confirmation
and any refactor check remain green.

At final validation, report files, behavior, validation evidence, limitations,
and any canonical handoff. A blocked prerequisite or required approval remains
`BLOCKED`; a non-blocking unavailable optional gate is `COMPLETE_WITH_LIMITATIONS`
with its limitation and handoff. Route config recovery to `gopher:config` and
other ownership or scope decisions to the owner named in `SKILL.md`.
