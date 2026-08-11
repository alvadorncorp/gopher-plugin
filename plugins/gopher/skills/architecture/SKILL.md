---
name: architecture
description: Designs, reviews, and migrates Go packages, internal boundaries, dependency direction, public APIs, evidence-backed seams, and the module and workspace lifecycle from creation through split, merge, retirement, and release. Use during planning for package layout, module split, public-API moves, migration sequencing, or "where should this live" questions; mode triage classifies local vs cross-package vs application-boundary ownership before design. Use for cross-package, module-topology, or public-contract work, including sequenced migrations. Hand open code/module pattern selection without a pattern.* ID to `gopher:design-patterns`, local one-package implementation to `gopher:developer`, language-agnostic app boundaries alone to `gopher:application-architecture`, multidimensional cleanup orchestration to `gopher:refactor`, and multi-lens diff review to `gopher:review`.
---

# Go Architecture

## Context and ownership

Own Go package/module/workspace structure, `internal` boundaries, dependency
direction, public APIs, interface seams, migrations, and architecture tests.
Primary owner: `gopher:architecture`.

Receive conceptual application boundaries from `gopher:application-architecture`.
Hand open code/module pattern forces without a `pattern.*` ID to
`gopher:design-patterns`, then resume package placement after that selection when
needed. Hand local implementation to `gopher:developer`, runtime synchronization
to `gopher:concurrency`, performance cost and throughput to `gopher:performance`,
and explicit security analysis to `gopher:security`.

Receive public-API and module-topology modernization from `gopher:modernize`;
contract-changing modernization remains owned here.

Metadata, dependencies, and toolchain maintenance stay with `gopher:modernize`:
the declared Go and toolchain versions, the dependency version policy, and
idiomatic API modernization inside the current contract are that skill's work.
`gopher:architecture` owns module topology: which modules exist, what each one
contains, how they depend on each other, and how they are versioned and released.
One example on each side keeps the split testable: bumping a dependency to a
patch release is `gopher:modernize`; splitting a package into a second module
with its own version line is `gopher:architecture`.

## Modes

| Mode | When | Stop condition |
|---|---|---|
| `triage` | Ownership is unclear: local package work vs cross-package Go structure vs language-agnostic application boundaries vs open code/module pattern forces. Prefer this first on planning prompts | Emits a handoff decision: stay on `gopher:architecture` (name next mode), hand off to `gopher:developer`, hand off to `gopher:design-patterns`, hand off to `gopher:application-architecture`, or `gopher:refactor` for multidimensional cleanup — with evidence and `authorization_gate` |
| `design` | Packages, boundaries, seams, or public APIs are the open question. The default after triage selects architecture | Every proposed boundary carries its evidence, its dependency direction, its public-contract effect, and at least one executable architecture gate (test, `go list`/import rule, or project-adopted checker) |
| `module-lifecycle` | A module is created, split, merged, or retired, or `go.work` membership, `replace` directives, or release grouping is the open question | Every affected module has a decided import path, version line, workspace membership, `replace` set, and release step, each verified by the commands that prove it |
| `migration` | An agreed structural change reaches live code and needs sequencing | Every slice has met its entry condition, passed its verification, held its compatibility guarantee, and kept its rollback available |

State the mode before proposing anything, and carry it in the report. A single
request may traverse modes in order; each transition restates the evidence the
next mode needs.
`triage` is always read-only: it classifies ownership and names the next action
without editing files, creating packages, or opening a migration. When triage
selects architecture, name the next mode (`design`, `module-lifecycle`, or
`migration`) and the evidence that mode needs. When triage selects another
owner, emit `mode`, `authorization_gate`, `primary_owner`, and `handoff`, then
stop.

## Policy gating

The `[architecture]` table of the project contract (`gopher:config`, schema v3)
constrains what these modes may propose.

| Key | Values | Default | What it restricts |
|---|---|---|---|
| `workspace_mode` | `off` \| `advisory` \| `required` | `advisory` | whether `go.work` membership is proposed, recommended, or mandatory in `module-lifecycle` |
| `tidy_mode` | `off` \| `advisory` \| `required` | `advisory` | whether module tidying is part of a lifecycle or migration slice |
| `release_mode` | `independent` \| `grouped` | `independent` | whether modules version and release separately or as a group |
| `replace_mode` | `forbid` \| `local-only` \| `allow` | `local-only` | which `replace` directives a lifecycle change may introduce |

The policy narrows what a mode may propose and leaves every authorization
boundary exactly as it stands: a cross-package, public-contract, boundary, or
ADR-affecting edit keeps its explicit approval gate under every value above.
A tidy that only adds or drops requirements to match the existing import graph
stays inside the slice. A tidy that changes a selected dependency version is a
dependency-policy change: record the before and after versions, stop, and hand it
to `gopher:modernize` under `modernize.dependency_updates`. `tidy_mode =
required` makes a tidy graph a completion condition for the slice, never an
authorization to move a dependency version.

Resolve the effective values through `gopher:config` and report the
`config_status` that applies. `ABSENT` applies the defaults in this table.
`VALID` and `MIGRATION_AVAILABLE` proceed on that contract's effective values,
and migrating the schema belongs to `gopher:config --bootstrap`. `INVALID`
allows design analysis and blocks every structural edit until the contract is
corrected. `UNSUPPORTED_VERSION` stays read-only.

