---
type: adr
id: adr:gopher:004
context: gopher
title: Add native Kimi Code packaging and harness adapters
status: Accepted
tags: [go, plugins, skills, kimi, marketplace]
deciders: [Alvadorncorp]
date: 2026-07-28
---
# ADR-004: Add native Kimi Code packaging and harness adapters

## Context and Problem

Gopher ships one physical skill tree with native packaging for Codex, Claude
Code, and Grok Build (`adr:gopher:001`, `adr:gopher:003`). Kimi Code loads the
same `SKILL.md` skill format, but it has its own plugin manifest
(`.kimi-plugin/plugin.json`) and custom marketplace catalog format, review and
refactor need a documented subagent adapter for the host, and structural tests
only assert triple-harness parity.

## Decision Drivers

- Preserve one physical skill tree and avoid generated or copied content trees.
- Publish a native marketplace and plugin manifest that Kimi Code reads through
  its documented `/plugins install` and `/plugins marketplace` flows.
- Keep review and refactor orchestration portable across hosts with explicit
  adapters for fan-out, degradation, and retry.
- Extend deterministic packaging and routing validation without requiring live
  model execution in CI.

## Considered Options

### Option 1: Native Kimi packaging plus harness adapters (chosen)

Add `.kimi-plugin/marketplace.json`, `plugins/gopher/.kimi-plugin/plugin.json`,
and `review`/`refactor` adapters under `references/harnesses/kimi.md`. Keep
Codex, Claude, and Grok packaging unchanged. Extend structural and forward-test
harness lists to four hosts.

**Pros:** first-class install path, explicit orchestration contract, parity with
the existing multi-host design.

**Cons:** four marketplace/manifest formats to keep identity-aligned.

### Option 2: Skills-only installation without packaging

Document that Kimi users load `plugins/gopher/skills/` through `--skills-dir`
and skip native packaging.

**Pros:** no new manifest or marketplace files.

**Cons:** no first-class plugin identity, no marketplace path, and no managed
install or update flow through `/plugins`.

### Option 3: Fork a Kimi-only skill tree

Copy or generate skills under a Kimi-specific package.

**Pros:** free to diverge per host.

**Cons:** content drift and synchronization cost rejected by `adr:gopher:001`.

## Decision

**Chosen option: Native Kimi packaging plus harness adapters.**

- Marketplace identity remains `alvadorncorp`; plugin identity remains `gopher`.
- Shared fields (`name`, `version`, `description`, `author`) stay aligned across
  Codex, Claude, Grok, and Kimi manifests. The Kimi catalog keeps the documented
  `version: "2"` envelope with a per-plugin `id`/`source` entry.
- `gopher:review` and `gopher:refactor` load `references/harnesses/kimi.md` on
  Kimi Code, using the `Agent`/`AgentSwarm` subagent tools, parallel fan-out
  when available, sequential degradation, and one retry.
- The Kimi forward-test harness runs `kimi -p --output-format stream-json` and
  extracts the structured payload from assistant output because the CLI has no
  schema-enforcement flag.
- Version `0.2.2` records the fourth-host packaging expansion without changing
  skill ownership or introducing hooks, MCP, apps, LSP, or assets.

## Consequences

**Positive:**

- Kimi Code install and validation match the documented first-class path.
- Orchestrators have an explicit Kimi adapter with the same degradation rules.
- Structural tests enforce quad-harness packaging parity.

**Negative:**

- Release tooling and identity checks must track four manifests and
  marketplaces.

**Neutral / Follow-up actions:**

- Keep live forward tests (`--harness kimi`) operator-gated like the other
  hosts.
