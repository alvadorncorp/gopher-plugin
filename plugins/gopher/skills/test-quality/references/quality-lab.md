# Quality Lab

The `quality-lab` mode answers one question: which single technique can show
that a named claim about this code is false, at the lowest cost the project can
afford. It is entered only when the user selects it by name. Load this file and
`references/lab-families.md` together, and only in that mode.

## The eligible set is not a plan

The eligible-set gate lives in `SKILL.md`, over the
`test-quality.quality_lab_families` value that `gopher:config` owns; read it
there. What follows from it here: a `quality-lab` run selects exactly one family
per named risk and says why the cheaper families were rejected.

## The five-step selection ladder

Work the steps in order. A step that cannot be answered stops the ladder and
becomes the reported gap.

### 1. Name the risk

State the specific claim about the code that might be false, in one sentence,
about observable behavior.

> Worked example: "The rate limiter admits at most N requests per window, even
> when requests arrive from several goroutines at the window boundary."

"The concurrency code might be buggy" is not a risk; it names no claim and no
observation that could contradict one. Send it back for a claim before choosing
anything.

### 2. Find an independent oracle

Name what, other than the code under test, can say the claim is false. An oracle
is a specification, an invariant, a reference implementation, a reviewed
artifact, a model, an injected fault, or a runtime analysis such as the race
detector.

> Worked example: the limiter's own admission invariant — the count of admitted
> requests within one simulated window — asserted against the configured N,
> which is stated in the contract and not read back from the limiter.

`SKILL.md` holds the rule that disqualifies an oracle which is the code under
test; apply it here and stop the ladder when it bites. In practice it catches a
golden file regenerated with `-update` and never reviewed, and an expected value
copied from the current output. `references/refactoring-safety.md` applies the
same gate to characterization tests.

### 3. Resolve the declared Go version

Read the version declared in `go.mod` and resolve every candidate technique
against it, never against the current stable release. `references/lab-families.md`
carries the guard table.

> Worked example: the risk suits `deterministic-concurrency`, which wants
> `testing/synctest`. The project declares Go 1.22, which does not ship it, so
> that candidate is rejected with the guard stated and the ladder continues with
> an injected-clock variant or `flake` plus `race-leak`.

### 4. Find an available seam

Name where the technique observes or substitutes behavior: an injectable clock,
an interface at the dependency boundary, a `httptest` server, a filesystem
abstraction, an exported operation set, a compilable package.

> Worked example: the limiter takes a clock through its constructor and exposes
> `Allow`, so a fake clock plus concurrent callers is an available seam. Had the
> limiter called `time.Now` directly with no injection point, the seam would be
> absent, and the honest output is that creating the seam is a production change
> owned by `gopher:developer` or `gopher:refactor`.

### 5. Choose the cheapest technique that falsifies the claim

Order the surviving candidates by cost and select the cheapest one that could
actually produce a counterexample. Record the rejected candidates with the
reason: a missing oracle, a missing seam, a version guard, or a cost that
outruns the risk.

> Worked example: `mutation` over the limiter package would also expose weak
> assertions, but it is the most expensive family and it does not directly
> address the boundary-timing claim. `flake` with `-count`, `-shuffle`, and
> `-race` reaches the claim at a fraction of the cost and is selected;
> `mutation` is recorded as rejected on cost.

## Evidence requirements

Every `quality-lab` run reports all of the following. A run that cannot produce
one of them reports the gap and downgrades its status rather than presenting an
unqualified result.

| Requirement | Content |
|---|---|
| Reproducible baseline | The suite state before the technique ran, from the same commands, and whether it was passing |
| Exact commands | Every command verbatim, including flags, package selectors, and counts |
| Environment | Operating system, architecture, CPU count, and whether the run was local or CI |
| Seeds | Every seed that influenced the run: `-shuffle` seed, generator seed, corpus selection |
| Fixtures | The fixture, golden artifact, container image tag, or corpus revision used |
| Tool versions | The Go toolchain version and the exact version of every non-standard tool |
| Reproduction | The minimal command sequence a reader runs to see the same result |
| Before and after evidence | The measurement on both sides of the change, under identical conditions |
| Limitations | What the run did not cover, stated as scope, not as an apology |

## Reproducibility contract

- Record the Go toolchain version reported by `go version` and the version
  declared in `go.mod`; they can differ and both matter.
- Pin every generator and shuffle seed and print it in the failure message, so a
  failing run is replayable from its own output.
- Treat `-count=1` as the default for anything that must not read the test
  cache, and say when the cache was allowed.
- Name the fixture revision. "The test data" is not a fixture; a path plus a
  commit or a checksum is.
- A run that is not reproducible is evidence about the harness, not about the
  code, and is reported that way.

## Presenting before and after evidence

Present both sides under identical commands, environment, seeds, fixtures, and
tool versions, and show the delta explicitly:

- the claim under test and the family selected;
- the before measurement, with its command and its raw result;
- the change made to the suite, which is test-only in this skill;
- the after measurement, from the same command;
- the interpretation, separating what the technique proved from what it merely
  exercised;
- what a passing result still does not prove, taken from the family entry in
  `references/lab-families.md`.

A single run is `observed` evidence. Repeated runs under a stable environment are
`reproduced` evidence. Static reasoning with no run is `suspected` and is a
measurement request, not a result.

## Unavailable tooling

An unavailable tool is a stated limitation, never a silent omission and never an
installation. When a selected technique needs a tool the project has not adopted:

1. Name the tool and the exact capability it would have provided.
2. Name the risk that stays unfalsified without it.
3. Offer the cheapest standard-library alternative that reaches part of the
   claim, and state which part it does not reach.
4. Record the result as `COMPLETE_WITH_LIMITATIONS` rather than `COMPLETE`.

The Go standard library covers most families on its own — `testing`,
`testing/synctest` on the versions that ship it, `go test -race`, `httptest`,
`testing/iotest`, `testing/fstest`, `testing/quick` — so a missing third-party
tool usually narrows a run rather than blocking it. Mutation is the exception,
and its policy lives in `references/mutation.md`.

## Boundary handoffs

A `quality-lab` run that reaches a named neighbor's territory hands off with the
risk and the evidence already written down: a fuzz target and its campaign to
`gopher:fuzz`, a benchmark or profile to `gopher:performance`, a chaos
experiment to `gopher:resilience`, security testing to `gopher:security`, and any
production change to `gopher:developer`.

Sources: <https://pkg.go.dev/testing>, <https://pkg.go.dev/cmd/go#hdr-Testing_flags>.
Last verified: 2026-08-05.