## Workflow

1. Name the mode. In `triage`, classify the request as local implementation
   (`gopher:developer`), open code/module pattern selection without a
   `pattern.*` ID (`gopher:design-patterns`), language-agnostic application
   boundaries (`gopher:application-architecture`), multidimensional cleanup
   (`gopher:refactor`), or Go package/module/public-contract work (continue
   here). When the owner is not architecture, emit the output with `handoff`
   and `authorization_gate`, and stop — later steps do not run. Prefer
   `gopher:design-patterns` when Strategy/Factory/Proxy/clone/snapshot/intern
   forces are still undecided; keep façade and consumer-interface seam work
   here only when the general pattern is already decided or the evidence is
   already package-level ownership.
2. When the question is conceptual bounded-context or domain ownership rather
   than Go packages, hand off to `gopher:application-architecture` before any
   package design; resume here only with that skill's boundary decisions as
   input. When design-patterns returns a `pattern.*` that needs package
   placement, resume in `design` with that ID in evidence.
3. Detect module, workspace, Go version, packages, imports, public consumers,
   tests, and accepted ADR/constraints. Resolve the `[architecture]` policy and
   record `config_status`.
4. State evidence, forces, and the no-refactor baseline. Classify supporting
   claims as `observed`, `inferred`, or `unknown`. When an unknown blocks the
   next mode step, stop at that gate and name the exact evidence or user/owner
   decision required to continue.
5. Map current and proposed dependencies; identify cycles and public-contract effects.
6. Prefer concrete types and consumer-owned interfaces at demonstrated seams.
7. In `module-lifecycle`, settle module membership, import paths, version lines,
   workspace use, the `replace` set, and release order using
   `references/modules-workspaces.md`, within the policy above.
8. In `migration`, sequence the work into slices that each declare an entry
   condition, a change, a verification, a compatibility guarantee, and a
   rollback, using `references/migrations.md`.
9. When more than one structure or migration path is outcome-relevant, compare
   at most three candidates and record rejected alternatives with evidence;
   when only one candidate meets the mode stop condition, record it against the
   no-refactor baseline without inventing alternatives.
10. Define compatibility, rollback, and verification that is the cheapest
    observable proof of each declared gate and compatibility claim. In `design`
    and `migration`, require at least one machine-checkable architecture gate
    (see `references/architecture-tests.md`); a design with only diagrams and no
    proposed executable rule is incomplete.
11. Obtain explicit approval for cross-package, public-contract, boundary, or
    ADR-affecting edits (`authorization_gate`: `none` when the change stays
    inside already-approved scope, `approval-required` until granted, `blocked`
    when policy or config forbids progress); then execute incremental slices or
    hand implementation off via `structure_decision` (see
    `references/structure-decision.md`). After handoff, the receiving peer
    applies its own authorization gate.

## Output format

```yaml
mode: triage | design | module-lifecycle | migration
config_status: ABSENT | VALID | MIGRATION_AVAILABLE | INVALID | UNSUPPORTED_VERSION
problem_and_evidence:
forces_and_constraints:
baseline_without_pattern_or_refactor:
candidates_and_liabilities:
decision:
rejected_alternatives:
public_contract_impact:
migration_and_rollback:
validation:
structure_decision:
  decision_id:
  mode: design | module-lifecycle | migration
  packages_touched: []
  public_contract_delta: none | additive | breaking
  architecture_tests_to_add: []
  slices: []
  authorization_gate: none | approval-required | blocked
  notes:
authorization_gate: none | approval-required | blocked
primary_owner: gopher:architecture
handoff: gopher:<skill> | null
```

Omit `structure_decision` only for pure `triage` handoffs that carry no
structural proposal; for every other successful architecture result, emit the
card (`slices: []` when the decision is design-only).

## Quality checklist

- Base every boundary on observed ownership, dependency, or change pressure.
- Keep interfaces at consumers and only for real seams.
- Treat exported names, signatures, behavior, errors, and option semantics as contracts.
- Use `internal` and modules for enforceable ownership, not aesthetic grouping.
- Match migration, rollback, and machine-checkable dependency obligations to the
  active mode stop condition; keep no-change when the baseline already satisfies it.
- Report `authorization_gate` (`none` | `approval-required` | `blocked`) before
  structural edits; leave specialist gates to the owning peer after handoff.
- Report the active mode together with the effective `[architecture]` values that
  shaped the proposal.
- Justify a second module by a durable version, release, ownership, or
  consumption boundary, and name the `go` commands that carry the change.
- Give every migration slice an entry condition, a verification command, a
  compatibility guarantee, and a rollback that has been exercised.

## References

- `references/packages-internal.md` — package cohesion and `internal` boundaries.
- `references/interfaces-seams.md` — concrete types and consumer-owned seams.
- `references/modules-workspaces.md` — the module lifecycle, `go.work`, `replace`, and release grouping.
- `references/public-api.md` — compatibility and public contracts.
- `references/migrations.md` — the slice protocol for sequenced migrations.
- `references/architecture-tests.md` — deterministic dependency gates.
- `references/pattern-mappings.md` — package/seam pattern adaptations.
- `references/structure-decision.md` — Structure Decision Card for implementers and handoffs.
