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
(`references/tooling.md`). Use them only when the active toolchain is Go 1.26
or newer and compatible with the declared version.

Default-enabled analyzers propose most of these rewrites: `any` (interface{} ->
any), `fmtappendf`, `forvar`, `hostport`, `inline`, `mapsloop`, `minmax`,
`newexpr`, `omitzero`, `plusbuild`, `rangeint`, `reflecttypefor`,
`slicescontains`, `slicessort`, `stditerators`, `stringsbuilder`,
`stringscut`, `stringscutprefix`, `stringsseq`, `testingcontext`, `waitgroup`,
plus the `buildtag` vet check. Four analyzers are off by default because their
fix can change observable behavior and require explicit judgment before
enabling: `appendclipped`, `bloop`, `slicesdelete`, `errorsastype`.

- `any` is disproportionately high-volume; review it as its own increment:
  `go fix -any=true ./...` first, then `go fix -any=false ./...` for the rest.
- A bulk `go fix` apply changes many files at once, so preview diagnostics with
  `go fix -diff ./...`, apply the suggested fixes incrementally
  (`references/migration.md`), and validate after each increment.
- Record the exact Go toolchain version (`go version`); a different version can
  add analyzers, change defaults, or propose different rewrites.
- A loop collapsed into a single call can discard comments that were inside
  it — review is still required, not just a diff scan.

## Boundaries

- A change to a public API, an exported signature, or a cross-package contract
  is handed to `gopher:architecture`.
- Keep every rewrite behavior-preserving; a modernization that changes observable
  behavior is a code change for `gopher:developer`, not a modernization.
