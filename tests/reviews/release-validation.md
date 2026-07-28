# Gopher 0.3.0 Release Validation

## Scope

Validated the ownership split recorded in `adr:gopher:005`: the retirement of
the combined owner with no compatibility facade, the new
`gopher:concurrency` and `gopher:performance` peers, the `concurrency`,
`performance`, and `complexity` review lenses with a seven-lens `--mode full`,
the split routing rows in `gopher:diagnose` and `gopher:refactor`, and the
retargeted and extended forward corpus. Packaging, the four harness manifests,
and the `.gopher-plugin.toml` contract are unchanged from `0.2.3`.

This is a breaking change on a `0.x` line. A direct invocation of
the retired combined skill no longer resolves.

## Deterministic Gates

- `python3 tests/validate_repo.py` — exit 0; observed
  `Repository validation passed (14 skills, 95 references, 4 manifests, 4 marketplaces).`
- `python3 -m unittest discover -s tests -q` — exit 0; observed `Ran 19 tests`
  and `OK`.
- `python3 tests/run_forward_tests.py --validate-only` — exit 0; observed
  `Validated 47 forward-test cases for codex, claude, grok, and kimi.`

## Live Routing

- `python3 tests/run_forward_tests.py --harness <host>` — operator-gated and
  billed, consistent with `adr:gopher:004`. Record the host, the date, and the
  observed pass count here when the operator runs it; leave the entry marked as
  not run otherwise.

## Skill Review Chain

- `skill-creator` description-triggering evals for `concurrency` and
  `performance`.
- `plugin-dev:skill-reviewer` and `plugin-dev:plugin-validator` over both new
  packages.
- `rashomon:skill-reviewer`, one dispatch per skill file, across the two created
  and six modified skills.

Reports are kept with the plan under `.plans/go-algorithmic-performance/reviews/`.
