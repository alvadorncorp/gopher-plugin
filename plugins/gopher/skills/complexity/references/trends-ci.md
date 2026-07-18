# Trends and CI policy

Complexity work covers both one-time remediation and ongoing guardrails. Use
trend and CI guidance when the goal is to hold or improve complexity over time
rather than fix a single hotspot.

## Trend tracking

- Record measurements over time using the same pinned analyzer and
  configuration, so movement reflects code change, not tool change.
- Track direction per hotspot and for the scope as a whole; a rising trend
  inside thresholds is still a signal.

## CI policy

- Prefer a regression gate: fail when the measured scope worsens versus its
  recorded baseline, rather than failing every pre-existing violation in a
  legacy project.
- Set thresholds from `[complexity]` and treat `complexity.mode = required` as
  the blocking gate; `advisory` reports without failing the build.
- Keep the CI analyzer and configuration pinned and identical to local runs so
  developers can reproduce a failure exactly.
- Scope the gate to changed packages when a whole-repository gate would be
  dominated by legacy debt.
