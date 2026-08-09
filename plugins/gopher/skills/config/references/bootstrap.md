# `--bootstrap` flow

Bootstrap creates or edits `.gopher-plugin.toml`. It never writes without a
shown preview or diff and explicit confirmation, and it never overwrites a file
merely because one exists.

## File absent

1. Confirm the detected project root and the target path.
2. Ask whether to accept all defaults or customize:
   - Accept all: prepare the complete canonical file from
     `templates/default.gopher-plugin.toml`.
   - Customize: ask only the relevant interactive questions (below), leaving
     every unasked value at its default.
3. Show the exact file preview.
4. Require confirmation, then write the file once.
5. Report the written path and the resulting `VALID` state.

### Interactive question set (customize)

Ask only what the user wants to change; accept the default for anything skipped:

- Project scope: `module_roots` and `package_patterns`.
- Complexity: `mode`, and any of `cyclomatic_max`, `cognitive_max`,
  `maintainability_min`, `function_lines_max`, `file_lines_max`.
- Test quality: `coverage_target`, `coverage_regression_max`, `mutation_mode`,
  `mutation_target`.
- Modernize: `target_go`, `apply_fixes`, `dependency_updates`.
- Refactor safeguards: `require_passing_baseline`, `require_behavior_tests`.
- Tool policy: `complexity`, `mutation`, `modernize` under `[tools]`.
- Doctor: `profile`, `deadline_ms`, `max_findings`, `required_rules`.
- Fuzz budgets: `local_budget_seconds`, `ci_budget_seconds`, `repro_runs`.
- Architecture: `workspace_mode`, `tidy_mode`, `release_mode`, `replace_mode`.
- Agents: `enabled`, the per-role model and effort policy,
  `reviewer_max_parallel`, `authorization`, and `policy_divergence`.
- Developer: `idiom_policy` and `test_workflow` under `[developer]`.

Validate every supplied value against `references/schema.md` before preview.

## File present

1. Load and validate the current file (`references/validation.md`).
2. If the state is `INVALID`, report the exact violations and offer to correct
   only the invalid values; keep every valid value unchanged.
3. If the state is `UNSUPPORTED_VERSION`, stop: the file is read-only and is not
   rewritten. Report the unsupported version.
4. If the state is `MIGRATION_AVAILABLE`, run the migration flow below.
5. Apply requested edits in memory, preserving all unchanged content, comments,
   and key order where possible.
6. Show the exact diff.
7. Require confirmation, then write once. Report the resulting state.

## Migration flow (`MIGRATION_AVAILABLE`)

Migration is the only path that changes `schema_version`, and it runs only here.

1. Report the `schema_version` found and the version this skill supports.
2. Build the migration in memory. What it adds depends on the version found:

   | From | The migration adds |
   |---|---|
   | `1` | the version bump to `schema_version = 4`, the tables `[doctor]`, `[fuzz]`, `[architecture]`, and `[agents]` at their documented defaults, the key `quality_lab_families = []` in `[test-quality]`, and `[developer]` with `idiom_policy = "latest-compatible"` and `test_workflow = "adaptive-tdd"` |
   | `2` | the version bump to `schema_version = 4`, the table `[agents]` at its documented defaults, and `[developer]` with `idiom_policy = "latest-compatible"` and `test_workflow = "adaptive-tdd"` |
   | `3` | the version bump to `schema_version = 4` and `[developer]` with `idiom_policy = "latest-compatible"` and `test_workflow = "adaptive-tdd"` |

3. Preserve every value the user already set. Migration adds what the current
   schema introduces and changes nothing the existing file already states.
4. Show the exact diff of the version bump and the added tables and keys.
5. Require explicit confirmation. Declining leaves the file untouched and keeps
   the state `MIGRATION_AVAILABLE`; workflows continue on the older contract.
6. On confirmation, write once and report the resulting `VALID` state.

## Never-overwrite rule

Editing preserves unchanged content, migration preserves compatible values, and
both require an explicit, previewed confirmation before any write. Presence of a
file is therefore never a reason to replace it.
