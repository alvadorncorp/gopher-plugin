# Go Modules and Workspaces

One module is the default. This reference carries the `module-lifecycle` mode of
`gopher:architecture`: creating, splitting, merging, and retiring modules,
`go.work` membership, `replace` directives, and release grouping. Every operation
below names the `go` commands that actually carry it, and every module-topology
change is a public-contract change under the skill's approval gate.

## A package, or a second module

A package is enough while the code ships on one version line, under one
dependency policy, from one release, owned by one team. Splitting inside a single
module is cheap: import paths inside the module change, consumers outside it stay
untouched.

A second module earns its permanent cost when at least one of these is real and
durable:

- an independent version line, so this code can release a breaking change while
  the rest stays still;
- a separate release cadence or a separate release owner;
- a dependency set that must stay isolated, so a heavy or risky requirement stops
  at this boundary instead of reaching every consumer;
- independent consumption: someone imports this code without the rest of the
  repository.

Counter-signals: a folder that only wants a shorter import path, a desire to
"enforce" a boundary that `internal/` already enforces, or a split proposed
before any consumer exists. Record the chosen justification; a module without one
is a versioning obligation with no payer.

## Creating a module

```sh
go mod init example.com/org/repo/component   # inside the new module directory
go mod tidy                                  # resolve its own requirement set
go work use ./component                      # local development only
go build ./... && go test ./...
```

State from the start: the import path, the initial version (`v0` while the API
moves, `v1` once it is promised), the CI entry that builds and tests it, and its
direction of dependency against every existing module.

## Splitting a module

A split moves packages out of an existing module into a new one, so every moved
package changes import path for every consumer. Sequence it:

1. Choose the new module path and confirm no consumer already uses it.
2. Move the packages, `go mod init` the new module, and let the old module
   require the new one, keeping the dependency direction one-way and acyclic.
3. Keep a forwarding entry point in the old module for the migration window: an
   exported alias, wrapper, or type alias that delegates to the new path and
   carries a `// Deprecated:` comment naming the replacement.
4. Release the new module first, then the old module's release that requires it.
5. Migrate consumers in bounded batches, then remove the forwarding path in a
   separate, separately approved release.

```sh
go mod init example.com/org/repo/component
go mod edit -require=example.com/org/repo/component@v0.1.0
go mod tidy
go list -m all              # confirm the resolved graph
go build ./... && go test ./...
```

### The `v2+` major-version suffix rule

Module paths at major version 2 and above carry the major version as a path
suffix: `example.com/org/repo/v2`. Versions `v0` and `v1` carry no suffix. The
suffix is part of the import path, so a `v2` release is a new import path and old
and new majors can coexist in one build — that coexistence is what makes an
incremental consumer migration possible.

```sh
go mod edit -module=example.com/org/repo/v2   # then update every internal import
go mod tidy
go build ./... && go test ./...
git tag v2.0.0                                # or sub/dir/v2.0.0 for a nested module
```

Two layouts are available: a `v2/` subdirectory inside the same branch, or a
major-version branch. Pick one per module and record it, so the release tooling
and the tag format stay predictable.

### Staged deprecation

Deprecation is a schedule, not a comment. Publish, in order: the replacement, the
`// Deprecated:` marker naming that replacement, the migration guide, the window
end date, and finally the removal release. Keep the old symbol working and tested
for the whole window.

## Merging modules back

A merge is the split in reverse and is usually cheaper, because consumers of the
absorbed module keep importing a path that keeps resolving until the final
release. Fold the packages into the surviving module, drop the requirement and
any local `replace`, drop the workspace entry, then retire the absorbed module.

```sh
go mod edit -dropreplace=example.com/org/repo/component
go mod edit -droprequire=example.com/org/repo/component
go work edit -dropuse=./component
go mod tidy
go build ./... && go test ./...
```

Consumers still on the absorbed path need the retirement path below: a final
release that deprecates the module and points at the surviving import path.

## Retiring a module

Retirement is a published event, so it needs a release of its own:

1. Mark the module deprecated with a `// Deprecated: <replacement>` comment
   directly above the `module` line in its `go.mod`. The comment reaches users
   through `go list -m -u` and the module proxy.
2. Add `retract` directives for versions that should stop being selected. A
   retraction lives in the retiring module's own `go.mod` and only becomes
   visible once a *newer* version carrying it is published.
3. Publish that final release. It is the last version of the module and it is the
   one that carries both the deprecation marker and the retractions.
4. Leave the published versions in place. Existing builds keep resolving; the
   markers steer new work toward the replacement.

