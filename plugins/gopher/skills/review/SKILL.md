---
name: review
description: Reviews Go diffs read-only through explicit correctness, tests, security, architecture, concurrency, performance, and complexity lenses, then consolidates findings and verdicts. Use during development after a local implementation completes, before opening a PR, or when the user asks to review a diff/PR. Supports exact --mode subsets, --mode full, --mode auto (heuristic lenses), and --mode delta (risk-surface focused). Fixes and technical solution ownership remain with canonical peers — never apply fixes in this skill.
---

# Go Multi-lens Review

## Context and ownership

Own read-only review fan-out, deterministic consolidation, narrow adjudication,
and verdict. Primary owner: `gopher:review`. This is the sole read-only bounded
orchestrator in Gopher — repository-wide or multidimensional refactoring is the
separate bounded orchestrator `gopher:refactor` — and is not an entry point for
routine development. Hand implementation fixes to the finding's `owner`
(`gopher:<skill>`); leave production code, generated output, and fix application
unchanged in this skill.

## Modes

Allowed lenses, in canonical order: `correctness`, `tests`, `security`,
`architecture`, `concurrency`, `performance`, and `complexity`.

- `--mode full` selects all seven.
- `--mode correctness` selects one.
- `--mode tests,security` selects exactly those two in canonical order.
- `--mode auto` selects a heuristic subset from the table below, writes
  `selected_lenses` and `selection_reasons` into the bundle, reports them, and
  dispatches without confirmation.
- `--mode delta` captures the immutable bundle, sets `scope: delta`, restricts
  reviewer attention to changed files, affected call sites, and public contracts
  listed in the bundle, and selects lenses via the same heuristic table unless
  the user also passed an explicit lens list as `--mode delta:tests,security`
  (optional form). When a harness cannot parse the `delta:<lenses>` form, treat
  `delta` as heuristic lenses with risk-surface scope notes in the bundle.
- Any comma-separated subset must contain unique allowed names, ordered by the
  canonical list above.

An explicit mode is exact. Without `--mode`, perform only scope preflight,
recommend lenses with reasons, and wait for confirmation before dispatch —
unless project `[workflow].post_implementation_review` is `auto` and the request
uses post-implementation or pre-PR review intent without an explicit mode; then
behave as `--mode auto` and report `mode_source: workflow-policy`.

### Heuristic lens table (`auto` / `delta`)

Always include `correctness` and `tests` unless the diff is documentation-only
with no Go files (then recommend skip / no dispatch and report that).

| Diff signal (any match) | Add lens |
|---|---|
| only `*_test.go` among Go files | keep `tests` and `correctness` by default; treat test-only production helpers as still requiring both |
| `crypto/`, auth, JWT, password, TLS, `http.Client` + user URL | `security` |
| `go.mod` / `go.sum`, exported API signature changes, new package | `architecture` |
| `go ` keyword, `chan`, `Mutex`, `WaitGroup`, `Context` cancel paths | `concurrency` |
| nested loops over collections, `bytes.Buffer` in hot-path comments, pprof/bench files | `performance` |
| net +N growth of roughly 30+ lines in one function, or new nested branch clusters in the diff | `complexity` |

Default automatic set when no extra signal: `correctness,tests`.
Expand `auto` to additional lenses only when a table signal matches each added
lens, or when the user asked for `full`.

## Workflow

1. Parse and validate the logical mode (`full`, subset, `auto`, `delta`, or
   missing). For `auto`/`delta`, materialize the exact lens list into the bundle
   as `selected_lenses` (plus `selection_reasons`) before dispatch and treat that
   list as the selected mode for consolidation.
2. Capture one immutable bundle using `references/controller.md`. On re-review
   after fixes, allocate a new `review_id` and set `parent_review_id` to the
   previous `review_id`.
3. Run shared verification once before fan-out; reviewers receive those results
   and leave shared build/test targets to the controller.
4. Load the active harness adapter and one lens file per selected lens.
5. Dispatch one distinct read-only reviewer per selected lens, in successive
   parallel windows of at most `agents.reviewer_max_parallel` reviewers each.
   The windows partition the selection so every selected lens runs. If
   concurrency is unavailable, run the same isolated reviews sequentially and
   report the degradation.
