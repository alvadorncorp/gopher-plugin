# Go Project Detection

Run this preflight in order. For each step, record the observed path, value,
document, or command; the selected value and source when a policy is resolved;
and the exact command, exit status, and concise observation when a command runs.
Classify evidence as `observed`, `inferred`, or `unknown`.

```text
DETECT ROOT → CLASSIFY CONFIG → RESOLVE IDIOM POLICY → RESOLVE TEST WORKFLOW → DETECT DECLARED GO → DISCOVER COMMANDS AND CONVENTIONS
```

1. **DETECT ROOT**: locate the repository root and `.gopher-plugin.toml`; record
   both paths, or record the config path's observed absence. If the repository
   root cannot be established, mark it `unknown` and stop this gate.
2. **CLASSIFY CONFIG**: use `gopher:config` validation to classify the file as
   `ABSENT`, `VALID`, `MIGRATION_AVAILABLE`, `INVALID`, or
   `UNSUPPORTED_VERSION`. For a failure or limitation, retain the validation
   rule, TOML path or parse location, observed value or structure, expected
   contract, and allowed or blocked work.
3. **RESOLVE IDIOM POLICY**: resolve `idiom_policy` independently using the
   source labels `session | file | adopted | default` in descending precedence.
   Its default is `latest-compatible`; record the selected value and source.
4. **RESOLVE TEST WORKFLOW**: resolve `test_workflow` independently in
   descending precedence `session | file | adopted | default`. Its default is
   `adaptive-tdd`; record the selected value and source.
5. **DETECT DECLARED GO**: inspect `go.mod` for the module path, `go`
   directive, dependencies, replacements, and any `toolchain` directive; when
   present, inspect `go.work` for its `go` or `toolchain` directive and `use`d
   workspace modules.
6. **DISCOVER COMMANDS AND CONVENTIONS**: inspect CI, Makefile/Taskfile,
   scripts, contributor docs, existing code/tests, and adopted lint,
   generation, vulnerability, race, fuzz, and benchmark tooling. Record each
   adopted command and the project surface that establishes it.

Advance only after the current step's evidence is recorded. If required
evidence cannot be observed, mark it `unknown`, name the exact file, command, or
user decision needed, and stop the affected gate instead of inferring a result.

`ABSENT` and `MIGRATION_AVAILABLE` continue with effective defaults for missing
policy values, using source `default` and without persisting them. `INVALID` and
`UNSUPPORTED_VERSION` produce read-only diagnosis and block production edits:
report the validation evidence, state the blocked work, and hand off to
`gopher:config` for recovery rather than changing code. For
`UNSUPPORTED_VERSION`, mark future-schema values and dependent effects `unknown`
rather than inferring them or rewriting the file.

Use the declared `go` version for compatibility advice even when a newer local
toolchain exists; record a selected `toolchain` separately. For a new project
with no declaration, verify the current stable Go release from the official Go
site before choosing it. Record version requirements beside advice that depends
on newer APIs.

Official sources: <https://go.dev/ref/mod>, <https://go.dev/doc/toolchain>.
Last verified: 2026-07-14.
