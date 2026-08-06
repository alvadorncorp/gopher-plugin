---
name: architecture
description: Designs, reviews, and migrates Go packages, internal boundaries, dependency direction, public APIs, evidence-backed seams, and the module and workspace lifecycle from creation through split, merge, retirement, and release. Use for cross-package, module-topology, or public-contract work, including sequenced migrations. Route routine local implementation and language-agnostic application structure to their canonical peers.
---

# Go Architecture

## Context and ownership

Own Go package/module/workspace structure, `internal` boundaries, dependency
direction, public APIs, interface seams, migrations, and architecture tests.
Primary owner: `gopher:architecture`.

Receive conceptual application boundaries from `gopher:application-architecture`.
Route local implementation to `gopher:developer`, runtime synchronization to
`gopher:concurrency`, performance cost and throughput to `gopher:performance`, and
explicit security analysis to `gopher:security`.

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
| `design` | Packages, boundaries, seams, or public APIs are the open question. The default behavior of this skill | Every proposed boundary carries its evidence, its dependency direction, its public-contract effect, and an executable architecture gate |
| `module-lifecycle` | A module is created, split, merged, or retired, or `go.work` membership, `replace` directives, or release grouping is the open question | Every affected module has a decided import path, version line, workspace membership, `replace` set, and release step, each verified by the commands that prove it |
| `migration` | An agreed structural change reaches live code and needs sequencing | Every slice has met its entry condition, passed its verification, held its compatibility guarantee, and kept its rollback available |

State the mode before proposing anything, and carry it in the report. A single
request may traverse modes in order; each transition restates the evidence the
next mode needs.

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

1. Name the mode, then detect module, workspace, Go version, packages, imports,
   public consumers, tests, and accepted ADR/constraints. Resolve the
   `[architecture]` policy and record `config_status`.
2. State evidence, forces, and the no-refactor baseline.
3. Map current and proposed dependencies; identify cycles and public-contract effects.
4. Prefer concrete types and consumer-owned interfaces at demonstrated seams.
5. In `module-lifecycle`, settle module membership, import paths, version lines,
   workspace use, the `replace` set, and release order using
   `references/modules-workspaces.md`, within the policy above.
6. In `migration`, sequence the work into slices that each declare an entry
   condition, a change, a verification, a compatibility guarantee, and a
   rollback, using `references/migrations.md`.
7. Compare at most three structures or migration paths and reject alternatives.
8. Define compatibility, rollback, architecture tests, and proportional verification.
9. Obtain explicit approval for cross-package, public-contract, boundary, or
   ADR-affecting edits; then execute incremental slices or hand implementation off.

## Output format

```yaml
mode: design | module-lifecycle | migration
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
authorization_gate: none | approval-required | blocked
primary_owner: gopher:architecture
handoff: gopher:<skill> | null
```

## Quality checklist

- Base every boundary on observed ownership, dependency, or change pressure.
- Keep interfaces at consumers and only for real seams.
- Treat exported names, signatures, behavior, errors, and option semantics as contracts.
- Use `internal` and modules for enforceable ownership, not aesthetic grouping.
- Include incremental migration, rollback, and machine-checkable dependency rules.
- Record approval status before structural edits.
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
