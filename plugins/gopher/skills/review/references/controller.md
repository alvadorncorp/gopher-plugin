# Review Controller

## Immutable bundle

Capture once before dispatch:

```yaml
review_id:
parent_review_id:
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
selection_reasons:
scope: full | delta
```

Use a concrete base SHA and head SHA. A changed head invalidates the bundle.
Each reviewer receives the same bundle plus exactly one lens reference and sees
no peer report.

## Lifecycle

1. Validate mode and gather bundle.
2. Read the `[agents]` policy before any dispatch, as `## Agent policy` below
   describes.
3. Run shared verification once.
4. Dispatch the selected lenses in successive windows of at most the effective
   bound, never leaving a selected lens undispatched.
5. Drain every reviewer in a window before opening the next, and drain every
   reviewer in flight when one fails.
6. Retry a failed lens once with corrected context, in a window of its own that
   stays inside the same bound.
7. Mark overall review `INCOMPLETE` after a second lens failure.
8. Consolidate only after the union of every window has drained and every
   possible result is collected.

The controller prepares and consolidates; it does not act as an extra reviewer.

## auto and delta

- `auto` must write `selected_lenses` and `selection_reasons` into the bundle
  before dispatch and must not prompt for confirmation.
- `delta` uses the same bundle fields but adds `scope: delta` and instructs each
  lens reviewer to prefer changed files, affected call sites, and public
  contracts listed in the bundle over untouched packages.
- Neither mode may edit files or invoke fix owners.

## Agent policy

Read the `[agents]` table of `.gopher-plugin.toml` through the precedence
`gopher:config` defines. This applies to every review, whether the run was
delegated to the packaged `reviewer` agent or the skill was invoked directly.

- `agents.enabled = false` stops the run before the first dispatch. Report
  `policy_status: BLOCKED_BY_POLICY` and hand back without reviewing.
- The effective `agents.reviewer_max_parallel` is the window bound. Its default
  of `7` equals the lens count, so it never binds by default.
- Report `parallel_window: full` when the selection fit one window and
  `parallel_window: bounded-by-policy` when the bound forced successive windows.
  A bound of `1` is still `bounded-by-policy` and never
  `degradation: sequential_no_parallel_support`, which states only that the host
  could not run lenses together.
- Report one `policy_status` with notes, on the ordered partition
  `BLOCKED_BY_POLICY`, `NOT_CONFIGURED`, `UNVERIFIABLE`, `DIVERGED`, `ALIGNED`.
  Evaluate them in that order and report the first that holds.
  `NOT_CONFIGURED` when the parsed contract declares no `[agents]` table.
  `UNVERIFIABLE` when a role model or effort declares anything other than
  `shipped` and the active binding cannot be observed, which is the usual case,
  and is always the case on a direct skill invocation because no packaged agent
  was loaded to carry one. `BLOCKED_BY_POLICY` also holds when
  `agents.policy_divergence` is `block` and the value that would otherwise hold
  is `UNVERIFIABLE` or `DIVERGED`.

The shipped agent definition is the authoritative binding and this table is the
project's declared policy over it. Never present a declared value as an applied
one.
