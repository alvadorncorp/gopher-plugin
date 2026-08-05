# Overrides

An override lets a project accept a known finding for a bounded time without
losing sight of it. It is declared in the project contract, it is read from
`gopher:config`, and it changes one thing only: the disposition of a single
rule, from `deny` to `warn`.

## Shape

`[[doctor.overrides]]` is an array of tables. It is absent from the default
template; entries are added deliberately.

```toml
[[doctor.overrides]]
rule = "module.replace-policy"
until = "2026-03-31"
reason = "Local replace kept while the shared client module is extracted."
```

| Field | Type | Requirement |
|---|---|---|
| `rule` | string | A rule id present in `references/rules.md` |
| `until` | string | An ISO-8601 date; the override applies through that date |
| `reason` | string | Non-empty text stating why the finding is accepted |

All three fields are required. An entry names exactly one rule, so accepting two
rules takes two entries.

## What an override changes

A valid, unexpired override downgrades a `deny` disposition to `warn` for its
rule. The run continues, the finding stays in `findings` with its original
evidence, and the entry appears in `override_summary` with its rule, its expiry,
and its reason.

An override therefore changes the terminal state only through aggregation: a run
whose sole blocking finding is downgraded reports `WARN` instead of `BLOCKED`.

## What an override preserves

Two properties hold for every override, valid or otherwise:

- The original finding stays in the evidence. An override records an accepted
  risk; it never deletes the observation, the rule id, the owner, or the
  remediation. A reader of the bundle sees exactly what would have blocked.
- An authorization boundary stays where it is. An override never grants a
  write, a network probe, a credential read, a tool installation, or any scope
  outside the safe project root. Those gates are decided by the authorization
  rules in `SKILL.md`, and configuration does not relax them.

An override also leaves the check itself untouched: the rule still runs, still
collects its evidence, and still names its owner and handoff.

## Expiry

`until` is compared against the run's own date. An override applies through the
end of the date it names.

| Condition | Result |
|---|---|
| `until` is today or later | The override applies; the finding is downgraded to `warn` |
| `until` is in the past | The override is expired; the finding keeps its original disposition |
| `until` is missing or unparsable | The override is malformed; the finding keeps its original disposition |

An expired override is reported in `override_summary` with its expiry date, so a
project sees why a previously accepted finding started blocking again. Renewing
one is an explicit contract edit through `gopher:config`.

## Malformed entries

An entry is malformed when a required field is absent, when `rule` names no rule
in the catalog, when `until` is not an ISO-8601 date, or when `reason` is empty.

A malformed entry is ignored for disposition purposes and reported in
`override_summary` with the reason it was ignored. The rest of the array still
applies, and the run continues: one bad entry costs its own effect and nothing
more. A contract whose `[[doctor.overrides]]` array cannot be parsed at all is a
`config.contract-valid` finding, owned by `gopher:config`.
