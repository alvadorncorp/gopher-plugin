# Go APIs, Errors, and Values

- Return `(T, bool)` for expected presence/absence without an explanatory failure.
- Return `(T, error)` for fallible operations; add context with `%w` when callers
  need cause inspection through `errors.Is` or `errors.As`.
- Keep sentinel and typed errors stable only when callers have a documented branch.
- Keep error text lowercase and free of redundant operation chains.
- Preserve partial-result semantics explicitly; zero values must not masquerade as success.
- Treat exported identifiers, signatures, behavior, error identity, and option
  semantics as public compatibility surface.
- Prefer native multiple returns over generic Option/Result wrappers unless
  domain or interoperability evidence requires a first-class value.

Sources: <https://pkg.go.dev/errors>, <https://go.dev/blog/error-handling-and-go>,
<https://go.dev/wiki/CodeReviewComments#in-band-errors>.
Last verified: 2026-07-14.
