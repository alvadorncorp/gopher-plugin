# Go Modules and Workspaces

Use one module by default. Add a module when versioning, release ownership,
dependency policy, or independent consumption is real and durable. Use
`go.work` for local multi-module development, not as a published dependency
contract. Review `replace` directives and workspace-only success before release.

A module split specifies import compatibility, versioning, CI for each module,
dependency direction, release sequence, rollback, and consumer migration.

Official sources: <https://go.dev/ref/mod>, <https://go.dev/doc/tutorial/workspaces>.
Last verified: 2026-07-14.
