import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEVELOPER_SKILL = ROOT / "plugins/gopher/skills/developer/SKILL.md"
REFERENCES = {
    "project-detection": ROOT / "plugins/gopher/skills/developer/references/project-detection.md",
    "idioms": ROOT / "plugins/gopher/skills/developer/references/idioms.md",
    "testing": ROOT / "plugins/gopher/skills/developer/references/testing.md",
    "tooling": ROOT / "plugins/gopher/skills/developer/references/tooling.md",
    "refactoring": ROOT / "plugins/gopher/skills/developer/references/refactoring.md",
}


def text(path):
    return path.read_text(encoding="utf-8")


def assert_order(document, *markers):
    positions = [document.index(marker) for marker in markers]
    if positions != sorted(positions):
        raise AssertionError(f"markers are not ordered: {markers}")


class DeveloperContractTest(unittest.TestCase):
    def test_preflight_resolves_config_and_policy_before_baseline_or_implementation(self):
        document = text(DEVELOPER_SKILL)
        assert_order(
            document,
            "CLASSIFY CONFIG",
            "RESOLVE IDIOM POLICY",
            "RESOLVE TEST WORKFLOW",
            "ESTABLISH FOCUSED BASELINE",
            "IMPLEMENT",
        )

    def test_detection_uses_the_authoritative_preflight_order(self):
        document = text(REFERENCES["project-detection"])
        assert_order(
            document,
            "DETECT ROOT",
            "CLASSIFY CONFIG",
            "RESOLVE IDIOM POLICY",
            "RESOLVE TEST WORKFLOW",
            "DETECT DECLARED GO",
            "DISCOVER COMMANDS AND CONVENTIONS",
        )

    def test_policy_values_resolve_independently_and_legacy_states_use_defaults(self):
        document = text(REFERENCES["project-detection"])
        for marker in (
            "`idiom_policy`",
            "`test_workflow`",
            "session | file | adopted | default",
            "`latest-compatible`",
            "`adaptive-tdd`",
            "ABSENT",
            "MIGRATION_AVAILABLE",
            "without persisting",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, document)

    def test_invalid_and_unsupported_configs_block_production_edits(self):
        document = text(REFERENCES["project-detection"])
        for state in ("INVALID", "UNSUPPORTED_VERSION"):
            with self.subTest(state=state):
                self.assertIn(state, document)
        self.assertIn("read-only diagnosis", document)
        self.assertIn("block production edits", document)

    def test_existing_specialist_owners_remain_named(self):
        document = text(DEVELOPER_SKILL)
        for owner in (
            "gopher:architecture",
            "gopher:concurrency",
            "gopher:performance",
            "gopher:security",
            "gopher:diagnose",
            "gopher:refactor",
            "gopher:complexity",
            "gopher:test-quality",
            "gopher:modernize",
            "gopher:codegen",
            "gopher:fuzz",
            "gopher:cgo",
        ):
            with self.subTest(owner=owner):
                self.assertIn(owner, document)

    def test_owned_references_remain_available(self):
        for name, path in REFERENCES.items():
            with self.subTest(reference=name):
                self.assertTrue(path.is_file())

    def test_idiom_policy_values_and_boundaries_are_explicit(self):
        document = text(REFERENCES["idioms"])
        for marker in (
            "latest-compatible",
            "project-aligned",
            "explicit-only",
            "declared Go version",
            "new or directly changed code",
            "modernize.target_go",
            "gopher:modernize",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, document)

    def test_idiom_policy_semantics_are_distinct(self):
        document = text(REFERENCES["idioms"])
        self.assertIn("newest suitable declared-version idiom", document)
        self.assertIn("nearby adopted conventions", document)
        self.assertIn("only on explicit request", document)

    def test_write_time_forms_follow_the_declared_go_directive(self):
        document = text(REFERENCES["idioms"])
        for marker in (
            "## Write-time forms",
            "modernize/references/language-apis.md",
            "declared `go` directive",
            "Do not invoke `go fix`",
            "`omitzero`",
            "not blind substitutions",
            "new or directly changed code",
            "roster drift",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, document)

    def test_test_workflow_matrix_covers_every_change_class(self):
        document = text(REFERENCES["testing"])
        for workflow in ("adaptive-tdd", "strict-tdd", "test-after"):
            with self.subTest(workflow=workflow):
                self.assertIn(workflow, document)
        for change_class in ("Behavior or bug fix", "Behavior-preserving refactor", "Mechanical change", "Test-only change"):
            with self.subTest(change_class=change_class):
                self.assertIn(change_class, document)

    def test_tdd_signals_and_exceptions_are_attributable_and_ordered(self):
        testing = text(REFERENCES["testing"])
        skill = text(DEVELOPER_SKILL)
        for marker in ("attributable red signal", "assertion failure or compile failure", "never an unrelated failure", "passing characterization", "recorded test-first exception", "Block production edits", "Implement first, then add or update behavior tests", "same focused command must turn green", "explicit reason"):
            with self.subTest(marker=marker):
                self.assertIn(marker, testing)
        assert_order(
            skill,
            "**ESTABLISH FOCUSED BASELINE**",
            "**CLASSIFY CHANGE**",
            "**COLLECT FIRST SIGNAL**",
            "**IMPLEMENT**",
            "**CONFIRM GREEN**",
            "**REFACTOR WHILE GREEN**",
            "**FINAL VALIDATION**",
        )

    def test_workflow_evidence_and_refactoring_safety_are_explicit(self):
        tooling = text(REFERENCES["tooling"])
        refactoring = text(REFERENCES["refactoring"])
        for marker in ("exact command", "exit status", "concise observation", "skip reason", "non-applicable"):
            with self.subTest(marker=marker):
                self.assertIn(marker, tooling)
        assert_order(refactoring, "RESOLVE EFFECTIVE CONFIG", "FOCUSED BASELINE", "CHARACTERIZATION SAFETY NET", "LOCAL REVERSIBLE REFACTOR")
        self.assertIn("passing characterization", refactoring)
        self.assertIn("before mutation", refactoring)

    def test_developer_output_contract_contains_complete_evidence_shape(self):
        document = text(DEVELOPER_SKILL)
        for marker in (
            "status: COMPLETE | COMPLETE_WITH_LIMITATIONS | BLOCKED",
            "config_status: ABSENT | VALID | MIGRATION_AVAILABLE | INVALID | UNSUPPORTED_VERSION",
            "declared_go:",
            "idiom_policy:",
            "value: latest-compatible | project-aligned | explicit-only",
            "source: session | file | adopted | default",
            "test_workflow:",
            "value: adaptive-tdd | strict-tdd | test-after",
            "requested_behavior:",
            "change_class: behavior | bug-fix | refactor | mechanical | test-only",
            "baseline_status: passing | failing | not-run",
            "test_evidence:",
            "pre_change:",
            "first_signal:",
            "kind: red | characterization | test-after | exception | not-applicable",
            "command:",
            "observed:",
            "reason:",
            "green:",
            "refactor:",
            "authorization_gate: none | approval-required | blocked",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, document)


if __name__ == "__main__":
    unittest.main()
