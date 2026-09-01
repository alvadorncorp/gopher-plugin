# Language and API modernization

Modernize Go source toward idioms and APIs available in the declared version,
one reviewable increment at a time.

## Scope

- Language idioms supported by the declared Go version (for example range-over
  constructs, generics where they simplify, standard-library helpers that
  replace hand-rolled code).
- Standard-library API adoption that is available at the declared version and
  preserves behavior.
- Deprecated-API replacement, when the replacement exists at the declared
  version.

## The `go fix` modernizer suite

The `modernize` analyzers ship inside the Go toolchain and run through `go fix`
(`references/tooling.md`). Two separate guards apply: the active toolchain must
be Go 1.26 or newer for the modernizer to exist at all, and each analyzer's own
floor must be met by the project's declared version for its rewrite to compile.

Every registered analyzer runs by default — `go tool fix help` states it
outright — so a bare `go fix ./...` is the whole suite, not a curated subset.
On a Go 1.27 toolchain the roster is:

| Analyzer | Rewrite | Declared-version floor |
|---|---|---|
| `any` | `interface{}` to `any` | 1.18 |
| `atomictypes` | primitive `sync/atomic` calls to the typed wrappers | 1.19 |
| `buildtag` | checks `//go:build` and `// +build` form (report only, no fix) | none |
| `embedlit` | drops the nested literal for a promoted embedded field | 1.27 |
| `errorsastype` | `errors.As` to `errors.AsType[T]` | 1.26 |
| `forvar` | removes redundant loop-variable re-declaration | 1.22 |
| `hostport` | checks address form passed to `net.Dial` (suggests `net.JoinHostPort`) | none |
| `inline` | applies fixes driven by `//go:fix inline` directives | set by the inlined body |
| `mapsloop` | explicit loops over maps to `maps` calls | 1.23 |
| `minmax` | if/else to the `min` and `max` builtins | 1.21 |
| `newexpr` | `new(expr)` | 1.26 |
| `omitzero` | `omitempty` to `omitzero` on struct fields | 1.24 |
| `plusbuild` | removes obsolete `//+build` comments | 1.18 |
| `rangeint` | 3-clause loops to range-over-int | 1.22 |
| `reflecttypefor` | `reflect.TypeOf(x)` to `reflect.TypeFor[T]()` | 1.22 |
| `slicesbackward` | backward loops to `slices.Backward` | 1.23 |
| `slicescontains` | loops to `slices.Contains` or `slices.ContainsFunc` | 1.21 |
| `slicessort` | `sort.Slice` to `slices.Sort` for basic types | 1.21 |
| `stditerators` | Len/At-style APIs to iterators | 1.23 |
| `stringsbuilder` | `+=` accumulation to `strings.Builder` | 1.10 |
| `stringscut` | `strings.Index` patterns to `strings.Cut` | 1.18 |
| `stringscutprefix` | `HasPrefix`/`TrimPrefix` to `CutPrefix` | 1.20 |
| `stringsseq` | ranging over `Split`/`Fields` to `SplitSeq`/`FieldsSeq` | 1.24 |
| `testingcontext` | `context.WithCancel` to `t.Context` in tests | 1.24 |
| `unsafefuncs` | unsafe pointer arithmetic to `unsafe` function calls | 1.17 |
| `waitgroupgo` | `wg.Add(1)`/`go`/`wg.Done()` to `wg.Go` | 1.25 |

The floor column is the *declared* version the rewritten code needs, distinct
from the Go 1.26 floor on the active toolchain that makes the modernizer
available at all. It comes from `go tool fix help <analyzer>`, which states the
version each rewrite targets, and from the API the rewrite introduces.

Under `target_go = "declared"`, an analyzer whose floor exceeds the resolved
target is out of scope: its rewrite would not compile. Report it as an
out-of-scope modernization with the floor stated rather than proposing it. A
project declaring Go 1.21 therefore has nine of the twenty-six out of scope, and
`embedlit` is out of scope for every project below Go 1.27.

`appendclipped`, `bloop` and `slicesdelete` are documented in the upstream
`x/tools` `modernize` pass but are **not** registered in the in-toolchain
`go fix`. They are reachable only through `go fix -fixtool=PROG` against an
`x/tools`-based analyzer binary, which is a separate adoption decision.

- `any` is disproportionately high-volume; review it as its own increment:
  `go fix -any=true ./...` first, then `go fix -any=false ./...` for the rest.
- `atomictypes` and `unsafefuncs` change how shared state and pointer
  arithmetic are expressed, so they earn their own increments too: their diffs
  need a reader who can confirm the memory semantics, not a diff scan.
- A bulk `go fix` apply changes many files at once, so preview diagnostics with
  `go fix -diff ./...`, apply the suggested fixes incrementally
  (`references/migration.md`), and validate after each increment.
- Record the exact Go toolchain version (`go version`); a different version can
  add analyzers, remove them, rename them, or propose different rewrites.
- A loop collapsed into a single call can discard comments that were inside
  it — review is still required, not just a diff scan.

## Roster drift between releases

The analyzer roster is a versioned surface, and the names are part of a
project's tooling contract. Go 1.27 both added and withdrew names:

- Added: `atomictypes`, `embedlit`, `slicesbackward`, `unsafefuncs`.
- Removed: `fmtappendf` (withdrawn as stylistic). A command carrying
  `-fmtappendf` no longer runs.
- Renamed: `waitgroup` became `waitgroupgo`. A command carrying `-waitgroup`
  no longer runs.

Both withdrawals fail the invocation rather than degrading quietly, so a
pinned `[tools].modernize` command, a Makefile target, or a CI step naming an
analyzer must be revalidated on every toolchain upgrade.

Derive the roster from `go tool fix help` on the toolchain actually in hand.
Release notes and the `x/tools` package documentation describe a different,
larger set and disagree with the shipped `go fix` on which analyzers exist and
which run by default. When the roster in hand differs from the table above,
report the difference as a limitation so this file can be refreshed
(`docs/go-release-upgrade.md`).

## Boundaries

- A change to a public API, an exported signature, or a cross-package contract
  is handed to `gopher:architecture`.
- Keep every rewrite behavior-preserving; a modernization that changes observable
  behavior is a code change for `gopher:developer`, not a modernization.

Last verified: 2026-08-31 against a local go1.27.0 toolchain.
