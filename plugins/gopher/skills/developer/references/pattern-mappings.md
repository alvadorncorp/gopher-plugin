# Routine Pattern Mappings to Go

| General ID | Go mapping | Default Go baseline |
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
| `pattern.iterator` | `go.range-or-iterator` | `range`; `iter.Seq` only on compatible Go |
| `pattern.state` | `go.enum-switch-or-state-func` | enum + switch before state functions |
| `pattern.visitor` | `go.traversal` | recursion/callback/type switch/iterator |
| `pattern.observer` | `go.callbacks-or-events` | direct calls; explicit unsubscribe/lifetime |
| `pattern.null-object` | `go.no-op-or-useful-zero` | explicit absence when no-op masks failure |
| `pattern.optional-value` | `go.comma-ok` | `(T, bool)` |
| `pattern.result` | `go.error-return` | `(T, error)` with wrapping/inspection |
| `pattern.prototype` | `go.clone-or-copy` | assignment, value copy, or stdlib clone (`maps.Clone`, `slices.Clone`) first; `Clone()` / explicit deep copy only with a documented aliasing contract; reject prototype registries |
| `pattern.flyweight` | `go.canonical-intern` | allocate normally; intern/canonicalize only with measured memory benefit and safe identity/lifetime; package table or construction-time map—not speculative shared mutables; not `sync.Pool` |
| `pattern.memento` | `go.snapshot-value` | immutable snapshot values or explicit copy for undo/restore; document cost and aliasing; reject hidden deep-clone magic and ownerless global history |
| `pattern.interpreter` | `go.ast-eval` | direct functions or closed op set first; AST + pure `Eval` only with real grammar, node set, and consumers; reject accidental languages |

`pattern.facade` and `pattern.dependency-injection` cross package/seam ownership
and map in `gopher:architecture`. Context and pipeline boundary cards map in
`gopher:concurrency`; the pooling boundary card maps in `gopher:performance`.
Identity interning (`go.canonical-intern`) is not object pooling.
