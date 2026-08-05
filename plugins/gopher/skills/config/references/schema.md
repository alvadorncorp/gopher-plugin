# `.gopher-plugin.toml` schema

Every value lives inside a canonical table. Root-level loose keys and dotted
keys (for example `complexity.cyclomatic_max = 15` at the root) are not
canonical and fail validation. The ten canonical tables are `gopher`,
`project`, `complexity`, `test-quality`, `modernize`, `refactor`, `tools`,
`doctor`, `fuzz`, and `architecture`.

Defaults are configurable targets, not universal claims about Go code. A legacy
project below a target does not automatically fail when the measured scope
maintains or improves its baseline.

## `[gopher]`

| Key | Type | Range / enum | Default | Consumed by |
|---|---|---|---|---|
| `schema_version` | integer | `1` (supported, migratable) \| `2` (current) | `2` | validation, every workflow |

`schema_version` pins the contract. A newer value than this skill supports is
`UNSUPPORTED_VERSION` and is treated read-only. An older but still supported
value is `MIGRATION_AVAILABLE`: the contract stays usable on its own effective
values, and migration to the current schema happens only inside `--bootstrap`,
with a shown diff and explicit confirmation.

## `[project]`

| Key | Type | Range / enum | Default | Consumed by |
|---|---|---|---|---|
| `module_roots` | list of string | module directories, relative to root | `[]` (auto-detect) | every workflow's scope |
| `package_patterns` | list of string | `go` package patterns | `["./..."]` | every workflow's scope |

## `[complexity]`

| Key | Type | Range / enum | Default | Consumed by |
|---|---|---|---|---|
| `mode` | string | `advisory` \| `required` | `advisory` | `gopher:complexity` |
| `cyclomatic_max` | integer | `> 0` | `15` | `gopher:complexity` |
| `cognitive_max` | integer | `> 0` | `20` | `gopher:complexity` |
| `maintainability_min` | integer | `0`–`100` | `20` | `gopher:complexity` |
| `function_lines_max` | integer | `> 0` | `60` | `gopher:complexity` |
| `file_lines_max` | integer | `> 0` | `500` | `gopher:complexity` |

## `[test-quality]`

| Key | Type | Range / enum | Default | Consumed by |
|---|---|---|---|---|
| `coverage_target` | integer | `0`–`100` | `80` | `gopher:test-quality` |
| `coverage_regression_max` | integer | `>= 0` (percentage points) | `0` | `gopher:test-quality` |
| `mutation_mode` | string | `advisory` \| `required` | `advisory` | `gopher:test-quality` |
| `mutation_target` | integer | `0`–`100` | `75` | `gopher:test-quality` |
| `quality_lab_families` | list of string | any subset of the twelve canonical families | `[]` | `gopher:test-quality` |

`quality_lab_families` is the eligible set for the `quality-lab` mode of
`gopher:test-quality`, never an instruction to run every technique it names. An
empty list means every canonical family is eligible. The twelve canonical
families are `deterministic-concurrency`, `integration`, `contract`, `hermetic`,
`flake`, `race-leak`, `golden`, `property`, `metamorphic`, `differential`,
`model-state`, and `mutation`.

## `[modernize]`

| Key | Type | Range / enum | Default | Consumed by |
|---|---|---|---|---|
| `target_go` | string | `declared` \| an explicit Go version | `declared` | `gopher:modernize` |
| `apply_fixes` | boolean | `true` \| `false` | `false` | `gopher:modernize` |
| `dependency_updates` | string | `none` \| `patch` \| `minor` | `none` | `gopher:modernize` |

`target_go = "declared"` keeps the project's declared Go version and prevents an
implicit upgrade; modernization may still recommend or apply changes compatible
with that version. `apply_fixes = false` makes modernization preview-only until
a run explicitly enables application. `dependency_updates` never defaults to an
unattended `latest`.

## `[refactor]`

| Key | Type | Range / enum | Default | Consumed by |
|---|---|---|---|---|
| `require_passing_baseline` | boolean | `true` \| `false` | `true` | `gopher:refactor` |
| `require_behavior_tests` | boolean | `true` \| `false` | `true` | `gopher:refactor` |

## `[tools]`

