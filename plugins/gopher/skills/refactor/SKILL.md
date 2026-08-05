---
name: refactor
description: Orchestrates repository-wide or multidimensional Go refactoring from an immutable baseline through prioritized, sequential remediation and a fresh read-only review. Use to coordinate correctness, test-safety, complexity, and modernization work across a codebase. Route single-dimension work to its canonical owner and local reversible refactors to `gopher:developer`.
---

# Go Refactor Orchestrator

## Context and ownership

Own bounded, multidimensional refactoring: capture an immutable baseline,
coordinate the specialist owners in priority order, and close with a fresh
read-only review. Primary owner: `gopher:refactor`. This is the second bounded
orchestrator in Gopher, alongside the read-only `gopher:review`.

Coordinate through the canonical owners. Route single-dimension work to its
owner (`gopher:complexity`, `gopher:test-quality`, `gopher:modernize`,
`gopher:security`, `gopher:concurrency`, `gopher:performance`,
`gopher:architecture`) and a local reversible refactor to `gopher:developer`.
Record and follow every handoff using `references/handoffs.md`, keeping each
dimension with its owner.

## State machine

```text
CONFIGURATION -> IMMUTABLE BASELINE -> MULTIDIMENSIONAL ANALYSIS -> PRIORITIZATION -> SEQUENTIAL REMEDIATION -> RE-MEASUREMENT -> FRESH REVIEW
```

Read-only analysis may run per dimension. Mutating phases run sequentially so
each one starts from a known passing state (`references/controller.md`).

## Workflow

1. Load the effective configuration. If it is absent, offer
   `gopher:config --bootstrap`; if the user declines, use ephemeral defaults,
   report them explicitly, and state that no project policy was persisted.
2. Capture an immutable baseline (`references/baseline.md`): source commit,
   diff range, config path/state/hash, and a passing build and test run.
3. Choose the applicable dimensions and gather read-only analysis from the
   specialist owners.
4. Prioritize per `references/prioritization.md`.
5. Remediate sequentially. Each mutating phase has its own passing boundary and
   evidence bundle; a failed phase stops subsequent mutations and preserves
   unrelated work.
6. Re-measure each dimension by the same method used for the baseline.
7. Run a fresh read-only review with `gopher:review` and report the terminal
   state, applied and skipped work, handoffs, blockers, and limitations.

## Prioritization

1. Correctness and security risk.
2. Test safety.
3. Complexity reduction.
4. Concurrency and performance dimensions.
5. Modernization.
6. Whole-scope validation and a fresh review.

## Proportional blockers

- A failing test baseline blocks refactoring but permits analysis.
- Missing behavior tests block production refactoring; an explicitly approved
  safety-net phase may add characterization tests first.
- `MIGRATION_AVAILABLE` is a supported past schema whose rules all pass:
  analysis and remediation proceed on that contract's effective values, and
  migrating it belongs to `gopher:config --bootstrap`.
- A dirty working tree permits analysis; edits stay scoped and preserve
  unrelated user changes.
- A missing optional tool is a limitation; a tool configured as required blocks
  only its dimension, not unrelated read-only analysis.
- Cross-package, public-contract, module, security-boundary, persistence, or
  ADR-affecting changes retain their canonical owner and approval gate.
- A failed or skipped dimension stays visible in the result and is reported with
  its actual status.

## Terminal states

- `COMPLETE`: configured objectives are met and all applicable gates pass.
- `COMPLETE_WITH_LIMITATIONS`: safe in-scope work is complete, but named tools or
  dimensions were unavailable or advisory targets remain.
- `BLOCKED`: a mandatory safety, evidence, configuration, or authorization
  condition prevents safe mutation.

## Output format

```yaml
selected_skill: gopher:refactor
primary_owner: gopher:refactor
status: COMPLETE | COMPLETE_WITH_LIMITATIONS | BLOCKED
config_status: ABSENT | VALID | MIGRATION_AVAILABLE | INVALID | UNSUPPORTED_VERSION
baseline_status: passing | failing | not-run
selected_dimensions: [correctness, security, tests, complexity, concurrency, performance, modernization]
authorization_gate: none | approval-required | blocked
handoff: gopher:<skill> | null
```

## Authorization boundaries

- The final review runs `gopher:review` read-only and cannot apply fixes; a new
  diff invalidates a prior approval.
- Each specialist keeps its own authorization gate; the orchestrator requests
  and records approvals and defers to each specialist gate.
- Mutating phases stay sequential; never run two mutating phases concurrently on
  intersecting scope.
- Ephemeral defaults are reported as ephemeral; only `gopher:config` persists
  project policy.

## References

- `references/controller.md` — the bounded flow, sequencing, and handoff discipline.
- `references/baseline.md` — immutable baseline capture and phase-boundary recovery.
- `references/prioritization.md` — the six-step priority order.
- `references/handoffs.md` — recording and following specialist handoffs.
- `references/reports.md` — the evidence and output contract and terminal states.
- `references/harnesses/codex.md`, `references/harnesses/claude.md`, `references/harnesses/grok.md`, and `references/harnesses/kimi.md` — per-harness orchestration.
