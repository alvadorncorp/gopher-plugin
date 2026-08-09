---
name: developer
description: Implements and maintains idiomatic Go code, including local APIs, types, errors, values, local module edits, tooling, tests, fixes, and reversible refactors. Use when adding or changing a function, type, or local API, wrapping or classifying an error, choosing a constructor or option shape, writing focused tests, or fixing a bug inside one package. Route cross-package architecture to `gopher:architecture`, security audits to `gopher:security`, and specialized concurrency or performance investigations to `gopher:concurrency` and `gopher:performance`; route generated-output lifecycle to `gopher:codegen`, fuzz target and campaign design to `gopher:fuzz`, and Go/C boundary design or audit to `gopher:cgo`.
---

# Go Developer

## Context and ownership

Own routine, local Go implementation and maintenance. Primary owner:
`gopher:developer`. Use the target project's declared Go version, conventions,
dependencies, commands, and adopted tooling as the baseline for each decision;
resolve missing project values through `references/project-detection.md`.

| Question | Owner |
|---|---|
| Cross-package dependency, module lifecycle, or public-contract work | `gopher:architecture` |
| Goroutine, synchronization, or cancellation work | `gopher:concurrency` |
| Cost, allocation, or throughput work | `gopher:performance` |
| Explicit security work | `gopher:security` |
| An unattributed symptom | `gopher:diagnose` |
| Repository-wide or multidimensional refactoring | `gopher:refactor` |
| Complexity, test-quality, or modernization work beyond a purely local edit | `gopher:complexity`, `gopher:test-quality`, `gopher:modernize` |
| The lifecycle of generated output, including any `// Code generated ... DO NOT EDIT.` file | `gopher:codegen` |
| Fuzz target, invariant, and campaign design | `gopher:fuzz` |
| A new allocation, lifetime, pointer rule, callback, or build-matrix decision at a Go/C boundary | `gopher:cgo` |
| Local implementation: local APIs, types, errors, values, tests, and reversible fixes | `gopher:developer` |

Three splits keep those rows testable. The generator's own Go code is written
here, while reproducing its output and deciding whether the checked-in copy still
matches its inputs is `gopher:codegen`. The defect a fuzz campaign found is fixed
here, while the target, its invariant, and the campaign are `gopher:fuzz`. A
`C.CString` call that follows an ownership and release pairing the boundary
already documents — allocation, `defer C.free`, and a stated lifetime — stays
here, while every new allocation, lifetime, pointer rule, callback, or
build-matrix decision is `gopher:cgo`.

## Workflow

1. **CLASSIFY CONFIG** using `references/project-detection.md`. `INVALID` and
   `UNSUPPORTED_VERSION` permit read-only diagnosis only, block production
   edits, and route recovery to `gopher:config`. Record the config status and
   validation evidence.
2. **RESOLVE IDIOM POLICY** and **RESOLVE TEST WORKFLOW** independently using
   `session | file | adopted | default`; use `latest-compatible` and
   `adaptive-tdd` when their values are absent or migratable. Record each
   resolved value and source. Keep effective defaults session-scoped and persist
   them only through the `gopher:config` bootstrap flow.
3. Detect the declared Go version, project commands, and conventions using
   `references/project-detection.md`, and record the detected values.
4. **ESTABLISH FOCUSED BASELINE** with the narrowest adopted command that
   exercises the affected package or behavior; record its exact command, exit
   status, and observation before classifying a change or editing production
   behavior.
5. **CLASSIFY CHANGE** as behavior, bug-fix, refactor, mechanical, or test-only;
   restate its behavior, affected local API,
   error semantics, and compatibility constraints.
6. Load `references/testing.md` and **COLLECT FIRST SIGNAL** required by the
   resolved `test_workflow`; record that signal before editing production
   behavior.
7. Inspect callers, tests, and nearby conventions before editing.
8. Prefer direct code, concrete types, functions, and useful zero values.
9. When the request or project supplies a `pattern.*` mapping, load
   `references/pattern-mappings.md` and
   accept, adapt, or veto it with Go-specific evidence.
10. For a local reversible refactor, load `references/refactoring.md` and follow
   its FOCUSED workflow; hand multidimensional or repository-wide work to
   `gopher:refactor`.
11. **IMPLEMENT** the smallest cohesive change that satisfies the requested
   behavior, with tests for changed observable behavior.
12. **CONFIRM GREEN** with the same focused command and record its evidence,
   then **REFACTOR WHILE GREEN**.
13. Run **FINAL VALIDATION** with the affected-risk ladder in
   `references/tooling.md` and existing project commands.
14. Report files, behavior, validation, limitations, and any handoff.

For each workflow gate, classify supporting claims as `observed`, `inferred`, or
`unknown`. If an unknown blocks the next gate, stop at that gate and record the
exact evidence or user/owner decision required in `limitations`; route to the
owning skill when the unresolved decision is outside this skill's scope.

## Output format

```yaml
selected_skill: gopher:developer
primary_owner: gopher:developer
status: COMPLETE | COMPLETE_WITH_LIMITATIONS | BLOCKED
project_contract:
  config_status: ABSENT | VALID | MIGRATION_AVAILABLE | INVALID | UNSUPPORTED_VERSION
  declared_go:
  idiom_policy:
    value: latest-compatible | project-aligned | explicit-only
    source: session | file | adopted | default
  test_workflow:
    value: adaptive-tdd | strict-tdd | test-after
    source: session | file | adopted | default
requested_behavior:
change_class: behavior | bug-fix | refactor | mechanical | test-only
baseline_status: passing | failing | not-run
test_evidence:
  pre_change:
  first_signal:
    kind: red | characterization | test-after | exception | not-applicable
    command:
    observed:
    reason:
  green:
  refactor:
implementation:
pattern_decision:
  general_id: pattern.<id> | none
  go_mapping: go.<id> | none
  disposition: accepted | adapted | vetoed | not-applicable
validation:
limitations:
authorization_gate: none | approval-required | blocked
handoff: gopher:<skill> | null
```

Evidence entries record the exact command, exit status, and concise observation.
When a stage is skipped or not applicable, record an explicit reason rather than
omitting the entry.

## Authorization

Proceed with explicitly requested local and reversible changes. For a file
carrying a `// Code generated ... DO NOT EDIT.` header, change its input or its
generator and route the regeneration decision to `gopher:codegen`.
Cross-package, public-contract, persistence, security-boundary, or ADR-affecting
changes need evidence, alternatives, and explicit approval before editing.
Existing project tools may run locally. Request approval before installing tools
or probing production.

When the evidence leaves it undecided whether a boundary is already designed or
whether a file is generated, record the ambiguity in `limitations` and hand off
with that evidence in place of editing.

## Quality checklist

- Respect the declared Go/toolchain version and repository conventions.
- Keep concrete types until real behavior variability or a consumer seam exists.
- Preserve error identity and context; keep expected absence distinct from failure.
- Define Functional Options ordering, duplicate, nil, and validation semantics.
- Test observable behavior with independent expected values.
- Run `gofmt` plus the smallest relevant adopted test/static gates.

## References

- `references/project-detection.md` — version, module, CI, and convention detection.
- `references/idioms.md` — concrete types, interfaces, context, and ownership.
- `references/construction-options.md` — constructor/config/builder/options decisions.
- `references/api-errors-values.md` — APIs, values, errors, and compatibility.
- `references/testing.md` — Go-specific behavioral test guidance.
- `references/tooling.md` — proportional validation ladder.
- `references/pattern-mappings.md` — canonical general-to-Go mappings.
- `references/refactoring.md` — local reversible refactor workflow and outward routing.
