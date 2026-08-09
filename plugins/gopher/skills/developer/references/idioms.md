# Idiomatic Go Baselines

## Resolved idiom policy

Use `references/project-detection.md` to establish the declared Go version and
local conventions before choosing an idiom. The resolved `idiom_policy` selects
one of these bounded behaviors:

| Policy | Semantics |
|---|---|
| `latest-compatible` | Prefer the newest suitable declared-version idiom locally; "suitable" means supported by the declared Go version and compatible with the current local API and requested behavior. |
| `project-aligned` | Prioritize nearby adopted conventions when choosing an idiom; use the closest relevant package, callers, and tests as evidence. |
| `explicit-only` | Introduce a newer idiom only on explicit request naming that idiom in the current change. |

All three policies are capped by the declared Go version and apply only to
new or directly changed code in the current local change. Keep
`modernize.target_go` with `gopher:modernize`; hand broad, package-wide, or
unrelated rewrites to that skill. When a required input remains unknown after
project detection, report the missing evidence and pause idiom selection until
compatibility or adoption is evidenced.

- Prefer useful zero values, literals, and explicit constructors.
- Start with concrete types; introduce an interface at the consumer only when
  real variability, a test/process boundary, or compatibility seam exists.
- Accept interfaces and return concrete types; choose another return shape only
  when the API contract requires it.
- Keep interfaces small and behavior-focused.
- Pass `context.Context` explicitly as the first parameter for request-scoped
  cancellation/deadlines; keep stored configuration structs request-independent.
- Make resource ownership and `Close` responsibility explicit.
- Keep package APIs cohesive and names meaningful at the call site.
- Use `defer` when lifetime is clear and its cost is appropriate for the path.

Official source: <https://go.dev/wiki/CodeReviewComments>.
Last verified: 2026-07-14.
