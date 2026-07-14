# Falsifiable Diagnosis Heuristic

## Hypothesis record

```yaml
hypothesis:
explains:
predicts:
evidence_for:
evidence_against:
discriminating_probe:
probe_risk:
result:
```

Rank at most three active hypotheses. Prefer a probe that yields different
predictions for the top two, is local and reversible, and uses a project-adopted
tool. Re-rank after every probe; remove weakened hypotheses rather than adding
an unbounded list.

`ATTRIBUTED` requires a reproducible signal, a hypothesis that explains it,
weakened leading alternatives, and one supported owner. Timing correlation,
log adjacency, a tool warning, or a keyword alone remains evidence to test.
