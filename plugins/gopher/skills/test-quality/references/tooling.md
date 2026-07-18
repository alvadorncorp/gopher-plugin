# Tool discovery

`[tools].mutation` governs mutation-tool selection; coverage uses the Go
toolchain directly. `auto` discovers an adopted or already-available tool and
never installs one.

## Coverage

- Always available through the Go toolchain: `go test -coverprofile` and
  `go tool cover`. No discovery is needed; record the Go version used.

## Mutation

1. An explicit command in `[tools].mutation` (used verbatim).
2. An already-available, pinned mutation binary declared or vendored by the
   project (for example a fixed Gremlins version).
3. Otherwise, report an explicit limitation — do not install a tool.

Record the mutation tool name and exact version with every run so the score is
reproducible.

## Degradation

- `off` disables mutation; report it as not run.
- An unavailable `auto` mutation tool is a limitation in `advisory` mode. In
  `required` mode it blocks the mutation dimension only, leaving coverage and
  effectiveness analysis intact.
