# Version-sensitive sources

These references change with Go releases and library versions. Confirm each
against the toolchain the target project actually declares before relying on a
detail here.

## Cancellation and time budgets

- `context`: <https://pkg.go.dev/context>
- Context blog post: <https://go.dev/blog/context>
- Code review comments, contexts: <https://go.dev/wiki/CodeReviewComments#contexts>
- `context.AfterFunc`: <https://pkg.go.dev/context#AfterFunc>
- `context.WithTimeoutCause`: <https://pkg.go.dev/context#WithTimeoutCause>
- `time.Timer` and `time.After`: <https://pkg.go.dev/time#Timer>

## Errors and classification

- `errors`: <https://pkg.go.dev/errors>
- Error wrapping: <https://go.dev/blog/go1.13-errors>
- `net.Error`: <https://pkg.go.dev/net#Error>
- `errors.Join`: <https://pkg.go.dev/errors#Join>

## Servers, clients, and lifecycle

- `http.Server`: <https://pkg.go.dev/net/http#Server>
- `http.Server.Shutdown`: <https://pkg.go.dev/net/http#Server.Shutdown>
- `http.ErrServerClosed`: <https://pkg.go.dev/net/http#ErrServerClosed>
- `http.Transport`: <https://pkg.go.dev/net/http#Transport>
- `http.MaxBytesReader`: <https://pkg.go.dev/net/http#MaxBytesReader>
- `os/signal.NotifyContext`: <https://pkg.go.dev/os/signal#NotifyContext>
- `net.Dialer` and keep-alive: <https://pkg.go.dev/net#Dialer>

## Limits and bulkheads

- `golang.org/x/time/rate`: <https://pkg.go.dev/golang.org/x/time/rate>
- `golang.org/x/sync/semaphore`: <https://pkg.go.dev/golang.org/x/sync/semaphore>
- `golang.org/x/sync/errgroup`: <https://pkg.go.dev/golang.org/x/sync/errgroup>
- `sync`: <https://pkg.go.dev/sync>

## Data, delivery, and durability

- Executing transactions: <https://go.dev/doc/database/execute-transactions>
- Managing connections: <https://go.dev/doc/database/manage-connections>
- Cancelling database operations: <https://go.dev/doc/database/cancel-operations>
- `database/sql`: <https://pkg.go.dev/database/sql>

## Fault injection for control tests

- `net/http/httptest`: <https://pkg.go.dev/net/http/httptest>
- `http.RoundTripper`: <https://pkg.go.dev/net/http#RoundTripper>
- `net.Pipe`: <https://pkg.go.dev/net#Pipe>
- `testing/synctest`: <https://pkg.go.dev/testing/synctest>

## Review cadence

- Re-read this list after every stable Go release. Timeout, cancellation, and
  server-shutdown behavior have changed across releases, and a control that was
  correct one release earlier can be restated by a new standard-library
  affordance.
- Record the Go version, the module versions of any third-party control, and
  the environment with every proven-control citation, so a later reviewer can
  reproduce the demonstration.
- When an official source deprecates or renames a knob, update the affected
  reference and restate the control before comparing it to an earlier
  assessment.
- Re-verify the declared objectives with the project on each assessment; an
  objective that has changed invalidates the alerting derived from it.

Last verified: 2026-08-05.
