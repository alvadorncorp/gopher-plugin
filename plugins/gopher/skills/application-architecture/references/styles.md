# Internal Application Styles

| Style | Select when | Liabilities |
|---|---|---|
| Cohesive modules | Capabilities need explicit APIs but share one deployment and operational model. | Accidental cross-module access without checks. |
| Layered architecture | Dependency direction follows stable policy layers and cross-layer calls are predictable. | Anemic layers and pass-through indirection. |
| Ports and adapters | External mechanisms vary around stable application policy with real seams. | Port proliferation and domain wrappers around trivial libraries. |
| Modular monolith | Independent capability evolution is needed without distributed operations. | Hidden shared database/contracts and unenforced boundaries. |

Start with cohesive modules. Add layers or ports only for demonstrated policy
and variability. A style name never substitutes for explicit dependency rules.
