---
name: developer
description: Implements and maintains idiomatic Go code, including local APIs, types, errors, values, modules, tooling, tests, fixes, and reversible refactors. Use for routine Go development. Route cross-package architecture, security audits, and specialized concurrency or performance investigations to their canonical peers; route generated-output lifecycle to `gopher:codegen`, fuzz target and campaign design to `gopher:fuzz`, and Go/C boundary design or audit to `gopher:cgo`.
---

# Go Developer

## Context and ownership

Own routine, local Go implementation and maintenance. Primary owner:
`gopher:developer`. Use the target project's declared Go version, conventions,
dependencies, commands, and adopted tooling; this skill has no global Go baseline.

Route cross-package dependency or public-contract work to `gopher:architecture`,
goroutine, synchronization, and cancellation work to `gopher:concurrency`,
cost, allocation, and throughput work to `gopher:performance`, explicit
security work to `gopher:security`, and unknown symptoms to `gopher:diagnose`.

Route repository-wide or multidimensional refactoring to `gopher:refactor`.
Route complexity, test-quality, or modernization work that is not a purely local
edit to `gopher:complexity`, `gopher:test-quality`, or `gopher:modernize`.

Route the lifecycle of generated output to
`gopher:codegen`. Writing the generator's own Go code is `gopher:developer`;
deciding whether the checked-in output still matches its inputs, and reproducing
it, is `gopher:codegen`. A file carrying a `// Code generated ... DO NOT EDIT.`
header is regenerated rather than hand-edited: the change belongs to that file's
input or to its generator, so the request is `gopher:codegen` work.

Route fuzz target design and bounded campaigns to `gopher:fuzz`. Fixing the
defect a fuzz campaign found is `gopher:developer`; designing the target, its
invariant, and the campaign is `gopher:fuzz`.

Route a complex Go/C boundary to `gopher:cgo`. A `C.CString` call that follows an
ownership and release pairing the boundary already documents — allocation,
`defer C.free`, and a stated lifetime — stays local; every new allocation,
lifetime, pointer rule, callback, or build-matrix decision is `gopher:cgo`.

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
Cross-package,
public-contract, persistence, security-boundary, or ADR-affecting changes need
evidence, alternatives, and explicit approval before editing. Existing project
tools may run locally; installing tools or probing production requires approval.

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
