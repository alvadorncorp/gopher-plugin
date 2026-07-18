---
type: adr
id: adr:gopher:001
context: gopher
title: Adopt independent peer skills in the Gopher plugin
status: Accepted
tags: [go, plugins, skills, architecture]
deciders: [Alvadorncorp]
date: 2026-07-14
---
# ADR-001: Adopt independent peer skills in the Gopher plugin

## Context and Problem

The Gopher plugin must provide specialized Go engineering guidance while
loading only context relevant to the current request, keeping a central skill
from becoming a mandatory router, and preserving the future extraction of
language-agnostic knowledge. The same physical skill set must also work in the
native Codex and Claude packages.

Responsibilities include pattern selection, application architecture, Go
implementation, package architecture, concurrency and performance, diagnosis,
security, and review. Mixed requests need one primary owner and verifiable
handoffs.

## Decision Drivers

- Preserve progressive disclosure and independent intent-based loading.
- Keep `developer` focused instead of making it orchestrate every domain.
- Permit future extraction of language-agnostic knowledge without path dependencies.
- Keep ownership, authorization, output, and validation auditable.
- Share one physical skill tree between Codex and Claude.

## Considered Options

### Option 1: Independent peer skills with a lightweight textual contract

Each skill owns its triggers, routing boundaries, workflow, output format, and
validation. Integrations use stable identifiers and a textual contract;
exactly one skill owns the primary result. Only `review` acts as a bounded
orchestrator, and only for review requests.

**Pros:**

- Loads only knowledge relevant to the current intent.
- Preserves isolated installation and extraction boundaries.
- Makes ownership and handoffs testable.

**Cons:**

- Requires precise descriptions, a routing matrix, and overlap tests.
- Repeats a small intentional part of the textual contract across skills.

### Option 2: Hub-and-spoke with `developer` as orchestrator

A central skill classifies every Go request and invokes specialists.

**Pros:**

- Provides one obvious entry point.
- Centralizes initial routing.

**Cons:**

- Loads unrelated context and tends to become a god skill.
- Creates rigid dependencies and duplicates specialist rules.

### Option 3: Shared kernel consumed by every skill

Contracts, baselines, and common rules live in shared resources.

**Pros:**

- Reduces textual repetition.

**Cons:**

- Couples installation, caching, and extraction to cross-skill paths.
- Makes every kernel change affect all skills at once.

## Decision

**Chosen option: Independent peer skills with a lightweight textual contract**

We chose eight independent peers because progressive disclosure, isolated
installation, and future extraction are priority drivers that a hub or shared
kernel does not preserve. The skills are `design-patterns`,
`application-architecture`, `developer`, `architecture`,
`concurrency-performance`, `diagnose`, `security`, and `review`.

A request has exactly one `primary_owner`. Handoffs use `gopher:<skill>`
identifiers and an adaptive textual contract. `diagnose` attributes and stops
without implementation. `review` remains read-only and orchestrates only the
explicitly selected lenses.

## Consequences

**Positive:**

- Each skill remains independently usable and validatable.
- Language-agnostic knowledge can be extracted without migrating a shared runtime.
- Routing, authorization, and output become observable in tests.
- Codex and Claude consume the same physical skill tree.

**Negative:**

- Descriptions and routing boundaries require careful overlap maintenance.
- The short textual contract appears in more than one skill.
- Review needs harness-specific adapters.

**Neutral / Follow-up actions:**

- Maintain forward tests for positive routing, negative routing, and handoffs.
- Revisit extraction of `design-patterns` only after a real non-Go consumer exists.
- Record future ownership changes in a new ADR.

---

*References: `.plans/gopher-plugin/design.md` and `.plans/gopher-plugin/interview.md` (planning sources ignored by Git)*

*Amended by `adr:gopher:002` — permits `gopher:refactor` as a second bounded orchestrator.*
