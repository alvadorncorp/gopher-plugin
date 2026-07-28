---
type: adr
id: adr:gopher:003
context: gopher
title: Add native Grok packaging and harness adapters
status: Accepted
tags: [go, plugins, skills, grok, marketplace]
deciders: [Alvadorncorp]
date: 2026-07-28
---
# ADR-003: Add native Grok packaging and harness adapters

## Context and Problem

Gopher already ships one physical skill tree with native packaging for Codex and
Claude Code (`adr:gopher:001`). Grok Build can discover Claude-compatible
marketplace and plugin manifests as a fallback, but that is not a first-class
public contract: the host's primary index is `.grok-plugin/marketplace.json`,
review and refactor need a documented subagent adapter, and structural tests only
assert dual-harness parity.

## Decision Drivers

- Preserve one physical skill tree and avoid generated or copied content trees.
- Publish a native marketplace and plugin manifest that Grok reads without
  relying on Claude compatibility.
- Keep review and refactor orchestration portable across hosts with explicit
  adapters for fan-out, degradation, and retry.
- Extend deterministic packaging and routing validation without requiring live
  model execution in CI.

## Considered Options

### Option 1: Native Grok packaging plus harness adapters (chosen)

Add `.grok-plugin/marketplace.json`, `plugins/gopher/.grok-plugin/plugin.json`,
and `review`/`refactor` adapters under `references/harnesses/grok.md`. Keep
Codex and Claude packaging unchanged. Extend structural and forward-test harness
lists to three hosts.

**Pros:** first-class install path, explicit orchestration contract, parity with
existing dual-host design.

**Cons:** three marketplace/manifest formats to keep identity-aligned.

### Option 2: Rely only on Claude compatibility

Document that Grok should load the Claude marketplace and skip native files.

**Pros:** minimal packaging work.

**Cons:** depends on a compatibility path, omits Grok-native install docs, and
leaves multi-lens review without a Grok adapter.

### Option 3: Fork a Grok-only skill tree

Copy or generate skills under a Grok-specific package.

**Pros:** free to diverge per host.

**Cons:** content drift and synchronization cost rejected by `adr:gopher:001`.

## Decision

**Chosen option: Native Grok packaging plus harness adapters.**

- Marketplace identity remains `alvadorncorp`; plugin identity remains `gopher`.
- Shared fields (`name`, `version`, `description`, `author`) stay aligned across
  Codex, Claude, and Grok manifests.
- `gopher:review` and `gopher:refactor` load `references/harnesses/grok.md` on
  Grok Build, using `spawn_subagent`, parallel fan-out when available, sequential
  degradation, and one retry.
- Version `0.2.2` records the third-host packaging expansion without changing
  skill ownership or introducing hooks, MCP, apps, LSP, or assets.

## Consequences

**Positive:**

- Grok install and validation match the documented first-class path.
- Orchestrators have an explicit Grok adapter with the same degradation rules.
- Structural tests enforce triple-harness packaging parity.

**Negative:**

- Release tooling and identity checks must track three manifests and marketplaces.

**Neutral / Follow-up actions:**

- Keep live forward tests (`--harness grok`) operator-gated like Codex and Claude.
- Optionally publish `plugin-index.json` later for richer marketplace browsing.
