# Incremental migration

Apply modernization as a sequence of small, verifiable steps. Preview first,
apply one increment, verify, then continue.

## Sequence

1. Establish a compatibility baseline: a passing build and test run under the
   current declared versions.
2. Produce a preview of the proposed changes, grouped by kind (language, API,
   module, dependency).
3. With `apply_fixes = false`, stop here and report the preview.
4. With application authorized, apply one increment, run the adopted build and
   tests, and confirm the baseline still passes.
5. Repeat per increment; a failing increment stops the sequence, preserves the
   last passing state, and reports where it stopped.

## Records

- Record the exact tool name and version and the resolved target version with
  every increment.
- Preserve unrelated user changes; keep each increment scoped to its stated
  modernization.

## Manual review required

Route to a human reviewer any merge conflict, any generated or machine-authored
comment a rewrite would touch, and any change that affects a contract. These are
never applied automatically.
