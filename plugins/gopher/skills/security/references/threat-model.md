# Threat Model

Capture the model before scanning for issues:

```yaml
scope:
authorization:
assets:
actors:
entry_points:
trust_boundaries:
security_invariants:
impact_categories:
excluded_targets:
```

For each hypothesis, state attacker capability, preconditions, action, violated
invariant, affected asset, and observable impact. Prioritize exposed and
reachable paths over pattern matching. Update the model when new evidence
changes a boundary or actor capability.
