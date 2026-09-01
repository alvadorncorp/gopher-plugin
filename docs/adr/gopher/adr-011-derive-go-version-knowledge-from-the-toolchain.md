---
type: adr
id: adr:gopher:011
context: gopher
title: Derive Go version knowledge from the toolchain and keep it distributed
status: Accepted
tags: [go, skills, versioning, modernize, maintenance]
deciders: [Alvadorncorp]
date: 2026-08-31
---
# ADR-011: Derive Go version knowledge from the toolchain and keep it distributed

## Context and Problem

Gopher encodes Go version knowledge in several skills: guard tables that decide
whether a technique may be recommended, and a roster of the `go fix` modernizer
analyzers. Go 1.27 showed that this knowledge does not merely age — it becomes
wrong, and wrongness here is not inert. A guard table is what a skill uses to
reject a technique, so a stale row makes a skill reject something valid or offer
something that will not compile in the target project.

Three concrete defects existed when Go 1.27 shipped:

- `modernize/references/language-apis.md` listed `fmtappendf`, removed in 1.27,
  and `waitgroup`, renamed to `waitgroupgo`; it omitted the four analyzers added
  in 1.27; and it claimed four analyzers were off by default when `go fix` runs
  every registered analyzer by default and does not register three of the four.
- `performance/references/version-sensitive.md` recorded a forecast — that
  `GOEXPERIMENT=nogreenteagc` would disappear in Go 1.27 — as if it were
  settled. Go 1.27 still accepts it.
- Several guard tables stopped at Go 1.26 while the toolchain moved on.

The first two defects came from the same source: the release notes and the
`x/tools` package documentation, both of which disagree with the shipped `go`
binary. Third-party summaries repeat the disagreement. This ADR settles where
version knowledge comes from and where it lives.

## Decision Drivers

- A wrong guard is worse than a missing one, because it is acted on silently.
- Version knowledge must be verifiable by whoever maintains the plugin, not
  taken on trust from prose.
- Twenty skills consume version knowledge; the maintenance cost of a release
  refresh must stay proportional.
- The repository's structural tests pin the reference-file layout, so a
  reorganization is not free.

## Considered Options

### Option 1: derive from the toolchain, keep the tables distributed (chosen)

Version facts are verified against an installed toolchain of the target release
before being written. The tables stay in the skills that own them, and a
checklist in `docs/go-release-upgrade.md` enumerates every file that carries
version knowledge plus the commands that verify it.

**Pros:** each fact is checked against the artifact users actually run; each
skill keeps its guard beside the guidance it gates; no change to the reference
layout the structural tests pin.

**Cons:** the checklist is a manual step, and a fact repeated in two skills can
still drift between them.

### Option 2: one shared version matrix, other skills point at it

Create a single reference file as the source of truth for "available from"
rows, and reduce the other tables to pointers.

**Pros:** removes duplication and the drift it allows.

**Cons:** a shared file must be edited to serve every consumer's question, and
guards read best next to the guidance they gate — a reviewer reading
`lab-families.md` should not have to open another skill to learn whether a
technique is permitted. It also adds a reference file, which requires editing
the pinned layout fixture in `tests/fixtures/expected-layout.json`.

### Option 3: keep the tables distributed and rely on release notes

Refresh each table from the release notes when a Go version ships.

**Pros:** no new process.

**Cons:** this is the status quo that produced all three defects above.

## Decision

**Chosen option: derive from the toolchain, keep the tables distributed.**

- The authoritative source for the analyzer roster is `go tool fix help` on the
  toolchain in hand. Release notes and the `x/tools` `modernize` package
  documentation are background on what a rewrite does, never the roster.
- The authoritative source for an API, a package, a GODEBUG, or a GOEXPERIMENT
  is the installed toolchain: `go list std`, `go doc`, `go env`, `go help`, and
  a minimal module that exercises the behavior.
- A forecast is recorded as a forecast and re-tested on the release it names. A
  removal is written down only after the toolchain refuses the setting.
- Guard tables stay in the skills that own them:
  `performance/references/version-sensitive.md` remains the primary table,
  `test-quality/references/lab-families.md` and `cgo/references/sources.md` keep
  theirs, and `modernize` keeps the toolchain and analyzer surface.
- `docs/go-release-upgrade.md` lists every file carrying version knowledge, the
  verification commands, and the repository gates a release refresh touches.
- No new files are added under `skills/*/references/` for a version refresh, so
  `tests/fixtures/expected-layout.json` stays untouched.

## Consequences

**Positive:**

- Every version fact in the plugin is reproducible with a command a maintainer
  can run, and each refresh records the toolchain it was verified against.
- Three factual defects are corrected, and the class of defect that produced
  them has a named remedy.
- Guards remain adjacent to the guidance they gate.

**Negative:**

- A release refresh requires an installed toolchain of that release, so it
  cannot be done from documentation alone.
- The checklist is a convention, not an enforced test; nothing fails if it is
  skipped.

**Neutral / Follow-up actions:**

- Reference files that carry a `Last verified:` line record the toolchain used,
  not only the date, when the verification was performed against one.
- A future release may justify a shared matrix if duplication between guard
  tables grows; the decision here is scoped to the current five tables.
