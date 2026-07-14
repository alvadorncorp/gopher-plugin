# Gopher 0.1.0 Release Validation

## Scope and Commit

Validated the worker branch through `8a4559e` before this release-evidence
commit. Scope includes deterministic packaging, repository contracts, forward
corpus structure, and both Rashomon reports. Live local installation and model
execution are covered by exception D005.

## Codex and Claude Versions

- `codex --version` — exit 0; `codex-cli 0.144.3`.
- `claude --version` — exit 0; `2.1.209 (Claude Code)`.

## Deterministic Gates

- `python3 tests/validate_repo.py` — exit 0; 8 skills, 52 references, 2
  manifests, and 2 marketplaces validated.
- `python3 -m unittest discover -s tests -p 'test_*.py'` — exit 0; 13 tests,
  `OK`.
- Codex `validate_plugin.py plugins/gopher` — exit 0.
- `claude plugin validate . --strict` — exit 0.
- `python3 tests/run_forward_tests.py --validate-only` — exit 0; 24-case
  corpus validated without model execution.

## Marketplace Conflict Preflight

Not run. D005 preserves the user's decision not to inspect, register, or
replace local marketplace configuration.

## Local Installation Results

Not run. D005 prohibits `codex plugin marketplace add`, `codex plugin add`,
`claude plugin marketplace add`, and `claude plugin install` until an operator
explicitly authorizes local state changes.

## Forward-test Smoke Results

Not run. D005 prohibits the 8-case model-backed smoke command. Future operator
command: `python3 tests/run_forward_tests.py --harness codex --harness claude --max-cases 8 --output /private/tmp/gopher-forward-smoke.json`.

## Full Cross-harness Results

Not run. D005 prohibits the 24-case-per-harness model-backed command. Future
operator command: `python3 tests/run_forward_tests.py --harness codex --harness claude --output /private/tmp/gopher-forward-full.json`.

## Rashomon Review Summary

`rashomon-foundation.md` and `rashomon-risk-orchestration.md` both report grade
A, zero P1/P2/P3 issues, zero growth, and validated English-only skill content.

## Active Exceptions

- D001: user-directed cleanup remains required for the unintended commit on
  `main`.
- D003: AKB must be rerun after directed main cleanup or merge.
- D005: live marketplace installation and 48 forward-test model executions
  were declined; no local harness configuration was mutated.

## Verdict

PASS_WITH_EXCEPTION. Deterministic validators, both Rashomon reports, and the
24-case structural corpus pass. Before changing this verdict to `PASS`, an
authorized operator must run marketplace conflict preflight, local registration
and installation, the 8-case smoke command, and the full 48-result command.
