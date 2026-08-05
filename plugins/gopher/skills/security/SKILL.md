---
name: security
description: Threat-models and secures Go applications using trust boundaries, data flow, reachability, safe verification, and evidence-backed remediation, and owns exposure of debug and profiling endpoints plus redaction rules for secrets, credentials, authorization material, and personal data in telemetry attributes. Use for explicit security, threat, vulnerability, or exploitability work. Designing and implementing the telemetry itself belongs to `gopher:observability`; route generic functional review and unauthorized destructive or production probes outside this workflow.
---

# Go Security

## Context and ownership

Own Go threat modeling, trust boundaries, data flow, reachable vulnerabilities,
safe verification, and requested local remediation. Primary owner:
`gopher:security`. Generic diff review belongs to `gopher:review`; broad package
or public-contract fixes hand off to `gopher:architecture` or `gopher:developer`.

Two telemetry-adjacent responsibilities are owned here:

- **Exposure of debug and profiling endpoints.** `net/http/pprof` registers its
  handlers on `http.DefaultServeMux` as an import side effect, so an unguarded
  import can serve profiling — and with it heap contents and goroutine stacks —
  on a public listener. Reviewing that exposure, the listener it is bound to,
  and the authorization in front of it is security work.
- **Redaction of telemetry attributes.** Whether a log, metric, or span
  attribute may carry a secret, a credential, authorization material, or
  personal data is a security decision, and it is ruled on here.

`gopher:observability` designs the signal, its instrumentation, and its export;
`gopher:security` rules on what that signal may carry and on who may reach the
endpoints that serve it.

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
   Count debug and profiling endpoints as entry points: record every import that
   registers handlers on `http.DefaultServeMux`, the listener each one is served
   on, its network exposure, and the authorization in front of it.
3. Form threat hypotheses with attacker, preconditions, source-to-sink path,
   reachability, and expected control failure.
4. Inspect Go-specific risk families relevant to that path, including the
   telemetry sinks on it: rule on whether each log, metric, or span attribute
   may carry a secret, a credential, authorization material, or personal data,
   and state the redaction the signal must apply.
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
- Treat each debug or profiling endpoint as an entry point with a named
  listener, exposure, and authorization decision.
- Rule on what every telemetry attribute may carry; designing and implementing
  the telemetry itself belongs to `gopher:observability`.
- Use project-aware tools and preserve authorization boundaries.
- Validate remediation against the original path and state residual risk.

## References

- `references/threat-model.md` — scope, assets, actors, boundaries, threats.
- `references/data-flow.md` — source-to-sink mapping and reachability.
- `references/go-risk-catalog.md` — Go-specific risk families.
- `references/tooling.md` — safe project-aware verification.
- `references/finding-format.md` — exact finding and report schemas.
- `references/sources.md` — official sources and freshness metadata.
