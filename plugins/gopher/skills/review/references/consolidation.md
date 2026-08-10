# Review Consolidation

1. Preserve each lens report unchanged under its lens identity.
2. Validate required fields and `NO_FINDINGS` consistency.
3. Merge findings only when location, root cause, and failure scenario all match.
4. Combine evidence and retain the highest demonstrated impact severity.
5. Keep separate findings when any merge key differs.
6. Send a genuine validity or impact disagreement to one narrow adjudicator.
7. Apply the verdict table from SKILL.md after lens/adjudication status is final.

Adjudicator input contains only the conflicting findings, shared evidence, and
the decision question. Outcomes are `KEEP_A`, `KEEP_B`, `MERGE`, or
`INSUFFICIENT_EVIDENCE`. The adjudicator cannot search for new findings.

Final output sections: Scope and bundle identity; Selected lenses; Verification;
Parallel window and policy; Per-lens reports; Consolidated findings;
Adjudications; Verdict; Fix queue; Parent review; Handoffs; Limitations/degradation.

`Parallel window and policy` carries two fields. `parallel_window` is `full` when
every selected lens ran in one window and `bounded-by-policy` when the effective
`agents.reviewer_max_parallel` forced successive windows; it is never the same
thing as `degradation: sequential_no_parallel_support`, which belongs in
`Limitations/degradation` and states only that the host could not run lenses
together. `policy_status` is the value `references/controller.md` resolved, with
its notes. Consolidate only after the union of every window has drained.

## Fix queue emission

Build `fix_queue` only from consolidated findings after adjudication. Sort by
severity (critical, important, minor), then by `file_line` ascending. Preserve
finding ids.
