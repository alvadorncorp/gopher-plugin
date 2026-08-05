---
type: adr
id: adr:gopher:006
context: gopher
title: Add six capability peers and migrate the project contract to schema 2
status: Accepted
tags: [go, plugins, skills, doctor, resilience, observability, codegen, cgo, fuzz, config]
deciders: [Alvadorncorp]
date: 2026-08-05
---
# ADR-006: Add six capability peers and migrate the project contract to schema 2

## Context and Problem

Fourteen peer skills covered design, implementation, diagnosis, security, and
review. Six recurring Go engineering intents had no canonical owner, so each one
was absorbed by whichever adjacent skill was nearest rather than by a skill whose
workflow was written for it.

- **Proactive readiness.** "Is this project ready for the change I am about to
  make?" reached `gopher:diagnose`, whose entire protocol is built around
  reproducing an unexplained symptom and attributing a cause. Checking a written
  invariant needs neither reproduction nor a hypothesis.
- **Failure semantics.** Retries, idempotency, backoff, overload, degradation,
  and recovery split between `gopher:concurrency` and `gopher:performance`.
  Neither owns them: the first answers goroutine and synchronization mechanics,
  the second answers cost. A retry storm is neither.
- **Telemetry design.** Deciding what a service emits, at what cardinality and
  cost, reached `gopher:performance` because both touch `pprof`. Reading a
  captured profile and deciding to expose profiles continuously in production are
  different questions with different evidence.
- **Generated-code lifecycle**, **Go/C boundaries**, and **native fuzzing** all
  reached `gopher:developer`, whose contract is routine local implementation.
  Each carries a failure mode that local implementation guidance does not
  address: stale or nondeterministic output, a pointer that outlives its
  guarantee, and an unbounded campaign.

`adr:gopher:001` records that an ownership change must be recorded in a new ADR.
`adr:gopher:005` records that a change to the configuration schema is a schema
migration and needs its own ADR. Both obligations are discharged here.

## Decision Drivers

- One `primary_owner` per intent, with dominant-risk routing for mixed symptoms.
- Progressive disclosure: a small `SKILL.md` that selects focused references.
- A skill declares its modes, its terminal states, and its authorization
  boundary, and reports a limitation rather than an unqualified result.
- Discoverability never wins over ownership: when both pull, ownership wins.
- Additive routing. No existing owner loses work it is written to do.

## Considered Options

### Option 1: Six capability peers plus bounded extensions to two owners (chosen)

Add `gopher:doctor`, `gopher:resilience`, `gopher:observability`,
`gopher:codegen`, `gopher:cgo`, and `gopher:fuzz`. Give `gopher:architecture`
explicit `design`, `module-lifecycle`, and `migration` modes, and give
`gopher:test-quality` an explicit `quality-lab` mode. Adjust the adjacent owners'
negative boundaries so each new intent reaches its new owner.

**Pros:** each new owner has one failure mode and one evidence discipline; the
two extensions absorb intents that genuinely belong to an existing owner rather
than minting a skill for them; every boundary becomes testable in the routing
corpus.

**Cons:** twenty skills is a larger description surface to keep mutually
distinct, and six new owners must each be reachable from the owner that used to
absorb their intent.

### Option 2: Extend the existing owners instead of adding peers

Give `gopher:diagnose` a readiness mode, `gopher:concurrency` the failure
semantics, `gopher:performance` the telemetry design, and `gopher:developer` the
generated-code, CGO, and fuzzing work.

**Pros:** no new skills, no new descriptions to disambiguate, no routing corpus
growth.

**Cons:** it recreates exactly the problem `adr:gopher:005` solved by splitting
the combined concurrency/performance owner. `gopher:diagnose` would carry two
opposite protocols — reproduce-and-attribute for the unknown, and check-a-rule
for the known — and `gopher:developer` would carry three specialized failure
modes behind one routine-implementation description. Trigger overlap grows
faster than the skill count it avoids.

### Option 3: Fewer, broader peers

Add two skills instead of six: one "reliability" owner covering failure semantics
and telemetry, and one "build integrity" owner covering generated code, CGO, and
fuzzing.

**Pros:** half the descriptions; fewer boundaries to document.

**Cons:** each broad owner would hold intents whose evidence has nothing in
common. A telemetry cardinality budget and a circuit-breaker policy do not share
a workflow; a cgo pointer audit and a fuzz campaign share neither tooling nor
terminal states. The merged skills would need internal mode dispatch that is
indistinguishable from separate skills, minus the routing clarity.

### Option 4: Keep the configuration schema at version 1

Let each new skill document its policy inline in its own references and leave
`.gopher-plugin.toml` closed at seven canonical tables.

**Pros:** no schema migration, no fifth configuration state, no change to the
configuration contract test.

**Cons:** a fuzz budget, a doctor profile, and a workspace or replace policy are
exactly the kind of per-project policy the contract exists to carry. Documenting
them outside the contract means they cannot be set once for a repository, and it
would make `gopher:config` an incomplete account of what drives the workflows.

## Decision

**Chosen option: six capability peers plus bounded extensions to two owners, and
a migration of the project contract to schema version 2.**

### Ownership

