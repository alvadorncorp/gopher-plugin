# Local reversible refactoring

`gopher:developer` refactors idiomatic Go directly, within a single local,
reversible scope. It leaves repository-wide metric assessment and
multidimensional orchestration to their canonical owners.

## Focused workflow

```text
RESOLVE EFFECTIVE CONFIG -> FOCUSED BASELINE -> CHARACTERIZATION SAFETY NET -> LOCAL REVERSIBLE REFACTOR -> FOCUSED TESTS -> RE-MEASURE
```

1. Resolve effective config from `gopher:config` for the relevant scope
   and targets.
2. Establish a FOCUSED BASELINE that passes for the unit under change.
3. Create or identify a passing characterization safety net before mutation;
   it must pin the behavior the refactor preserves.
4. Apply the local, reversible refactor with idiomatic Go, preserving behavior.
5. Run focused behavior tests for the changed unit and keep them green through
   any follow-up refactoring.
6. Re-measure the same way and report the change, tests, and any limitation.

## Boundaries and routing

- Keep the change local and reversible. Route repository-wide or multidimensional
  work — two or more of correctness, test-safety, complexity, and modernization
  — to `gopher:refactor`.
- Route single-dimension specialist work to its owner: complexity to
  `gopher:complexity`, test quality to `gopher:test-quality`, modernization to
  `gopher:modernize`.
- Cross-package, public-contract, persistence, security-boundary, and
  ADR-affecting changes keep their existing approval gates and canonical owners.
