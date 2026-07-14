# Behavior and Coordination Patterns

| ID | Select when | Direct baseline | Main liabilities | Validation |
|---|---|---|---|---|
| `pattern.command` | An operation needs identity, storage, scheduling, retry, undo, or lifecycle. | Call a function directly. | Command type proliferation and duplicated dispatch. | Demonstrate why the operation must be a value. |
| `pattern.observer` | Multiple subscribers react to events with explicit lifecycle. | Call known collaborators directly. | Leaks, ordering, backpressure, reentrancy, weak delivery semantics. | Specify subscribe/unsubscribe, delivery, failure, and ownership. |
| `pattern.template-method` | Diagnostic only for inheritance-shaped fixed skeletons. | Compose functions/callbacks around explicit steps. | Hidden extension points and fragile base behavior. | Show why composition cannot express the stable skeleton. |
| `pattern.mediator` | Diagnostic only for a real coordination protocol. | Keep collaboration explicit between a small set. | God coordinator and opaque coupling. | Bound responsibilities and reject domain logic accumulation. |

Commands and events often combine with Strategy, Adapter, or Decorator. Record
each pattern's separate force; one name must not hide multiple responsibilities.
