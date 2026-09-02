import unittest
from pathlib import Path

import validate_repo


ROOT = Path(__file__).resolve().parents[1]


class DocumentationTest(unittest.TestCase):
    def test_sdd_records_schema_five_workflow_policy_and_evolution(self):
        text = (ROOT / "docs/sdd/gopher/gopher_plugin.md").read_text(encoding="utf-8")
        required = (
            "adr:gopher:008",
            "adr:gopher:009",
            "schema version `5`",
            "Versions `1`–`4` remain `MIGRATION_AVAILABLE`",
            "gopher:developer",
            "adaptive-tdd",
            "migration",
            "Phase 8",
            "Phase 9",
            "[workflow]",
        )
        for value in required:
            self.assertTrue(value in text, f"SDD is missing {value!r}")

    def test_readme_documents_identity_skills_and_install_flows(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        required = (
            "# Gopher Plugin", "## Skills and ownership", "## Install locally in Codex",
            "## Install locally in Claude Code", "## Install locally in Grok Build",
            "## Install locally in Kimi Code", "gopher@alvadorncorp", "--mode full",
            "## Install in OpenCode", "@alvadorncorp/gopher", "gopher-reviewer",
            "## Install locally in omp",
            "omp binds no packaged agent model, effort, or tool restriction",
            "does not apply a `gopher:`\nnamespace",
            "All repository documentation is written in English.",
            "## Agents", "plugins/gopher/agents/",
            "Kimi Code does not load packaged plugin agents",
            "policy_status",
            "It may narrow an agent and it can never widen one.",
            "schema version `5`",
            "[developer]",
            "[workflow]",
            "idiom_policy",
            "test_workflow",
            "post_implementation_review",
            "latest-compatible",
            "adaptive-tdd",
            "MIGRATION_AVAILABLE",
            "config --bootstrap",
            "ships no user-triggered hooks",
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
