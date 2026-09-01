# Go Release Upgrade Checklist

What to revisit in this repository when a new stable Go version ships. The
decision behind this process is `adr:gopher:011`.

## The rule that matters most

**Derive facts from an installed toolchain of the target release, not from
release notes.** Install the release, then verify each fact with a command.

This is not a stylistic preference. When Go 1.27 shipped, the release notes and
the `x/tools` `modernize` package documentation each disagreed with the shipped
`go` binary about which analyzers exist and which run by default, and widely
repeated third-party summaries described a `crypto/tls` API surface that the
toolchain does not expose. Every one of those would have entered a skill as a
confident, wrong guard.

Record the toolchain the verification ran against on the `Last verified:` line
of every file touched.

## Where version knowledge lives

Every file below encodes a Go version fact. A release refresh reads all of them
and edits the ones the release moves.

### Primary guard tables

| File | What it gates |
|---|---|
| `plugins/gopher/skills/performance/references/version-sensitive.md` | The primary table. Runtime, GC, allocation, profiling, and GOEXPERIMENT guards. |
| `plugins/gopher/skills/test-quality/references/lab-families.md` | Testing capability guards, per quality-lab family. |
| `plugins/gopher/skills/cgo/references/sources.md` | cgo mechanism guards, plus linker and sanitizer surface. |

### The toolchain and modernizer surface

| File | What it encodes |
|---|---|
| `plugins/gopher/skills/modernize/references/language-apis.md` | The `go fix` analyzer roster, per-analyzer declared-version floors, and roster drift between releases. |
| `plugins/gopher/skills/modernize/references/tooling.md` | Discovery order, `go fix` commands, skipped-fix messages, and degradation below the modernizer floor. |
| `plugins/gopher/skills/modernize/references/modules-toolchain.md` | `go mod tidy` behavior, removed GODEBUG settings, version-control support, and standard-library packages that retire a dependency. |
| `plugins/gopher/skills/modernize/references/project-contract.md` | The declared-versus-active version split and the modernizer floor. |
| `plugins/gopher/skills/modernize/references/sources.md` | Which sources are authoritative, and the review cadence. |
| `plugins/gopher/skills/modernize/SKILL.md` | Safeguards that name a version or a versioned surface. |

### Skills that carry release-sensitive guidance

| File | What the release can move |
|---|---|
| `plugins/gopher/skills/performance/references/{profiling,benchmarking,allocation-runtime,sources}.md` | Profile symbols, trace tooling, allocation behavior, baseline comparability. |
| `plugins/gopher/skills/concurrency/references/{diagnostics,goroutine-lifetime,channels-synchronization}.md` | Leak evidence, timer channel semantics, synchronization idioms. |
| `plugins/gopher/skills/observability/references/{profiles-runtime,logging-slog,sources}.md` | Profile kinds, traceback content, runtime metric catalog. |
| `plugins/gopher/skills/security/references/{go-risk-catalog,sources}.md` | Crypto and TLS defaults, removed GODEBUGs, server limits, parser strictness. |
| `plugins/gopher/skills/resilience/references/{overload,runtime-controls,sources}.md` | Server-side limits supplied by the toolchain, and error shapes the taxonomy matches on. |
| `plugins/gopher/skills/architecture/references/modules-workspaces.md` | Module and workspace command behavior. |
| `plugins/gopher/skills/codegen/references/{inventory,provenance,reproduction}.md` | Tool directives, `//line` resolution, reproduction determinism. |
| `plugins/gopher/skills/developer/references/{idioms,pattern-mappings,project-detection}.md` | Newly available language shapes and standard-library APIs. |
| `plugins/gopher/skills/fuzz/references/sources.md` | The native fuzzing floor. |

## Verification commands

Run these against the new toolchain and paste the results into the edit, rather
than paraphrasing a release note.

```bash
go version

# Analyzer roster and the actual default. This is the roster, full stop.
go tool fix help | sed -n '/Registered analyzers/,/^By default/p'
go tool fix help <analyzer>          # what one analyzer rewrites, with an example

# Standard-library surface
go list std | grep -E '^(<package>)$'
go doc <pkg>.<Symbol>
GOEXPERIMENT=<name> go list std      # packages that appear only under an experiment

# GOEXPERIMENT names: an unknown one errors, an accepted one echoes back
GOEXPERIMENT=<name> go env GOEXPERIMENT

# Tool behavior
go help test | grep -A6 'go vet'
go tool trace -h
go tool link -h
go doc cmd/test2json
```

Behavior that no command reports directly is verified with a throwaway module.
Two that paid off for Go 1.27:

```bash
# Which GODEBUG settings were removed: an old value fails at load time.
# Always include a control that is still accepted.
printf 'godebug <name>=<old-value>\n' >> go.mod && go build ./...

# Whether a go.mod behavior is gated on the declared version: run the same
# input at two `go` directives and diff the result.
go mod tidy
```

## Repository gates a release refresh runs into

- **English only, no placeholders.** `tests/validate_repo.py` scans every `*.md`
  in the repository — including `docs/`, `.plans/`, and `.lessons/` — for
  Portuguese markers and for a list of placeholder tokens defined in that file.
  The match is a literal substring, so a document cannot even quote the tokens
  to explain them; read the list from the validator rather than from prose. An
  ADR written for this repository is written in English, whatever the default
  language of the tool that drafts it.
- **The reference layout is pinned.** Adding a file under
  `skills/*/references/` requires editing `tests/fixtures/expected-layout.json`;
  the check is exact set and order equality plus a total count. Prefer editing
  an existing file.
- **The design-pattern catalog is frozen** at 36 `pattern.*` IDs with
  dispositions `{full: 23, diagnostic: 10, deferred: 0, boundary: 3}`, asserted
  in both `tests/validate_repo.py` and `tests/test_repository.py`. A new
  language feature revises the prose of a mapping row, never the ID set.
- **The routing corpus count is literal.** Adding a case to
  `tests/fixtures/forward-tests.json` requires bumping the count in
  `tests/test_forward_corpus.py`.
- **`SKILL.md` stays under 500 lines**, and `README.md` must keep the literal
  strings asserted in `tests/test_documentation.py`.
- `[modernize].target_go` is a free-form string, so a new Go version needs no
  configuration schema change and no `schema_version` bump.

Finish with:

```bash
python3 tests/validate_repo.py
python3 -m unittest discover -s tests
```

## Recording the result

- Bump `Last verified:` on every file touched, naming the toolchain when the
  verification ran against one.
- Add the release-notes URL to the `sources.md` of each skill that gained a
  fact from it.
- Write a forecast as a forecast. A removal is recorded only once the toolchain
  refuses the setting, and the forecast is re-tested on the release it names.
