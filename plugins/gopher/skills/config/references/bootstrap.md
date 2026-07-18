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

Validate every supplied value against `references/schema.md` before preview.

## File present

1. Load and validate the current file (`references/validation.md`).
2. If the state is `INVALID`, report the exact violations and offer to correct
   only the invalid values; keep every valid value unchanged.
3. If the state is `UNSUPPORTED_VERSION`, stop: the file is read-only and is not
   rewritten. Report the unsupported version.
4. For an older but supported `schema_version`, offer migration to the current
   version, preserving every compatible value.
5. Apply requested edits in memory, preserving all unchanged content, comments,
   and key order where possible.
6. Show the exact diff.
7. Require confirmation, then write once. Report the resulting state.

## Never-overwrite rule

Presence of a file is never a reason to replace it. Editing preserves unchanged
content; migration preserves compatible values; both require an explicit,
previewed confirmation before any write.
