# Gopher 0.2.0 Release Validation

## Scope and Commit

Validated the worker branch `worker-gopher-python-refactoring-parity` through
`a963ba8` for the 0.2.0 release, which adds five peer skills (`config`,
`complexity`, `test-quality`, `modernize`, `refactor`), the `.gopher-plugin.toml`
project contract, `adr:gopher:002`, and an expanded routing corpus. Scope
includes deterministic packaging, repository contracts, forward-corpus
structure, and both plugin validators. Live local installation and model
execution are covered by exception AR1.

## Codex and Claude Versions

- `codex --version` — `codex-cli 0.144.5`.
- `claude --version` — exit 0; `2.1.214 (Claude Code)`.

## Deterministic Gates

- `python3 tests/validate_repo.py` — exit 0; 13 skills, 82 references, 2
  manifests, and 2 marketplaces validated.
- `python3 -m unittest discover -s tests -p 'test_*.py'` — exit 0; 19 tests,
  `OK`.
- `python3 tests/run_forward_tests.py --validate-only` — exit 0; 42-case corpus
  validated for codex and claude without model execution.
- Codex `validate_plugin.py plugins/gopher` — exit 0; plugin validation passed.
- `claude plugin validate . --strict` — exit 0; validation passed.

## Skill-review Gate

Every new `SKILL.md` (`config`, `complexity`, `test-quality`, `modernize`,
`refactor`) was reviewed by the `rashomon:skill-reviewer` subagent in creation
mode and accepted at grade A (0 P1, 0 P2); applied findings were P3 polish only.
The two existing skills whose bodies materially changed (`developer`, `review`)
passed modification-mode review at grade A with no regressions.

## Fresh Read-only Review

A fresh read-only `gopher:review` over the full branch diff
(`43bf7fad..ed8e389c`) returned `APPROVED_WITH_NOTES`: all five lenses
completed, zero blocking findings, two minor non-blocking notes recorded in
`.plans/gopher-python-refactoring-parity/reviews/01-fresh-review.md`.

## Marketplace Conflict Preflight

Not run. AR1 preserves the operator's control over local marketplace
configuration; no local state was inspected, registered, or replaced.

## Local Installation Results

Not run. AR1 defers `codex plugin marketplace add`, `codex plugin add`,
`claude plugin marketplace add`, and `claude plugin install` until an operator
explicitly authorizes local state changes.

## Live Cross-harness Forward Results

Not run. AR1 defers the credentialed model-backed run. Future operator command:
`python3 tests/run_forward_tests.py --harness codex --harness claude`
Expected: `Forward tests passed: 42 cases x 2 harnesses.`

## Active Exceptions

- AR1: the credentialed live Codex/Claude parity run (42 cases x 2 harnesses)
  requires an installed plugin snapshot plus authenticated Codex and Claude and
  operator approval; it is not autonomously runnable. The deterministic
  `--validate-only` corpus check is the automatable substitute and passed. The
  operator runs the live parity command (or explicitly waives it) to close the
  design's definition-of-done.

## Verdict

PASS_WITH_EXCEPTION. Every deterministic validator, both plugin validators, the
five creation-mode skill reviews, the two modification-mode reviews, and the
fresh read-only review pass; the 42-case structural corpus is validated for both
harnesses. Before changing this verdict to `PASS`, an authorized operator must
run local registration and installation and the live 42-case-per-harness
command under AR1.
