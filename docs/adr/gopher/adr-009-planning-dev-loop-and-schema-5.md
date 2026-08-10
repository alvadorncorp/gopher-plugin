---
type: adr
id: adr:gopher:009
context: gopher
title: Planning and development skill loop with schema 5 workflow policy
status: Accepted
tags: [go, plugins, architecture, refactor, developer, review, config, schema]
deciders: [Alvadorncorp]
date: 2026-08-10
---
# ADR-009: Planning and development skill loop with schema 5 workflow policy

## Context and Problem

Architecture and refactor skills were weak as planning entry points; developer
and review skills lacked first-class post-implementation loop hooks. Session
auto-trigger policy had no project contract representation, and hook runtime
remains intentionally unshipped.

## Decision Drivers

- Preserve ADR-001 independent peers and single primary owner.
- Preserve ADR-002: only `review` and `refactor` are bounded orchestrators.
- Prefer opt-in automation defaults that fail safe (`post_implementation_review = off`).
- Keep installable package free of hook executables.

## Considered Options

### Schema v5 `[workflow]` + skill modes (chosen)

Add `architecture:triage`, `refactor:plan`/`PLAN_READY`, developer `from_slice`/
fast paths, review `auto`/`delta`/`fix_queue`, and a `[workflow]` policy table.

### Hook-driven skill auto-dispatch (rejected)

Would require runtime assets excluded from the package and risks a central
router (ADR-001).

### Prose-only descriptions without schema (rejected)

Improves routing somewhat but cannot express per-repo policy for auto review.

## Decision

Accept schema version 5 with `[workflow]` keys documented in
`gopher:config` schema. Skill modes and output contracts from the core four
skills form a planning→implementation→review loop without adding orchestrators.
Versions 1–4 remain `MIGRATION_AVAILABLE` via confirmed bootstrap.

## Consequences

- Projects can opt into `post_implementation_review = auto` without hooks.
- Forward corpus and contract tests guard routing and markers.
- Hook mode remains a doctor contract only until a future delivery ships runtime.
