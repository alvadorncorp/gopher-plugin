# Security Lens

Review only changed trust boundaries, inputs, controls, data flows, dangerous
sinks, dependency/symbol reachability, secret exposure, and security-sensitive
races. Require attacker, preconditions, source-to-sink path, failed control,
and impact for a confirmed finding.

Keep unverified exploitability as `MISSING_EVIDENCE`. Route focused security
analysis/remediation to `gopher:security`; route broad package/public-contract
fixes through `gopher:architecture`. Execute no destructive or production probe.