| Key | Type | Range / enum | Default | Consumed by |
|---|---|---|---|---|
| `complexity` | string | `auto` \| `off` \| an explicit command | `auto` | `gopher:complexity` |
| `mutation` | string | `auto` \| `off` \| an explicit command | `auto` | `gopher:test-quality` |
| `modernize` | string | `auto` \| `off` \| an explicit command | `auto` | `gopher:modernize` |

`auto` means discover and use a compatible project-adopted or already-available
tool. It never means install one; an unavailable optional tool becomes an
explicit limitation unless its mode is `required`.

## `[doctor]`

| Key | Type | Range / enum | Default | Consumed by |
|---|---|---|---|---|
| `profile` | string | `quick` \| `standard` \| `strict` | `standard` | `gopher:doctor` |
| `deadline_ms` | integer | `> 0` | `2000` | `gopher:doctor` |
| `max_findings` | integer | `> 0` | `20` | `gopher:doctor` |
| `required_rules` | list of string | doctor rule ids | `[]` | `gopher:doctor` |
| `overrides` | array of tables | see `[[doctor.overrides]]` | `[]` (absent from the default template) | `gopher:doctor` |

`profile` selects how much readiness evidence the check collects; `deadline_ms`
bounds a single readiness run so a hook stays fast; `max_findings` caps the
reported findings without changing the terminal state; `required_rules` names
the doctor rule ids that must pass before the run can report `READY`.

Config validates `required_rules` and `[[doctor.overrides]].rule` as strings
only. The rule-id catalog belongs to `gopher:doctor` (`references/rules.md`); an
id this skill cannot resolve keeps the file `VALID` here and is reported by
`gopher:doctor` as an unknown rule.

### `[[doctor.overrides]]`

An array of tables. Each entry carries `rule` (string, a doctor rule id), `until`
(string, an ISO-8601 date), and `reason` (string). It is not part of the default
template; add entries only deliberately.

| Key | Type | Range / enum | Default | Consumed by |
|---|---|---|---|---|
| `rule` | string | a doctor rule id | none (required) | `gopher:doctor` |
| `until` | string | an ISO-8601 date | none (required) | `gopher:doctor` |
| `reason` | string | free text | none (required) | `gopher:doctor` |

An override may only relax a `deny` to a `warn`. It can never relax an
authorization boundary, and it never removes the original finding from the
evidence. An expired or malformed override is ignored and reported.

## `[fuzz]`

| Key | Type | Range / enum | Default | Consumed by |
|---|---|---|---|---|
| `local_budget_seconds` | integer | `> 0` | `60` | `gopher:fuzz` |
| `ci_budget_seconds` | integer | `> 0` | `300` | `gopher:fuzz` |
| `repro_runs` | integer | `> 0` | `3` | `gopher:fuzz` |

`local_budget_seconds` bounds an interactive fuzzing session, `ci_budget_seconds`
bounds the longer unattended run, and `repro_runs` is how many times a candidate
failure must reproduce before it is reported as a stable finding.

## `[architecture]`

| Key | Type | Range / enum | Default | Consumed by |
|---|---|---|---|---|
| `workspace_mode` | string | `off` \| `advisory` \| `required` | `advisory` | `gopher:architecture` |
| `tidy_mode` | string | `off` \| `advisory` \| `required` | `advisory` | `gopher:architecture` |
| `release_mode` | string | `independent` \| `grouped` | `independent` | `gopher:architecture` |
| `replace_mode` | string | `forbid` \| `local-only` \| `allow` | `local-only` | `gopher:architecture` |

These four keys restrict the `module-lifecycle` and `migration` modes of
`gopher:architecture`. `workspace_mode` and `tidy_mode` decide whether a
workspace layout and a tidy module graph are ignored, recommended, or enforced.
`release_mode` states whether modules are versioned one by one or released as a
group. `replace_mode` bounds `replace` directives: `forbid` allows none,
`local-only` allows local development paths, and `allow` permits any replacement
the project declares.

## Effective-value precedence

The authoritative four-tier precedence and the rule that it never relaxes an
authorization or safety boundary live in the `## Configuration states` section
of `SKILL.md`. Resolve every effective value there, then apply the per-table
ranges, enums, and defaults above.
