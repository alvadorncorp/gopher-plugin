# Go Construction and Options

## Decision order

1. Useful zero value or literal.
2. `NewT(required...)` for a small stable required set and invariants.
3. `Config`/`Options` struct when data is declarative, stored, compared,
   decoded, or validated as a whole.
4. Builder only when construction is genuinely incremental.
5. Functional Options when a public API has strong defaults, many independent
   optional dimensions, private configuration behavior, and credible evolution.

## Functional Options contract

Evaluate and specify:

- `func(*T)`, `func(*T) error`, sealed `Option` interface, or immutable transform;
- ordering and duplicate behavior;
- idempotency and composition;
- validation before final construction and avoidance of partial mutation;
- closure capture and mutation after option creation;
- nil option behavior;
- exported option namespace growth and compatibility;
- whether a constructor or config struct remains simpler.

Adding `...Option` to an existing constructor changes its signature. Preserve
the old entry point or treat the change as a public-contract migration.

Sources: <https://go.dev/doc/effective_go#allocation_new>,
<https://go.dev/blog/module-compatibility>.
Last verified: 2026-07-14.
