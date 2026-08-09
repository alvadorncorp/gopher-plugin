import unittest
from pathlib import Path

import validate_repo


ROOT = Path(__file__).resolve().parents[1]


class DocumentationTest(unittest.TestCase):
    def test_sdd_records_schema_four_developer_policy_and_evolution(self):
        text = (ROOT / "docs/sdd/gopher/gopher_plugin.md").read_text(encoding="utf-8")
        required = (
            "adr:gopher:008",
            "schema version `4`",
            "Versions `1`–`3` remain `MIGRATION_AVAILABLE`",
            "gopher:developer",
            "adaptive-tdd",
            "migration",
            "Phase 8",
        )
        for value in required:
            self.assertTrue(value in text, f"SDD is missing {value!r}")

    def test_readme_documents_identity_skills_and_both_install_flows(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        required = (
            "# Gopher Plugin", "## Skills and ownership", "## Install locally in Codex",
            "## Install locally in Claude Code", "## Install locally in Grok Build",
            "## Install locally in Kimi Code", "gopher@alvadorncorp", "--mode full",
            "All repository documentation is written in English.",
            "## Agents", "plugins/gopher/agents/",
            "Kimi Code does not load packaged plugin agents",
            "policy_status",
            "It may narrow an agent and it can never widen one.",
            "schema version `4`",
            "[developer]",
            "idiom_policy",
            "test_workflow",
            "latest-compatible",
            "adaptive-tdd",
            "MIGRATION_AVAILABLE",
            "config --bootstrap",
        )
        for value in required:
            # assertIn would dump the whole README on failure; name the string instead.
            self.assertTrue(value in text, f"README is missing {value!r}")

    def test_license_is_mit_for_project_author(self):
        text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("MIT License", text)
        self.assertIn("Copyright (c) 2026 Igor Sant'Ana @ Alvadorn Corp", text)

    def test_all_repository_markdown_passes_english_gate(self):
        errors = [error for error in validate_repo.validate_repository() if "documentation must be English" in error]
        self.assertEqual([], errors)


if __name__ == "__main__":
    unittest.main()
