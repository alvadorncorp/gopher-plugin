# `.gopher-plugin.toml` schema

Every value lives inside a canonical table. Root-level loose keys and dotted
keys (for example `complexity.cyclomatic_max = 15` at the root) are not
canonical and fail validation. The thirteen canonical tables are `gopher`,
`project`, `complexity`, `test-quality`, `modernize`, `refactor`, `tools`,
`doctor`, `fuzz`, `architecture`, `agents`, `developer`, and `workflow`.

Defaults are configurable targets, not universal claims about Go code. A legacy
project below a target does not automatically fail when the measured scope
maintains or improves its baseline.

## `[gopher]`

| Key | Type | Range / enum | Default | Consumed by |
|---|---|---|---|---|
| `schema_version` | integer | `1` \| `2` \| `3` \| `4` (supported, migratable) \| `5` (current) | `5` | validation, every workflow |

`schema_version` pins the contract. A newer value than this skill supports is
`UNSUPPORTED_VERSION` and is treated read-only. An older but still supported
value is `MIGRATION_AVAILABLE`: the contract stays usable on its own effective
values, and migration to the current schema happens only inside `--bootstrap`,
with a shown diff and explicit confirmation.

## `[developer]`

| Key | Type | Range / enum | Default | Consumed by |
|---|---|---|---|---|
| `idiom_policy` | string | `latest-compatible` \| `project-aligned` \| `explicit-only` | `latest-compatible` | `gopher:developer` |
| `test_workflow` | string | `adaptive-tdd` \| `strict-tdd` \| `test-after` | `adaptive-tdd` | `gopher:developer` |

`idiom_policy` selects how newly written or directly changed code chooses
idioms. It is always capped by the project's declared Go version and never
consumes `modernize.target_go`. `latest-compatible` prefers the newest suitable
idiom within that cap, `project-aligned` gives nearby adopted conventions
priority, and `explicit-only` introduces a newer idiom only when the current
request explicitly asks for it.

`test_workflow` selects the test and implementation sequencing plus the
required evidence for `gopher:developer`. Schema versions `1`, `2`, and `3`
remain supported and migratable; until a confirmed
`gopher:config --bootstrap` migration writes them, an absent `[developer]`
table resolves `idiom_policy` and `test_workflow` to these defaults without
persisting them.

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

## `[agents]`

| Key | Type | Range / enum | Default | Consumed by |
|---|---|---|---|---|
| `enabled` | boolean | `true` \| `false` | `true` | the packaged `developer`, `architect`, and `reviewer` agents |
| `developer_model` | string | `shipped` \| `inherit` \| `haiku` \| `sonnet` \| `opus` | `shipped` | the packaged `developer` agent |
| `developer_effort` | string | `shipped` \| `inherit` \| `low` \| `medium` \| `high` \| `xhigh` | `shipped` | the packaged `developer` agent |
| `architect_model` | string | `shipped` \| `inherit` \| `haiku` \| `sonnet` \| `opus` | `shipped` | the packaged `architect` agent |
| `architect_effort` | string | `shipped` \| `inherit` \| `low` \| `medium` \| `high` \| `xhigh` | `shipped` | the packaged `architect` agent |
| `reviewer_model` | string | `shipped` \| `inherit` \| `haiku` \| `sonnet` \| `opus` | `shipped` | the packaged `reviewer` agent |
| `reviewer_effort` | string | `shipped` \| `inherit` \| `low` \| `medium` \| `high` \| `xhigh` | `shipped` | the packaged `reviewer` agent |
| `reviewer_max_parallel` | integer | `1`–`7` | `7` | the `gopher:review` controller, however the review was entered; the Kimi and omp review adapters |
| `authorization` | string | `handback` \| `request-approval` \| `inherit-session` | `handback` | the packaged `developer` and `architect` agents; the Kimi and omp refactor adapters |
| `policy_divergence` | string | `report` \| `block` | `report` | all three packaged agents |

Each packaged agent ships with a fixed binding for its model, its reasoning
effort, and its tools. The host reads that binding when it loads the agent, so no
project file can rebind it. This table is the project's declared policy over that
binding. It may narrow an agent and it can never widen it beyond that binding,
and a declared value is never presented as an applied one.

