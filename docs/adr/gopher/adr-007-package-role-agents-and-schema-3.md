---
type: adr
id: adr:gopher:007
context: gopher
title: Package three role agents and migrate the project contract to schema 3
status: Accepted
tags: [go, plugins, agents, config, packaging, claude, codex, grok, kimi]
deciders: [Alvadorncorp]
date: 2026-08-05
---
# ADR-007: Package three role agents and migrate the project contract to schema 3

## Context and Problem

The package shipped twenty skills and nothing else. Every one of the eight
harness adapters under `skills/review/references/harnesses/` and
`skills/refactor/references/harnesses/` ends its fifth step the same way: inherit
the session model when per-task model controls are unavailable, and report the
limitation.

That sentence is an accurate description of a gap, not a design. When
`gopher:review` fans out one reviewer per selected lens, or `gopher:refactor`
delegates a dimension to its canonical owner, each child runs on whatever model,
reasoning effort, and tool set the ambient session happened to carry. A read-only
reviewer and a mutating implementer are dispatched with identical capability. The
prohibition that the reviewer applies no fix is prose in a prompt, and the only
thing standing between it and an edit is the child's compliance.

An adapter cannot close this. An adapter is text the controller reads at run
time; the capability envelope is decided by the host when it loads a definition.
Nothing in the package participated in that moment.

`adr:gopher:001` records that a future ownership change must be recorded in a new
ADR, and `adr:gopher:005` records that a change to the configuration schema needs
its own ADR. Both obligations are discharged here.

## Decision Drivers

- One authoritative binding per role, decided by the package rather than by the
  ambient session.
- No new owner and no new orchestrator. `adr:gopher:001` rejected a hub, and
  `adr:gopher:002` fixed the orchestrator count at two.
- Honest reporting over silent pretence: a declared policy the host cannot apply
  is reported as declared, never as applied.
- One physical tree with hand-maintained per-host variants, as
  `docs/sdd/gopher/gopher_plugin.md` requires. No generated trees, no symlinks.
- Kimi Code must not be left with a silently weaker envelope than the other three
  hosts.

## Considered Options

### Option 1: Three role agents as thin skill wrappers, plus schema 3 (chosen)

Package `developer`, `architect`, and `reviewer` as markdown agents for Claude
Code and Grok Build and as TOML agents for Codex. The markdown dialect carries a
fixed model, a fixed reasoning effort, and a fixed tool set. The Codex agent
dialect accepts `name`, `description`, `sandbox_mode`, and
`developer_instructions` and nothing else, so a Codex agent binds the sandbox and
binds neither a model nor a reasoning effort. Every agent in both dialects
carries a constraint envelope and delegates the workflow to the skill it wraps.
Add an `[agents]` table to the project contract as a declared policy.

**Pros:** the binding lands where the host reads it; the skill keeps its
workflow, evidence discipline, and output schema unchanged; the envelope for the
architect is partly machine-enforced rather than only stated; per-project policy
lives in the contract that already carries per-project policy.

**Cons:** six hand-maintained files across two dialects, and a declared policy
whose model and effort halves are reportable but not applicable.

### Option 2: Three role agents plus seven lens-child agents

Package a definition for each review lens as well, so every reviewer child
carries its own binding.

**Pros:** closes the inherited-model limitation for the lens children too.

**Cons:** ten definitions to keep in parity across two dialects. A lens child
already receives its full contract from the immutable bundle plus exactly one
lens reference, so a packaged definition would add a binding and nothing else,
while multiplying the surface that can drift. Revisit only if a lens shows a
measurable need for a binding of its own.

### Option 3: No packaged agents; strengthen the harness adapters

Write the envelope more forcefully into the eight adapter files.

**Pros:** no new component type, no schema change, no ADR obligation.

**Cons:** an adapter is prose the controller may follow. The binding gap is
precisely what prose cannot close, because the host has already decided the
capability before the controller reads anything.

### Option 4: Ship the agents, document the policy outside the contract

Keep `.gopher-plugin.toml` closed at ten canonical tables and document agent
policy in the agents' own references.

**Pros:** no schema migration.

