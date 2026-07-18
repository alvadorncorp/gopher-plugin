---
type: adr
id: adr:gopher:002
context: gopher
title: Permit gopher:refactor as a second bounded orchestrator
status: Accepted
tags: [go, plugins, skills, architecture, refactoring]
deciders: [Alvadorncorp]
date: 2026-07-17
---
# ADR-002: Permit gopher:refactor as a second bounded orchestrator

## Context and Problem

ADR-001 adopted independent peer skills with exactly one `primary_owner` per
request and named `review` as the only bounded orchestrator, and only for
review requests. The Gopher plugin now adds four specialist owners (`config`,
`complexity`, `test-quality`, `modernize`) and needs a way to run
repository-wide or multidimensional refactoring that establishes a safety
baseline, sequences remediation across dimensions, and compares before/after
evidence. No single specialist owns cross-dimensional sequencing, and routing
all such work through `developer` would rebuild the god skill ADR-001 rejected.
A decision is required on whether a second orchestrator is admissible without
breaking the independent-peer model.

## Decision Drivers

- Preserve independent, intent-matched peers and progressive disclosure.
- Keep exactly one `primary_owner` per request.
- Keep `review` read-only and lens-bounded.
- Make repository-wide refactoring safe and measurable through baselines, tests,
  proportional authorization, and like-for-like metrics.
- Avoid a central router that loads unrelated context.

## Considered Options

### Option 1: Add gopher:refactor as a second bounded orchestrator

A new peer bounded to refactor-type requests only. It captures an immutable
baseline, gathers read-only per-dimension analysis, prioritizes, and sequences
mutating phases, recording and following specialist handoffs instead of
performing work owned elsewhere.

**Pros:**

- Gives repository-wide refactoring an explicit, safe, measurable owner.
- Preserves one primary owner and independent specialist ownership via handoffs.
- Leaves `review` read-only and every specialist canonical.

**Cons:**

- Introduces a second orchestrator, so "only review orchestrates" no longer holds.
- Adds routing-overlap surface that the corpus must cover.

### Option 2: Fold repository-wide refactoring into gopher:developer

`developer` orchestrates cross-dimensional refactoring in addition to local work.

**Pros:**

- Adds no new skill.

**Cons:**

- Rebuilds the hub-and-spoke god skill ADR-001 rejected.
- Blurs local implementation with repository-wide assessment and sequencing.

### Option 3: Extend gopher:review to apply fixes

`review` gains a mutating repository-wide refactoring mode.

**Pros:**

- Reuses the existing bounded orchestrator.

**Cons:**

- Breaks ADR-001's read-only review invariant.
- Couples analysis with correction in one skill.

## Decision

**Chosen option: Add gopher:refactor as a second bounded orchestrator**

We admit exactly one more named bounded orchestrator, `gopher:refactor`, scoped
to repository-wide or multidimensional refactoring, in the same way `review` is
scoped to review requests. This amends ADR-001's "only review orchestrates"
consequence to "review and refactor are the two bounded orchestrators" while
preserving every other ADR-001 decision:

- The thirteen skills remain independent peers; `refactor` is not a hub that
  routes all requests.
- A request still has exactly one `primary_owner`; `refactor` records and
  follows specialist handoffs rather than absorbing ownership.
- `review` stays read-only and lens-bounded; `refactor`'s final review runs
  `gopher:review` read-only and cannot apply fixes.

## Consequences

**Positive:**

- Repository-wide refactoring gains a safe, measurable, single owner.
- Specialist ownership and one-primary-owner routing are preserved.
- The read-only review boundary is intact.

**Negative:**

- Two orchestrators exist, requiring clear refactor-versus-review and
  refactor-versus-specialist routing in descriptions and the forward corpus.

**Neutral / Follow-up actions:**

- Extend the routing corpus with positive, negative, overlap, and handoff cases
  for `refactor` and the four new specialists.
- Record any further orchestrator changes in a new ADR.

---

*Amends `adr:gopher:001`. References: `.plans/gopher-python-refactoring-parity/design.md` and `.plans/gopher-python-refactoring-parity/interview.md` (planning sources ignored by Git).*
