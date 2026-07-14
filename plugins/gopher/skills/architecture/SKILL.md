---
name: architecture
description: Designs, reviews, and migrates Go packages, internal boundaries, modules/workspaces, dependency direction, public APIs, and evidence-backed seams. Use for cross-package or public-contract work. Route routine local implementation and language-agnostic application structure to their canonical peers.
---

# Go Architecture

## Context and ownership

Own Go package/module/workspace structure, `internal` boundaries, dependency
direction, public APIs, interface seams, migrations, and architecture tests.
Primary owner: `gopher:architecture`.

Receive conceptual application boundaries from `gopher:application-architecture`.
Route local implementation to `gopher:developer`, runtime synchronization and
performance to `gopher:concurrency-performance`, and explicit security analysis
to `gopher:security`.

## Workflow

1. Detect module, workspace, Go version, packages, imports, public consumers,
   tests, and accepted ADR/constraints.
2. State evidence, forces, and the no-refactor baseline.
3. Map current and proposed dependencies; identify cycles and public-contract effects.
4. Prefer concrete types and consumer-owned interfaces at demonstrated seams.
5. Compare at most three structures or migration paths and reject alternatives.
6. Define compatibility, rollback, architecture tests, and proportional verification.
7. Obtain explicit approval for cross-package, public-contract, boundary, or
   ADR-affecting edits; then execute incremental slices or hand implementation off.

## Output format

```yaml
problem_and_evidence:
forces_and_constraints:
baseline_without_pattern_or_refactor:
candidates_and_liabilities:
decision:
rejected_alternatives:
public_contract_impact:
migration_and_rollback:
validation:
primary_owner: gopher:architecture
handoff:
```

## Quality checklist

- Base every boundary on observed ownership, dependency, or change pressure.
- Keep interfaces at consumers and only for real seams.
- Treat exported names, signatures, behavior, errors, and option semantics as contracts.
- Use `internal` and modules for enforceable ownership, not aesthetic grouping.
- Include incremental migration, rollback, and machine-checkable dependency rules.
- Record approval status before structural edits.

## References

- `references/packages-internal.md` — package cohesion and `internal` boundaries.
- `references/interfaces-seams.md` — concrete types and consumer-owned seams.
- `references/modules-workspaces.md` — module/workspace decisions.
- `references/public-api.md` — compatibility and public contracts.
- `references/migrations.md` — incremental architecture changes.
- `references/architecture-tests.md` — deterministic dependency gates.
- `references/pattern-mappings.md` — package/seam pattern adaptations.
