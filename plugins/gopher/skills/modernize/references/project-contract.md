# Project contract

Modernization is bounded by what the project already declares. Read the contract
before proposing any change.

## Declared inputs

- Go version: the version declared in `go.mod` (and the `toolchain` directive
  when present). This is the compatibility floor and, with `declared`, the
  ceiling.
- Active toolchain version (`go version`): distinct from the declared version.
  A version manager pin (asdf, `.tool-versions`, `gvm`) can make the two
  disagree. Below Go 1.26, the `go fix` modernizer is unavailable regardless of
  what `go.mod` declares — that Go version's `go fix` is a different, older
  tool (`references/tooling.md`).
- Module and workspace structure: `go.mod`, any `go.work`, and the module roots
  from `[project]`.
- Adopted commands: the project's build, test, lint, and generate commands.

## Policy semantics

- `target_go = "declared"`: keep the declared version. Recommend or apply only
  changes that compile and pass under it. A version bump is out of scope here and
  is a separate, explicitly approved decision.
- `target_go = "<version>"`: an explicit target the operator has chosen; still
  preview first and verify against a baseline built on that target.
- `apply_fixes = false`: produce a preview and stop. Application requires an
  explicit opt-in.
- `dependency_updates`: `none`, `patch`, or `minor`. It never resolves to an
  unattended latest version.

Record the declared versions and the resolved target with the result so a
reviewer can reproduce the scope.
