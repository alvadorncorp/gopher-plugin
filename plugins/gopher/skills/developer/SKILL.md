---
name: developer
description: Implements and maintains idiomatic Go code, including local APIs, types, errors, values, modules, tooling, tests, fixes, and reversible refactors. Use for routine Go development. Route cross-package architecture, security audits, and specialized concurrency/performance investigations to their canonical peers.
---

# Go Developer

## Context and ownership

Own routine, local Go implementation and maintenance. Primary owner:
`gopher:developer`. Use the target project's declared Go version, conventions,
dependencies, commands, and adopted tooling; this skill has no global Go baseline.

Route cross-package dependency or public-contract work to `gopher:architecture`,
goroutine/synchronization/memory/performance work to
`gopher:concurrency-performance`, explicit security work to `gopher:security`,
and unknown symptoms to `gopher:diagnose`.

Route repository-wide or multidimensional refactoring to `gopher:refactor`.
Route complexity, test-quality, or modernization work that is not a purely local
edit to `gopher:complexity`, `gopher:test-quality`, or `gopher:modernize`.

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
handoff:
```

## Authorization

Explicitly requested local and reversible changes may proceed. Cross-package,
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
