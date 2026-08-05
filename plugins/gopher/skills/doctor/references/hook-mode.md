# Automatic Mode Contract

`hook` is the automatic mode: a host event asks for a readiness answer, and the
answer has to arrive fast enough that the caller keeps working. This file is the
contract that mode honors.

## Delivery scope

This delivery ships the contract, not a runtime. There is no hook executable, no
event dispatcher, and no host wiring in this package. What lives here is the
behavior an implementation must reproduce and the shape of the result it must
return. Treat that as an honest limitation of the current package: a host that
wants automatic readiness supplies the runtime and follows this contract.

Every statement below therefore describes the mode's obligations, and each one
is verifiable against a result bundle once a runtime exists.

## Budget

| Property | Value |
|---|---|
| Profile | `quick`, and only `quick` |
| Internal budget | strictly smaller than the host's outer timeout |
| Finding cap | `doctor.max_findings` |
| Stop condition | the internal deadline or the finding cap, whichever comes first |
| Evidence | read-only file, configuration, and metadata reads |

The internal budget derives from `doctor.deadline_ms` and stays under whatever
outer timeout the host enforces, so the mode returns its own result before the
host cancels it. A run that reaches the deadline stops, reports the rules it
completed, and lists the rest in `checks_skipped`.

## Fail-open semantics

Automatic mode yields a non-blocking result whenever it cannot complete
confidently:

- An internal error while reading or parsing yields a non-blocking result with
  the failing rule listed as skipped and the error class recorded.
- An exceeded deadline yields a non-blocking result with the remaining rules
  listed as skipped.
- A missing capability — an absent command, an unreadable path, an
  unauthorized probe — yields a non-blocking result with that capability named.

In each case the status carries `LIMITED` alongside whatever the completed rules
produced, and the caller proceeds. The mode's job is to inform an automatic
caller, so an incomplete readiness answer stays advisory rather than becoming an
obstacle.

`BLOCKED` remains reachable in automatic mode, and only through the ordinary
blocking policy: a block-eligible rule that ran to completion, on a complete
evidence set, with an actionable in-project remediation and no valid override.
That is a deliberate, evidence-backed result rather than a failure of the run.

## Operational guards

These two guards are absolute, because an automatic caller cannot review the
run before it happens:

- Automatic mode never mutates the project. It reads files, configuration, and
  metadata, and it writes nothing inside the project root.
- Automatic mode never invokes another skill. It names the owner and the handoff
  in the result, and the caller decides what to do with them.

Everything else automatic mode does — rule selection, override application,
aggregation, bundle emission — follows the same rules as `check`, at the `quick`
profile.

## Result shape

Automatic mode emits the bundle in `references/evidence-bundle.md` with
`mode: hook`. A host that only needs a yes or no reads `status`: `READY` and
`WARN` and `LIMITED` are non-blocking, and `BLOCKED` is the single blocking
value. The full bundle stays available for a caller that wants the findings,
the skipped list, and the handoffs.