**Cons:** rejected on the same ground `adr:gopher:006` rejected for `[doctor]`,
`[fuzz]`, and `[architecture]`. Whether a repository wants the roster enabled, how
wide the review window may open, and how an authorization gate resolves are
per-project policy, and policy set outside the contract cannot be set once for a
repository.

### Option 5: Make `[agents]` authoritative and rebind at run time

Let the project contract decide the model, effort, and tools, and have each agent
reconfigure itself when it starts.

**Pros:** one place to decide policy.

**Cons:** impossible and dishonest. The host reads the definition at load time,
so a run-time rebinding would be a claim about a capability the agent does not
have. Rejected outright.

## Decision

**Chosen option: three packaged role agents as thin skill wrappers, and a
migration of the project contract to schema version 3.**

### Roster and bindings

Names are bare and match the roles rather than the skills: `developer`,
`architect`, and `reviewer`. Each agent's body delegates to `gopher:developer`,
`gopher:architecture`, and `gopher:review` respectively. The body carries the
constraint envelope and may name a mode or a gate value as part of that envelope;
the workflow, the evidence discipline, and the output schema stay in the skill.

The model, effort, and capability columns below describe the markdown dialect.
The Codex dialect has no model key and no effort key, so a Codex agent binds the
sandbox column alone and inherits the session's model and reasoning effort.

| Agent | Model | Effort | Capability | Codex sandbox |
|---|---|---|---|---|
| `developer` | `sonnet` | `medium` | `Read, Grep, Glob, Edit, Write, Bash` | `workspace-write` |
| `architect` | `opus` | `high` | `Read, Grep, Glob, Bash, Edit` | `read-only` |
| `reviewer` | `opus` | `high` | denies `Edit`, `Write`, `NotebookEdit` | `read-only` |

`developer` is the highest-volume role and works inside one package on reversible
changes, with the skill supplying the judgment; work that needs deeper reasoning
trips the authorization gate and hands off instead. `architect` and `reviewer`
make the least reversible and the most consequential judgments in the package.

### The tool decisions and what each one buys

`architect` holds `Edit` and deliberately does not hold `Write`. A subagent has
no channel to the user, so the wrapped skill's "obtain explicit approval" gate
collapses to a handback. Withholding `Write` removes the direct route to
creating a package, module, or workspace member, but it does not close the
constraint: `Bash` can create a file, and `Bash` cannot be withheld because the
skill's stop condition is an executable architecture gate. So "creates no file"
is a host guarantee only on Codex, where the sandbox is read-only, and rests on
the agent's own instruction on Claude Code and Grok Build. Withholding `Write`
still narrows the surface and costs nothing the role needs.

`reviewer` is the one role bound by a deny-list. Its contract combines a
prohibition — it applies no fix of any kind — with an open requirement: it must
fan out through whatever dispatch primitive the host provides, and that primitive
is named differently on each host. An allow-list would have to name one of them
and would silently degrade the reviewer to a sequential single-context review on
the others, which is the failure the review design exists to prevent. The
residual risk is recorded rather than hidden: `Bash` survives the deny-list and
can write, through a redirect, `tee`, an in-place editor, or `git apply`. Three
things bound it, and each is worth stating at its true scope rather than as a
stack. The Codex `read-only` sandbox is a host guarantee, and it covers Codex
alone. The agent's own instruction covers the other two hosts, and it is prose —
the same mechanism Option 3 was rejected for, so it is a mitigation and not a
control. The rule that a changed diff invalidates the verdict is keyed to the
base and head SHAs the review controller captures, so it catches a committed
change and does not fire on an uncommitted working tree, which is the common
review target. A per-agent command allowlist would close this; no host offers
one today.

`developer` holds no dispatch capability at all. A leaf worker that could
delegate would rebuild the hub `adr:gopher:001` rejected and would put two
`primary_owner` values in one request.

Codex exposes one coarse sandbox switch instead of a per-tool set, so the Codex
`architect` is `read-only` and cannot execute a slice, which is stricter than the
binding it carries on the other hosts. Keeping the Codex floor at or below the
Claude floor is the safe direction of that asymmetry.

### Per-host packaging

