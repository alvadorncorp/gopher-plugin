---
type: sdd
id: sdd:gopher:gopher_plugin
context: gopher
title: Package Go engineering workflows for Codex, Claude, and Grok
status: Accepted
tags: [go, codex, claude, grok, skills, marketplace]
related: [adr:gopher:001, adr:gopher:002, adr:gopher:003, adr:gopher:004, adr:gopher:005, adr:gopher:006, adr:gopher:007, adr:gopher:008, adr:gopher:009]
date: 2026-07-14
---
# SDD: Package Go engineering workflows for Codex, Claude, and Grok

## Context and Drivers

Go engineering guidance is fragmented across generic knowledge, pattern
catalogs, and reviews without auditable lenses. The product must diagnose
before prescribing, favor idiomatic Go, require evidence for abstractions and
optimizations, and separate review from correction.

No approved PRD exists for this initiative. This gap is recorded here; no
`prd:` key is invented. The approved scope comes from the brainstorm design
and `adr:gopher:001`, with the third host recorded in `adr:gopher:003`.

## Solution Overview

Publish marketplace `alvadorncorp` with plugin `gopher` version `0.5.1`.
Codex, Claude, and Grok receive native manifests while loading the same physical
tree at `plugins/gopher/skills/`. Twenty peer skills have canonical ownership
and a textual decision and handoff contract. A `.gopher-plugin.toml` project
contract, owned by `gopher:config`, carries thresholds, tool policy, and
refactoring safeguards for the quality workflows; it is at schema version `5`
and reports a version-`1`, version-`2`, version-`3`, or version-`4` file as
`MIGRATION_AVAILABLE`. The `[developer]` policy carries idiom and test-workflow
choices, resolved independently by session, file, adopted project policy, then
default. The `[workflow]` policy carries planning preflight hints and
post-implementation review defaults as session policy only (no hooks).
Versions `1`–`4` remain `MIGRATION_AVAILABLE`. Three
packaged role agents wrap `gopher:developer`, `gopher:architecture`, and
`gopher:review` with a fixed per-role binding.

## Architecture

- **Components:** Codex/Claude/Grok marketplaces; plugin manifests; twenty
  skills (`design-patterns`, `application-architecture`, `developer`,
  `architecture`, `concurrency`, `performance`, `diagnose`, `security`,
  `review`, `config`, `complexity`, `test-quality`, `modernize`, `refactor`,
  `doctor`, `resilience`, `observability`, `codegen`, `cgo`, `fuzz`);
  references; three packaged role agents (`developer`, `architect`, `reviewer`)
  in Claude/Grok markdown and Codex TOML form; validators; cross-harness corpus.
- **Data:** versioned Markdown, YAML, and JSON only. No database, production
  state, generated copies, or symlinks.
- **Integrations:** official `plugin-creator` and `skill-creator` scripts,
  native Codex/Claude/Grok validators, and local CLIs for forward tests.
- **End-to-end flows:** intent → primary owner → specialized workflow →
  proportional validation → handoff; unexplained symptom → `diagnose` → evidence →
  owner; diff → `review` → explicit lenses → consolidation → verdict.

## Ownership and Contracts

| Skill | Canonical ownership |
|---|---|
| `design-patterns` | language-agnostic code/module forces and patterns |
| `application-architecture` | language-agnostic internal application boundaries |
| `developer` | local Go implementation, APIs, errors, tests, and tooling |
| `architecture` | Go packages, modules, dependencies, and public contracts |
| `concurrency` | goroutine lifecycle, synchronization, cancellation, and backpressure mechanics |
| `performance` | algorithmic cost, allocation, GC, and measured sequential performance |
| `diagnose` | evidence-based attribution without solution or editing |
| `security` | threats, reachability, safe verification, and remediation |
| `review` | read-only lens review, consolidation, and verdict |
| `config` | `.gopher-plugin.toml` bootstrap, validation, explanation, and schema evolution |
| `complexity` | complexity measurement, hotspots, reduction, trends, and CI guidance |
| `test-quality` | coverage, mutation, test effectiveness, and refactoring safety nets |
| `modernize` | declared-version Go language, API, module, dependency, and toolchain modernization |
| `refactor` | repository-wide or multidimensional refactoring orchestration and evidence |
| `doctor` | proactive readiness against known invariants, with one owner per finding |
| `resilience` | failure semantics, runtime safeguards, degradation, recovery, and residual risk |
| `observability` | telemetry contracts, instrumentation boundaries, and signal audit |
| `codegen` | generated-output provenance, reproduction, staleness, and verification |
| `cgo` | Go/C boundary representation, ownership, pointers, threads, and build matrix |
| `fuzz` | native fuzz targets, corpora, bounded campaigns, triage, and promotion |

The packaged role agents add no ownership row. Each one's `primary_owner` is the
skill it wraps, and the shipped definition is the authoritative binding because
the host reads it at load time. The `[agents]` table of the project contract is a
declared policy that narrows an agent and never widens one. Kimi Code discards
packaged agents, so its review and refactor adapters reproduce the same
constraint envelope inline.

