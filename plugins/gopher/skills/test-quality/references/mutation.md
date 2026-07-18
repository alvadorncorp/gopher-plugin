# Mutation analysis

Mutation testing injects small faults and checks whether the suite detects them.
It is optional and advisory by default, because available Go mutation tooling is
pre-1.0 and does not scale to every repository.

## Result classes

Keep the five outcomes separate; never merge them:

- `killed`: a mutant the suite detected (a test failed). This is the goal.
- `lived`: a mutant the suite missed (all tests still passed). This exposes a gap.
- `not-covered`: the mutated line is not executed by any test.
- `timed-out`: the run exceeded its time budget; outcome unknown.
- `not-viable`: the mutant did not compile or could not run.

## Score

The normalized mutation score is:

```text
score = killed / (killed + lived)
```

Timeouts and non-viable mutations are excluded from the denominator; they never
inflate the score. Report `not-covered` alongside coverage gaps, not as kills.

## Policy

- Run mutation only when `[tools].mutation` resolves to an available, pinned
  binary (`references/tooling.md`).
- Compare the score against `test-quality.mutation_target`.
- In `advisory` mode a missing tool or a below-target score is a limitation, not
  a failure. In `required` mode a missing tool blocks the mutation dimension
  only, not the rest of the analysis.
