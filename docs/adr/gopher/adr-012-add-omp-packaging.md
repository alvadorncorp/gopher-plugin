---
type: adr
id: adr:gopher:012
context: gopher
title: Add omp catalog packaging and task-based adapters
status: Accepted
tags: [go, plugins, skills, omp, marketplace]
deciders: [Alvadorncorp]
date: 2026-09-02
---
# ADR-012: Add omp catalog packaging and task-based adapters

## Context and Problem

omp (Oh My Pi) is a sixth host that installs Claude-compatible marketplace
plugins. It reads a catalog at `.omp-plugin/marketplace.json` before falling
back to `.claude-plugin/marketplace.json`, discovers skills at
`<plugin>/skills/*/SKILL.md` under their bare frontmatter names, and discovers
task agents at `<plugin>/agents/*.md` under its own frontmatter contract.
Gopher needs a native omp port without forking the shared skill tree.

Three omp facts shape the decision. First, the only plugin-manifest key omp
reads from `.omp-plugin/plugin.json` is `mcpServers`, and Gopher ships no MCP
servers, so an omp plugin manifest would be inert; install version resolution
reads the catalog entry, then `.claude-plugin/plugin.json`, `plugin.json`, and
`package.json`. Second, omp binds no packaged agent model, effort, or tool
restriction: its agent parser ignores `disallowedTools`, `skills`, `effort`,
and `color`, and matches a `model` value such as `opus` against no selector, so
the read-only `reviewer` role arrives unbound and shadows omp's bundled agent
of the same name. Third, omp namespaces no skill, so a same-named skill from
another installed plugin can win by provider precedence; a
`skills.customDirectories` entry overrides the same-named provider skill.

## Decision Drivers

- One physical skill tree at `plugins/gopher/skills/` (`adr:gopher:001`).
- Marketplace identity stays `alvadorncorp`; plugin identity stays `gopher`.
- The packaged agent envelope must hold on every host that loads it, or the
  adapter must restate it inline (`adr:gopher:007` precedent).
- No hooks, MCP servers, apps, LSP servers, or runtime visual assets.
- Cross-harness forward tests must cover omp like every other host.

## Considered Options

### Option 1: Catalog-only packaging with Kimi-shaped adapters (chosen)

**Pros:** one new catalog file; zero new runtime surface; version inherits the
release-engine-managed `.claude-plugin/plugin.json`; adapters restate the agent
envelope inline exactly where Kimi already does.
**Cons:** omp users get no enforced packaged-agent binding, and bare skill
names remain collision-prone.

### Option 2: Ship an omp plugin manifest and omp-dialect agents

**Pros:** an omp-native agent dialect could bind tools and models exactly.
**Cons:** the `.omp-plugin/plugin.json` manifest is inert outside `mcpServers`;
an omp-dialect agent file placed in `plugins/gopher/agents/` would also load
into Claude Code and Grok Build, which read the same directory, doubling the
roster on those hosts.

### Option 3: Fork an omp-only skill tree

**Pros:** omp-specific content freedom.
**Cons:** duplicates content and creates drift, rejected by `adr:gopher:001`.

## Decision

**Chosen option: Option 1, catalog-only packaging with Kimi-shaped adapters.**

- Marketplace identity stays `alvadorncorp`; plugin identity stays `gopher`.
- `.omp-plugin/marketplace.json` declares no `version`, so omp resolves the
  installed version from `plugins/gopher/.claude-plugin/plugin.json`, which the
  release engine already bumps.
- Skills load bare-named from the shared tree; the README documents the
  collision hazard and the `skills.customDirectories` remedy.
- omp discovers the packaged markdown agents but binds none of their model,
  effort, or tool keys, so the omp review and refactor adapters restate the
  constraint envelope inline and dispatch bundled read-only `scout` children
  through omp's `task` tool.
- `gopher:review` and `gopher:refactor` load `references/harnesses/omp.md`.
- The forward-test runner invokes `omp -p --mode json --tools read` and parses
  the assistant text from the NDJSON event stream; a temporary config overlay
  pins the repository's skill tree through `skills.customDirectories` so a
  same-named plugin cannot answer for a Gopher skill during measurement.

## Consequences

**Positive:**

- omp installs Gopher with two commands and inherits version discipline from
  the existing manifest with no new drift surface.
- The omp adapters carry the whole envelope inline, enforced by
  `tests/test_agents.py`, so a declared policy is never presented as applied.
- The catalog-version parity test now also gates the three pre-existing
  catalogs that pin a version.

**Negative:**

- omp users who dispatch the discovered `developer`, `architect`, or `reviewer`
  roles get session tools and models instead of the packaged binding, and
  Gopher's `reviewer` shadows omp's bundled agent; the README documents
  `task.disabledAgents` as the remedy.

**Neutral / Follow-up actions:**

- Revisit omp-dialect agents if omp grows manifest-driven agent path remapping
  or honors disallowed-tool keys.
- Keep the forward-runner overlay aligned with omp's config overlay format.

Version 6 of the host matrix: omp joins without changing skill ownership and
without introducing hooks, MCP, apps, LSP, or assets.
