---
name: doctor
description: Checks whether a Go project, its configuration, toolchain, module state, generated output, and a pending action satisfy known readiness invariants, then reports READY, WARN, BLOCKED, or LIMITED with one owner per finding. Use for a health check, a doctor check, a pre-flight or readiness check, or a question about whether a Go project is set up correctly and its toolchain is in order, all against rules that are already known. Route an unexplained symptom to `gopher:diagnose`, and route every repair to the canonical owner of its area such as `gopher:codegen`, `gopher:config`, `gopher:architecture`, or `gopher:modernize`.
---

# Go Readiness Doctor

## Context and ownership

Own proactive Go readiness: whether a project, its configuration, toolchain,
module state, generated output, and a pending action satisfy invariants this
skill already knows. Primary owner: `gopher:doctor`. Check, report, and stop.

Doctor answers one question: does this project satisfy an invariant I already
know? `gopher:diagnose` answers a different one: why is this behaving in a way
nobody has explained yet? Hypothesis formation, reproduction, and causal
attribution of an unexplained symptom belong to `gopher:diagnose`.

Every repair belongs to the canonical specialist of its area: a generated
artifact that no longer matches its generator to `gopher:codegen`, which also
classifies it, an invalid project contract to `gopher:config`, a
module or workspace inconsistency to `gopher:architecture`, a toolchain or
declared-version issue to `gopher:modernize`, a missing or unrecorded test
baseline to `gopher:test-quality`, and a local code fix to `gopher:developer`.
Doctor names the owner and the remediation.

Read table `[doctor]` from `gopher:config`, schema v3: `profile` (`quick`,
`standard`, `strict`; default `standard`) selects the rule set, `deadline_ms`
(default `2000`) bounds a single run, `max_findings` (default `20`) caps
reported findings without changing the terminal state, `required_rules` (default
`[]`) names rule ids that must pass before a run reports `READY`, and each
`[[doctor.overrides]]` entry carries `rule`, `until`, and `reason`.

## Modes

| Mode | Trigger | Evidence budget | Stop condition |
|---|---|---|---|
| `check` | a manual readiness request before an action | read-only project evidence at profile `standard` or `strict`, bounded by `deadline_ms` and `max_findings` | a terminal state with the full bundle |
| `hook` | an automatic host event | the `quick` profile only: metadata and bounded parse evidence, inside a budget smaller than the host timeout | the deadline or `max_findings`, whichever comes first |
| `explain` | a question about exactly one rule id | the rule catalog only, read-only, no project scan | the single-rule report |

Terminal states are `READY`, `WARN`, `BLOCKED`, and `LIMITED`. `status` carries
one value. `BLOCKED` outranks `LIMITED`, which outranks `WARN`, which outranks
`READY`, so `LIMITED` never masks a blocking verdict for a caller that branches
on this field alone. Incompleteness stays visible in `checks_skipped` at every
status, and `LIMITED` is the reported status when checks were skipped or work
stayed incomplete and nothing blocked.

`hook` is fail-open: an internal error, an exceeded deadline, or a missing
capability yields a non-blocking result with the reason recorded, so the caller
proceeds. This delivery ships that contract, not a hook runtime or host wiring
(`references/hook-mode.md`). `explain` resolves one rule and reports its
applicability, evidence shape, owner, remediation, block eligibility, and
override rules (`references/rules.md`).

## Workflow

1. Normalize the invocation context and the capabilities, then resolve the safe
   project root through the same `DETECT_ROOT` step `gopher:config` owns. That
   one resolved directory is the read boundary of the whole run: every declared
   action scope, every `project.module_roots` entry, and every evidence path
   counts as safe while it resolves inside that directory, whatever the current
   working directory or the configuration file's own location happens to be.
2. Read bounded configuration and project metadata.
3. Select rules by profile, event, tool class, and remediation exemption
   (`references/profiles.md`).
4. Execute rules in stable rule-id order until the deadline or `max_findings`
   (`references/rules.md`).
5. Apply only valid, unexpired `deny -> warn` overrides, preserving the original
   finding in the evidence (`references/overrides.md`).
6. Aggregate `BLOCKED > WARN > READY`, and report `LIMITED` when any check was
   skipped or any work stayed incomplete.
7. Emit the bundle from `references/evidence-bundle.md`: rules considered,
   findings, skipped checks, deadline, configuration, overrides, and handoffs.

## Blocking policy

A finding blocks when all five conditions hold:

1. Its rule is block-eligible in `references/rules.md`.
2. The active profile includes that rule.
3. The check ran to completion and its evidence is complete.
4. The remediation is actionable inside the project's own contract.
5. No valid unexpired override downgrades it.

Every other finding warns. A check that ran without completing its evidence
warns, names the missing observation in its evidence, and contributes `LIMITED`.
Each finding carries a single owner, bounded evidence, and actionable
remediation. A check that did not run is reported as skipped, contributes
`LIMITED`, and stays out of the passed set.

## Output format

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

## Authorization boundaries

- Use evidence that leaves the working tree unchanged: project files,
  configuration, and metadata already present, plus the subprocess probes the
  active profile declares. A declared probe runs against the module cache and
  toolchain already installed, may populate a read cache outside the project
  root, writes nothing inside it, and reproduces generator output only in a
  temporary location outside the project root.
- Keep every repair with the named owner; doctor reports remediation and handoff.
- An override downgrades a `deny` to a `warn` only. It never relaxes an
  authorization boundary, and the original finding stays in the evidence.
- Automatic mode stays inside the project root, mutates nothing, and invokes no
  other skill.
- A probe that would fetch from the network, install a tool, read a credential,
  or reach production requires explicit authorization. Without it the dependent
  check is skipped with reason `authorization-required` and reported in
  `checks_skipped`.

## Quality checklist

- Name exactly one real skill id as the owner of each finding.
- Keep evidence bounded, non-secret, and sufficient to act on.
- Report a skipped check in `checks_skipped` with its reason, never as passed.
- Block only when all five conditions hold; every other finding warns.
- Preserve the original finding when an override downgrades it.
- Route an unexplained symptom to `gopher:diagnose` rather than inferring a cause.

## References

- `references/rules.md` — the eleven-rule catalog with owners, costs, evidence, and handoffs.
- `references/profiles.md` — what `quick`, `standard`, and `strict` include, and how `required_rules` composes.
- `references/hook-mode.md` — the automatic-mode contract, fail-open semantics, and delivery scope.
- `references/overrides.md` — the `[[doctor.overrides]]` shape, `deny -> warn` limits, and expiry handling.
- `references/evidence-bundle.md` — the exact terminal bundle schema, field by field.
