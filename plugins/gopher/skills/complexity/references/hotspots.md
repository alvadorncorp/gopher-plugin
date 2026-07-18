# Hotspot ranking

A hotspot is a unit that concentrates complexity and therefore risk. Rank
hotspots so remediation targets the highest-value work first.

## Ranking signals

- Absolute complexity: functions and files furthest past their thresholds.
- Concentration: a small number of units holding a large share of total
  measured complexity.
- Change frequency: units that churn often, where complexity compounds review
  and defect risk (use adopted history when available).
- Coupling to risk: units on correctness- or security-sensitive paths.

## Reporting

- Present a ranked list with each unit's metrics, its distance from target, and
  why it ranks where it does.
- Separate one-time remediation candidates from units better handled by trend
  and CI policy (`references/trends-ci.md`).
- Name the owning workflow for any recommended change: local reduction to
  `gopher:developer`, boundary or contract change to `gopher:architecture`.
