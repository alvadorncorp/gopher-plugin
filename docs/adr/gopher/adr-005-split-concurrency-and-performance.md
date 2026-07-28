---
type: adr
id: adr:gopher:005
context: gopher
title: Split concurrency and performance into independent peer skills
status: Accepted
tags: [go, plugins, skills, concurrency, performance]
deciders: [Alvadorncorp]
date: 2026-07-28
---
# ADR-005: Split concurrency and performance into independent peer skills

## Context and Problem

The retired combined concurrency/performance skill owned two dimensions that fail for different
reasons and demand different evidence. Goroutine lifetime and synchronization
are answered by race detection, goroutine dumps, and contention profiles.
Asymptotic cost, allocation, and GC are answered by benchmarks over an
input-size series, one attributing profile, and a bounded execution trace only
for a timeline question.

Sequential performance was the under-served half. The plugin carried no
concrete `testing.B`, `-benchmem`, profile-generation, `go tool pprof`, or
`go tool trace` protocol, and Go code whose runtime is quadratic, cubic, or
otherwise super-linear had no explicit owner. A request to make existing Go code
faster reached a skill whose workflow was written around concurrency
correctness.

`adr:gopher:001` records that future ownership changes must be recorded in a new
ADR.

## Decision Drivers

- One primary owner per request, with dominant-risk routing for mixed symptoms.
- Evidence-first analysis that avoids speculative optimization.
- Progressive disclosure: a small main file that selects focused references.
- Asymptotic cost kept distinct from the cyclomatic and cognitive complexity
  owned by `gopher:complexity`.

## Considered Options

### Option 1: Two peer skills with a symptom-gated evidence ladder (chosen)

Replace the combined owner with `gopher:concurrency` and `gopher:performance`.
`gopher:performance` analyzes and produces an optimization plan, then hands
local implementation to `gopher:developer`. Its references are tiered: a
claim-to-probe router, a benchmark protocol, a profiling protocol, three
technique tiers, and a declared-Go-version guard table.

**Pros:** each skill has one failure mode and one evidence discipline; the
technique catalog gains concrete Go guidance without becoming a checklist.

**Cons:** a breaking change for anyone invoking the combined skill directly; the
version guard table needs maintenance per Go release.

### Option 2: Fixed linear tool ladder plus a literal optimization cookbook

Keep one owner and always run correctness checks, benchmarks, `pprof`, and an
execution trace in that order, driven by a checklist of named transformations.

**Pros:** easy to teach, audit, and cover with positive routing cases; fewest
files.

**Cons:** official Go diagnostics states an execution trace is not the preferred
tool for CPU or memory hot spots, so a fixed ladder collects evidence that
answers no question. A checklist also encourages speculative rewrites, because
most entries are conditional on ordering, duplicates, aliasing, output size,
update frequency, input distribution, Go version, and memory budget.

### Option 3: Three skills, separating algorithmic from runtime performance

Create one owner for algorithms and data structures and another for allocation,
compiler, GC, and operational tuning.

**Pros:** narrower context per skill; runtime and version maintenance could
evolve independently.

**Cons:** a single investigation commonly crosses both dimensions, which
produces ownership churn and ambiguous primary-owner routing, and expands the
ADR, lens, and test surface without demonstrated need.

### Option 4: Configuration-driven performance policy

Add a `[performance]` table to `.gopher-plugin.toml` with thresholds, required
tools, run counts, and workload presets, and make the evidence ladder enforce
them.

**Pros:** repeatable in CI; centralized policy; a path to regression gates.

**Cons:** the configuration schema is deliberately closed at seven canonical
tables, so this is a schema migration rather than an additive change. Universal
latency, throughput, or memory defaults also contradict the workload-specific
trade-offs this plugin accepts.

## Decision

**Chosen option: two peer skills with a symptom-gated evidence ladder.**

- `gopher:concurrency` owns goroutine lifetime, channels, synchronization,
  atomics, context, races, deadlocks, leaks, and backpressure.
- `gopher:performance` owns asymptotic and algorithmic cost, data structures,
  allocations, GC, cache behavior, parsing, I/O amplification, benchmarking,
  profiling, latency, and throughput when concurrency is not the dominant risk.
- `gopher:performance` analyzes and plans; it does not edit production code.
  Local reversible implementation goes to `gopher:developer` with the exact
  before and after verification attached. An independent revalidation happens
  when the user asks for it.
- Evidence is collected one discriminating diagnostic at a time, because precise
  memory profiling can skew a CPU profile and block profiling can affect a
  scheduler trace. An execution trace is reserved for a latency, scheduling,
  utilization, syscall or network wait, blocking, or GC-timeline question.
- Every technique entry states semantic preconditions, expected rather than
  guaranteed cost, a Go version guard where one applies, failure modes, the
  evidence required, and the implementation owner. No entry claims a fixed
  speedup, a universal slice-versus-map crossover threshold, an allocation count
  as a latency predictor, or a complexity class inferred from one benchmark
  point.
- `gopher:review` replaces the combined lens with independently selectable
  `concurrency`, `performance`, and `complexity` lenses; `--mode full` selects
  seven.
- `gopher:refactor` stays a bounded multidimensional orchestrator and gains two
  handoff rows rather than owning a performance dimension.
- The retired combined skill is removed with no compatibility facade.

## Consequences

**Positive:**

- Each owner has one failure mode, one evidence discipline, and one description
  to keep clear of its peer.
- Sequential performance gains a concrete, version-guarded protocol that the
  plugin previously lacked.
- Asymptotic cost and maintainability complexity are measured by different
  lenses and owned by different skills.

**Negative:**

- A direct invocation of the retired combined skill stops working. This is
  accepted; version `0.3.0` marks it.
- The Go version guard table is a maintenance obligation per Go release.
- A symptom with both a cost and a waiting component needs deliberate
  dominant-risk routing so that `gopher:diagnose` never assigns two primary
  owners.

**Neutral / Follow-up actions:**

- Revisit a `[performance]` configuration table only when a project demonstrates
  a need for shared thresholds or a CI regression gate; that change is a schema
  migration and needs its own ADR.
- Re-read the version guard table after every stable Go release.
- Record future ownership changes in a new ADR.
