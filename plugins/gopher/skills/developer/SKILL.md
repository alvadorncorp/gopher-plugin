---
name: developer
description: Implements and maintains idiomatic Go code, including local APIs, types, errors, values, local module edits, tooling, tests, fixes, and reversible refactors. Use when adding or changing a function, type, or local API, wrapping or classifying an error, choosing a constructor or option shape, writing focused tests, or fixing a bug inside one package. Route cross-package architecture to `gopher:architecture`, security audits to `gopher:security`, and specialized concurrency or performance investigations to `gopher:concurrency` and `gopher:performance`; route generated-output lifecycle to `gopher:codegen`, fuzz target and campaign design to `gopher:fuzz`, and Go/C boundary design or audit to `gopher:cgo`.
---

# Go Developer

## Context and ownership

Own routine, local Go implementation and maintenance. Primary owner:
`gopher:developer`. Use the target project's declared Go version, conventions,
dependencies, commands, and adopted tooling; this skill has no global Go baseline.

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

1. Detect the project contract using `references/project-detection.md`.
2. Restate the requested behavior, affected local API, error semantics, and
   compatibility constraints.
3. Inspect callers, tests, and nearby conventions before editing.
4. Prefer direct code, concrete types, functions, and useful zero values.
5. When a `pattern.*` handoff exists, load `references/pattern-mappings.md` and
   accept, adapt, or veto it with Go-specific evidence.
6. For a local reversible refactor, load `references/refactoring.md` and follow
   its FOCUSED workflow; hand multidimensional or repository-wide work to
   `gopher:refactor`.
7. Implement the smallest cohesive change and behavior-focused tests.
8. Format and validate proportionally using existing project commands.
9. Report files, behavior, validation, limitations, and any handoff.

## Output format

```yaml
selected_skill: gopher:developer
primary_owner: gopher:developer
project_contract:
requested_behavior:
implementation:
pattern_decision:
  general_id: pattern.<id> | none
  go_mapping: go.<id> | none
  disposition: accepted | adapted | vetoed | not-applicable
validation:
limitations:
handoff: gopher:<skill> | null
```

## Authorization

Explicitly requested local and reversible changes may proceed, except an edit to
a file carrying a `// Code generated ... DO NOT EDIT.` header: change its input
or its generator and route the regeneration decision to `gopher:codegen`.
Cross-package, public-contract, persistence, security-boundary, or ADR-affecting
changes need evidence, alternatives, and explicit approval before editing.
Existing project tools may run locally; installing tools or probing production
requires approval.

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
