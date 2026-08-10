# Local reversible refactoring

`gopher:developer` owns idiomatic Go refactors within one affected package or
local API and a reversible scope. It reports repository-wide metric assessment
and multidimensional orchestration to their canonical owners.

## Focused workflow

```text
RESOLVE EFFECTIVE CONFIG -> FOCUSED BASELINE -> CHARACTERIZATION SAFETY NET -> LOCAL REVERSIBLE REFACTOR -> FOCUSED TESTS -> RE-MEASURE
```

1. Run the config preflight from `references/project-detection.md` for the
   affected package and targets. Record `config_status`, independently resolved
   `idiom_policy` and `test_workflow`, and each source (`session | file | adopted
   | default`) before the baseline. For `ABSENT`, use documented effective
   defaults without persisting them; for `MIGRATION_AVAILABLE`, use its
   effective values without migrating. For `INVALID` or `UNSUPPORTED_VERSION`,
   do read-only diagnosis only, stop production edits, and hand off recovery to
   `gopher:config`.
2. Establish a FOCUSED BASELINE that passes for the affected package or
   behavior. Record the exact command, exit status, and concise observation
   before classifying or mutating the refactor.
3. Create or identify a passing characterization safety net before mutation;
   it must pin the behavior the refactor preserves. Record its focused command
   and passing result.
4. Apply the local, reversible refactor with idiomatic Go, using the resolved
   `idiom_policy` and declared Go version while preserving behavior and public
   contracts.
5. Run focused behavior tests for the changed unit and keep them green through
   any follow-up refactoring. If a focused check fails, stop further mutation,
   return to the last green state when the change is reversible, and report the
   failure as evidence before continuing.
6. Re-measure with the same focused commands and method, compare with the
   baseline, and report changed files and behavior, exact tests and results,
   limitations, and any handoff using the parent output contract.

## Evidence gates

Classify each claim as `observed`, `inferred`, or `unknown`. Advance only when
the prior step's evidence is recorded: resolved config and policies -> passing
baseline -> passing characterization -> scoped refactor -> green focused tests
-> comparable re-measurement. If required evidence is `unknown` or a gate
fails, stop at that gate, name the exact command, file, or owner decision
needed, preserve the last green state, and record the limitation instead of
inferring a pass.

## Boundaries and routing

- Keep the change local and reversible. Route repository-wide or multidimensional
  work — two or more of correctness, test-safety, complexity, and modernization
  — to `gopher:refactor`.
- Route single-dimension specialist work to its owner: complexity to
  `gopher:complexity`, test quality to `gopher:test-quality`, modernization to
  `gopher:modernize`.
- Cross-package, public-contract, persistence, security-boundary, and
  ADR-affecting changes keep their existing approval gates and canonical owners.

## from_slice local implementation

When executing a Structure Decision Card slice, keep FOCUSED workflow. The slice
`verification` is an additional green gate, not a replacement for the
characterization safety net on `change_class: refactor`.
