# Idiomatic Go Baselines

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
