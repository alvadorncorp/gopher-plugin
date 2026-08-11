# Go Construction and Options

Select a local Go construction shape after the API need is fixed. Pattern
diagnosis (which general pattern) belongs to `gopher:design-patterns`; this
reference chooses among zero value, `NewT`, config struct, builder, and
Functional Options.

## Pattern force gate

Hand off to `gopher:design-patterns` and stop before the steps below when
construction forces are still open (which pattern, not which Go shape) and the
request supplies neither a `pattern.*` ID nor an already-decided local Go shape
to implement.

Stay here when a `pattern.*` ID is supplied or returned from
`gopher:design-patterns`, or when the request names a local Go shape to
implement (for example Functional Options). When a `pattern.*` is present, load
`pattern-mappings.md` and implement the accepted Go mapping; use the decision
order as the default preference inside that mapping.

## Decision order

Apply the first step that fits:

1. Useful zero value or literal when it is ready to use without a constructor
   (`go.constructor` baseline).
2. `NewT(required...)` for a small, stable required set that must establish
   invariants a zero value cannot (`go.constructor`).
3. `Config`/`Options` struct when data is declarative, stored, compared,
   decoded, or validated as a whole (`go.config-struct`).
4. Builder only when construction is genuinely incremental — ordered or
   accumulated across steps — and a single literal or config expression cannot
   complete it (`go.builder`).
5. Functional Options when a public API has strong defaults, many independent
   optional dimensions, private configuration behavior, and credible evolution
   (`go.functional-options`). Prefer a constructor or config struct when either
   remains smaller and more inspectable.

If the choice remains open after this order, hand off to
`gopher:design-patterns`.

## Functional Options contract

When Functional Options is the chosen shape, evaluate and specify:

- option form: `func(*T)`, `func(*T) error`, sealed `Option` interface, or
  immutable transform;
- ordering and duplicate behavior;
- idempotency and composition;
- full validation before final construction so the constructed value is complete
  only on success;
- closure capture and mutation after option creation;
- nil option behavior;
- exported option namespace growth and compatibility;
- whether a constructor or config struct remains smaller and more inspectable.

Adding `...Option` to an existing constructor changes its signature. Preserve
the old entry point or treat the change as a public-contract migration.

Sources: <https://go.dev/doc/effective_go#allocation_new>,
<https://go.dev/blog/module-compatibility>.
Last verified: 2026-07-14.
