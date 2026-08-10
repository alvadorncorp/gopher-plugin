import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "plugins/gopher/skills/refactor/SKILL.md"
CONTROLLER = ROOT / "plugins/gopher/skills/refactor/references/controller.md"
REPORTS = ROOT / "plugins/gopher/skills/refactor/references/reports.md"


class RefactorContractTest(unittest.TestCase):
    def test_plan_mode_and_terminal(self):
        skill = SKILL.read_text(encoding="utf-8")
        for marker in (
            "`plan`",
            "`remediate`",
            "PLAN_READY",
            "refactor_plan",
            "Do not use for package/module",
            "local reversible refactors",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, skill)

    def test_controller_stops_plan_before_mutation(self):
        text = CONTROLLER.read_text(encoding="utf-8")
        self.assertIn("Scope preflight", text)
        self.assertIn("PLAN_READY", text)

    def test_reports_define_backlog(self):
        text = REPORTS.read_text(encoding="utf-8")
        self.assertIn("PLAN_READY", text)
        self.assertIn("refactor_plan", text)
        self.assertIn("dimension:", text)


if __name__ == "__main__":
    unittest.main()