- `gopher:doctor` owns proactive readiness against known invariants, in `check`,
  `hook`, and `explain` modes, terminating in `READY`, `WARN`, `BLOCKED`, or
  `LIMITED`. It performs no causal investigation and repairs nothing.
- `gopher:resilience` owns failure semantics, runtime safeguards, distributed
  degradation, recovery, and reliability assessment, in `runtime`,
  `distributed`, and `assessment` modes, terminating in `COMPLETE`,
  `COMPLETE_WITH_RISK`, or `BLOCKED`.
- `gopher:observability` owns telemetry design, instrumentation, and audit, in
  `design`, `instrument`, and `audit` modes, terminating in `COMPLETE`,
  `COMPLETE_WITH_LIMITATIONS`, or `BLOCKED`.
- `gopher:codegen` owns the lifecycle and trustworthiness of generated code, in
  `check`, `generate`, and `adopt` modes, terminating in `FRESH`, `STALE`,
  `NONDETERMINISTIC`, or `BLOCKED`.
- `gopher:cgo` owns Go/C boundaries, in `design`, `implement`, `audit`, and
  `build-matrix` modes, terminating in `COMPLETE`, `RISKS_FOUND`, or `BLOCKED`.
- `gopher:fuzz` owns native Go fuzzing, in `design`, `run`, `triage`, and
  `promote` modes, terminating in `PASS`, `CRASH`, `FLAKY`, `LIMITED`, or
  `BLOCKED`.

### The boundaries that make the split testable

- `gopher:doctor` answers whether a written invariant holds; `gopher:diagnose`
  keeps the symptom that needs reproduction and causal attribution before an
  owner can be named. A doctor finding whose cause is unexplained returns to
  `gopher:diagnose`.
- `gopher:resilience` states what must detect and contain a failure mode;
  `gopher:concurrency` keeps goroutine and synchronization mechanics, and
  `gopher:performance` keeps the cost of the work.
- `gopher:performance` keeps the interpretation of captured profiles and
  execution traces; `gopher:observability` owns the decision to emit and expose
  signals at all, with their cost and cardinality.
- `gopher:developer` keeps writing the generator's own code; `gopher:codegen`
  owns whether the checked-in output still matches its inputs. Hand-editing a
  generated file is never the remediation.
- `gopher:diagnose` keeps an unattributed crash at a Go/C boundary; `gopher:cgo`
  takes the attributed boundary work. The presence of `import "C"` is a keyword,
  not an attribution.
- `gopher:test-quality`'s `quality-lab` mode selects which technique falsifies a
  named risk; `gopher:fuzz` designs the target, the invariant, and the bounded
  campaign. A production fix that a campaign surfaces belongs to
  `gopher:developer` or the matching risk specialist.
- `gopher:security` takes the exposure of debug and profiling endpoints and the
  redaction rules for telemetry attributes, because both are authorization
  decisions about what may leave the process.
- `gopher:architecture` takes module lifecycle and sequenced migration;
  `gopher:modernize` keeps metadata, dependencies, and toolchain maintenance.

### Configuration

`.gopher-plugin.toml` moves to `schema_version = 2`. Three canonical tables are
added — `[doctor]`, `[fuzz]`, and `[architecture]` — and `[test-quality]` gains
`quality_lab_families`, whose value is the eligible set of techniques and never
an instruction to run all of them. Validation gains a fifth state,
`MIGRATION_AVAILABLE`: a file at an older but supported schema version is valid
to read and drives workflows on its own effective values, and it is migrated only
inside `gopher:config --bootstrap`, with a shown diff and explicit confirmation.
`UNSUPPORTED_VERSION` keeps its meaning of a future schema that is never
rewritten. Nothing migrates automatically.

### Scope held out

The `hook` mode of `gopher:doctor` is delivered as a documented contract —
automatic, bounded, fail-open, and read-only. No hook runtime and no host wiring
ship with it. This is stated in the skill's own references rather than implied.

## Consequences

**Positive:**

- Six intents gain a workflow written for them, with declared modes, terminal
  states, and authorization boundaries.
- `gopher:diagnose` and `gopher:developer` shed intents their contracts never
  described, and each keeps a sharper description.
- Per-project policy for readiness, fuzzing, and module lifecycle now lives in
  the one contract that already carries project policy.
- Every boundary added here is asserted by a routing corpus case, so a regression
  in a `description` shows up as a failing case rather than as silent drift.

**Negative:**

- Twenty descriptions must stay mutually distinct. Trigger overlap is now the
  dominant maintenance risk, and the routing corpus is the control for it.
- `schema_version = 2` is a breaking change to the configuration contract.
  Existing version-1 files keep working and report `MIGRATION_AVAILABLE`, but a
  project that pins the schema will see the new state.
- Six new packages add version-sensitive surface — OpenTelemetry semantic
  conventions, `runtime.Pinner` and `runtime/cgo.Handle` version gates, and
  `testing/synctest` availability — each of which is a maintenance obligation.

**Neutral / Follow-up actions:**

- Implement the `gopher:doctor` hook runtime and host wiring under its own plan
  and ADR when a host contract is settled.
- Assign the release version for this phase during packaging; this change leaves
  manifests untouched.
- Record future ownership changes in a new ADR.
