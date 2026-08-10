---
name: developer
description: Implements and maintains idiomatic Go code, including local APIs, types, errors, values, local module edits, tooling, tests, fixes, and reversible refactors. Use during development when adding or changing a function, type, or local API, wrapping or classifying an error, choosing a constructor or option shape, writing focused tests, fixing a bug inside one package, or implementing an approved structure_decision slice that stays local. Prefer after a structure decision exists for cross-cutting features. Hand cross-package architecture to gopher:architecture, security audits to gopher:security, specialized concurrency or performance investigations to gopher:concurrency and gopher:performance; hand generated-output lifecycle to gopher:codegen, fuzz target and campaign design to gopher:fuzz, Go/C boundary design or audit to gopher:cgo, multidimensional cleanup to gopher:refactor, and multi-lens diff review to gopher:review.
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

## Progressive reference loading

Load only the references required by the current change:

| Situation | Load |
|---|---|
| Any change | `project-detection.md`, then `testing.md` + `tooling.md` as the workflow needs them |
| Construction / options | `construction-options.md` |
| Errors / values / public local API | `api-errors-values.md` |
| Idiom policy disputes | `idioms.md` |
| Local reversible refactor | `refactoring.md` |
| pattern.* mapping supplied | `pattern-mappings.md` |
| `from_slice` input present | `refactoring.md` plus the architecture Structure Decision Card fields from the request |

Keep unloaded references out of context until a row above requires them.

## Workflow

1. **CLASSIFY CONFIG** using `references/project-detection.md`. `INVALID` and
   `UNSUPPORTED_VERSION` permit read-only diagnosis only, block production
   edits, and hand recovery to `gopher:config`. Record the config status and
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

## Change-class fast path

After **CLASSIFY CHANGE**, select the FAST PATH:

| change_class | Path |
|---|---|
| `mechanical` with `adaptive-tdd` or `test-after` | FOCUSED BASELINE → record first_signal `exception` → IMPLEMENT → `gofmt` + focused package test → FINAL VALIDATION (package only). Skip red-green ceremony. |
| `mechanical` with `strict-tdd` | unchanged: blocked without session override |
| `test-only` | no production edits; add/strengthen tests; CONFIRM GREEN on focused command |
| `behavior` / `bug-fix` | full workflow (first signal → implement → green → refactor → final validation) |
| `refactor` | characterization path in `references/refactoring.md` |

Fast path still runs CLASSIFY CONFIG, policy resolution, and multi-package
detection before any production edit.

6. Load `references/testing.md` and **COLLECT FIRST SIGNAL** required by the
   resolved `test_workflow`; record that signal before editing production
   behavior. On the mechanical adaptive/test-after path, the first signal is the
   recorded `exception` and red-green ceremony is omitted.
7. Inspect callers, tests, and nearby conventions before editing.
8. Prefer direct code, concrete types, functions, and useful zero values.
9. When the request or project supplies a `pattern.*` mapping, load
   `references/pattern-mappings.md` and
   accept, adapt, or veto it with Go-specific evidence.
10. For a local reversible refactor, load `references/refactoring.md` and follow
    its FOCUSED workflow; hand multidimensional or repository-wide work to
    `gopher:refactor`.
11. **DETECT PACKAGE ENVELOPE.** If the planned edit set spans more than one
    package import path, or requires an exported API move across packages, stop
    without editing, set `authorization_gate: approval-required` when the change
    is cross-package or public-contract structural work, and
    `handoff: gopher:architecture` (or `gopher:refactor` when multidimensional).
    Record the package list in `limitations`.
12. **IMPLEMENT** the smallest cohesive change that satisfies the requested
    behavior, with tests for changed observable behavior.
13. **CONFIRM GREEN** with the same focused command and record its evidence,
    then **REFACTOR WHILE GREEN**.
14. Run **FINAL VALIDATION** with the affected-risk ladder in
    `references/tooling.md` and existing project commands. On the mechanical
    adaptive/test-after fast path, use the package-only ladder in
    `references/tooling.md` (focused package test + `gofmt`).
15. Complete **Micro-review** (below), then report files, behavior, validation,
    limitations, `micro_review`, and any handoff.

