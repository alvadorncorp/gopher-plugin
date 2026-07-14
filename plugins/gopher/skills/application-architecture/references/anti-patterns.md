# Application Architecture Anti-patterns

| Signal | Why it fails | Recovery |
|---|---|---|
| Layer for every noun | Adds pass-through indirection without policy. | Collapse layers until a stable dependency rule appears. |
| Ports for every library | Wraps mechanisms without real variability. | Keep direct dependencies; add a seam at the consumer when evidence appears. |
| Shared domain model | Couples capabilities through one change surface. | Give each boundary owned terms and explicit translation. |
| Modular folders over shared data | Hides coupling behind paths. | Make invariant and transaction ownership explicit. |
| Big-bang migration | Removes rollback and comparison. | Introduce compatibility seams and migrate cohesive slices. |
| Premature services | Adds distributed failure before operational need. | Keep a modular monolith baseline. |

Treat each row as a diagnostic signal, not an automatic verdict. Cite the
observed dependency, change, or ownership evidence.
