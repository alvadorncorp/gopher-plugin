import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "plugins/gopher/skills/developer/SKILL.md"


class DeveloperPhaseContractTest(unittest.TestCase):
    def test_from_slice_and_micro_review(self):
        document = SKILL.read_text(encoding="utf-8")
        for marker in (
            "from_slice",
            "structure_decision",
            "Micro-review",
            "DETECT PACKAGE ENVELOPE",
            "SELECT FAST PATH",
            "Progressive reference loading",
            "slice_id:",
            "micro_review:",
            "gopher:review",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, document)


if __name__ == "__main__":
    unittest.main()
