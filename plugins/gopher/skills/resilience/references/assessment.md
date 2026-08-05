# Assessment Mode

`assessment` answers "how reliable is this system?" with a bounded, read-only
synthesis of evidence other specialists have already produced. It is the mode
that turns scattered findings into one honest reliability statement.

## The contract

- Read-only. The mode reads code, configuration, tests, and existing reports.
- Bounded. The scope is the boundary named at intake, and it stays there.
- Synthesizing. It arranges existing evidence; it does not manufacture new
  evidence.
- Attributed. Every claim names the specialist and artifact that produced its
  evidence.
- Honest. A gap in evidence is reported as a gap.

The mode implements nothing, configures nothing, deploys nothing, and runs no
production probe. Every change it identifies is handed to the owning skill with
the evidence attached. Widening the scope requires an explicit request from the
user.

## Evidence it consumes

| Evidence | Produced by | What it supports |
|---|---|---|
| Goroutine lifetime, cancellation, race, and leak findings | `gopher:concurrency` | Whether cancellation and shutdown paths actually terminate work |
| Attributed incident causes and evidence bundles | `gopher:diagnose` | Which failure-model rows have occurred in reality |
| Benchmarks, profiles, and latency measurements | `gopher:performance` | Whether the budget and the concurrency limit match measured service time |
| Signal inventory and alert definitions | `gopher:observability` | Whether each failure-model row is detectable |
| Threat model, authorization, and secret-handling findings | `gopher:security` | Whether a degraded tier preserves the security posture |
| Coverage and test effectiveness | `gopher:test-quality` | Whether a control is exercised by the suite |
| Package boundaries and dependency direction | `gopher:architecture` | Whether a bulkhead boundary exists in the code |
| Diff-level findings and verdicts | `gopher:review` | Whether a recent change altered a control |

## Citing evidence

Each line in the synthesis carries four parts:

- **Claim** — the reliability statement, in one sentence.
- **Evidence** — the artifact: a test name, a benchmark result, an incident
  report, an alert definition, a code path with its file and symbol.
- **Producer** — the skill id that produced it.
- **Strength** — `proven` (an artifact demonstrates the behavior), `observed`
  (a single run or a real incident showed it), or `asserted` (the code implies
  it and nothing exercises it).

An `asserted` control is a proposed control. It reaches the `proposed_controls`
list, never the `proven_controls` list, however convincing the code reads.

## Classifying the output

| Bucket | Admission rule |
|---|---|
| `proven_controls` | An artifact demonstrates the control working against the failure it addresses |
| `proposed_controls` | The control exists in code or in a plan, and nothing exercises it yet |
| `missing_evidence` | A failure-model row whose control, detection, or recovery cannot be assessed from the available evidence, with the named probe that would close it |
| `residual_risk` | What survives the proven controls, including absent objectives and untested paths |

## The gap rule

A gap in evidence is reported as a gap rather than filled by assumption. Three
concrete forms:

- No declared objective exists for a failure mode: report the absence, carry it
  as residual risk, return `COMPLETE_WITH_RISK`.
- A control exists but nothing exercises it: it is a proposed control, and the
  missing exercise is named as the probe that would promote it.
- The evidence needed belongs to another specialist: name the skill and the
  specific question, rather than estimating the answer.

Assessment with no consumable evidence at all returns `BLOCKED` with the
ordered list of evidence to gather first.

## Terminal state selection

| Condition | Status |
|---|---|
| Every failure-model row has a proven control, a detection signal, a recovery path, and a declared objective | `COMPLETE` |
| Controls are specified but named residual risk remains, or a declared objective is absent | `COMPLETE_WITH_RISK` |
| The boundary is unknown, or no consumable evidence exists | `BLOCKED` |

`COMPLETE_WITH_RISK` is the ordinary outcome for a real system. Reaching
`COMPLETE` by leaving a known gap unnamed is the one failure mode of this mode
itself.

Last verified: 2026-08-05.
