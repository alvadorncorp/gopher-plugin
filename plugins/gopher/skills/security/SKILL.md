---
name: security
description: Threat-models and secures Go applications using trust boundaries, data flow, reachability, safe verification, and evidence-backed remediation. Use for explicit security, threat, vulnerability, or exploitability work. Route generic functional review and unauthorized destructive or production probes outside this workflow.
---

# Go Security

## Context and ownership

Own Go threat modeling, trust boundaries, data flow, reachable vulnerabilities,
safe verification, and requested local remediation. Primary owner:
`gopher:security`. Generic diff review belongs to `gopher:review`; broad package
or public-contract fixes hand off to `gopher:architecture` or `gopher:developer`.

## Workflow

```text
SCOPE_AND_AUTHORIZATION
  -> ASSETS_AND_ACTORS
  -> TRUST_BOUNDARIES
  -> DATA_FLOW
  -> THREAT_HYPOTHESES
  -> REACHABILITY_AND_CONTROLS
  -> SAFE_VERIFICATION
  -> FINDINGS
  -> REMEDIATION_AND_RESIDUAL_RISK
```

1. Record in-scope code/environment, authorization, assets, actors, and impact.
2. Map entry points, transformations, sinks, trust transitions, and controls.
3. Form threat hypotheses with attacker, preconditions, source-to-sink path,
   reachability, and expected control failure.
4. Inspect Go-specific risk families relevant to that path.
5. Use the smallest safe project-adopted verification; report tool limits.
6. Confirm a finding only when evidence shows an exploit path or a demonstrably
   missing required control. Keep other results as labeled hypotheses.
7. Provide remediation, validation, residual risk, and one owner.
8. Implement only an explicitly requested local remediation within the approved scope.

## Authorization boundaries

Local read-only analysis and safe tests may proceed. Production access,
destructive probes, credential/secret access, broad load, external-target
testing, or tool installation requires explicit authorization. Redact secrets
from prompts, commands, logs, and reports. Stop when safe evidence cannot close
the hypothesis and name the missing evidence.

## Output format

Use `references/finding-format.md`. Separate confirmed findings, hypotheses,
and no-finding coverage. Every confirmed finding includes reachability,
failure scenario, evidence, safe reproduction, remediation, residual risk, and owner.

## Quality checklist

- Tie every threat to an asset, actor, boundary, precondition, and path.
- Evaluate existing controls before asserting a vulnerability.
- Keep severity independent from confidence.
- Report reflection, `unsafe`, cgo, build tags, and binary visibility limits.
- Use project-aware tools and preserve authorization boundaries.
- Validate remediation against the original path and state residual risk.

## References

- `references/threat-model.md` — scope, assets, actors, boundaries, threats.
- `references/data-flow.md` — source-to-sink mapping and reachability.
- `references/go-risk-catalog.md` — Go-specific risk families.
- `references/tooling.md` — safe project-aware verification.
- `references/finding-format.md` — exact finding and report schemas.
- `references/sources.md` — official sources and freshness metadata.
