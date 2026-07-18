---
name: test-quality
description: Analyzes Go coverage, test effectiveness, and optional mutation score, then strengthens safety nets without changing production behavior. Use to check coverage, evaluate whether tests detect faults, run mutation analysis, or protect a refactor. Route production defects and behavior changes to `gopher:developer`.
---

# Go Test Quality

## Context and ownership

Own Go test-suite quality: coverage, behavior effectiveness, optional mutation
analysis, and refactoring safety nets. Primary owner: `gopher:test-quality`.
Read the effective scope and targets from `gopher:config`.

Strengthen tests only. Hand a discovered production defect or a requested
behavior change to `gopher:developer` with the evidence, and make a failing test
pass only by strengthening the test or by handing off the defect.

## State machine

```text
PASSING BASELINE -> COVERAGE -> BEHAVIOR EFFECTIVENESS -> OPTIONAL MUTATION -> IMPROVE SAFETY NET -> RE-MEASURE
```

## Workflow

1. Establish a passing test baseline. A failing baseline is reported and blocks
   any production edit; test-only work may still proceed.
2. Measure package and relevant-scope coverage using `references/coverage.md`
   and the configured regression tolerance.
3. Identify untested behavior and weak assertions with
   `references/effectiveness.md`, and evaluate whether the tests actually protect
   the intended refactor.
4. Optionally run mutation analysis (`references/mutation.md`) when a pinned
   tool is available.
5. Strengthen the safety net without changing production behavior; add
   characterization tests only under an approved phase
   (`references/refactoring-safety.md`).
6. Re-measure with the same commands and tool versions and report before/after
   coverage, mutation score, limitations, and handoffs.

## Mutation scoring

- Keep the five result classes separate: `killed`, `lived`, `not-covered`,
  `timed-out`, and `not-viable`.
- The normalized score is `killed / (killed + lived)`.
- Timeouts and non-viable mutations never inflate the score; report them as
  their own counts.
- Mutation is advisory by default. Treat it as required only when configured so.

## Output format

```yaml
selected_skill: gopher:test-quality
primary_owner: gopher:test-quality
status: COMPLETE | COMPLETE_WITH_LIMITATIONS | BLOCKED
config_status: ABSENT | VALID | INVALID | UNSUPPORTED_VERSION
baseline_status: passing | failing | not-run
authorization_gate: none | approval-required | blocked
handoff: gopher:developer | null
```

## Authorization boundaries

- Strengthen tests only. A discovered production defect or a requested behavior
  change is handed to `gopher:developer` with the evidence.
- Add characterization tests before production edits only under an explicitly
  approved safety-net phase.
- Missing mutation tooling is a limitation in advisory mode and a blocker only
  when `test-quality.mutation_mode` is `required`.
- Use only adopted or already-available tools; report a missing tool as an
  explicit limitation.

## References

- `references/coverage.md` — the `go test -coverprofile` and `go tool cover` workflow.
- `references/effectiveness.md` — untested behavior, weak assertions, refactor protection.
- `references/mutation.md` — optional mutation, the five classes, the kill score.
- `references/refactoring-safety.md` — characterization tests under an approved phase.
- `references/tooling.md` — `auto` discovery for coverage and mutation.
- `references/sources.md` — version-sensitive official references and review cadence.