Claude Code and Grok Build load `plugins/gopher/agents/*.md` by convention. Codex
loads `plugins/gopher/agents/codex/*.toml`. Kimi Code discards packaged plugin
agents silently, so no manifest declares them, a test asserts their absence from
both Kimi manifests, and the Kimi review and refactor adapters restate the
constraint envelope inline as instruction text with no binding behind it: the
review adapter dispatches through the runtime `Agent` and `AgentSwarm` tools, and
the refactor adapter through `Agent`. That duplication is deliberate: no skill
holds a relative path into a peer.

### Configuration

`.gopher-plugin.toml` moves to `schema_version = 3` with one added canonical
table, `[agents]`, carrying `enabled`, a model and effort key per role,
`reviewer_max_parallel`, `authorization`, and `policy_divergence`. Version `1`
and version `2` files keep working and report `MIGRATION_AVAILABLE`; a table the
current schema adds is simply absent from an older file, and that absence is
never an unknown key.

The invariant that governs the whole table: the shipped definition is the
authoritative binding, because the host reads it at load time and no project file
can rebind it. The table is the project's declared policy. It may narrow an agent
and it can never widen one, and a declared value is never presented as an applied
one. `enabled`, `reviewer_max_parallel`, `authorization`, and `policy_divergence`
are enforceable by the agent itself; the model and effort keys are declared and
reported only. `inherit-session` never grants a capability the packaged binding
withheld.

Every agent reports one `policy_status` alongside its skill's own output:
`NOT_CONFIGURED` when the contract declares no table, `ALIGNED`, `DIVERGED` with
the difference field by field, `UNVERIFIABLE` when the host exposes no way to
observe the active binding, and `BLOCKED_BY_POLICY` when the roster is disabled
or a divergence exists under `policy_divergence = "block"`.

`gopher:doctor` gains one rule, `agents.policy-declared`, which is not
block-eligible. It checks that the declaration is self-consistent and nothing
more: the packaged bindings live in the host's plugin installation, outside the
safe project root that doctor resolves, so the applied-versus-declared comparison
stays a run-time `policy_status` and never becomes a readiness finding.

### What this does not change

This adds no owner and no orchestrator. Each agent's `primary_owner` remains the
skill it wraps, and `gopher:review` and `gopher:refactor` remain the only two
bounded orchestrators of `adr:gopher:002`.

## Consequences

**Positive:**

- Delegating a review or a bounded implementation now carries a deterministic,
  capability-restricted envelope instead of an inherited one.
- The architect's file-creation constraint is a host guarantee on Codex and is
  narrowed, though not closed, on the other hosts by withholding `Write`.
- Per-project agent policy lives in the one contract that already carries project
  policy, and every value it declares is either enforced or honestly reported.
- The thin-wrapper shape has a structural gate. That gate is a bounded guarantee
  and not a proof of non-duplication: it rejects the wrapped skill's section
  headings and three of its field labels, and it caps the body size. An agent
  that pastes a whole workflow under a heading the gate does not name would pass
  it, so the shape still depends on review.

**Negative:**

- Six hand-maintained agent files across two dialects join the manifests already
  kept in parity by hand.
- The inherited-model gap this ADR exists to close stays open on Codex. That
  dialect exposes no model key and no effort key, so a Codex `developer`,
  `architect`, or `reviewer` still runs on whatever model and reasoning effort
  the session carries. Only the capability half of the envelope lands there,
  through `sandbox_mode`. Closing it needs a Codex dialect that accepts a
  per-agent model, and that is outside this package.
- The declared model and effort are reportable but never applicable. The contract
  therefore carries values whose only effect is a report, which is a documented
  asymmetry rather than a hidden one.
- `schema_version = 3` makes both version-1 and version-2 files
  `MIGRATION_AVAILABLE`, so a project that pins the schema sees the new state.
- Kimi Code carries the constraint envelope as duplicated prose in two adapters,
  which must be kept in step with the agent files. A test asserts the duplication
  exists; only review keeps it accurate.

**Neutral / Follow-up actions:**

- Record further roster or schema changes in a new ADR.
- Revisit packaged lens-child agents only if a lens shows a measurable need for a
  binding of its own.
- The release version for this phase is `0.4.0`; every plugin manifest and every
  versioned marketplace catalog already carries it.
