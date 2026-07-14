# Gopher Plugin

Gopher is an evidence-driven Go engineering plugin for Codex and Claude. One
physical skill tree provides pattern decisions, application architecture,
routine Go development, package architecture, concurrency/performance diagnosis,
security workflows, symptom attribution, and read-only multi-lens review.

## Package layout

- Codex marketplace: `.agents/plugins/marketplace.json`
- Claude marketplace: `.claude-plugin/marketplace.json`
- Shared plugin: `plugins/gopher/`
- Shared skills: `plugins/gopher/skills/`
- Structural and forward tests: `tests/`

Version `0.1.0` intentionally ships no hooks, MCP servers, apps, LSP servers,
or visual assets.

## Skills and ownership

| Skill | Primary ownership |
|---|---|
| `design-patterns` | Language-agnostic code/module pattern diagnosis and selection |
| `application-architecture` | Language-agnostic internal application boundaries |
| `developer` | Routine local Go implementation, APIs, errors, tests, and tooling |
| `architecture` | Go packages, modules/workspaces, dependency direction, seams, and public APIs |
| `concurrency-performance` | Goroutine lifetime, synchronization, context, races, benchmarks, profiles, and measured optimization |
| `diagnose` | Evidence-driven attribution of vague Go symptoms |
| `security` | Go threat modeling, reachability, safe verification, and remediation |
| `review` | Read-only exact-mode review fan-out, consolidation, and verdict |

Each request has one primary owner. Skills exchange stable `gopher:<skill>` and
`pattern.*`/`go.*` identifiers through textual handoffs; no skill depends on a
relative path into a peer.

## Install locally in Codex

From this repository root:

```bash
codex plugin marketplace add .
codex plugin add gopher@alvadorncorp
```

Restart or open a new Codex session after installation so the current plugin
snapshot is loaded.

## Install locally in Claude Code

From this repository root:

```bash
claude plugin marketplace add . --scope user
claude plugin install gopher@alvadorncorp --scope user
```

For development without installation, start Claude Code with:

```bash
claude --plugin-dir ./plugins/gopher
```

## Use Gopher

Codex can select skills naturally or through explicit skill selection. Claude
exposes namespaced commands such as `/gopher:review --mode full`.

Examples:

- `Diagnose this Go problem before proposing a fix.`
- `Choose an idiomatic pattern for this Go design.`
- `Review this Go change with --mode tests,security.`

Review lenses are `correctness`, `tests`, `security`, `architecture`, and
`concurrency-performance`. `--mode full` selects all five. A comma-separated
mode selects exactly that subset. Without a mode, `review` recommends lenses and
waits for confirmation before dispatch.

## Development and validation

Run deterministic gates:

```bash
python3 tests/validate_repo.py
python3 -m unittest discover -s tests -p 'test_*.py'
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/plugin-creator/scripts/validate_plugin.py" plugins/gopher
claude plugin validate . --strict
python3 tests/run_forward_tests.py --validate-only
```

Live forward tests require authenticated local harnesses and installed Codex
and Claude plugin snapshots:

```bash
python3 tests/run_forward_tests.py --harness codex --harness claude
```

Review official, version-sensitive Go references after every stable Go release
and at least quarterly. All repository documentation is written in English.

## License

MIT — see [LICENSE](LICENSE).
