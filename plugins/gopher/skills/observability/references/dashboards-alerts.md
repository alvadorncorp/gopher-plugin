# Dashboards and Alerts

Every panel and every alert traces to a declared decision or objective. A panel
that answers no question is cost and visual noise; an alert that triggers no
action is fatigue.

## Panel review

| Field | Requirement |
|---|---|
| Question | The operational question the panel answers, written out |
| Decision | What the viewer does differently depending on the value |
| Signal | The contracted signal from `references/signal-contracts.md` |
| Reading | What normal looks like, so an abnormal value is recognizable |
| Owner | The team that maintains it when the signal changes |

A dashboard is ordered from the user-visible symptom to the internal cause: the
first screen answers "is the service healthy for its users", and deeper panels
answer "which component explains the current answer". Reversing that order makes
an operator read a hundred internal panels before learning whether anything is
wrong.

Retire a panel whose question was answered permanently, or whose signal has no
consumer. Retirement is part of the signal lifecycle, not a cleanup task.

## Alert quality

| Criterion | Passing form | Failing form |
|---|---|---|
| Symptom over cause | Fires on user-visible degradation: elevated errors, latency past the threshold, work not completing | Fires on an internal proxy such as CPU, memory, or queue depth that often moves without user impact |
| Actionability | A human can take a specific action now | The recipient reads it and waits |
| Ownership | One named team receives it | Broadcast to a channel nobody owns |
| Runbook | Linked, and it names the first three checks | Absent, or a stale page |
| Threshold provenance | Derived from a declared objective | Chosen because the graph looked wrong once |
| Window | Long enough to survive a scrape gap, short enough to matter | Instantaneous, so a single sample pages |
| Severity | Paging severity reserved for action needed now; the rest is a ticket | Everything pages |

Cause-based alerts remain useful as diagnostic context attached to a
symptom-based page. They earn a page of their own only when the cause is both
irreversible and invisible in any symptom, such as a certificate that expires in
a week or storage that will fill before the next working day.

## Alert design steps

1. Name the objective or decision the alert defends, and get it from
   `gopher:resilience` when it is a service level objective.
2. Pick the signal that expresses the symptom, and confirm its contract supports
   the required window and retention.
3. Choose the threshold and evaluation window from the objective, then state the
   expected trigger rate under normal operation.
4. Write the runbook first. An alert whose runbook cannot be written is not yet
   actionable.
5. Name the receiving owner and the severity.
6. Test the alert against recorded data covering a real incident and a normal
   period, and record the false-positive count.

## Coverage and noise review

| Check | Signal of a problem |
|---|---|
| Every objective has an alert | An objective with no alert is a hope |
| Every alert has an objective or decision | An orphan alert is untuned by construction |
| Alerts that fired without action in the last quarter | Threshold, window, or severity needs revision |
| Incidents found by a user before an alert | A coverage gap; add the signal, then the alert |
| Alerts firing together every time | Merge them, or make one a diagnostic panel |
| Alerts querying a signal past its retention | A silent evaluation failure |

## Handoff

The objective itself — its target, measurement window, error budget, and the
policy applied when the budget is spent — belongs to `gopher:resilience`. This
skill supplies the signal that measures the objective, its contract, its cost,
and the alerting expression built on it. Attribution of a firing alert to a
change or component belongs to `gopher:diagnose`.

Last verified: 2026-08-05.
