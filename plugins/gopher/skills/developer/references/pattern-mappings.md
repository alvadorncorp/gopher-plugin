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

`pattern.facade` and `pattern.dependency-injection` cross package/seam ownership
and map in `gopher:architecture`. Context and pipeline boundary cards map in
`gopher:concurrency`; the pooling boundary card maps in `gopher:performance`.
