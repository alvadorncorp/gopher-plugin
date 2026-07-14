---
type: sdd
id: sdd:gopher:gopher_plugin
context: gopher
title: Package Go engineering workflows for Codex and Claude
status: Accepted
tags: [go, codex, claude, skills, marketplace]
related: [adr:gopher:001]
date: 2026-07-14
---
# SDD: Package Go engineering workflows for Codex and Claude

## Context and Drivers

Go engineering guidance is fragmented across generic knowledge, pattern
catalogs, and reviews without auditable lenses. The product must diagnose
before prescribing, favor idiomatic Go, require evidence for abstractions and
optimizations, and separate review from correction.

No approved PRD exists for this initiative. This gap is recorded here; no
`prd:` key is invented. The approved scope comes from the brainstorm design
and `adr:gopher:001`.

## Solution Overview

Publish marketplace `alvadorncorp` with plugin `gopher` version `0.1.0`.
Codex and Claude receive native manifests while loading the same physical tree
at `plugins/gopher/skills/`. Eight peer skills have canonical ownership and a
textual decision and handoff contract.

## Architecture

- **Components:** Codex/Claude marketplaces; plugin manifests; eight skills
  (`design-patterns`, `application-architecture`, `developer`, `architecture`,
  `concurrency-performance`, `diagnose`, `security`, `review`); references;
  validators; cross-harness corpus.
- **Data:** versioned Markdown, YAML, and JSON only. No database, production
  state, generated copies, or symlinks.
- **Integrations:** official `plugin-creator` and `skill-creator` scripts,
  native Codex/Claude validators, and local CLIs for forward tests.
- **End-to-end flows:** intent → primary owner → specialized workflow →
  proportional validation → handoff; vague symptom → `diagnose` → evidence →
  owner; diff → `review` → explicit lenses → consolidation → verdict.

## Ownership and Contracts

| Skill | Canonical ownership |
|---|---|
| `design-patterns` | language-agnostic code/module forces and patterns |
| `application-architecture` | language-agnostic internal application boundaries |
| `developer` | local Go implementation, APIs, errors, tests, and tooling |
| `architecture` | Go packages, modules, dependencies, and public contracts |
| `concurrency-performance` | lifecycle, synchronization, and measured performance |
| `diagnose` | evidence-based attribution without solution or editing |
| `security` | threats, reachability, safe verification, and remediation |
| `review` | read-only lens review, consolidation, and verdict |

Explicitly requested local and reversible changes may proceed. Cross-package,
public-contract, boundary, persistence, security-boundary, or ADR-affecting
changes require evidence, alternatives, and explicit approval before editing.

## Considered Alternatives

### Alternative 1: One physical tree with native packaging per harness

**Pros:** one content source, verifiable parity, and no content drift.
**Cons:** manifests and subagent adapters remain harness-specific.

### Alternative 2: Copied or generated trees per harness

**Pros:** each tree can use its own extensions.
**Cons:** duplicates content, creates drift, and requires a synchronization build.

### Alternative 3: Codex-only plugin with later compatibility

**Pros:** lower initial effort.
**Cons:** fails the approved cross-harness parity requirement.

## Key Decisions

- Use independent peer skills — recorded in `adr:gopher:001`.
- Use one physical tree and two marketplace/manifest formats.
- Use the project's declared Go version; use the current baseline only for a new project.
- Keep `review` read-only with exact selection across five lenses.
- Keep hooks, MCP, apps, LSP, and assets outside version `0.1.0`.

## Risks and Trade-offs

- Trigger overlap → ownership boundaries in descriptions and a routing corpus.
- Harness divergence → one corpus and comparison of semantic output fields.
- Stale Go guidance → official sources, `last_verified`, and version gates.
- Unavailable parallel review → explicit sequential degradation with the same output.
- Forward-test cost → execution under operator approval and budget.

## Evolution Plan

- Phase 1: packaging, eight skills, references, and structural validation.
- Phase 2: cross-harness forward tests and Rashomon corrections.
- After a real non-Go consumer exists: evaluate extracting `design-patterns`
  and `application-architecture` without changing handoff identifiers.
- After every stable Go release and at least quarterly: review
  version-sensitive sources and update `last_verified`.
