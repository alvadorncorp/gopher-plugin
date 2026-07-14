# Architecture Pattern Mappings to Go

| General ID | Go mapping | Selection rule |
|---|---|---|
| `pattern.facade` | `go.package-api` | cohesive package surface; reject god-package aggregation |
| `pattern.dependency-injection` | `go.consumer-interface` | constructor parameter plus consumer-owned interface at a real seam |
| `pattern.bridge` | `go.composed-axes` | two demonstrated independent variation axes |
| `pattern.proxy` | `go.semantic-wrapper` | real access, lazy, remote, or lifecycle semantics |
| `pattern.abstract-factory` | `go.constructor-family` | two active product families, otherwise concrete constructors |
| `pattern.service-locator` | `go.explicit-wiring` | veto dynamic lookup unless legacy evidence requires containment |
| `pattern.registry` | `go.explicit-registration` | only for a real open plugin ecosystem with lifecycle rules |

Architecture may veto a general selection when it would introduce a package,
interface, or public API without observed variability or ownership evidence.
Return the original `pattern.*` ID, chosen `go.*` mapping or veto, liabilities,
and validation in the textual handoff.