`shipped` accepts the packaged binding, so a default file states nothing to
compare and can never diverge. `inherit` states that the project prefers the
session binding over the packaged pin; when the host honors the pin instead, the
agent reports the difference rather than claiming the declared value was applied.

`authorization` selects how an agent resolves a gate it cannot put to the user,
and it moves along one axis only. `handback`, the default, is the most
restrictive: return the evidence and the named owner. `request-approval` returns
an explicit approval request instead. `inherit-session` is the least restrictive:
the agent proceeds on the delegating session's authorization, up to but never
past the capability the packaged binding already grants. Raising this key
therefore relaxes a default the package chose, which is the one direction this
table can move against the shipped posture; it still cannot grant a capability
the binding withheld. `gopher:doctor` reports any non-default value through the
`agents.policy-declared` rule so the relaxation is never silent. The packaged
`reviewer` has no gated action, so this key does not reach it.

`reviewer_max_parallel` bounds the review fan-out window; a window narrowed by
this key is reported as `parallel_window: bounded-by-policy` and is never
reported as `degradation: sequential_no_parallel_support`, which states only that
the host could not run the lenses together. Lower it when seven concurrent
reviewers would exhaust a rate limit or a context budget; the default of `7`
equals the lens count and so never binds. It reaches a review dispatched through
the packaged `reviewer` agent or the Kimi and omp adapters. A review invoked
directly as `gopher:review` reads it through `references/controller.md`.

Every packaged agent reports one `policy_status` alongside its skill's own
output, and so does `gopher:review` when the skill is invoked directly. The five
values are an ordered partition: evaluate them top to bottom and report the first
that holds.

| Value | Holds when |
|---|---|
| `BLOCKED_BY_POLICY` | `enabled` is `false`, or `policy_divergence` is `block` and the value that would otherwise hold is `UNVERIFIABLE` or `DIVERGED`. The agent does no work and hands back |
| `NOT_CONFIGURED` | The parsed contract declares no `[agents]` table. The packaged binding is authoritative and nothing can diverge |
| `UNVERIFIABLE` | A role model or effort declares anything other than `shipped` and the host exposes no way to observe the active binding. No host exposes one today, so this is the usual result of declaring a model or an effort |
| `DIVERGED` | An observable binding contradicts a declared one, listed field by field, and the run continued because `policy_divergence` is `report` |
| `ALIGNED` | Nothing above holds. This includes every declaration left at `shipped`, because `shipped` accepts the packaged binding and states nothing to compare |

A version-`1` or version-`2` file usually reports `NOT_CONFIGURED` because it
predates this table, but the classification follows the parsed document and not
the schema version: rules 3 and 4 of `references/validation.md` are
version-independent, so an older file that does declare `[agents]` is read like
any other and its `enabled` and `policy_divergence` values take effect.

## `[workflow]`

| Key | Type | Range / enum | Default | Consumed by |
|---|---|---|---|---|
| `planning_preflight` | list of string | advisory skill hints such as `architecture:triage`, `refactor:plan` | `["architecture:triage"]` | session agents during planning prompts |
| `planning_require_structure_decision` | boolean | `true` \| `false` | `false` | session agents before large multi-package implementation |
| `implementation_owner` | string | `developer` | `developer` | session routing for local implementation |
| `post_implementation_review` | string | `off` \| `recommend` \| `auto` | `off` | whether to suggest or auto-select `gopher:review` after green local implementation |
| `post_implementation_lenses` | string | `heuristic` \| `full` \| comma-separated lens list | `heuristic` | lens selection when post review is `auto` or `recommend` |
| `max_auto_review_files` | integer | `> 0` | `20` | upper bound on changed Go files for `auto` review without confirmation |

These keys are **session policy hints**. They do not install hooks, do not mutate
the tree, and cannot widen packaged agent bindings. `post_implementation_review
= auto` authorizes `gopher:review --mode auto` behavior when the host session
chooses to honor the policy; it never grants edit rights to review.

Schema versions `1`, `2`, `3`, and `4` remain supported and migratable; until a
confirmed `gopher:config --bootstrap` migration writes them, an absent
`[workflow]` table resolves these keys to the defaults above without
persisting them.

## Effective-value precedence

The authoritative four-tier precedence and the rule that it never relaxes an
authorization or safety boundary live in the
`## Configuration states and precedence` section of `SKILL.md`. Resolve every
effective value there, then apply the per-table ranges, enums, and defaults
above.
