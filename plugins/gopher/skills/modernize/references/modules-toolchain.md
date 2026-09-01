# Modules, toolchain, and dependencies

Modernize module metadata, workspace layout, and dependencies conservatively,
staying inside the declared version and adopted commands.

## Modules and workspace

- Align `go.mod` directives with the declared version without raising it under
  `target_go = "declared"`.
- Respect an existing `go.work`; propose workspace changes as previews and hand
  a module-topology change to `gopher:architecture`.
- From Go 1.27, `go mod tidy` merges duplicate `require` blocks in a module
  declaring `go 1.27` or later, leaving at most one direct and one indirect
  block and preserving existing comment blocks. The first tidy after a version
  bump therefore produces a structural `go.mod` diff that is not a dependency
  change; preview it and describe it as such rather than folding it into a
  dependency increment.

## Toolchain

- Keep the declared `toolchain` directive authoritative. Recommend, but do not
  silently change, a toolchain version.
- Use the project's adopted build and generate commands; do not substitute a
  different toolchain invocation.
- The `go` command dropped support for the `bzr` version control system in Go
  1.27. A dependency resolved over `bzr` no longer fetches and is a blocking
  finding for a toolchain upgrade, not a modernization.

## Removed GODEBUG settings are an upgrade gate

From Go 1.27 the `go` command reads removed `GODEBUG` settings — `godebug`
lines in `go.mod` and `//go:debug` comments in source — and accepts them only
at their final default value. An old value fails the build rather than being
ignored, at load time and with an exact message:

```text
go: error loading go.mod:
go.mod:13: removed GODEBUG "asynctimerchan" set to old value "1" (https://go.dev/doc/godebug#go-127)
```

Audit `godebug` lines and `//go:debug` comments before recommending a bump to
Go 1.27. The settings removed in that release are `asynctimerchan`,
`gotypesalias`, `tls10server`, `tls3des`, `tlsrsakex`, `tlsunsafeekm` and
`x509keypairleaf`. Each pin encodes a behavior the project deliberately held
back; removing the pin restores the current default, which is a behavior change
to verify against the compatibility baseline, and for the TLS and x509 settings
a security posture change owned by `gopher:security`.

## Dependencies

- Follow `modernize.dependency_updates`: `none` proposes no version bump,
  `patch` allows patch-level updates, `minor` allows up to minor updates.
- A dependency update never resolves to an unattended latest version and always
  previews the resulting `go.mod` and `go.sum` diff.
- Verify the build and tests against the compatibility baseline after any
  accepted update, and record the exact before/after versions.
- A standard-library package that lands in a new release can retire a
  dependency outright. Go 1.27 added `uuid` (RFC 9562) and `encoding/json/v2`
  with `encoding/json/jsontext`. Retiring a dependency for a standard-library
  equivalent is a preview-first change like any other, and it is only in scope
  when the declared version provides the package.
