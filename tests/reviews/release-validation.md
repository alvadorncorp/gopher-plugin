# Gopher 0.2.2 Release Validation

## Scope

Validated packaging for native Grok Build support (`adr:gopher:003`): third-host
marketplace and plugin manifests, `review`/`refactor` Grok harness adapters,
triple-harness structural tests, optional `--harness grok` forward runner, and
documentation updates. Skill ownership and the `.gopher-plugin.toml` contract
are unchanged from `0.2.1`.

## Host Versions

- `codex --version` — deferred to operator environment (unchanged packaging path).
- `claude --version` — deferred to operator environment (unchanged packaging path).
- `grok --version` — `grok 0.2.112 (02d9359) [alpha]`.

## Deterministic Gates

- `python3 tests/validate_repo.py` — exit 0; 13 skills, 84 references, 3
  manifests, and 3 marketplaces validated.
- `python3 -m unittest discover -s tests -p 'test_*.py'` — exit 0.
- `python3 tests/run_forward_tests.py --validate-only` — exit 0; 42-case corpus
  validated for codex, claude, and grok without model execution.
- `grok plugin validate plugins/gopher` — exit 0; plugin validation passed.
- Codex `validate_plugin.py` and `claude plugin validate . --strict` — operator
  environment when available; packaging identity fields remain aligned.

## Local Installation Results

Not run as a mandatory gate. Recommended smoke after merge:

```bash
grok plugin marketplace add .
grok plugin install gopher --trust
grok plugin details gopher
```

## Live Cross-harness Forward Results

Not run. AR1 defers the credentialed model-backed run. Future operator command:

```bash
python3 tests/run_forward_tests.py --harness codex --harness claude --harness grok
```

Expected: `Forward tests passed: 42 cases x 3 harnesses.`

## Active Exceptions

- AR1: the credentialed live multi-harness parity run requires installed plugin
  snapshots plus authenticated hosts and operator approval; it is not
  autonomously runnable. The deterministic `--validate-only` corpus check is the
  automatable substitute.

## Verdict

PASS_WITH_EXCEPTION for deterministic packaging and Grok-native packaging.
Before changing this verdict to `PASS`, an authorized operator may run local
registration/installation and the live forward-test matrix under AR1.
