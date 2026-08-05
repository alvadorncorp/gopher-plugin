---
name: fuzz
description: Designs native Go fuzz targets and invariants, curates seeds and corpora, runs bounded `go test -fuzz` campaigns, and minimizes, reproduces, and promotes crashing inputs as regressions. Use for fuzzing intent, a `testing.F` target, a seed corpus question, or a crash a campaign produced. Route the production fix to `gopher:developer` or the matching risk specialist, and suite-wide technique selection to `gopher:test-quality`.
---

# Go Fuzzing

## Context and ownership

Own the design and execution of native Go fuzzing (`testing.F`, `go test -fuzz`):
target selection, falsifiable invariants, seed and corpus curation, bounded
campaigns, minimization, reproduction, and promotion. Primary owner: `gopher:fuzz`.

A campaign here produces a reproducible failing case and a handoff. The
production fix happens under the receiving owner.

- Fixing the defect goes to `gopher:developer`, or to `gopher:security`,
  `gopher:concurrency`, or `gopher:performance` for a defect of that risk class.
- Overall test-suite strategy goes to `gopher:test-quality`.
- Benchmarks and throughput measurement go to `gopher:performance`.

The boundary with `gopher:test-quality` is sharp. Choosing which testing
technique falsifies a named risk across the suite is its `quality-lab` mode;
designing a fuzz target, its invariant, and its campaign is `gopher:fuzz`.

Read the `[fuzz]` table of `.gopher-plugin.toml` (schema v2) through
`gopher:config`: `local_budget_seconds` (default `60`), `ci_budget_seconds`
(default `300`), and `repro_runs` (default `3`). An absent configuration means the
budget is confirmed with the user before a campaign runs, never silently defaulted.

## Modes

| Mode | When | Stop condition |
|---|---|---|
| `design` | A function needs a fuzz target, or an existing target carries no stated invariant. | The target, a falsifiable invariant, and an independent oracle are written down. |
| `run` | A designed target is ready to execute inside a budget. | The configured local or CI budget is exhausted, or the campaign reports a failing input. |
| `triage` | A campaign produced a failing input. | The input is minimized and either reproduces `repro_runs` times or is attributed to the environment. |
| `promote` | A minimized case reproduces and belongs in the checked-in corpus. | The seed lives under `testdata`, and the handoff record names the owner who fixes the defect. |

## State machine

```text
TARGET AND INVARIANT -> SEED CORPUS -> BOUNDED CAMPAIGN -> MINIMIZE -> REPRODUCE -> CLASSIFY -> PROMOTE
```

## Workflow

1. Choose the function under test with `references/target-design.md`. Parsers,
   decoders, state machines, and round-trip pairs are the natural candidates.
2. Define a falsifiable invariant and an independent oracle. An oracle that
   re-implements the function under test restates its assumptions and adds none.
3. Select real seeds and previously fixed failures with `references/corpus.md`,
   carrying no secrets and no personal data.
4. Run inside `local_budget_seconds` or `ci_budget_seconds` using
   `references/campaigns.md`, one target per invocation.
5. Minimize, then reproduce the written failure `repro_runs` times with `references/triage.md`.
6. Distinguish a real input-driven crash from a flaky environment using the
   decision table in `references/triage.md`.
7. Promote only a minimized, replayable seed suitable for `testdata` with
   `references/promotion.md`, and record the handoff.

## Output format

```yaml
selected_skill: gopher:fuzz
primary_owner: gopher:fuzz
mode: design | run | triage | promote
status: PASS | CRASH | FLAKY | LIMITED | BLOCKED
config_status: ABSENT | VALID | MIGRATION_AVAILABLE | INVALID | UNSUPPORTED_VERSION
target:
invariant:
oracle:
budget:
minimized_input:
reproduction:
authorization_gate: none | approval-required | blocked
handoff: gopher:<skill> | null
```

### Terminal states

| Status | Meaning |
|---|---|
| `PASS` | The budget was exhausted with no failing input. This is a bounded negative result and not proof of correctness; report the budget that produced it. |
| `CRASH` | A failing input was found, minimized, and reproduced. |
| `FLAKY` | The failure stayed unreproduced across `repro_runs` and is attributed to the environment rather than to the input. |
| `LIMITED` | The campaign could not run at its configured shape: the budget was cut short, the seed corpus was empty or unrepresentative, a required tool was unavailable, or a failure reproduced on only one machine, operating system, or Go version. A campaign that ran its full configured budget with no failing input is `PASS`, reported with that budget. |
| `BLOCKED` | A precondition is missing, such as a declared Go version below 1.18, a package that fails to build, or an unconfirmed budget. |

## Authorization boundaries

- Every campaign runs inside a budget resolved from `[fuzz]`:
  `local_budget_seconds` for an interactive run, `ci_budget_seconds` for an
  unattended one, passed as `-fuzztime`. When `[fuzz]` is absent or unreadable,
  confirm the budget with the user first and report `BLOCKED` with
  `authorization_gate: approval-required` until it is confirmed. An unbounded
  `go test -fuzz` run is an open-ended resource commitment; the budget is what
  makes it a bounded experiment.
- Promote a crash after it is minimized to load-bearing elements and reproduces
  `repro_runs` times through a plain `go test -run` replay. Until both hold,
  report it as evidence and name the missing step; an unminimized input is
  evidence, not a regression test.
- Hand the minimized case, the reproduction command, and the campaign evidence to
  the receiving owner, who makes the production fix. This skill's deliverable is
  the reproducible failing case and the handoff record.
- Seeds carry sanitized values only. A real-world sample becomes a seed after
  secrets and personal data are replaced with structurally equivalent stand-ins.
- Use the Go toolchain and the tools the project already adopts, and report a
  missing capability as an explicit limitation.

## Quality checklist

- The invariant is falsifiable and written before the campaign runs.
- The oracle is independent of the implementation under test.
- Every seed is reproducible from the repository and free of sensitive data.
- The reported budget, Go version, and command line reproduce the campaign.
- A promoted regression fails before the fix and passes after it.
- Exactly one receiving owner appears in `handoff` when a defect is confirmed.

## References

- `references/target-design.md` — target choice, falsifiable invariants, independent oracles, the four invariant families, and the `testing.F` shape.
- `references/corpus.md` — seed selection, the `testdata/fuzz` layout and file format, the cache corpus, and seed sanitization.
- `references/campaigns.md` — `go test -fuzz` flags, one target per run, local and CI budget shapes, parallelism, and progress output.
- `references/triage.md` — automatic and manual minimization, replaying a written failure, `repro_runs`, and the real-crash versus flaky-environment table.
- `references/promotion.md` — promoting a minimized case into the checked-in corpus, naming, provenance, and the handoff record.
- `references/sources.md` — version-sensitive official references, the Go 1.18 gate, and the review cadence.
