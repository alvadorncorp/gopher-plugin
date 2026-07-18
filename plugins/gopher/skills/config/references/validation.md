# Validation rules and states

Validation classifies `.gopher-plugin.toml` into one of four states and decides
what work the effective configuration may drive.

## Rules

1. Schema version: `[gopher].schema_version` must be present and an integer.
   A value newer than this skill supports is `UNSUPPORTED_VERSION`.
2. Canonical tables: only `gopher`, `project`, `complexity`, `test-quality`,
   `modernize`, `refactor`, and `tools` are allowed. Root-level loose keys and
   dotted keys are not canonical.
3. Known keys: every key must be defined for its table in
   `references/schema.md`. An unknown key in the current schema is invalid.
4. Value types: each value must match its documented type (integer, boolean,
   string, or list of string).
5. Ranges: numeric values must fall inside their documented range (for example
   `coverage_target` within `0`–`100`, `cyclomatic_max` greater than `0`).
6. Enums: string values constrained to an enum must match a documented member
   (for example `mode` is `advisory` or `required`).

## States

- `ABSENT`: no file exists. Analysis is allowed; `--bootstrap` can create the
  file.
- `VALID`: every rule passes. The effective configuration can drive workflows.
- `INVALID`: at least one rule fails. Explanation and diagnosis are allowed, but
  non-config mutations are blocked until the file is corrected.
- `UNSUPPORTED_VERSION`: the schema version is newer than supported. Read-only
  guidance is allowed; automatic rewriting is forbidden.

## Recovery

- An older but supported `schema_version` is migrated only inside `--bootstrap`,
  with a preview and explicit confirmation. Validation itself never rewrites.
- An unavailable optional tool does not make the configuration invalid; it is an
  explicit limitation unless its configured mode is `required`, which blocks
  only the dependent dimension.
