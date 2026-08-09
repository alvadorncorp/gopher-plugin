# Idiomatic Go Baselines

## Resolved idiom policy

The resolved `idiom_policy` selects one of these bounded behaviors:

| Policy | Semantics |
|---|---|
| `latest-compatible` | Prefer the newest suitable declared-version idiom locally. |
| `project-aligned` | Prioritize nearby adopted conventions when choosing an idiom. |
| `explicit-only` | Introduce a newer idiom only on explicit request. |

All three policies are capped by the declared Go version and apply only to
new or directly changed code. They never consume `modernize.target_go`; broad or
unrelated rewrites are handed to `gopher:modernize`.

- Prefer useful zero values, literals, and explicit constructors.
- Start with concrete types; introduce an interface at the consumer only when
  real variability, a test/process boundary, or compatibility seam exists.
- Accept interfaces and return concrete types unless the API contract requires otherwise.
- Keep interfaces small and behavior-focused.
- Pass `context.Context` explicitly as the first parameter for request-scoped
  cancellation/deadlines; keep it out of stored configuration structs.
- Make resource ownership and `Close` responsibility explicit.
- Keep package APIs cohesive and names meaningful at the call site.
- Use `defer` when lifetime is clear and its cost is appropriate for the path.

Official source: <https://go.dev/wiki/CodeReviewComments>.
Last verified: 2026-07-14.
