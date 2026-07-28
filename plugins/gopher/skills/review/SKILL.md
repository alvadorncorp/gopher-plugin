---
name: review
description: Reviews Go diffs read-only through explicit correctness, tests, security, architecture, and concurrency-performance lenses, then consolidates findings and verdicts. Use for review, diff, or PR intent. Fixes and technical solution ownership remain with canonical peers.
---

# Go Multi-lens Review

## Context and ownership

Own read-only review fan-out, deterministic consolidation, narrow adjudication,
and verdict. Primary owner: `gopher:review`. This is the sole read-only bounded
orchestrator in Gopher — repository-wide or multidimensional refactoring is the
separate bounded orchestrator `gopher:refactor` — and is not an entry point for
routine development.

## Modes

Allowed lenses are `correctness`, `tests`, `security`, `architecture`, and
`concurrency-performance`.

- `--mode full` selects all five.
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
5. Dispatch one distinct read-only reviewer per selected lens in one parallel
   window. If concurrency is unavailable, run the same isolated reviews
   sequentially and report the degradation.
6. Drain all in-flight reviewers. Retry one failed lens once with corrected context.
7. Preserve each report and consolidate using `references/consolidation.md`.
8. Use one narrow read-only adjudicator only for a genuine validity/impact
   disagreement; it receives the conflict and cannot search for new findings.
9. Emit the verdict and route findings to canonical owners. Make no code edits.

## Reviewer output

```yaml
LENS: correctness | tests | security | architecture | concurrency-performance
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

## References

- `references/controller.md` — bundle capture, dispatch lifecycle, failure handling.
- `references/consolidation.md` — preservation, deduplication, adjudication, verdict.
- `references/severity.md` — shared severity and confidence scales.
- `references/harnesses/codex.md`, `references/harnesses/claude.md`, and `references/harnesses/grok.md` — native adapters.
- `references/lenses/*.md` — five non-overlapping review criteria.
