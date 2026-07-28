---
name: design-patterns
description: Diagnoses forces and selects, combines, rejects, or names no code/module pattern from a language-agnostic catalog. Use when users ask to choose, compare, or review a design pattern. Route Go implementation, application architecture, concurrency, and performance mechanics to their canonical peers.
---

# Design Patterns

## Context and ownership

Own code- and module-level pattern diagnosis. Begin with the problem and forces,
not a pattern name. Keep the catalog language-agnostic and use stable
`pattern.*` identifiers so language owners can adapt or veto a selection.

Primary owner: `gopher:design-patterns`.

Route internal application boundaries to `gopher:application-architecture`, Go
implementation to `gopher:developer`, Go package/public-contract decisions to
`gopher:architecture`, concurrency mechanics to `gopher:concurrency`, and
performance mechanics to `gopher:performance`.

## Workflow

1. Capture the problem, evidence, desired outcome, and current design.
2. State forces and constraints; mark missing evidence explicitly.
3. Describe the direct baseline without a pattern or refactor.
4. Load only the problem-family reference needed for the request.
5. Compare at most three candidates using signals, counter-signals, mechanics,
   liabilities, useful combinations, and validation questions.
6. Decide `selected`, `rejected`, `combined`, or `no-pattern`. A named request
   still receives the baseline and counter-signals.
7. Define proportional validation and hand off language mechanics to one owner.

Use `references/diagnostics.md` when the family is unclear or the request names
an anti-pattern candidate. Use the other references only after classifying the
problem family.

## Output format

Use the compact form for a local reversible decision and every field for a
structural decision:

```yaml
problem_and_evidence:
forces_and_constraints:
baseline_without_pattern_or_refactor:
candidates_and_liabilities:
decision: selected | rejected | combined | no-pattern
rejected_alternatives:
validation:
primary_owner: gopher:design-patterns
handoff:
  owner: gopher:<skill>
  pattern: pattern.<id> | none
  language_mapping: go.<id> | pending
  evidence:
  liabilities:
```

## Authorization and stopping rules

Analysis and design output are read-only. Implementation starts only after a
language owner accepts the handoff. Structural, public-contract, persistence,
security-boundary, or ADR-affecting changes require evidence, alternatives,
and explicit approval before editing. If evidence cannot distinguish the
leading candidates, return the direct baseline plus the missing evidence.

## Quality checklist

- Start from forces and include the direct baseline.
- Use only IDs listed in `references/diagnostics.md`.
- Give every candidate at least one liability and counter-signal.
- Keep language mechanics in the receiving owner.
- Prefer `no-pattern` when direct code satisfies the forces.
- Make validation observable and proportionate to the decision risk.

## References

- `references/construction.md` — object/configuration creation decisions.
- `references/composition.md` — seams, wrappers, composition, and dispatch.
- `references/behavior.md` — commands, events, and coordination.
- `references/state-traversal.md` — iteration, state, traversal, and deferred cards.
- `references/values-errors.md` — optional and fallible value protocols.
- `references/diagnostics.md` — canonical index, dispositions, and card schema.
