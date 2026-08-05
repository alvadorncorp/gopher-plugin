# Readiness Evidence Bundle

Every mode ends by emitting exactly these fields, in this order.

```yaml
selected_skill: gopher:doctor
primary_owner: gopher:doctor
mode: check | hook | explain
status: READY | WARN | BLOCKED | LIMITED
config_status: ABSENT | VALID | MIGRATION_AVAILABLE | INVALID | UNSUPPORTED_VERSION
rules_considered:
findings:
checks_skipped:
deadline:
override_summary:
authorization_gate: none | approval-required | blocked
handoffs:
```

## Fields

| Field | Content |
|---|---|
| `selected_skill` | Always `gopher:doctor` |
| `primary_owner` | Always `gopher:doctor`; the owner of the readiness verdict, not of any repair |
| `mode` | The mode that produced the bundle |
| `status` | The aggregated terminal state, with `LIMITED` reported whenever `checks_skipped` is non-empty |
| `config_status` | The state of `.gopher-plugin.toml` as resolved by `gopher:config` |
| `rules_considered` | The rule ids selected by profile and `required_rules`, in execution order |
| `findings` | One entry per rule that produced a finding |
| `checks_skipped` | One entry per selected rule that did not run to completion |
| `deadline` | The configured `deadline_ms`, the elapsed time, and whether the deadline was reached |
| `override_summary` | One entry per `[[doctor.overrides]]` entry that was applied, expired, or ignored |
| `authorization_gate` | `none` when every check ran on permitted evidence; `approval-required` when a check awaits authorization; `blocked` when the run stopped at an authorization boundary |
| `handoffs` | One entry per distinct receiving skill, with the rule ids it receives |

## Finding entry

```yaml
- rule: module.go-sum-consistent
  owner: gopher:architecture
  disposition: deny | warn
  invariant:
  evidence:
  remediation:
  override: null | { until: , reason: }
```

Three rules hold for every finding:

- **One owner.** `owner` is exactly one real skill id, taken from the `Owner`
  column of `references/rules.md`. A finding that seems to belong to two areas
  is split into two findings or assigned to the area whose invariant it
  violates.
- **Bounded, non-secret evidence.** `evidence` carries the smallest observation
  that supports the finding: the path, the declared value, the directive line,
  the command and its exit status. Values are truncated to stay bounded, and
  tokens, keys, and credentials are redacted before serialization.
- **Actionable remediation.** `remediation` states the concrete change and where
  it happens, so the receiving owner starts work without re-deriving the
  finding.

`disposition` is `deny` only for a block-eligible rule under the full blocking
policy; the presence of an applied override is recorded in `override` while
`disposition` reads `warn`.

## Skipped entry

```yaml
- rule: toolchain.resolvable
  reason: deadline | missing-capability | authorization-required | internal-error
  detail:
```

A skipped check is serialized in `checks_skipped` and nowhere else. It is never
folded into `findings` as a passed rule, and it is never dropped from the
bundle: an unmeasured invariant reads as unmeasured, which is what makes the run
`LIMITED` rather than `READY`.

## Handoff entry

```yaml
- owner: gopher:codegen
  rules: [generated.output-current]
  summary:
```

Handoffs collect the routing already recorded per finding. The bundle names the
owner and stops there; `gopher:doctor` performs no repair and invokes no other
skill.

## `explain` mode

`explain` emits the same envelope with `mode: explain`, `status: READY`, an
empty `checks_skipped`, and a single entry in `rules_considered`. The `findings`
list carries one descriptive entry for the requested rule: its invariant,
evidence shape, owner, remediation, block eligibility, and override rules. No
project scan happens, so `deadline` records that no run was timed.
