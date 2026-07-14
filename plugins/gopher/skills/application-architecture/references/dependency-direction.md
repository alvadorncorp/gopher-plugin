# Dependency Direction

Define each rule as a machine-checkable pair. For example:

```yaml
source: internal/httpapi
may_depend_on: [internal/application]
must_not_depend_on: [internal/postgres]
reason: HTTP delivery calls application policy and does not own persistence.
check: go test ./internal/architecture -run TestHTTPAPIDependencies
```

Prefer dependencies from volatile mechanisms toward stable policy only when the
policy has a real independent contract. Keep data ownership explicit; shared
tables or schemas can invalidate an otherwise clean module graph. Cycles require
either a moved responsibility, an extracted stable contract, or evidence that
the proposed boundaries are false.
