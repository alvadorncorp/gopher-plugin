# Doctor Rule Catalog

Ten rules, and only these ten. Each rule states one invariant that is already
known, the evidence that decides it, the owner of the area, and the remediation
route. Rules execute in stable rule-id order so a truncated run is reproducible.

Costs are `metadata` (read a path or a declared value), `parse` (read and parse a
project file), and `subprocess` (invoke an already-available project command).

| Rule id | Owner | Profiles | Cost | Block-eligible | Invariant | Evidence | Remediation | Handoff |
|---|---|---|---|---|---|---|---|---|
| `action.scope-declared` | `gopher:doctor` | quick, standard, strict | metadata | yes | The pending action names the files, packages, or modules it touches, and that scope resolves inside the safe project root | The declared scope and the resolved project root | Declare the scope, or narrow it to paths inside the project root | none — the caller restates the action scope |
| `config.contract-valid` | `gopher:config` | quick, standard, strict | parse | yes | When `.gopher-plugin.toml` exists it parses, uses canonical tables, and declares a supported `schema_version` | `config_status` plus the offending table or key path | Correct the key, or migrate the contract through the `gopher:config` bootstrap flow | `gopher:config` |
| `generated.output-current` | `gopher:codegen` | standard, strict | subprocess | no | Committed generated artifacts match what their declared generator produces from the current inputs | The generator directive, the compared input and artifact identities, and the differing artifact paths | Regenerate through the project's generation entry point and commit the result | `gopher:codegen` |
| `module.go-mod-present` | `gopher:architecture` | quick, standard, strict | metadata | yes | The resolved project root, or each root declared in `project.module_roots`, carries a `go.mod` | The roots searched and the root that lacks the file | Initialize the module, or correct `project.module_roots` | `gopher:architecture` |
| `module.go-sum-consistent` | `gopher:architecture` | standard, strict | subprocess | no | Every requirement in `go.mod` has a matching verified entry in `go.sum` | The verification command, its exit status, and the modules it named | Run the project's tidy and verify flow, then commit the refreshed `go.sum` | `gopher:architecture` |
| `module.replace-policy` | `gopher:architecture` | standard, strict | parse | no | Every `replace` directive is permitted by the effective `architecture.replace_mode` | The directive lines and the effective mode | Remove the directive, or record the mode the project accepts | `gopher:architecture` |
| `test.baseline-known` | `gopher:test-quality` | quick, standard, strict | metadata | no | The project declares a test entry point and the run context records a known baseline result | The declared entry point and the recorded baseline marker, or their absence | Establish and record the baseline through `gopher:test-quality` | `gopher:test-quality`, or `gopher:developer` when the baseline fails on a production defect |
| `toolchain.resolvable` | `gopher:modernize` | strict | subprocess | no | A Go toolchain satisfying the declared `go` and `toolchain` lines is available to the current environment | The declared lines and the reported toolchain version | Select or install the declared toolchain in the environment, or adjust the declaration | `gopher:modernize` |
| `toolchain.version-declared` | `gopher:modernize` | quick, standard, strict | metadata | no | `go.mod` declares an explicit `go` version line, and a `toolchain` line when the project pins one | The declared lines, or the absence of a `go` line | Declare the Go version the project targets | `gopher:modernize` |
| `workspace.membership-consistent` | `gopher:architecture` | strict | parse | no | Every `go.work` `use` path exists, and every discovered module root is either a workspace member or deliberately outside it | The `use` list and its difference against the discovered module roots | Update `go.work`, or update the declared module roots | `gopher:architecture` |

## Block-eligible rules

Three of the ten rules are block-eligible. Each one is cheap, deterministic,
evidence-complete after a single read, and repairable inside the project's own
contract, which is what conditions 3 and 4 of the blocking policy require.

- `action.scope-declared` guards the authorization boundary of the run itself. A
  scope that resolves outside the safe project root leaves the doctor without a
  defensible read boundary, so it blocks and the caller restates the scope.
- `config.contract-valid` decides rule selection. An unparsable or unsupported
  contract makes every later selection untrustworthy, and the remediation is a
  single key in a file the project owns.
- `module.go-mod-present` is the precondition of every module, toolchain, and
  generated-output rule. Without it the rest of the catalog reports on nothing.

## Why the other seven warn

- `module.go-sum-consistent`, `toolchain.resolvable`, and
  `generated.output-current` depend on a subprocess whose availability is
  environmental. Their evidence is complete only when that command runs, so a
  restricted environment turns them into skipped checks rather than blocks.
- `toolchain.resolvable` also fails condition 4: installing or selecting a
  toolchain happens outside the project's own contract.
- `module.replace-policy` and `workspace.membership-consistent` measure a
  topology decision that `gopher:architecture` owns and enforces at its own
  gate; doctor surfaces the drift early.
- `toolchain.version-declared` and `test.baseline-known` describe a missing
  declaration rather than a broken one. Projects raise them to a hard
  requirement through `doctor.required_rules`, which keeps the decision with the
  project.

## Owner and handoff

`Owner` names the canonical specialist of the invariant's area. `Handoff` names
where the finding goes for repair, which is usually the same skill and
occasionally more specific: a failing test baseline caused by a production
defect reaches `gopher:developer` through `gopher:test-quality`. Every finding
carries exactly one owner.
