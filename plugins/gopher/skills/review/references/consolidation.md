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
Per-lens reports; Consolidated findings; Adjudications; Verdict; Handoffs;
Limitations/degradation.
