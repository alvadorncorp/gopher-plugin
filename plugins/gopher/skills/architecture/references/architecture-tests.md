# Go Architecture Tests

Choose deterministic gates that match the rule:

- `go list -deps -json` or an adopted dependency tool for import direction;
- `go list ./...` for package/module discovery;
- compile-time interface assertions only for intentional contracts;
- tests that reject imports across protected `internal`/module boundaries;
- API compatibility tooling already adopted by the project;
- `go test ./...` after module or public-contract migration.

Document the prohibited edge, command, and expected result. A diagram without
an executable rule remains explanatory only.