Explicitly requested local and reversible changes may proceed. Cross-package,
public-contract, boundary, persistence, security-boundary, or ADR-affecting
changes require evidence, alternatives, and explicit approval before editing.

The developer owns local Go implementation, APIs, errors, tests, and tooling.
Its evidence flow records the selected idiom policy and policy source, declared
Go-version compatibility, baseline conventions, and test evidence before
handoff. `adaptive-tdd` selects the smallest useful red-green-refactor loop for
the change while keeping modernization specialist-owned.

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
- Permit `gopher:refactor` as a second bounded orchestrator — recorded in `adr:gopher:002`.
- Use one physical tree and native marketplace/manifest formats per host
  (Codex, Claude, Grok) — third host recorded in `adr:gopher:003`.
- Use the project's declared Go version; use the current baseline only for a new project.
- Keep `review` read-only with exact selection across seven lenses.
- Keep hooks, MCP, apps, LSP, and assets outside version `0.3.0`.
- Add six capability peers (`doctor`, `resilience`, `observability`, `codegen`,
  `cgo`, `fuzz`) and give `architecture` and `test-quality` explicit modes
  instead of widening an existing owner — recorded in `adr:gopher:006`.
- Migrate the project contract to schema version `2` with a fifth configuration
  state, `MIGRATION_AVAILABLE` — recorded in `adr:gopher:006`, as
  `adr:gopher:005` required for any schema migration.
- Package three role agents as thin skill wrappers with a fixed per-role binding,
  adding no owner and no orchestrator — recorded in `adr:gopher:007`.
- Migrate the project contract to schema version `3` with the `[agents]`
  declared-policy table — recorded in `adr:gopher:007`, as `adr:gopher:005`
  required for any schema migration.
- Add the bounded `[developer]` policy and migrate the project contract to
  schema version `4`, preserving opt-in migration for versions `1`–`3` —
  recorded in `adr:gopher:008`, as `adr:gopher:005` requires for any schema
  migration.
- Add schema version `5` with the `[workflow]` session policy table and the
  planning→implementation→review skill-mode loop, preserving opt-in migration
  for versions `1`–`4` — recorded in `adr:gopher:009`, as `adr:gopher:005`
  requires for any schema migration.

## Risks and Trade-offs

- Trigger overlap → ownership boundaries in descriptions and a routing corpus.
- Harness divergence → one corpus and comparison of semantic output fields.
- Stale Go guidance → official sources, `last_verified`, and version gates.
- Unavailable parallel review → explicit sequential degradation with the same output.
- Forward-test cost → execution under operator approval and budget.
- Declared agent policy the host cannot apply → `policy_status` reporting plus the
  `agents.policy-declared` readiness rule.
- Kimi discards packaged agents → the constraint envelope duplicated inline in
  both Kimi adapters, with its presence enforced by test.

## Evolution Plan

- Phase 1: packaging, eight skills, references, and structural validation.
- Phase 2: cross-harness forward tests and Rashomon corrections.
- Phase 3: five new peers (`config`, `complexity`, `test-quality`, `modernize`, `refactor`), the `.gopher-plugin.toml` contract, and `adr:gopher:002` — version `0.2.0`.
- Phase 4: native Grok packaging and harness adapters (`adr:gopher:003`) —
  version `0.2.2`.
- Phase 5: split the combined concurrency/performance owner into `concurrency`
  and `performance`, add the `complexity` review lens (`adr:gopher:005`) —
  version `0.3.0`.
- Phase 6: six capability peers (`doctor`, `resilience`, `observability`,
  `codegen`, `cgo`, `fuzz`), explicit modes for `architecture` and
  `test-quality`, and configuration schema `2` (`adr:gopher:006`). The release
  version for this phase is not yet assigned; packaging and manifests are
  unchanged by it.
- Phase 7: three packaged role agents, the `[agents]` policy table at schema `3`,
  the Kimi inline fallback, and the `agents.policy-declared` readiness rule
  (`adr:gopher:007`) — version `0.4.0`, already carried by every manifest and by
  every versioned marketplace catalog.
- Phase 8: adaptive developer policy, schema `4`, migration compatibility for
  versions `1`–`3`, and the developer evidence flow (`adr:gopher:008`) — the
  existing `0.5.1` release state.
- Phase 9: planning and development skill loop with schema version `5`
  `[workflow]` policy (`architecture:triage`, `refactor:plan`, developer
  `from_slice`/fast paths, review `auto`/`delta`/`fix_queue`), opt-in
  migration for versions `1`–`4`, and no hook runtime (`adr:gopher:009`).
- After a real non-Go consumer exists: evaluate extracting `design-patterns`
  and `application-architecture` without changing handoff identifiers.
- After every stable Go release and at least quarterly: review
  version-sensitive sources and update `last_verified`.
