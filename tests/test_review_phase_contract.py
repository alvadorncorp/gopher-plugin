import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "plugins/gopher/skills/review/SKILL.md"
CONSOL = ROOT / "plugins/gopher/skills/review/references/consolidation.md"


class ReviewPhaseContractTest(unittest.TestCase):
    def test_auto_delta_fix_queue(self):
        skill = SKILL.read_text(encoding="utf-8")
        for marker in (
            "`--mode auto`",
            "`--mode delta`",
            "Heuristic lens table",
            "fix_queue",
            "parent_review_id",
            "never apply fixes",
            "after a local implementation",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, skill)

    def test_consolidation_mentions_fix_queue(self):
        text = CONSOL.read_text(encoding="utf-8")
        self.assertIn("Fix queue", text)


if __name__ == "__main__":
    unittest.main()
