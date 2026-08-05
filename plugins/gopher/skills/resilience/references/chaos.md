# Chaos Experiments

Chaos work is hypothesis testing against a failure model, and it starts
plan-only. A plan is produced here; execution requires explicit authorization
and a named environment.

## An experiment is a falsifiable hypothesis

An experiment without a prediction is an outage with better paperwork. Every
plan carries all seven fields:

| Field | Content |
|---|---|
| Hypothesis | The steady-state prediction that survives the fault, stated as a measurable claim |
| Failure-model row | The exact row from `references/failure-model.md` the experiment tests |
| Fault | The concrete injection: latency added to one dependency, a returned error rate, an instance stop, a connection reset |
| Blast radius | The named environment, the subset of traffic or tenants, and the ceiling that must never be exceeded |
| Abort condition | The measured value that stops the experiment immediately, decided before the run |
| Owner | The named person who runs it, watches it, and aborts it |
| Rollback | The exact steps that remove the fault and confirm the steady state has returned |

A hypothesis such as "checkout success rate stays above the declared objective
while the pricing dependency adds 500ms" is falsifiable. "The system should be
fine" is not.

## Readiness before running anything

An experiment is worth running only when all of these hold:

- The steady-state signal exists and is trusted, and it was implemented by
  `gopher:observability`.
- The failure-model row already has a control; the experiment tests that
  control rather than discovering the failure.
- The abort condition is observable within seconds, not after the run.
- The rollback is a single, tested action.
- An unrelated incident is not already in progress.

When any of these is absent, the plan records it as missing evidence and the
experiment stays unscheduled. That is the correct outcome, not a failure.

## Progression of environments

| Stage | Purpose | Gate |
|---|---|---|
| Unit and integration | Prove the control's logic: breaker transitions, backoff bounds, deadline propagation, shutdown drain | The project's normal test authorization |
| Local dependency faults | Inject latency and errors at a fake or proxied dependency | The project's normal test authorization |
| Staging with load | Observe the control under representative arrival rates | Explicit request, named environment |
| Production | Confirm the control under real traffic | Explicit authorization, named environment, owner, blast radius, and abort condition |

Go's own tooling covers the first two stages well: `httptest` servers that
inject latency or error status, fault-injecting `http.RoundTripper` wrappers,
`net.Pipe` for connection resets, and cancelled contexts for deadline paths.
These experiments run inside the project's ordinary test authorization and are
where most control defects are found.

## Authorization boundary

Production experiments are an authorization boundary. Never inject a fault into
production without an explicit authorization that names the environment, the
blast radius, the abort condition, and the owner. The same holds for any shared
environment other teams depend on, and for a drill that moves live traffic
between regions.

Absent that authorization, this skill delivers the plan, the expected
observations, and the readiness gaps, and stops there.

## Reading the result

- A refuted hypothesis is the valuable case: it names a control that does not
  hold and produces a failure-model update with a concrete owner.
- A confirmed hypothesis promotes a proposed control to a proven control, and
  the citation is the experiment record with its date and scope.
- An aborted run is recorded with the abort trigger; the hypothesis stays
  untested and remains residual risk.
- Every result records what it did not cover. One fault at one rate in one
  environment proves exactly that.

Sources: <https://pkg.go.dev/net/http/httptest>,
<https://pkg.go.dev/net/http#RoundTripper>, <https://pkg.go.dev/net#Pipe>.
Last verified: 2026-08-05.
