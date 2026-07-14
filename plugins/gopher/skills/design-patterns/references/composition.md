# Composition, Seams, and Dispatch Patterns

| ID | Select when | Prefer the baseline when | Main liabilities |
|---|---|---|---|
| `pattern.strategy` | One behavior varies behind a stable caller contract. | A direct call or function parameter expresses the variation. | Speculative interface hierarchies and scattered policy. |
| `pattern.adapter` | Two existing contracts must interoperate without changing either owner. | The caller can invoke the target directly. | Leaky translations and swallowed semantics. |
| `pattern.decorator` | Cross-cutting behavior wraps one operation while preserving its contract. | One explicit call is clearer. | Order-sensitive wrappers and hidden control flow. |
| `pattern.chain-of-responsibility` | An ordered sequence decides continue/stop/handle. | A loop or conditional is local and fixed. | Unclear stop semantics and difficult tracing. |
| `pattern.composite` | One value and a homogeneous collection share the same capability. | The collection can be iterated directly. | Cycles, ambiguous ownership, surprising aggregation. |
| `pattern.facade` | A cohesive boundary needs a smaller stable entry surface. | Package/module functions are already cohesive. | God façade and hidden capabilities. |
| `pattern.dependency-injection` | Real variability or a test/process boundary requires an explicit seam. | Concrete dependencies have one implementation and no seam. | Service plumbing and speculative abstractions. |
| `pattern.null-object` | A no-op or useful zero is a valid domain behavior. | Absence should be explicit and checked. | Masked missing configuration and silent failure. |
| `pattern.bridge` | Two independent dimensions vary and must compose. | Only one dimension varies. | Premature two-axis abstraction. |
| `pattern.proxy` | Access, remote, lazy, or lifecycle semantics differ from the target. | A transparent wrapper adds no distinct behavior. | Hidden I/O, identity, and failure modes. |
| `pattern.service-locator` | Diagnostic only; evaluate legacy dynamic lookup. | Explicit dependency wiring. | Hidden dependencies and runtime-only failures. |
| `pattern.registry` | A real open plugin ecosystem requires runtime registration. | A closed set can be wired explicitly. | Global mutation, initialization order, name collisions. |

For every selected wrapper or chain, document ordering, failure propagation,
identity, lifecycle, and observability. A language owner chooses the concrete
function/interface/package mechanics.
