# Routine Pattern Mappings to Go

When a supplied `pattern.*` matches a row, set `pattern_decision.general_id`
and `pattern_decision.go_mapping` from that row, apply the default baseline, and
choose `disposition` `accepted` | `adapted` | `vetoed` with Go-specific
evidence. When the ID is not in this table, do not invent a `go.*` or
`pattern.*` ID; use the ownership notes below or return to
`gopher:design-patterns` if selection is still open.

| General ID | Go mapping | Default Go baseline and selection rule |
|---|---|---|
| `pattern.factory-constructor` | `go.constructor` | zero value, literal, or `NewT` |
| `pattern.configuration-object` | `go.config-struct` | validated `Config` value |
| `pattern.builder` | `go.builder` | literal/config until incremental state exists |
| `pattern.configuration-options` | `go.functional-options` | constructor/config before options |
| `pattern.strategy` | `go.function-strategy` | function parameter/field before interface |
| `pattern.adapter` | `go.function-adapter` | named function type or thin wrapper |
| `pattern.decorator` | `go.middleware` | explicit wrapper preserving contract |
| `pattern.chain-of-responsibility` | `go.handler-chain` | ordered slice/loop with stop semantics |
| `pattern.composite` | `go.composite` | collection implementing one capability |
| `pattern.command` | `go.command-function` | function/closure before struct/interface |
| `pattern.iterator` | `go.range-or-iterator` | `range` first; `iter.Seq` only when the declared Go version provides `iter` |
| `pattern.state` | `go.enum-switch-or-state-func` | enum + switch before state functions |
| `pattern.visitor` | `go.traversal` | recursion/callback/type switch/iterator |
| `pattern.observer` | `go.callbacks-or-events` | direct calls; explicit unsubscribe/lifetime |
| `pattern.null-object` | `go.no-op-or-useful-zero` | explicit absence when no-op masks failure |
| `pattern.optional-value` | `go.comma-ok` | `(T, bool)` |
| `pattern.result` | `go.error-return` | `(T, error)` with wrapping/inspection |
| `pattern.prototype` | `go.clone-or-copy` | assignment, value copy, or stdlib clone (`maps.Clone`, `slices.Clone`, and from Go 1.27 `url.URL.Clone` and `url.Values.Clone`) first; `Clone()` / explicit deep copy only with a documented aliasing contract; reject prototype registries |
| `pattern.flyweight` | `go.canonical-intern` | allocate normally; intern/canonicalize only with measured memory benefit and safe identity/lifetime; package table or construction-time map—not speculative shared mutables; not `sync.Pool` |
| `pattern.memento` | `go.snapshot-value` | immutable snapshot values or explicit copy for undo/restore; document cost and aliasing; reject hidden deep-clone magic and ownerless global history |
| `pattern.interpreter` | `go.ast-eval` | direct functions or closed op set first; AST + pure `Eval` only with real grammar, node set, and consumers; reject accidental languages |

Package/seam catalog IDs map under `gopher:architecture`: `pattern.facade`,
`pattern.dependency-injection`, `pattern.bridge`, `pattern.proxy`,
`pattern.abstract-factory`, `pattern.service-locator`, and `pattern.registry`.
Context and pipeline boundary cards map in `gopher:concurrency`; the pooling
boundary card maps in `gopher:performance`. Diagnostic-only catalog IDs
(`pattern.singleton`, `pattern.template-method`, `pattern.mediator`,
`pattern.generic-option`, `pattern.generic-result`) have no developer `go.*`
mapping—veto or return to `gopher:design-patterns` rather than inventing an ID.
Identity interning (`go.canonical-intern`) is not object pooling.

Generic methods, available from Go 1.27, change how a mapping is realized, not
which mapping applies. Wherever a row's baseline is a free function over a
generic container, that function may now be a method on the container instead;
`go.traversal` and `go.function-strategy` are the common cases, and any row with
that baseline shape reads the same way. One limit bounds it: a generic method
cannot implement an interface method, so a shape that must satisfy an interface
keeps the free-function form. Choosing the method form is not by itself an
`adapted` disposition; set `accepted`, `adapted`, or `vetoed` from the row's own
selection rule. Below the declared-version guard the choice does not exist and
the baseline is unchanged.
