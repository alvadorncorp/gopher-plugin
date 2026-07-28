---
name: diagnose
description: Attributes vague Go symptoms through reproducible evidence and falsifiable hypotheses, then hands off to one canonical owner or returns UNKNOWN. Use when the cause is unclear. Stop after attribution; solution selection and code edits belong to the receiving owner.
---

# Diagnose Go Symptoms

## Context and ownership

Own evidence-driven attribution of vague Go symptoms. Primary owner:
`gopher:diagnose`. Produce an evidence bundle and stop; the receiving owner
selects and implements a solution.

## State machine

```text
INTAKE
  -> CONTEXT
  -> REPRODUCE_OR_MEASURE
  -> HYPOTHESES
  -> DISCRIMINATING_PROBE
  -> ATTRIBUTED -> HANDOFF
  -> UNKNOWN -> SAFE_NEXT_PROBE
```

## Workflow

1. Capture symptom, impact, expected and observed behavior, environment, and recent changes.
2. Detect Go/project context using existing files and adopted tools.
3. Reproduce or measure with the smallest safe probe.
4. Keep at most three falsifiable hypotheses; list evidence for and against each.
5. Choose the safe probe that best distinguishes the leading hypotheses.
6. Mark `ATTRIBUTED` only when one hypothesis explains the signals, alternatives
   are weakened, and exactly one canonical owner is supported.
7. Otherwise mark `UNKNOWN`, name missing evidence, and list safe next probes.
8. Emit the bundle from `references/evidence-bundle.md` and stop.

Use `references/signal-router.md` only after evidence identifies a dominant
risk. A keyword alone is not attribution.

## Authorization and stopping rules

Use read-only inspection and safe local probes already available in the
project. Obtain explicit authorization before production access, destructive
probes, tool installation, credential use, or broad load/security testing.
Preserve secrets through redaction. Stop at `ATTRIBUTED` or `UNKNOWN`; do not
edit code or select the final remedy.

## Quality checklist

- Separate observations from inferences.
- Keep no more than three active hypotheses.
- Choose probes for discrimination, not data volume.
- Support an attributed owner with reproducible evidence.
- Return `UNKNOWN` when the threshold is not met.
- Include missing evidence and one safe next step.

## References

- `references/heuristic.md` — hypothesis and probe protocol.
- `references/signal-router.md` — evidence-based canonical owner routing.
- `references/evidence-bundle.md` — exact terminal output schema.
