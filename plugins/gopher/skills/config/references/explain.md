# `--explain` flow

Use `--explain` to resolve and report the effective configuration and how each
value was resolved. Keep this operation read-only: do not write or edit
`.gopher-plugin.toml`. Route an edit or migration to `--bootstrap`, which
previews the change and requires confirmation before writing.

## Output contract

Use the YAML output envelope in `SKILL.md` with `config_mode: explain`, the
detected `config_status`, one `effective_values` entry for every resolved
`table.key`, and its `handoff` field. Expand every entry with:

- Name: the `table.key` path.
- Value: the effective value in use.
- Source: the exact precedence label `session | file | adopted | default`,
  where `session` is the current session instruction, `file` is
  `.gopher-plugin.toml`, `adopted` is adopted project configuration or
  commands, and `default` is the Gopher default.
- Default: the Gopher default from `templates/default.gopher-plugin.toml`.
- Effect: what the value changes in the consuming workflow.
- Accepted range or enum: from `references/schema.md`.
- Consumed by: the exact owner or owners in the matching `Consumed by` row of
  `references/schema.md`, including validation and every workflow for
  `gopher.schema_version`, `gopher:complexity`, `gopher:test-quality`,
  `gopher:modernize`, `gopher:refactor`, `gopher:doctor`, `gopher:fuzz`,
  `gopher:architecture`, the shared project scope, and `gopher:developer`.
  Preserve the packaged developer, architect, and reviewer agents, plus the
  direct `gopher:review` controller and Kimi review adapter wherever the schema
  names them.

Keep every effective key, including keys at their default and keys whose table
is absent but whose default still applies. For versions `1`, `2`, and `3`
without `[developer]`, report `idiom_policy = "latest-compatible"` and
`test_workflow = "adaptive-tdd"` with source `default`; these effective values
remain unpersisted until a confirmed `--bootstrap` migration.

Set the top-level `handoff` to a real receiving `gopher:<skill>` when the
explanation identifies follow-up work; otherwise set it to `null`. A consuming
workflow is an ownership label, not an instruction to invoke that workflow.

## Presentation

- Group values by canonical table (`gopher`, `project`, `complexity`,
  `test-quality`, `modernize`, `refactor`, `tools`, `doctor`, `fuzz`,
  `architecture`, `agents`, `developer`).
- Mark any value that differs from its default, and name the source tier that
  overrode it.

## Resolution order and state handling

1. Classify the file using `references/validation.md` and report the state
   before presenting values.
2. Resolve each known value in descending precedence: `session`, `file`,
   `adopted`, then `default`. Record the selected value and source as the
   evidence that permits the per-value explanation.
3. Group and present all resolved values using the output contract above.
4. Apply the state-specific rule:
   - `ABSENT`: report defaults with source `default` and direct creation to
     `--bootstrap`.
   - `VALID`: report the complete effective configuration.
   - `MIGRATION_AVAILABLE`: report the older contract's effective values, then
     apply the migration additions below.
   - `INVALID`: report known values that still resolve, the exact validation
     violation, and the workflows blocked by that violation. Mark any value
     that cannot be resolved as `unknown`; do not infer it.
   - `UNSUPPORTED_VERSION`: report only values whose meaning this skill can
     resolve, mark future-schema values and dependent effects as `unknown`,
     and state the affected workflows and read-only recovery guidance.

Classify evidence as observed, inferred, or unknown. When an unknown blocks the
next explanation step, stop that step and name the exact file evidence or user
decision required to continue.

## `MIGRATION_AVAILABLE`

When the state is `MIGRATION_AVAILABLE`, explain the effective values of the
older contract as usual and add:

- The `schema_version` found in the file and the supported version `4`.
- For that source version, use the matching migration row in
  `references/bootstrap.md` to name the version bump, every table or key the
  current schema adds, and the default each added value would take. For schema
  4, name `[developer]` and its `idiom_policy = "latest-compatible"` and
  `test_workflow = "adaptive-tdd"` defaults. Explain that `idiom_policy`
  selects compatible idioms for `gopher:developer`, while `test_workflow`
  selects its test and implementation sequencing.
- The fact that every value the file already sets is preserved by migration.
- The fact that `--explain` writes nothing. Migration happens only inside
  `--bootstrap`, with a shown diff and explicit confirmation.
- Name the resolved tool for each `[tools]` entry, or report the limitation when
  an `auto` tool is unavailable.
- For an `[agents]` value, state that the table is a declared policy that
  narrows a packaged agent and never rebinds it.