```sh
go mod edit -retract=v1.4.0
go mod edit -retract=[v1.0.0,v1.3.9]
go mod tidy
git tag v1.4.1                # the final release that publishes the retractions
go list -m -retracted all     # confirm what consumers will now see
```

Use `retract` for versions that are unsafe or published in error, and the
deprecation marker for the module as a whole.

## Workspaces (`go.work`)

A workspace is a local development tool rather than a published contract.
`go.work` changes build resolution only on the machine that holds the file;
everyone who imports the modules resolves them through each module's own
`go.mod`. Keep the workspace out of the release path and verify every module
without it before publishing.

```sh
go work init ./api ./component
go work use ./newmodule
go work edit -dropuse=./component
go work sync                        # push workspace-resolved versions into each go.mod
GOWORK=off go build ./... && GOWORK=off go test ./...   # prove the published contract
```

`GOWORK=off` is the check that separates a real requirement graph from a
workspace-only success: code that builds only inside the workspace has a missing
or stale `require` in some `go.mod`.

Under `workspace_mode`:

- `off` — leave workspace layout out of the proposal and resolve every module
  through its own `go.mod`.
- `advisory` — recommend a workspace for multi-module local development and state
  the benefit; the project decides.
- `required` — every module in scope is a `go.work` member, and the lifecycle
  change includes the `go work use` or `go work edit` step that keeps it so.

Under `tidy_mode`, `off` leaves the requirement set as found, `advisory` proposes
`go mod tidy` and shows its effect with `go mod tidy -diff`, and `required` makes
a tidy module graph part of the slice: the slice is complete when re-running
`go mod tidy` leaves every touched module unchanged, so one tidy that writes
inside the slice is part of the slice rather than a failure of it.

The first tidy after a module declares `go 1.27` writes even when the
requirement set is unchanged: from that version `go mod tidy` merges duplicate
`require` blocks, leaving at most one direct and one indirect block and
preserving existing comment blocks. A module declaring `go 1.26` keeps its
blocks as written, so the reformat lands exactly once, on the slice that raises
the directive.

That reformat adds and drops no requirement and moves no selected version, so it
stays inside the slice and needs neither a separate slice nor its own approval.
Give it its own entry in the slice `change:` field with the `require` block count
before and after, so a reviewer reading the `go.mod` diff does not classify it as
a dependency change.

## `replace` directives and `replace_mode`

A `replace` directive in a published module applies to builds of that module
itself and stays inert for anyone who imports it. That asymmetry is the whole
reason `local-only` is the sane default: a `replace` is a fine way to point at a
sibling checkout during development and a poor way to express a dependency
decision, because consumers resolve the original path regardless.

| `replace_mode` | What a lifecycle change may introduce |
|---|---|
| `forbid` | Requirements only. Every dependency is expressed through `require` and a published version |
| `local-only` | Local filesystem replacements for sibling modules under active development, removed before release |
| `allow` | Any replacement the project declares, each with a recorded reason and removal condition |

```sh
go mod edit -replace=example.com/org/repo/component=../component
go mod edit -dropreplace=example.com/org/repo/component
go list -m all              # what the current build actually resolves
go mod verify               # checksums for the downloaded modules
```

Prefer a workspace over a committed local `replace`: `go.work` achieves the same
local wiring and stays out of the published `go.mod`. Before any release, drop
every local replacement and re-run the build and tests with `GOWORK=off`.

## Release grouping and `release_mode`

`release_mode = "independent"`: each module carries its own version line and
releases when its own changes justify it. Cross-module changes release in
dependency order — the dependency first, then the dependent's release that
requires the new version. Expect brief windows where the repository holds a
module already released and a module about to be.

`release_mode = "grouped"`: modules move together to the same version and release
as one set, including modules with no change of their own. Grouping buys a single
comprehensible version for consumers and pays for it with version churn. Order
inside the group still follows the dependency graph.

Either way, a release step names: the modules and tags involved, the tag format
(`vX.Y.Z` at the root, `sub/dir/vX.Y.Z` for a nested module), the order, the
verification (`go build ./...`, `go test ./...`, `go list -m all`, `GOWORK=off`),
and how to respond if a tag is published in error — a new version plus a
`retract`, since a published version is permanent.

Official sources: <https://go.dev/ref/mod>,
<https://go.dev/doc/tutorial/workspaces>, <https://go.dev/blog/v2-go-modules>.
Last verified: 2026-08-31 against a local go1.27.0 toolchain.
