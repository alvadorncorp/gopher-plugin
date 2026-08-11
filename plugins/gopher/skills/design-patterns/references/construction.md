# Construction and Configuration Patterns

Use these cards only after stating the direct baseline. A useful zero value,
literal, or explicit constructor is the baseline for every construction choice.

| ID | Problem and signals | Counter-signals / direct baseline | Main liabilities | Validation |
|---|---|---|---|---|
| `pattern.factory-constructor` | Centralize invariants or hide concrete creation. | A literal or direct allocation already preserves invariants. | Hidden work, unnecessary naming, test indirection. | Invalid states are unrepresentable and call sites remain clear. |
| `pattern.configuration-object` | Configuration is declarative, stored, compared, decoded, or validated as a whole. | A few stable required parameters are clearer. | Large bags of unrelated options, zero-value ambiguity. | Validate once and document defaults. |
| `pattern.builder` | Construction is genuinely incremental, ordered, or accumulated across steps. | A literal/config object completes construction in one expression. | Temporal invalid states and verbose ceremony. | Every sequence ends in the same validated product contract. |
| `pattern.configuration-options` | Many independent optional dimensions, strong defaults, private configuration behavior, and credible evolution. | A constructor or configuration object is smaller and more inspectable. | Ordering, duplicates, non-idempotency, late validation, captured mutable state, namespace growth. | Specify ordering, duplicate, nil, validation, and compatibility semantics. |
| `pattern.abstract-factory` | Several real product families vary together. | Concrete constructors cover one family or speculative variants. | Type explosion and hidden coupling. | Demonstrate two active families and family-wide invariants. |
| `pattern.singleton` | Process-wide identity is a verified invariant. | Explicit dependency wiring and scoped lifetime. | Global state, test interference, lifecycle ambiguity. | Prove unique identity is required rather than convenient. |
| `pattern.prototype` | A new instance must be derived from an existing one and preserve a documented shallow/deep aliasing and ownership contract. | Assignment, value copy, or a one-off explicit copy is enough. | Hidden shared mutability, incomplete deep copies, prototype registries, clone-for-convenience. | Document which fields are shared vs copied; call sites remain clear; invalid aliasing is unrepresentable or tested. |

## Selection sequence

1. Test literal, zero-value, and direct-constructor baselines.
2. Choose a configuration object for declarative or serializable data.
3. Choose a builder only for incremental construction state.
4. Choose configuration options only after specifying option interactions.
5. Choose prototype only when clone-from-instance is required and aliasing is documented.
6. Keep Abstract Factory and Singleton diagnostic until their invariants are demonstrated.
