# Shared Review Severity and Confidence

| Severity | Demonstrated impact | Approval effect |
|---|---|---|
| critical | exploitable security, data loss/corruption, severely wrong behavior, or broken public contract | blocks |
| important | reproducible bug, race/leak, silent failure, missing essential test, or relevant regression | blocks |
| minor | localized improvement without demonstrated functional risk | non-blocking |

Confidence is independent:

- `high`: direct reproduction, deterministic proof, or complete source-to-sink path.
- `medium`: strong code evidence with one bounded unverified premise.
- `low`: plausible risk needing named evidence; normally report as missing evidence rather than a finding.

Every finding needs `file:line`, a concrete failure scenario, evidence, impact,
and an actionable fix. Formatting/lint-owned style remains outside review findings.
