# Go Project Detection

Run this preflight in order and record the source of each resolved value:

```text
DETECT ROOT → CLASSIFY CONFIG → RESOLVE IDIOM POLICY → RESOLVE TEST WORKFLOW → DETECT DECLARED GO → DISCOVER COMMANDS AND CONVENTIONS
```

1. **DETECT ROOT**: locate the repository root and `.gopher-plugin.toml`.
2. **CLASSIFY CONFIG**: use `gopher:config` validation to classify the file as
   `ABSENT`, `VALID`, `MIGRATION_AVAILABLE`, `INVALID`, or
   `UNSUPPORTED_VERSION`.
3. **RESOLVE IDIOM POLICY**: resolve `idiom_policy` independently by
   `session | file | adopted | default`. Its default is `latest-compatible`.
4. **RESOLVE TEST WORKFLOW**: resolve `test_workflow` independently by
   `session | file | adopted | default`. Its default is `adaptive-tdd`.
5. **DETECT DECLARED GO**: inspect `go.mod` for the module path, `go`
   directive, dependencies, and replacements; then inspect a `toolchain`
   directive or `go.work` for the selected toolchain and workspace modules.
6. **DISCOVER COMMANDS AND CONVENTIONS**: inspect CI, Makefile/Taskfile,
   scripts, contributor docs, existing code/tests, and adopted lint,
   generation, vulnerability, race, fuzz, and benchmark tooling.

`ABSENT` and `MIGRATION_AVAILABLE` continue with effective defaults for missing
policy values without persisting them. `INVALID` and `UNSUPPORTED_VERSION`
produce read-only diagnosis and block production edits; hand back the validation
evidence and the `gopher:config` recovery route rather than changing code.

Use the declared version even when a newer local toolchain exists. For a new
project with no declaration, verify the current stable Go release from the
official Go site before choosing it. Record version requirements beside advice
that depends on newer APIs.

Official sources: <https://go.dev/ref/mod>, <https://go.dev/doc/toolchain>.
Last verified: 2026-07-14.
