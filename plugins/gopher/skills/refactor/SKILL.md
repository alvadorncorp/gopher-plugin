---
name: refactor
description: Orchestrates repository-wide or multidimensional Go refactoring from an immutable baseline through prioritized, sequential remediation and a fresh read-only review. Use during planning to inventory multi-dimension debt (complexity + tests + modernization together) in plan mode without applying changes; use full orchestration only when the user asks to apply remediation. Route single-dimension work to its canonical owner and local reversible refactors (rename, extract helper in one function/package) to gopher:developer. Do not use for package/module public-contract design (gopher:architecture) or multi-lens PR review (gopher:review).
---

# Go Refactor Orchestrator

## Context and ownership

Own bounded, multidimensional refactoring: capture an immutable baseline,
coordinate the specialist owners in priority order, and close with a fresh
read-only review. Primary owner: `gopher:refactor`. This is the second bounded
orchestrator in Gopher, alongside the read-only `gopher:review`.

Coordinate through the canonical owners. Hand single-dimension work to its
owner (`gopher:complexity`, `gopher:test-quality`, `gopher:modernize`,
`gopher:security`, `gopher:concurrency`, `gopher:performance`,
`gopher:architecture`) and a local reversible refactor to `gopher:developer`.
Record and follow every handoff using `references/handoffs.md`, keeping each
dimension with its owner.

## Modes

| Mode | When | Stop condition |
|---|---|---|
| `plan` | Planning or inventorying multidimensional cleanup; user did not ask to apply changes | `PLAN_READY` with prioritized backlog, handoffs, and blockers; no production mutation; no mandatory final review |
| `remediate` | User explicitly wants sequential remediation applied (default when they ask to run/coordinate the refactor) | `COMPLETE`, `COMPLETE_WITH_LIMITATIONS`, or `BLOCKED` after re-measurement and fresh `gopher:review` |

State the mode before any phase and carry it in the report. Select `plan` when
the request is analysis, inventory, or backlog-only. Select `remediate` when the
user asks to apply, run, or coordinate the refactor. In `plan` mode remain
read-only through prioritization and emit `PLAN_READY`; never enter a mutating
phase in `plan` mode.

## State machine

```text
CONFIGURATION -> IMMUTABLE BASELINE -> MULTIDIMENSIONAL ANALYSIS -> PRIORITIZATION
  plan mode stops -> PLAN_READY
  remediate mode continues -> SEQUENTIAL REMEDIATION -> RE-MEASUREMENT -> FRESH REVIEW
```

Read-only analysis may run per dimension. Mutating phases run sequentially so
each one starts from a known passing state (`references/controller.md`).

## Workflow

1. Scope preflight: resolve whether more than one dimension applies. If exactly
   one dimension applies, hand off to that specialist (`handoff: gopher:<skill>`),
   set `primary_owner` to that specialist, and stop. Hand a local reversible
   refactor to `gopher:developer` the same way. Open multidimensional
   orchestration only when two or more dimensions apply together.
2. Load the effective configuration. If it is absent, offer
   `gopher:config --bootstrap`; if the user declines, use ephemeral defaults,
   report them explicitly, and state that no project policy was persisted.
3. Capture an immutable baseline (`references/baseline.md`): source commit,
   diff range, config path/state/hash, and a passing build and test run.
   Classify baseline and analysis claims as `observed`, `inferred`, or
   `unknown`. When an unknown blocks the next transition, stop at that gate and
   name the exact evidence or user decision required to continue.
4. Gather read-only analysis from the specialist owners for each applicable
   dimension.
5. Prioritize per `references/prioritization.md`.
6. If mode is `plan`, emit the `refactor_plan` backlog (`references/reports.md`),
   record handoffs as proposed (not executed), set `status: PLAN_READY`, and stop.
   Remain read-only: skip remediation, re-measurement, and `gopher:review` in
   `plan` mode.
7. If mode is `remediate`, remediate sequentially. Each mutating phase has its own
   passing boundary and evidence bundle; a failed phase stops subsequent mutations
   and preserves unrelated work.
8. Re-measure each dimension by the same method used for the baseline.
9. Run a fresh read-only review with `gopher:review` and report the terminal
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

- `PLAN_READY`: `plan` mode completed analysis and prioritization; no mutating
  phase ran; backlog and proposed handoffs are recorded.
- `COMPLETE`: configured objectives are met and all applicable gates pass.
- `COMPLETE_WITH_LIMITATIONS`: safe in-scope work is complete, but named tools or
  dimensions were unavailable or advisory targets remain.
- `BLOCKED`: a mandatory safety, evidence, configuration, or authorization
  condition prevents safe mutation.

## Output format

```yaml
selected_skill: gopher:refactor
primary_owner: gopher:refactor
mode: plan | remediate
status: COMPLETE | COMPLETE_WITH_LIMITATIONS | BLOCKED | PLAN_READY
config_status: ABSENT | VALID | MIGRATION_AVAILABLE | INVALID | UNSUPPORTED_VERSION
baseline_status: passing | failing | not-run
selected_dimensions: [correctness, security, tests, complexity, concurrency, performance, modernization]
authorization_gate: none | approval-required | blocked
handoff: gopher:<skill> | null
refactor_plan:
  items: []
```

On a single-dimension or local-refactor preflight handoff, set `primary_owner`
and `handoff` to that specialist and omit multidimensional remediation fields
that do not apply. For every successful `plan` result, emit `refactor_plan`
with prioritized items (`references/reports.md`).

## Authorization boundaries

- Report `authorization_gate` as `none` when work stays inside already-approved
  specialist scope, `approval-required` until the user grants explicit approval,
  and `blocked` when policy, config, baseline, or a mandatory gate forbids
  progress.
- The final review runs `gopher:review` read-only and applies no fixes; a new
  diff invalidates a prior approval. Fresh final review runs only in `remediate`.
- Each specialist keeps its own authorization gate; the orchestrator requests
  and records approvals and defers to each specialist gate after handoff.
- Mutating phases stay sequential; run one mutating phase at a time on
  intersecting scope.
- Ephemeral defaults are reported as ephemeral; only `gopher:config` persists
  project policy.

## Quality checklist

- State `mode` before any phase; keep `plan` read-only through `PLAN_READY`.
- Capture an immutable baseline before any remediation; stop subsequent mutations
  when a phase fails.
- Hand single-dimension and local reversible work to the canonical owner without
  opening multidimensional orchestration.
- Record every handoff (proposed in `plan`, executed in `remediate`) with its
  authorization gate.
- Emit exactly one terminal status and a `refactor_plan` whose item order follows
  prioritization.

## References

- `references/controller.md` — the bounded flow, sequencing, and handoff discipline.
- `references/baseline.md` — immutable baseline capture and phase-boundary recovery.
- `references/prioritization.md` — the six-step priority order.
- `references/handoffs.md` — recording and following specialist handoffs.
- `references/reports.md` — the evidence and output contract and terminal states.
- `references/harnesses/codex.md`, `references/harnesses/claude.md`, `references/harnesses/grok.md`, `references/harnesses/kimi.md`, and `references/harnesses/opencode.md` — per-harness orchestration.
