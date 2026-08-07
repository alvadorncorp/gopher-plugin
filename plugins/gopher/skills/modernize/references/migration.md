# Incremental migration

Apply modernization as a sequence of small, verifiable steps. Preview first,
apply one increment, verify, then continue.

## Sequence

1. Establish a compatibility baseline: a passing build and test run under the
   current declared versions.
2. Produce a preview of the proposed changes, grouped by kind (language, API,
   module, dependency). For language and API modernization, the preview is
   `go fix -diff ./...` (`references/tooling.md`).
3. With `apply_fixes = false`, stop here and report the preview.
4. With application authorized, apply one increment, run the adopted build and
   tests, and confirm the baseline still passes.
5. Repeat per increment; a failing increment stops the sequence, preserves the
   last passing state, and reports where it stopped.

## The `go fix` apply loop

`go fix` routinely applies only part of what it diagnosed in one pass
(`references/tooling.md` — "Skipped fixes"). Converge with a bulk-then-triage
loop rather than treating one bulk apply as done:

1. `go fix ./...` — one bulk apply as the first increment; run the adopted
   build and tests against the baseline.
2. If the tool reports fixes remain, run `go fix -json ./...` to inventory the
   residue grouped by analyzer.
3. Apply the remainder one analyzer at a time (`go fix -<analyzer> ./...`),
   verifying against the baseline after each. Analyzer families that tend to
   touch overlapping spans — `rangeint` / `stditerators` / `slicescontains`,
   and the `strings*` family (`stringscut`, `stringscutprefix`, `stringsseq`,
   `stringsbuilder`) — are the usual conflict source; do not share an
   increment between them.
4. Repeat step 3 until `go fix -diff ./...` exits clean, or until a round
   applies nothing new. **A no-progress round terminates the loop**; report the
   remaining diagnostics as a limitation rather than looping indefinitely.
5. Reconcile the last `-json` inventory against what actually landed. Anything
   still diagnosed after a no-progress round is either a generated-file skip
   (silent by design, and out of scope — generated-output modernization
   belongs to `gopher:codegen`) or needs the manual review below.

## Records

- Record the exact tool name and version and the resolved target version with
  every increment.
- Preserve unrelated user changes; keep each increment scoped to its stated
  modernization.

## Manual review required

Route to a human reviewer any merge conflict, any generated or machine-authored
comment a rewrite would touch, and any change that affects a contract. These are
never applied automatically. A concurrent-modification abort from `go fix`
means the tree changed under the tool mid-run — re-establish the compatibility
baseline before retrying rather than assuming the partial state is safe.
