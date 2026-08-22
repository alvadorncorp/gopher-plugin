---
type: adr
id: adr:gopher:010
context: gopher
title: Add OpenCode npm packaging and harness adapters
status: Accepted
tags: [go, plugins, skills, opencode, npm]
deciders: [Alvadorncorp]
date: 2026-08-21
---
# ADR-010: Add OpenCode npm packaging and harness adapters

## Context and Problem

Gopher has native packaging for Codex, Claude Code, Grok Build, and Kimi Code.
OpenCode discovers skills from configured directories and loads executable plugins
from npm packages or local paths; it has no equivalent marketplace manifest.
The package must preserve the one physical Gopher skill tree, provide native role
agents, and document review/refactor delegation using OpenCode's `task` tool.

## Decision Drivers

- Keep `plugins/gopher/skills/` as the only physical skill tree.
- Support both npm publication and local path installation.
- Bind native OpenCode permissions without widening a user's configuration.
- Reuse the shared routing corpus and deterministic validation.

## Considered Options

### Option 1: npm package with config hook and native agents (chosen)

Publish `@alvadorncorp/gopher`. Its plugin hook registers the shared skill path
and three role agents. Local installation uses the same package by path.

**Pros:** first-class OpenCode lifecycle, no copied skills, and real permission
bindings for architecture and review roles.

**Cons:** adds a small JavaScript runtime adapter and an npm release artifact.

### Option 2: skills-path documentation only

Ask each user to add the repository skill path to their own configuration.

**Pros:** no runtime JavaScript.

**Cons:** no distributable package, no native agents, and no repeatable install
contract.

### Option 3: prefixed wrapper skills

Copy or generate `gopher-*` wrappers to avoid OpenCode skill-name collisions.

**Pros:** avoids collisions with user-defined skills.

**Cons:** adds a second physical tree and drift risk, rejected by
`adr:gopher:001`.

## Decision

**Chosen option: npm package with a config hook and native agents.**

- `package.json` publishes `@alvadorncorp/gopher`; local installation is also
  supported through an absolute package path.
- The hook adds the canonical `plugins/gopher/skills/` directory exactly once.
- Skills retain their canonical names, such as `review`; OpenCode does not add a
  `gopher:` namespace, so name collisions remain a documented user concern.
- `gopher-architect` and `gopher-developer` are subagents. `gopher-reviewer` is
  a primary agent with `edit: deny`, allowing it to dispatch read-only `explore`
  lens tasks without increasing global subagent depth.
- Review and refactor use dedicated OpenCode harness adapters. The shared forward
  runner parses `opencode run --format json` events under explicit no-write
  permissions.

## Consequences

**Positive:**

- OpenCode receives a supported local and npm install path.
- All five harnesses use the same twenty skills and one semantic corpus.
- OpenCode permission rules technically deny edits for architecture and review.

**Negative:**

- The package must remain compatible with OpenCode's plugin API.
- OpenCode skill names can conflict with user-defined skills of the same name.

**Neutral / Follow-up actions:**

- Keep publication operator-controlled; this change prepares but does not publish
  `@alvadorncorp/gopher`.
- Restart OpenCode after installation or update because plugins and skills load
  at startup.
