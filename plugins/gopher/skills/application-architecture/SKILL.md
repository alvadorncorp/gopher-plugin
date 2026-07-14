---
name: application-architecture
description: Designs, reviews, and migrates language-agnostic internal application boundaries, modules, layers, ports/adapters, modular monoliths, and dependency direction. Use for internal application structure. Route distributed topology, infrastructure, data schemas, deployment, and Go package mechanics to their proper owners.
---

# Application Architecture

## Context and ownership

Own language-agnostic internal application structure: capability boundaries,
modules, layers, ports/adapters, modular monoliths, and dependency direction.
Primary owner: `gopher:application-architecture`.

Keep distributed topology, infrastructure, database schema, deployment, and UI
architecture outside this skill. Hand Go package/module/interface mechanics to
`gopher:architecture` after the conceptual decision is approved.

## Workflow

1. Capture business capability, current boundaries, dependency evidence,
   change pressure, invariants, and constraints.
2. State the no-refactor baseline and its measurable cost.
3. Load `references/boundaries.md` and only the style/reference files needed.
4. Compare at most three structures; name coupling, ownership, transaction,
   consistency, delivery, and team consequences.
5. Select `keep`, `incremental-migration`, or `new-boundary` and reject the
   alternatives explicitly.
6. Define an incremental migration with compatibility and rollback seams.
7. Require approval before structural edits and hand language mechanics to one owner.

## Output format

```yaml
problem_and_evidence:
forces_and_constraints:
baseline_without_pattern_or_refactor:
candidates_and_liabilities:
decision: keep | incremental-migration | new-boundary
rejected_alternatives:
validation:
primary_owner: gopher:application-architecture
handoff:
  owner: gopher:architecture | another explicit owner
  conceptual_boundaries:
  dependency_rules:
  migration_sequence:
  approval_status:
```

## Authorization and stopping rules

Analysis and design are read-only. Boundary, dependency-direction, persistence,
public-contract, or ADR-affecting edits require explicit approval after evidence
and alternatives are shown. If the current boundary cost is not demonstrated,
recommend the no-refactor baseline and the probes that would change the decision.

## Quality checklist

- Tie every boundary to capability ownership and change pressure.
- Separate conceptual architecture from language packaging.
- Include the no-refactor baseline and a rollback-compatible migration.
- Define dependency rules that a deterministic check can enforce.
- Keep system topology, infrastructure, schemas, and deployment out of scope.

## References

- `references/boundaries.md` — boundary discovery and ownership.
- `references/styles.md` — layered, ports/adapters, and modular-monolith forces.
- `references/dependency-direction.md` — policy and dependency rules.
- `references/migration.md` — incremental migration protocol.
- `references/validation.md` — observable architecture gates.
- `references/anti-patterns.md` — common structural failure modes.
