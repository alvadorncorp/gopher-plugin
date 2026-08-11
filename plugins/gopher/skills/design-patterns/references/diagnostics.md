# Catalog Diagnostics and Canonical Index

Load when the problem family is unclear, the request names an anti-pattern
candidate, or an ID must be checked against the canonical catalog.

## Card schema

| Disposition | Operational duty |
|---|---|
| full | Compare with the full card fields and the owning family reference. |
| diagnostic | Treat as selectable only after the evidence gates below and the family card pass; otherwise keep the direct baseline or `no-pattern`. |
| boundary | Name the concept and route mechanics to the listed owner; do not invent local mechanics here. |
| deferred | Not selectable in v1; the catalog currently has none. |

Every full card supplies: ID and aliases, problem, forces, direct baseline,
signals, counter-signals, mechanics, liabilities, useful combinations, and
validation questions.

## Canonical v1 index

| ID | Disposition | Canonical family / handoff |
|---|---|---|
| pattern.factory-constructor | full | construction |
| pattern.configuration-object | full | construction |
| pattern.builder | full | construction |
| pattern.configuration-options | full | construction |
| pattern.strategy | full | composition |
| pattern.adapter | full | composition |
| pattern.decorator | full | composition |
| pattern.chain-of-responsibility | full | composition |
| pattern.composite | full | composition |
| pattern.facade | full | composition |
| pattern.command | full | behavior |
| pattern.iterator | full | state-traversal |
| pattern.state | full | state-traversal |
| pattern.visitor | full | state-traversal |
| pattern.observer | full | behavior |
| pattern.dependency-injection | full | composition |
| pattern.null-object | full | composition |
| pattern.optional-value | full | values-errors |
| pattern.result | full | values-errors |
| pattern.abstract-factory | diagnostic | construction |
| pattern.singleton | diagnostic | construction |
| pattern.bridge | diagnostic | composition |
| pattern.proxy | diagnostic | composition |
| pattern.template-method | diagnostic | behavior |
| pattern.mediator | diagnostic | behavior |
| pattern.generic-option | diagnostic | values-errors |
| pattern.generic-result | diagnostic | values-errors |
| pattern.service-locator | diagnostic | composition |
| pattern.registry | diagnostic | composition |
| pattern.prototype | full | construction |
| pattern.flyweight | full | state-traversal |
| pattern.memento | full | state-traversal |
| pattern.interpreter | full | state-traversal |
| pattern.context-cancellation | boundary | gopher:concurrency |
| pattern.pipeline | boundary | gopher:concurrency |
| pattern.object-pool | boundary | gopher:performance |

Counts are normative: 23 full, 10 diagnostic, 0 deferred, and 3 boundary
candidates (36 total). No popularity ranking is implied. Use only IDs listed
above.

## Selection and diagnostic gates

### Baseline

- Return `no-pattern` when the direct baseline satisfies all forces.

### Diagnostic disposition gates

Select a diagnostic ID only when its evidence holds; otherwise keep the baseline
or `no-pattern`.

- `pattern.abstract-factory`: two active product families that vary together.
- `pattern.singleton`: process-wide identity is a verified invariant, not a
  convenience.
- `pattern.bridge`: two independent variation axes that must compose.
- `pattern.proxy`: distinct access, lazy, remote, or lifecycle semantics versus
  the target.
- `pattern.service-locator`, reflection-heavy injection, and global
  `pattern.registry`: keep diagnostic unless a real runtime plugin ecosystem is
  demonstrated.
- `pattern.template-method`, `pattern.mediator`, `pattern.generic-option`, and
  `pattern.generic-result`: apply the family card's diagnostic-only validation;
  select only when composition or native forms cannot express the force.

### Full-card high-risk gates

These IDs are full cards and still require the named proof before selection.

- `pattern.prototype`: documented shallow/deep aliasing and ownership contract
  for clone-from-instance; prefer assignment, value copy, or a one-off explicit
  copy when that contract is absent (not clone-for-convenience or a prototype
  registry).
- `pattern.flyweight`: measured memory value plus safe identity and lifetime
  semantics; otherwise allocate normally (interning is not object pooling).
- `pattern.memento`: explicit snapshot/restore contract with cost and aliasing
  rules; otherwise use an explicit copy or domain value.
- `pattern.interpreter`: real grammar, AST, semantics, and consumers; keep a
  closed set of direct operations when no general language is present.

### Boundary handoffs

- Route cancellation, pipelines, and fan-out/fan-in mechanics to
  `gopher:concurrency`.
- Route pooling to `gopher:performance` and require measurement before pooling.
