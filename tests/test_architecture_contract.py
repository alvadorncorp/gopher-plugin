import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "plugins/gopher/skills/architecture/SKILL.md"
CARD = ROOT / "plugins/gopher/skills/architecture/references/structure-decision.md"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class ArchitectureContractTest(unittest.TestCase):
    def test_modes_include_triage_and_card_reference(self):
        document = text(SKILL)
        for marker in (
            "`triage`",
            "`design`",
            "`module-lifecycle`",
            "`migration`",
            "structure_decision",
            "references/structure-decision.md",
            "gopher:application-architecture",
            "machine-checkable architecture gate",
            "always read-only",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, document)

    def test_structure_decision_reference_schema(self):
        document = text(CARD)
        for marker in (
            "decision_id",
            "public_contract_delta",
            "implementer: gopher:developer | gopher:architecture",
            "gopher:developer",
            "gopher:refactor",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, document)

    def test_description_has_planning_triggers_and_anti_triggers(self):
        head = text(SKILL).split("---", 2)[1]
        self.assertIn("during planning", head)
        self.assertIn("gopher:developer", head)
        self.assertIn("gopher:review", head)


if __name__ == "__main__":
    unittest.main()
