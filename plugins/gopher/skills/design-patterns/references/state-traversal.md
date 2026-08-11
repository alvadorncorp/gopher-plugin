# State and Traversal Patterns

| ID | Select when | Direct baseline | Main liabilities | Validation |
|---|---|---|---|---|
| `pattern.iterator` | Lazy or resumable traversal has a stable consumer contract. | Native loop/range over an existing collection. | Resource lifetime, early termination, mutation visibility. | Consumer can stop early; resource ownership is clear. |
| `pattern.state` | Transition-heavy behavior changes by explicit state. | Enum plus switch/conditional. | Distributed transitions and invalid state combinations. | Illegal transitions are unrepresentable or rejected. |
| `pattern.visitor` | Many stable node variants need external traversal operations. | Recursion, callback, type switch, or iterator. | Adding node types becomes expensive; double-dispatch ceremony. | New operations do not force node-type churn without evidence. |
| `pattern.flyweight` | Many logical values share immutable intrinsic state; canonicalization has **measured** memory value and safe identity/lifetime semantics. | Allocate normally; share only immutable constants. | Retention, contention, identity surprises, mutable shared state. | Measurement shows benefit; identity and lifetime rules are documented; interning is not object pooling. |
| `pattern.memento` | Capture and restore prior state under an explicit snapshot contract (undo, checkpoint) with known cost and aliasing. | Explicit copy or domain snapshot value at the call site. | Hidden deep copies, stale restoration, unbounded history, unclear ownership. | Snapshot/restore round-trip is tested; cost and aliasing are documented. |
| `pattern.interpreter` | A real language has grammar, AST, semantics, and consumers that evaluate expressions as data. | Direct functions, a closed op set, or a simple parser without a general language. | Accidental language growth, weak diagnostics, dual dispatch ceremony. | Grammar and node set are bounded; Eval is pure or has explicit effects; reject “turn this if/else into a language.” |

`pattern.prototype` is documented with construction because its core question
is copy-based creation. Useful combinations: memento + command for undo stacks;
interpreter + visitor/iterator for AST walks; flyweight only after allocate-normal
baseline fails a measured memory budget.
