---
name: review
description: Reviews Go diffs read-only through explicit correctness, tests, security, architecture, concurrency, performance, and complexity lenses, then consolidates findings and verdicts. Use for review, diff, or PR intent. Fixes and technical solution ownership remain with canonical peers.
---

# Go Multi-lens Review

## Context and ownership

Own read-only review fan-out, deterministic consolidation, narrow adjudication,
and verdict. Primary owner: `gopher:review`. This is the sole read-only bounded
orchestrator in Gopher — repository-wide or multidimensional refactoring is the
separate bounded orchestrator `gopher:refactor` — and is not an entry point for
routine development.

## Modes

Allowed lenses are `correctness`, `tests`, `security`, `architecture`,
`concurrency`, `performance`, and `complexity`.

- `--mode full` selects all seven.
- `--mode correctness` selects one.
- `--mode tests,security` selects exactly those two in canonical order.
- Any comma-separated subset must contain unique allowed names.

An explicit mode is exact. Without `--mode`, perform only scope preflight,
recommend lenses with reasons, and wait for confirmation before dispatch.

## Workflow

1. Parse and validate the logical mode.
2. Capture one immutable bundle using `references/controller.md`.
3. Run shared verification once before fan-out; reviewers receive results and
   do not execute shared build/test targets.
4. Load the active harness adapter and one lens file per selected lens.
5. Dispatch one distinct read-only reviewer per selected lens, in successive
   parallel windows of at most `agents.reviewer_max_parallel` reviewers each.
   The windows partition the selection, so no selected lens is ever left
   undispatched. If concurrency is unavailable, run the same isolated reviews
   sequentially and report the degradation.
6. Drain every reviewer in a window before opening the next, and drain the union
   of all windows before consolidating. Retry one failed lens once with corrected
   context; the retry opens a window of its own and stays inside the same bound.
7. Preserve each report and consolidate using `references/consolidation.md`.
8. Use one narrow read-only adjudicator only for a genuine validity/impact
   disagreement; it receives the conflict and cannot search for new findings.
9. Emit the verdict and route findings to canonical owners. Make no code edits.

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

A new diff invalidates prior approval. Fixes occur in a separate phase and a
fresh review receives a new immutable bundle.

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

## References

- `references/controller.md` — bundle capture, dispatch lifecycle, failure handling.
- `references/consolidation.md` — preservation, deduplication, adjudication, verdict.
- `references/severity.md` — shared severity and confidence scales.
- `references/harnesses/codex.md`, `references/harnesses/claude.md`, `references/harnesses/grok.md`, and `references/harnesses/kimi.md` — native adapters.
- `references/lenses/*.md` — seven non-overlapping review criteria.
