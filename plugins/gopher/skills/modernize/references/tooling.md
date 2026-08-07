# Tool discovery

`[tools].modernize` governs analyzer selection. `auto` discovers an adopted or
already-available tool and never installs one.

## Discovery order

1. An explicit command in `[tools].modernize` (used verbatim).
2. `go fix`, the in-toolchain modernizer, when the active toolchain
   (`go version`, not just the `go.mod` directive) is Go 1.26 or newer. It
   needs no install: the `modernize` analyzers ship inside the Go toolchain
   itself and run through `go fix`. An explicit `[tools].modernize` command can
   still point `go fix -fixtool=PROG` at a different analyzer set.
3. An adopted project modernization command already declared.
4. Otherwise, report an explicit limitation — do not install a tool.

## Commands

- `go fix -diff ./...` — preview only, no writes. Prints a unified diff and
  exits non-zero when the diff is non-empty; a non-zero exit here means
  "changes proposed", not "failure".
- `go fix -json ./...` — read-only diagnostic inventory, one JSON object per
  package, each keyed by analyzer name with the offending position and the
  suggested edits. Use it to triage what a bulk apply left behind.
- `go fix ./...` — applies every enabled analyzer's fixes in place.
- `go fix -<analyzer> ./...` — runs only the named analyzer;
  `-<analyzer>=false` runs every analyzer except that one. Use this to isolate
  one increment (`references/migration.md`) or to split a high-volume analyzer
  out of a review pass (`references/language-apis.md`).
- `go tool fix help` — lists every registered analyzer, default-enabled or not.
  `go tool fix help <name>` documents one analyzer and its flags.

## Skipped fixes

A bulk `go fix ./...` commonly applies only part of what it diagnosed. Two
distinct, exact messages report this:

- Apply mode: `applied N of M fixes; K files updated. (Re-run the command to
  apply more.)`
- `-diff` mode: `N of M fixes skipped (e.g. due to conflicts)`

Three causes, only two of them visible:

- **Conflict** — two fixes propose overlapping edits to the same file; the
  later one is dropped. Recoverable: re-run, or isolate the conflicting
  analyzers into separate increments.
- **Generated file** — any fix touching a generated file is dropped silently;
  nothing in the standard output reports it. Not recoverable by re-running;
  generated-output modernization is out of scope here.
- **Concurrent modification** — a file's size changed mid-run. This aborts the
  whole apply; re-establish the compatibility baseline before retrying.

Use `go fix -json ./...` after a partial apply to see exactly which analyzer
and file the remainder belongs to, then apply the rest one analyzer at a time
per `references/migration.md`.

## Degradation

- `off` disables the dimension; report it as not run.
- An active toolchain below Go 1.26 does not run the `go fix` modernizer: that
  version's `go fix` is the older `cmd/fix` API-rewriter, an unrelated tool
  with a different flag set (no `-json`, no per-analyzer flags). Treat the
  modernizer as unavailable rather than substituting the legacy tool.
- An unavailable `auto` tool is a limitation. Analysis still reports the
  modernizations it can identify by inspection and marks the rest as
  unverified.
