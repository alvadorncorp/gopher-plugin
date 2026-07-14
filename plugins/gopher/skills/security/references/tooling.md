# Safe Security Tooling

Use tools already present in the project and tie each to a hypothesis:

| Tool | Use | Required limitation statement |
|---|---|---|
| `govulncheck` | vulnerable symbol reachability | build tags, reflection, cgo, and dynamic paths may limit visibility |
| `go test -fuzz` | parser/decoder invariant exploration | bounded local corpus/time and non-production targets |
| `go test -race` | executed shared-state paths | schedule coverage is incomplete |
| `go vet` / adopted lint/SAST | configured static checks | rule and build coverage varies |
| focused unit/integration test | safe exploit/control reproduction | test environment differs from deployment |

Record command, version, scope, result, and limitation. Tool absence becomes a
limitation or approval request. Automatic installation, production probing,
destructive payloads, and secret output remain outside authorized defaults.
