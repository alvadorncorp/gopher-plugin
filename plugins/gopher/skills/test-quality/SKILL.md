---
name: test-quality
description: Analyzes Go coverage, test effectiveness, and optional mutation score, then strengthens safety nets without changing production behavior, and in an explicitly selected `quality-lab` mode picks the cheapest technique that falsifies a named risk against an independent oracle. Use to check coverage, evaluate whether tests detect faults, run mutation analysis, protect a refactor, or enter the quality lab by name. Route production defects and behavior changes to `gopher:developer`.
---

# Go Test Quality

## Context and ownership

Own Go test-suite quality: coverage, behavior effectiveness, optional mutation
analysis, and refactoring safety nets. Primary owner: `gopher:test-quality`.
Read the effective scope and targets from `gopher:config`.

Strengthen tests only. Hand a discovered production defect or a requested
behavior change to `gopher:developer` with the evidence, and make a failing test
pass only by strengthening the test or by handing off the defect.

## Modes

| Mode | When | Stop condition |
|---|---|---|
| `default` | Every coverage, effectiveness, mutation-score, or refactor-safety-net request. This mode is in effect unless `quality-lab` is named. | Before and after coverage, effectiveness findings, the optional mutation score, limitations, and handoffs are reported under the same commands and tool versions. |
| `quality-lab` | The user names the quality lab, or names a falsification technique and asks which one fits a stated risk. Selection of this mode is always explicit. | One family is selected against a named risk with an independent oracle, and the run reports its reproducible baseline, before and after evidence, and stated limitations, or reports the gap that prevented them. |

A coverage, mutation, or "make the tests better" request stays in `default`;
`quality-lab` is entered on an explicit request and on nothing else.

## State machine

```text
PASSING BASELINE -> COVERAGE -> BEHAVIOR EFFECTIVENESS -> OPTIONAL MUTATION -> IMPROVE SAFETY NET -> RE-MEASURE
```

## Workflow (`default` mode)

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

## Quality-lab selection

`test-quality.quality_lab_families` (schema v2, default empty, where empty means
every canonical family is eligible) is the ELIGIBLE SET: what may be considered,
never an instruction to run every technique it names. Selection works five
ordered steps and stops at the cheapest surviving technique that satisfies all
five:

1. **A named risk** — the specific claim about the code that might be false.
2. **An independent oracle** — something other than the code under test that can say the claim is false.
3. **The project's declared Go version** — which techniques the toolchain supports, read from `go.mod`.
4. **An available seam** — where the technique can observe or substitute behavior.
5. **The cheapest technique** that can falsify the claim.

A technique selected with no named risk, or one whose oracle is the code under
test itself, produces nothing worth trusting; both are reported as unusable,
naming what is missing. Every `quality-lab` run reports a reproducible baseline,
the exact commands, the environment, seeds, fixtures, tool versions, a
reproduction, before and after evidence, and stated limitations; a run that
cannot produce those reports the gap rather than an unqualified result. Load
`references/quality-lab.md` and `references/lab-families.md` when, and only when,
this mode is selected.

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
mode: default | quality-lab
status: COMPLETE | COMPLETE_WITH_LIMITATIONS | BLOCKED
config_status: ABSENT | VALID | MIGRATION_AVAILABLE | INVALID | UNSUPPORTED_VERSION
baseline_status: passing | failing | not-run
authorization_gate: none | approval-required | blocked
handoff: gopher:<skill> | null
quality_lab:
  eligible_families:
  selected_family:
  rejected_families:
  named_risk:
  oracle:
  seam:
  declared_go_version:
  baseline:
  commands:
  environment:
  seeds:
  fixtures:
  tool_versions:
  reproduction:
  before_after:
  limitations:
```

The `quality_lab` block is filled in `quality-lab` mode and omitted in `default`.

## Authorization boundaries

- Strengthen tests only. A discovered production defect or a requested behavior
  change is handed to `gopher:developer` with the evidence.
- Add characterization tests before production edits only under an explicitly
  approved safety-net phase.
- Missing mutation tooling is a limitation in advisory mode and a blocker only
  when `test-quality.mutation_mode` is `required`.
- Use only adopted or already-available tools; report a missing tool as an
  explicit limitation.
- A `config_status` of `INVALID` or `UNSUPPORTED_VERSION` keeps the run
  read-only: measure and report, and route the configuration fix to
  `gopher:config` before any test file is written.
- In `quality-lab` mode, adjacent work keeps its own canonical owner:

| Work | Owner |
|---|---|
| a native Go fuzz target, its invariant, its seed corpus, and its bounded campaign | `gopher:fuzz` |
| a race, deadlock, goroutine leak, or synchronization defect surfaced by a `race-leak` or `deterministic-concurrency` run | `gopher:concurrency` |
| benchmarks, profiles, and performance measurement | `gopher:performance` |
| chaos experiments against a failure model | `gopher:resilience` |
| security testing and adversarial security probes | `gopher:security` |
| creating the production seam a selected technique needs | `gopher:developer`, or `gopher:refactor` when the seam comes from a behavior-preserving restructure |
| application end-to-end testing | the project's own end-to-end owner, named as outside this mode |

The fuzz split is sharp: choosing which technique falsifies a named risk across
the suite is `quality-lab`; designing a fuzz target, its invariant, and its
bounded campaign is `gopher:fuzz`. Each row keeps its owner and its evidence.

## References

- `references/coverage.md` — the `go test -coverprofile` and `go tool cover` workflow.
- `references/effectiveness.md` — untested behavior, weak assertions, refactor protection.
- `references/mutation.md` — optional mutation, the five classes, the kill score.
- `references/refactoring-safety.md` — characterization tests under an approved phase.
- `references/quality-lab.md` — the `quality-lab` selection ladder, evidence, and reproducibility contract.
- `references/lab-families.md` — the twelve canonical families with risk, oracle, seam, cost, tooling, and version gating.
- `references/tooling.md` — `auto` discovery for coverage and mutation.
- `references/sources.md` — version-sensitive official references and review cadence.
