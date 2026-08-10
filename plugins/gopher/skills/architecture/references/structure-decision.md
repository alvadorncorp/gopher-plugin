# Structure Decision Card

`gopher:architecture` emits a Structure Decision Card whenever `design`,
`module-lifecycle`, or `migration` produces an approved or pending structural
decision that another skill may implement. `triage` may omit the card when it
only routes away from architecture.

## Card schema

    structure_decision:
      decision_id: <stable slug or short id for this decision>
      mode: design | module-lifecycle | migration
      packages_touched: [<import paths or package dirs>]
      public_contract_delta: none | additive | breaking
      architecture_tests_to_add:
        - <command or rule that becomes the gate>
      slices:
        - n: 1
          name: <slice name>
          entry_condition: <observable>
          change: <single structural edit>
          verification: <exact commands>
          compatibility: <consumer guarantee>
          rollback: <exact revert>
          implementer: gopher:developer | gopher:architecture
          approval: granted | pending
      authorization_gate: none | approval-required | blocked
      notes: <optional constraints for implementers>

## Consumer rules

- `gopher:developer` may implement a slice only when `implementer` is
  `gopher:developer`, `approval` is `granted` (or the session already carries
  explicit approval under the active authorization gate), and the change stays
  inside one package with a reversible local API.
- Cross-package or public-contract slices stay with `gopher:architecture`.
- `gopher:refactor` may reference `decision_id` in a handoff record; it does not
  rewrite the card.
- A card without `decision_id`, `packages_touched`, and at least one slice (for
  `migration`) or an explicit empty `slices: []` with a complete `design`
  decision is incomplete.

## When to omit

Omit `structure_decision` only for pure `triage` routing results that hand off
without a structural proposal. For every other successful architecture result,
emit the card, using `slices: []` when the decision is design-only and no
migration slice exists yet.
