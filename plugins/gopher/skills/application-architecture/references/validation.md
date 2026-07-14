# Architecture Validation

Select gates proportional to the decision:

- Dependency graph or import rule for every directional constraint.
- Characterization and contract tests around moved behavior.
- Cycle detection and prohibited-reference scans.
- Public/API compatibility checks where consumers cross the boundary.
- Data ownership and transaction tests when invariants move.
- Diff review against the approved boundary and migration sequence.

Validation succeeds only when commands, expected results, and rollback evidence
are recorded. Diagrams and folder layout are explanatory evidence, not gates.
