# Idiomatic Go Baselines

## Resolved idiom policy

Use `references/project-detection.md` to establish the declared Go version and
local conventions before choosing an idiom. The resolved `idiom_policy` selects
one of these bounded behaviors:

| Policy | Semantics |
|---|---|
| `latest-compatible` | Prefer the newest suitable declared-version idiom locally; "suitable" means supported by the declared Go version and compatible with the current local API and requested behavior. |
| `project-aligned` | Prioritize nearby adopted conventions when choosing an idiom; use the closest relevant package, callers, and tests as evidence. |
| `explicit-only` | Introduce a newer idiom only on explicit request naming that idiom in the current change. |

All three policies are capped by the declared Go version and apply only to
new or directly changed code in the current local change. Keep
`modernize.target_go` with `gopher:modernize`; hand broad, package-wide, or
unrelated rewrites to that skill. When a required input remains unknown after
project detection, report the missing evidence and pause idiom selection until
compatibility or adoption is evidenced.

## Write-time forms

The in-toolchain modernizer roster is the catalog of forms to emit while
writing. Read the analyzer table and its declared-version floor column in
`plugins/gopher/skills/modernize/references/language-apis.md`. That table is a
catalog. `gopher:modernize` owns running the analyzer and owns rewrites
outside this change. Do not invoke `go fix`.

The floor is the declared `go` directive in the `go.mod` of the module that
owns the code being written. When `go.work` is present, read its `go`
directive and do not let it, or a newer local toolchain, raise that floor.
When the declared `go` version is unknown, pause form selection and name the
missing file.

For new or directly changed code in the current change, the resolved
`idiom_policy` selects the form:

| Policy | Form to emit |
|---|---|
| `latest-compatible` | The post-rewrite form of every analyzer whose floor is at or below the declared `go` directive, when the substitution preserves the requested behavior. |
| `project-aligned` | That form only when the touched package already uses it. Otherwise repeat the local form and record the newer available form as a non-blocking limitation. Leave the newer form unapplied. |
| `explicit-only` | A newer form only when the current request names that idiom. |

Existing occurrences in the same file stay as they are. Converting them is
`gopher:modernize` work.

Three analyzers are not blind substitutions even when their floor is met:

- `omitzero` changes the zero-value contract. Keep `omitempty` when the zero
  value must be omitted differently from `omitzero`.
- `atomictypes` and `unsafefuncs` change how shared state and pointer
  arithmetic are written. Use the newer form only when this change already
  edits that state or that arithmetic.

`buildtag`, `hostport`, and `inline` are not write-time forms. Apply
`plusbuild` only when this change already edits the build-tag line.

When `go tool fix help` on the active toolchain disagrees with the table,
record the difference in `limitations` and follow the table. Do not invent an
analyzer, and do not block implementation on roster drift.

The declared-version-gated shapes below are language surface, not this roster.

## Baseline idioms

- Prefer useful zero values, literals, and explicit constructors.
- Start with concrete types; introduce an interface at the consumer only when
  real variability, a test/process boundary, or compatibility seam exists.
- Accept interfaces and return concrete types; choose another return shape only
  when the API contract requires it.
- Keep interfaces small and behavior-focused.
- Pass `context.Context` explicitly as the first parameter for request-scoped
  cancellation/deadlines; keep stored configuration structs request-independent.
- Make resource ownership and `Close` responsibility explicit.
- Keep package APIs cohesive and names meaningful at the call site.
- Use `defer` when lifetime is clear and its cost is appropriate for the path.
- Prefer `wg.Go` over `wg.Add(1)` / `go` / `defer wg.Done()` from Go 1.25
  when the Write-time forms table selects that form.

## Declared-version-gated shapes

Each entry selects a shape for new or directly changed code; converting existing
occurrences is `gopher:modernize` work. Every entry is capped by the declared
version like any other idiom: on a project declaring less, the shape is rejected
with the guard stated. For the standard-library entries the compiler enforces
the cap, so `go test` fails the build rather than reaching review.

The shapes below arrived in Go 1.27.

- **Generic methods.** A method may declare its own type parameters, so a
  transformation over a generic container no longer has to be a free function
  taking the container. Two limits are part of the rule, not footnotes: an
  interface method cannot declare type parameters, and a generic method cannot
  implement an interface method. A shape that needs to satisfy an interface
  still needs the free-function form.
- **Promoted field names in composite literals.** A key may be any valid field
  selector, so an embedded field initializes without a nested literal:
  `T{X: 1}` where `X` is promoted from an embedded `U`.
- **Generalized function type inference**: omit explicit type arguments where a
  generic function is assigned to a variable or converted to a matching function
  type.
- `strings.CutLast` and `bytes.CutLast`, for splitting on the last separator
  instead of `LastIndex` plus manual slicing.
- `hash/maphash.Hasher` and `ComparableHasher`, for a hash and equality contract
  a data structure can take as a parameter.
- `net/url.URL.Clone` and `url.Values.Clone`, replacing hand-written deep copies.
- `database/sql.ConvertAssign` and `driver.RowsColumnScanner`, for a driver that
  needs `Rows.Scan` conversions or a direct scan into the caller's destination.
- `math/big.Int.Divide`, for quotient and remainder under an explicit rounding
  mode rather than a correction after the fact.
- The standard-library `uuid` package (RFC 9562), which can retire a third-party
  dependency. Retiring the dependency itself is `gopher:modernize` work.

Official sources: <https://go.dev/wiki/CodeReviewComments>,
<https://go.dev/doc/go1.27>.
Last verified: 2026-08-31 against a local go1.27.0 toolchain.
