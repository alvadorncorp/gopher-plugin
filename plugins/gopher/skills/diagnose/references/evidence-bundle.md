# Diagnosis Evidence Bundle

Return exactly these fields in this order:

```yaml
status: ATTRIBUTED | UNKNOWN
symptom:
impact:
expected:
observed:
project_context:
reproduction:
hypotheses:
  - hypothesis:
    evidence_for:
    evidence_against:
    result:
probes:
  - command_or_action:
    expected_discrimination:
    observed_result:
evidence:
primary_owner: gopher:<skill> | null
confidence: high | medium | low
missing_evidence:
recommended_next_step:
```

For `ATTRIBUTED`, `primary_owner` contains exactly one canonical owner and the
next step is a handoff. For `UNKNOWN`, `primary_owner` is `null`, confidence
reflects the limitation, and the next step is one safe discriminating probe.
