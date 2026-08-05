# Structured Logging with `log/slog`

`log/slog` arrived in Go 1.21. Confirm the project's declared Go version before
recommending it, and confirm any handler helper added in a later release against
that same version.

## Handler selection

| Destination | Handler | Reason |
|---|---|---|
| Log collector or ingestion pipeline | `slog.NewJSONHandler` | Machine-parsable attributes survive transport |
| Developer terminal | `slog.NewTextHandler` | Readable during local work, weak for querying |
| Telemetry pipeline that already carries logs | A bridge handler supplied by the telemetry module | Log records inherit resource identity and trace context |
| Benchmarks and tests that ignore output | The discard handler for the declared Go version, otherwise `io.Discard` with a text handler | Removes formatting cost from the measurement |

Configure the handler once, in the composition root, through
`slog.HandlerOptions`: `Level` for the threshold, `AddSource` when the call site
earns its cost, and `ReplaceAttr` for renaming and redaction.

## Level policy

| Level | Meaning | Emission expectation |
|---|---|---|
| `DEBUG` | Detail useful while investigating | Off by default, switchable at runtime |
| `INFO` | A durable statement about a completed unit of work | Bounded per request or per job |
| `WARN` | A degraded path that continued | Rare enough to read |
| `ERROR` | A failed operation that a human may need to act on | Paired with a counter, since alerting on log volume is fragile |

Hold the threshold in a `slog.LevelVar` so verbosity changes without a restart.
A per-request logger raises the level for a sampled subset instead of raising it
globally.

## Attribute discipline

- Use a fixed key set per message. A message whose keys vary between call sites
  cannot be queried.
- Prefer `LogAttrs` with typed `slog.Attr` values on hot paths; the variadic
  `any` form pays conversion and allocation cost per call.
- Keep the message stable and low-cardinality. Identifiers, counts, and
  durations belong in attributes, not interpolated into the message.
- Record durations as a typed value with a stated unit, and errors through a
  single `error` key plus a closed `error.kind` enumeration.
- Attach the trace and span id to every record emitted inside a request so logs
  join traces.

## Grouping

`slog.Group` namespaces related attributes so unrelated subsystems stop
colliding on generic keys such as `id`, `status`, or `count`. A group renders as
a nested object in JSON and as dotted keys in text, which keeps queries explicit:
`db.query.rows` states its origin where a bare `rows` does not. `Logger.WithGroup`
applies the same namespace to every subsequent record from that logger, which
suits a component-scoped logger.

## Context-carried attributes

A handler receives the `context.Context` in its `Handle` method, so a custom
handler can read request-scoped values — trace id, span id, tenant, request id —
and attach them to every record without threading them through call signatures.
Two rules keep this safe:

- The context carries identity and correlation keys, never the payload. A
  context that accumulates arbitrary data becomes an unaudited log source.
- The extraction is total: a missing value produces no attribute rather than a
  panic or an empty string that pollutes queries.

Passing a `*slog.Logger` through the context is a separate decision from
carrying attributes; an explicit logger parameter or a component-scoped logger
field keeps the dependency visible.

## The library rule

A library does not choose the process's handler. Concretely:

- Accept a `*slog.Logger` through a constructor option and default to a
  no-output logger when the caller supplies none.
- Leave `slog.SetDefault`, handler construction, level policy, and output
  destination to the composition root, which owns process-wide configuration.
- Document the levels the library emits and the attribute keys it sets, so the
  application can budget volume and redaction.

A library that installs a default handler overwrites the application's format,
destination, and redaction policy from an import side effect, and the
application discovers it in production. See
`references/instrumentation-boundaries.md` for the same rule applied to
providers and exporters.

Last verified: 2026-08-05.