For each workflow gate, classify supporting claims as `observed`, `inferred`, or
`unknown`. If an unknown blocks the next gate, stop at that gate and record the
exact evidence or user/owner decision required in `limitations`; hand off to the
owning skill when the unresolved decision is outside this skill's scope.

## from_slice input

When the request carries a Structure Decision Card slice or a `refactor_plan`
item aimed at `gopher:developer`, treat it as `from_slice` before IMPLEMENT:

1. Require `decision_id` or plan item `id`, the slice `entry_condition`,
   `verification` command, and `implementer: gopher:developer`.
2. Verify `entry_condition` is observably met (run the named check when it is a
   command). If unmet, set status `BLOCKED` with the missing condition and leave
   production code unchanged.
3. Accept only slices whose `implementer` is `gopher:developer`,
   `public_contract_delta` is not `breaking`, and `packages_touched` stays inside
   one package for this slice. Otherwise hand off to `gopher:architecture` (or
   `gopher:refactor` when multidimensional) without editing.
4. Classify change (usually `behavior`, `refactor`, or `mechanical`) and follow
   the matching path, including package-envelope detection.
5. After green, run the slice `verification` command in addition to the focused
   package tests; record both in `test_evidence`.
6. Report `slice_id` and whether the structure card slice is complete.

## Micro-review (local, not gopher:review)

After CONFIRM GREEN and before claiming COMPLETE, answer these five checks in
`micro_review` using `pass | fail | n/a` plus a one-line note on any `fail`.
This local checklist is not multi-lens review and leaves full multi-lens work to
`gopher:review`.

1. Error wrap/identity preserved where errors change?
2. Useful zero values retained?
3. Interfaces remain consumer-owned at demonstrated seams?
4. Shared-state/goroutine changes covered by race-aware tests or handed to
   `gopher:concurrency`?
5. Expected absence vs failure distinguished in tests?

If any check is `fail`, fix locally when inside the one-package envelope;
otherwise hand off with evidence. When the session or
`[workflow].post_implementation_review` requests it, recommend `gopher:review`
next; keep multi-lens fan-out outside this skill.

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
slice_id: <id> | null
micro_review:
  error_identity: pass | fail | n/a
  zero_value: pass | fail | n/a
  interface_seam: pass | fail | n/a
  concurrency: pass | fail | n/a
  absence_vs_failure: pass | fail | n/a
```

Evidence entries record the exact command, exit status, and concise observation.
When a stage is skipped or not applicable, record an explicit reason rather than
omitting the entry. Set `slice_id` when executing `from_slice`; otherwise `null`.

## Authorization

Proceed with explicitly requested local and reversible changes inside one
package. Report `authorization_gate` as `none` when the edit stays in that
envelope and is already authorized, `approval-required` until the user grants
explicit approval for cross-package, public-contract, persistence,
security-boundary, or ADR-affecting work, and `blocked` when config, policy, or
an unmet `from_slice` entry condition forbids production edits.

For a file carrying a `// Code generated ... DO NOT EDIT.` header, change its
input or its generator and hand the regeneration decision to `gopher:codegen`.
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
- Run `gofmt` plus the smallest relevant adopted test/static gates (package-only
  on the mechanical adaptive/test-after fast path).
- Stop at **DETECT PACKAGE ENVELOPE** and hand multi-package or exported API moves
  to `gopher:architecture` (or `gopher:refactor` when multidimensional).
- On `from_slice`, meet entry conditions and slice verification before COMPLETE.
- Fill `micro_review` before COMPLETE; recommend `gopher:review` only when
  session/workflow policy asks for multi-lens review.
- Report `authorization_gate` (`none` | `approval-required` | `blocked`) with any
  handoff.

## References

- `references/project-detection.md` — version, module, CI, and convention detection.
- `references/idioms.md` — concrete types, interfaces, context, and ownership.
- `references/construction-options.md` — constructor/config/builder/options decisions.
- `references/api-errors-values.md` — APIs, values, errors, and compatibility.
- `references/testing.md` — Go-specific behavioral test guidance.
- `references/tooling.md` — proportional validation ladder.
- `references/pattern-mappings.md` — canonical general-to-Go mappings.
- `references/refactoring.md` — local reversible refactor workflow and outward routing.
