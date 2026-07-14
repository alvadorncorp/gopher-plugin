# Context and Cancellation

- Accept `context.Context` as the first parameter on request-scoped operations.
- Derive cancellation/deadlines at the owner and call the returned cancel function.
- Propagate context through call chains; keep it out of long-lived config structs.
- Use values only for request-scoped data crossing API/process boundaries.
- Distinguish caller cancellation, deadline, local failure, and partial result.
- Drain or stop dependent goroutines when a peer fails.

Sources: <https://pkg.go.dev/context>, <https://go.dev/blog/context>,
<https://go.dev/wiki/CodeReviewComments#contexts>.
Last verified: 2026-07-14.
