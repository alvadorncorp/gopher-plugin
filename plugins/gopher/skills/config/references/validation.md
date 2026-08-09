# Validation rules and states

Validation classifies `.gopher-plugin.toml` into one of five states and decides
what work the effective configuration may drive.

## Rules

1. Parse: the file must be valid TOML. Every rule below presupposes a parsed
   document, so a parse failure is `INVALID` on its own. Report the parse-error
   location and offer the correction under `--bootstrap`.
2. Schema version: `[gopher].schema_version` must be present and an integer.
   A value newer than this skill supports is `UNSUPPORTED_VERSION`. A value
   older than the current schema but still supported is `MIGRATION_AVAILABLE`
   once every other rule passes; it is not a failure. `schema_version` is
   classified by this rule alone: rules 6 and 7 below do not apply to it, so
   `4` is `VALID`, `1`, `2`, and `3` are `MIGRATION_AVAILABLE`, and any higher
   value is `UNSUPPORTED_VERSION`. A missing `[developer]` table — and therefore
   missing `idiom_policy` and `test_workflow` values — never invalidates versions
   `1`, `2`, or `3`; those supported older contracts resolve both values to their
   documented defaults until a confirmed migration writes them.
3. Canonical tables: only `gopher`, `project`, `complexity`, `test-quality`,
   `modernize`, `refactor`, `tools`, `doctor`, `fuzz`, `architecture`, and
   `agents`, and `developer` are allowed. Root-level loose keys and dotted keys are not canonical.
   The one canonical nested array of tables is `[[doctor.overrides]]`.
4. Known keys: every key must be defined for its table in
   `references/schema.md`. An unknown key in the current schema is invalid. A
   table or a key the current schema adds is simply absent from an older file,
   and that absence is never an unknown key. This covers a key added to a table
   that already existed, such as `test-quality.quality_lab_families`, as much as
   it covers a whole added table such as `[agents]` or `[developer]`. For the
   latter, the current keys are `idiom_policy` and `test_workflow`.
5. Value types: each value must match its documented type (integer, boolean,
   string, or list of string).
6. Ranges: numeric values must fall inside their documented range (for example
   `coverage_target` within `0`–`100`, `cyclomatic_max` greater than `0`).
7. Enums: string values constrained to an enum must match a documented member
   (for example `mode` is `advisory` or `required`).

## States

- `ABSENT`: no file exists. Analysis is allowed; `--bootstrap` can create the
  file.
- `VALID`: every rule passes at the current schema version. The effective
  configuration can drive workflows.
- `MIGRATION_AVAILABLE`: the file parses and every rule passes, but its
  `schema_version` is older than the version this skill supports. This is not an
  invalid file. Analysis and explanation proceed on the older contract's
  effective values.
- `INVALID`: at least one rule fails, including a parse failure under rule 1.
  Explanation and diagnosis are allowed, but non-config mutations are blocked
  until the file is corrected.
- `UNSUPPORTED_VERSION`: the schema version is newer than supported. Read-only
  guidance is allowed; automatic rewriting is forbidden.

`UNSUPPORTED_VERSION` and `MIGRATION_AVAILABLE` stay distinct and never collapse
into one state. `UNSUPPORTED_VERSION` is a future schema this skill cannot
interpret, so it is read-only and never rewritten. `MIGRATION_AVAILABLE` is a
past supported schema this skill fully understands, so it can be migrated under
`--bootstrap`.

## Recovery

- A `MIGRATION_AVAILABLE` file is migrated only inside `--bootstrap`, with the
  exact diff previewed and explicit confirmation required. Validation itself
  never rewrites, and nothing is ever migrated automatically.
- An unavailable optional tool does not make the configuration invalid; it is an
  explicit limitation unless its configured mode is `required`, which blocks
  only the dependent dimension.
