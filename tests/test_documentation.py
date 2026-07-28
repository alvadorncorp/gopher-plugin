import unittest
from pathlib import Path

import validate_repo


ROOT = Path(__file__).resolve().parents[1]


class DocumentationTest(unittest.TestCase):
    def test_readme_documents_identity_skills_and_both_install_flows(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        required = (
            "# Gopher Plugin", "## Skills and ownership", "## Install locally in Codex",
            "## Install locally in Claude Code", "## Install locally in Grok Build",
            "gopher@alvadorncorp", "--mode full",
            "All repository documentation is written in English.",
        )
        self.assertTrue(all(value in text for value in required))

    def test_license_is_mit_for_project_author(self):
        text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("MIT License", text)
        self.assertIn("Copyright (c) 2026 Igor Sant'Ana @ Alvadorn Corp", text)

    def test_all_repository_markdown_passes_english_gate(self):
        errors = [error for error in validate_repo.validate_repository() if "documentation must be English" in error]
        self.assertEqual([], errors)


if __name__ == "__main__":
    unittest.main()
