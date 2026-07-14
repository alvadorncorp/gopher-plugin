# Review Controller

## Immutable bundle

Capture once before dispatch:

```yaml
review_id:
intent_and_scope:
invariants:
base_and_diff_range:
diff:
changed_files:
affected_call_sites:
public_contracts:
go_version_and_project_conventions:
existing_adrs_or_constraints:
verification_commands:
verification_results:
decisions_taken:
```

Use a concrete base SHA and head SHA. A changed head invalidates the bundle.
Each reviewer receives the same bundle plus exactly one lens reference and sees
no peer report.

## Lifecycle

1. Validate mode and gather bundle.
2. Run shared verification once.
3. Open one dispatch window for all selected lenses.
4. Drain every reviewer when one fails.
5. Retry a failed lens once with corrected context.
6. Mark overall review `INCOMPLETE` after a second lens failure.
7. Consolidate only after every possible result is collected.

The controller prepares and consolidates; it does not act as an extra reviewer.
