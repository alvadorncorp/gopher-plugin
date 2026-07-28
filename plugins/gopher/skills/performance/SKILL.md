---
name: performance
description: Analyzes and plans Go sequential performance work across asymptotic and algorithmic cost, data structures, allocations, GC, cache behavior, parsing, I/O amplification, benchmarks, profiles, latency, and throughput. Use to make existing Go code faster, remove a quadratic or cubic scan, or interpret testing.B, pprof, and go tool trace evidence. Route goroutine, synchronization, and backpressure work to `gopher:concurrency` and local edits to `gopher:developer`. Asymptotic cost stays here even when the user calls it complexity; cyclomatic and cognitive complexity metrics belong to `gopher:complexity`.
---

# Go Performance

## Context and ownership

Own Go sequential performance analysis: asymptotic and algorithmic cost, data
structure selection, allocations, GC pressure, cache behavior, parsing, I/O
amplification, benchmarking, profiling, latency, and throughput. Primary owner:
`gopher:performance`.

This skill analyzes and produces an optimization plan. Local reversible
implementation goes to `gopher:developer` together with the exact before and
after verification. An independent revalidation by this skill after the change
happens when the user asks for it.

Route goroutine lifetime, channel, synchronization, cancellation, race,
deadlock, goroutine leak, and backpressure remedies to `gopher:concurrency`. Route a
package boundary, module topology, or public-contract change to
`gopher:architecture`. Route an unattributed symptom to `gopher:diagnose`.

Asymptotic time and space cost belong here. Cyclomatic complexity, cognitive
complexity, function and file size, and maintainability thresholds belong to
`gopher:complexity`. The two are different measurements and stay separate.

## State machine

```text
CORRECTNESS AND COST MODEL -> MAGNITUDE -> ATTRIBUTION -> GATED TIMELINE -> OPTIMIZATION PLAN -> HANDOFF -> LIKE-FOR-LIKE RE-MEASUREMENT
```

## Workflow

The ladder is symptom-gated. Collect one discriminating diagnostic at a time and
stop as soon as a single hypothesis has sufficient reproducible support.

1. **Establish the ground truth.** Record the user-visible metric, the
   correctness tests that must keep passing, the representative workload, input
   distribution and output size, update frequency, the environment, and the
   project's declared Go version. Write the explicit time and space cost model
   for the current code, including construction, output, and update terms.
2. **Quantify magnitude.** Use `references/benchmarking.md` to build a
   version-compatible `testing.B` matrix over small, representative, large, and
   adversarial inputs. Growth across input sizes is a scaling symptom; static
   analysis of the algorithm is what establishes the complexity class.
3. **Attribute the cost.** Use `references/evidence-matrix.md` to pick exactly
   one `pprof` view that discriminates between the surviving hypotheses, and
   capture it with `references/profiling.md`.
4. **Escalate to a timeline only when gated.** Capture a bounded execution trace
   only when the unresolved question is latency, scheduling, utilization,
   syscall or network wait, blocking, or GC timing. A trace is not the tool for
   a CPU or memory hot spot.
5. **Select techniques by tier.** Work down
   `references/algorithmic-transformations.md`, then
   `references/go-hot-paths.md`, then `references/allocation-runtime.md`, and
   resolve every candidate against `references/version-sensitive.md`. Change the
   access pattern and the asymptotic cost before removing copying, and remove
   proven copying before reaching for a runtime, compiler, or `unsafe`
   technique.
6. **Deliver the plan and the verification.** State the selected option, its
   semantic preconditions, expected cost and memory terms, the trade-off budget,
   rejected alternatives, evidence strength and limitations, the implementation
   owner, and the exact like-for-like measurement that accepts or rejects the
   change.

## Acceptance and trade-offs

- Correctness cannot regress. A change that alters observable semantics is a
  different proposal and needs its own approval.
- A secondary metric may regress only inside a budget declared before the
  change, per workload. There is no universal latency, throughput, or memory
  default.
- Evidence covers small, representative, large, and adversarial inputs.
- Report expected cost, never a guaranteed speedup. A prediction without a
  measurement stays a hypothesis.

## Output format

```yaml
selected_skill: gopher:performance
primary_owner: gopher:performance
status: COMPLETE | NEEDS_EVIDENCE | BLOCKED
metric_and_workload:
cost_model:
hypotheses_and_probes:
evidence_collected:
evidence_strength_and_limits:
rejected_hypotheses:
optimization_options:
selected_option_and_tradeoffs:
verification_plan:
authorization_gate: none | approval-required | blocked
handoff: gopher:developer | gopher:concurrency | gopher:architecture | gopher:diagnose | null
```

## Authorization boundaries

- An explicit request to make code faster permits the local reversible
  implementation handoff to `gopher:developer`. Analysis-only intent stops at
  the plan.
- Use benchmarks, profiles, and traces already adopted by the project. Tool
  installation, production profiling, destructive load generation, secret
  access, and broad security probes require explicit authorization.
- Cross-package, public-contract, architectural, and `unsafe` changes retain an
  explicit approval gate and their canonical owner; `GOMEMLIMIT` and
  profile-guided optimization carry the same gate.
- An optimization request with no stable baseline returns a measurement plan
  first rather than a code change.
- Production telemetry used as workload context stays bounded and
  privacy-aware.

## Quality checklist

- Separate the cost claim from the concurrency claim, and name one primary
  owner.
- State construction, output, and update cost terms, not just the query term.
- Keep the declared Go version in every recommendation; the current stable
  release is not a baseline.
- Report sampling, overhead, and interference limits with every diagnostic.
- Compare before and after under the same workload, inputs, Go version, flags,
  and machine state.
- Preserve correctness tests alongside every performance claim.

## References

- `references/evidence-matrix.md` — claim-to-probe selection and stopping rules.
- `references/benchmarking.md` — the `testing.B` and input-size matrix protocol.
- `references/profiling.md` — capture commands and one profile per hypothesis.
- `references/algorithmic-transformations.md` — tier 1 access-pattern and I/O changes.
- `references/go-hot-paths.md` — tier 2 Go copying and storage patterns.
- `references/allocation-runtime.md` — tier 3 allocation, runtime, and advanced techniques.
- `references/version-sensitive.md` — the declared-Go-version guard table.
- `references/pattern-mappings.md` — the object-pool mapping.
- `references/sources.md` — primary sources and review cadence.