6. Drain every reviewer in a window before opening the next, and drain the union
   of all windows before consolidating. Retry one failed lens once with corrected
   context; the retry opens a window of its own and stays inside the same bound.
7. Preserve each report and consolidate using `references/consolidation.md`.
8. Use one narrow read-only adjudicator only for a genuine validity/impact
   disagreement; it receives the conflict and searches for no new findings.
9. Emit the verdict, `fix_queue`, and peer handoffs. Leave production code
   unchanged; route fixes to each finding's `owner`.

For each gate, classify supporting claims as `observed`, `inferred`, or
`unknown`. When an unknown blocks the next gate, stop there, record the missing
evidence under `MISSING_EVIDENCE` or `limitations`, and continue only after that
evidence is supplied or the run is marked `INCOMPLETE`.

## Reviewer output

```yaml
LENS: correctness | tests | security | architecture | concurrency | performance | complexity
STATUS: COMPLETE | NEEDS_EVIDENCE | BLOCKED
FINDINGS:
  - id:
    severity: critical | important | minor
    confidence: high | medium | low
    file_line:
    failure_scenario:
    evidence:
    impact:
    actionable_fix:
    owner: gopher:<skill>
NO_FINDINGS: yes | no
MISSING_EVIDENCE:
```

## Verdicts

- `NEEDS_FIXES`: at least one critical or important finding.
- `APPROVED_WITH_NOTES`: every selected lens completed and findings are minor only.
- `APPROVED`: every selected lens completed with no findings.
- `INCOMPLETE`: a selected lens or required adjudication failed after its retry.

A new diff invalidates prior approval. Fixes occur in a separate phase; a fresh
review receives a new immutable bundle.

A lens is never left undispatched, so no verdict describes that state. A bound
below the selected lens count changes how many windows the run opens and changes
nothing about which lenses run.

## Parallel window

Every run reports one `parallel_window` value with its verdict:

- `full` — every selected lens ran in one window.
- `bounded-by-policy` — the effective `agents.reviewer_max_parallel` is below the
  selected lens count, so the selection ran in successive windows of at most that
  many reviewers.

`parallel_window` is never the same thing as
`degradation: sequential_no_parallel_support`. A bound of `1` is still
`parallel_window: bounded-by-policy`, because the project chose it; the
degradation states only that the host could not run lenses together.

## fix_queue

After consolidation, emit an ordered fix queue derived from findings:

    fix_queue:
      - finding_id: <id>
        severity: critical | important | minor
        owner: gopher:<skill>
        order: <1-based, critical/important first, then file path>
        authorization_gate: none | approval-required | blocked

Rules:
- Every critical/important finding appears once.
- Minor findings may be omitted from the queue when `delta` mode is active; they
  remain in consolidated findings.
- Owners match the finding `owner` field; fix owners are canonical peers only
  (`gopher:review` is never a fix owner).
- The queue is advisory ordering for the session agent; edit authorization stays
  with the session agent and peer owners.

## Re-review contract

A new diff invalidates prior approval. When the user requests re-review after
fixes, capture a new immutable bundle with a new `review_id` and set
`parent_review_id` to the previous `review_id`. Capture fresh lens reports for
the new review; parent lens reports and parent verdicts remain historical only.

## Quality checklist

- Materialize `selected_lenses` (and `selection_reasons` for `auto`/`delta`)
  before dispatch; exact modes stay exact.
- Capture one immutable bundle (`review_id`, optional `parent_review_id`,
  `scope`) before any lens runs.
- Run every selected lens; report `parallel_window` and `policy_status`.
- Consolidate only after every window drains; adjudicate only genuine
  validity/impact conflicts.
- Emit verdict, `fix_queue`, handoffs, and limitations; leave code unchanged.
- On re-review, use a new `review_id` with `parent_review_id` set; skip parent
  lens reuse.

## References

- `references/controller.md` — bundle capture, dispatch lifecycle, failure handling.
- `references/consolidation.md` — preservation, deduplication, adjudication, verdict.
- `references/severity.md` — shared severity and confidence scales.
- `references/harnesses/codex.md`, `references/harnesses/claude.md`, `references/harnesses/grok.md`, `references/harnesses/kimi.md`, and `references/harnesses/opencode.md` — native adapters.
- `references/lenses/*.md` — seven non-overlapping review criteria.
