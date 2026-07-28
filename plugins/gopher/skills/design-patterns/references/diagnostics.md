# Catalog Diagnostics and Canonical Index

## Card schema

Every full card supplies: ID and aliases, problem, forces, direct baseline,
signals, counter-signals, mechanics, liabilities, useful combinations, and
validation questions. Diagnostic cards need evidence before selection.
Deferred cards require a concrete use case and new review before promotion.
Boundary cards select a concept while routing mechanics to the named owner.

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
| pattern.prototype | deferred | construction |
| pattern.flyweight | deferred | state-traversal |
| pattern.memento | deferred | state-traversal |
| pattern.interpreter | deferred | state-traversal |
| pattern.context-cancellation | boundary | gopher:concurrency |
| pattern.pipeline | boundary | gopher:concurrency |
| pattern.object-pool | boundary | gopher:performance |

Counts are normative: 19 full, 10 diagnostic, 4 deferred, and 3 boundary
candidates (36 total). No popularity ranking is implied.

## Diagnostic rules

- Return `no-pattern` when the direct baseline satisfies all forces.
- Require two active product families before recommending Abstract Factory.
- Require process-wide identity rather than convenience for Singleton.
- Require two independent variation axes for Bridge.
- Require distinct access/lazy/remote/lifecycle semantics for Proxy.
- Keep Service Locator, reflection-heavy injection, and global Registry as
  diagnostics unless a real runtime plugin ecosystem is demonstrated.
- Route cancellation, pipelines, and fan-out/fan-in mechanics to
  `gopher:concurrency`; route pooling to `gopher:performance` and require
  measurement before pooling.
