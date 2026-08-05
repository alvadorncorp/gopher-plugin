# Security Finding and Report Format

## Finding

```yaml
id:
status: confirmed | hypothesis
asset:
attacker:
preconditions:
source_to_sink_path:
affected_code:
reachability:
existing_controls:
failure_scenario:
impact:
severity: critical | important | minor
confidence: high | medium | low
evidence:
safe_reproduction:
remediation:
validation:
residual_risk:
owner: gopher:<skill>
```

## Report

```markdown
## Scope and authorization
## Threat model and data flow
## Confirmed findings
## Open hypotheses and missing evidence
## Covered areas with no findings
## Remediation and validation
## Residual risk and handoffs
```

Critical and important describe impact, not confidence. A hypothesis remains
outside the confirmed findings section until its path or missing control is demonstrated.
