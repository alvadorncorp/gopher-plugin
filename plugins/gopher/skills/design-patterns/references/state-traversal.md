# State and Traversal Patterns

| ID | Select when | Direct baseline | Main liabilities | Disposition |
|---|---|---|---|---|
| `pattern.iterator` | Lazy or resumable traversal has a stable consumer contract. | Native loop/range over an existing collection. | Resource lifetime, early termination, mutation visibility. | Full v1 |
| `pattern.state` | Transition-heavy behavior changes by explicit state. | Enum plus switch/conditional. | Distributed transitions and invalid state combinations. | Full v1 |
| `pattern.visitor` | Many stable node variants need external traversal operations. | Recursion, callback, type switch, or iterator. | Adding node types becomes expensive; double-dispatch ceremony. | Full v1 |
| `pattern.flyweight` | Canonicalization has measured memory value and safe identity semantics. | Allocate normally. | Retention, contention, identity surprises. | Deferred |
| `pattern.memento` | A real snapshot/restore contract defines aliasing and cost. | Explicit copy or domain snapshot value. | Hidden deep copies and stale restoration. | Deferred |
| `pattern.interpreter` | A real language has grammar, AST, semantics, and users. | Direct parser or explicit operations. | Accidental language growth and weak diagnostics. | Deferred |

`pattern.prototype` is documented with construction because its core question
is copy-based creation. Deferred cards stay out of recommendations until real
evidence supplies their missing contracts.
