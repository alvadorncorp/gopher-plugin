import json
import tomllib
import unittest
from pathlib import Path

import validate_repo


ROOT = Path(__file__).resolve().parents[1]
LAYOUT = json.loads((ROOT / "tests/fixtures/expected-layout.json").read_text(encoding="utf-8"))
SPEC = LAYOUT["agents"]
AGENTS = ROOT / "plugins/gopher/agents"
SCHEMA_DOC = ROOT / "plugins/gopher/skills/config/references/schema.md"
KIMI_ADAPTERS = {
    "review": ROOT / "plugins/gopher/skills/review/references/harnesses/kimi.md",
    "refactor": ROOT / "plugins/gopher/skills/refactor/references/harnesses/kimi.md",
}
OPENCODE_AGENTS = AGENTS / "opencode"


def codex_agent(role: str) -> dict:
    with (AGENTS / "codex" / f"{role}.toml").open("rb") as handle:
        return tomllib.load(handle)


class PackagedAgentTest(unittest.TestCase):
    def test_agent_contract_reports_no_errors(self):
        self.assertEqual([], validate_repo.validate_agents(LAYOUT))

    def test_agents_are_thin_skill_wrappers(self):
        for role, skill_id in SPEC["skill_ids"].items():
            markdown = (AGENTS / f"{role}.md").read_text(encoding="utf-8")
            codex = (AGENTS / "codex" / f"{role}.toml").read_text(encoding="utf-8")
            self.assertIn(skill_id, markdown, role)
            self.assertIn("$" + skill_id.split(":", 1)[1], codex, role)
            # The banned surface is one list; importing it keeps this test from
            # asserting a subset of what the validator actually enforces.
            for surface in validate_repo.AGENT_BANNED_SURFACE:
                self.assertNotIn(surface, markdown, role)
                self.assertNotIn(surface, codex, role)

    def test_claude_and_codex_declare_identical_identity(self):
        for role in SPEC["skill_ids"]:
            metadata = validate_repo.parse_frontmatter(AGENTS / f"{role}.md")
            codex = codex_agent(role)
            self.assertEqual(role, metadata["name"])
            self.assertEqual(role, codex["name"])
            self.assertEqual(metadata["description"], codex["description"])

    def test_reviewer_can_delegate_and_declares_no_edit_tools(self):
        """The reviewer is the one role bound by a deny-list: it has to reach the
        host's own dispatch primitive, whose name differs per harness, while the
        skill forbids every edit."""
        metadata = validate_repo.parse_frontmatter(AGENTS / "reviewer.md")
        self.assertNotIn("tools", metadata)
        for tool in ("Edit", "Write", "NotebookEdit"):
            self.assertIn(tool, metadata["disallowedTools"])
        self.assertEqual("read-only", codex_agent("reviewer")["sandbox_mode"])

    def test_architect_cannot_create_files_and_developer_cannot_delegate(self):
        architect = validate_repo.parse_frontmatter(AGENTS / "architect.md")["tools"]
        developer = validate_repo.parse_frontmatter(AGENTS / "developer.md")["tools"]
        self.assertIn("Edit", architect)
        self.assertNotIn("Write", architect)
        self.assertIn("Write", developer)
        for delegation in ("Task", "Agent", "spawn_subagent"):
            self.assertNotIn(delegation, architect)
            self.assertNotIn(delegation, developer)

    def test_codex_sandboxes_never_widen_the_claude_binding(self):
        """Codex has one coarse switch, so the architect is read-only there even
        though it holds Edit on the other hosts."""
        self.assertEqual("read-only", codex_agent("architect")["sandbox_mode"])
        self.assertEqual("workspace-write", codex_agent("developer")["sandbox_mode"])

    def test_kimi_adapters_reproduce_the_agent_envelope_inline(self):
        for skill, path in KIMI_ADAPTERS.items():
            text = path.read_text(encoding="utf-8")
            self.assertIn("discards packaged plugin agents", text, skill)
            self.assertIn("policy_status", text, skill)
            self.assertIn("agents.enabled", text, skill)
            self.assertIn("agents.policy_divergence", text, skill)
            self.assertNotIn("../", text, skill)
            # Kimi has no binding at all, so this prose is the whole control.
            self.assertIn(SPEC["kimi_policy_contract_marker"], text, skill)
        # The architect envelope needs both conjuncts here or a Kimi controller
        # edits where the packaged agent must hand back.
        self.assertIn("inherit-session", KIMI_ADAPTERS["refactor"].read_text(encoding="utf-8"))

    def test_kimi_adapters_name_the_keys_they_consume(self):
        review = KIMI_ADAPTERS["review"].read_text(encoding="utf-8")
        refactor = KIMI_ADAPTERS["refactor"].read_text(encoding="utf-8")
        self.assertIn("agents.reviewer_max_parallel", review)
        self.assertIn("agents.authorization", refactor)

    def test_opencode_agents_are_thin_native_wrappers(self):
        for role, agent_id in SPEC["opencode_agent_ids"].items():
            path = OPENCODE_AGENTS / f"{role}.md"
            metadata = validate_repo.parse_frontmatter(path)
            body = validate_repo.agent_body(path)
            self.assertEqual(agent_id, metadata["name"])
            self.assertIn("declared policy may narrow this agent and it can never widen it", body)
            self.assertLessEqual(validate_repo.normalized_size(body), validate_repo.AGENT_BODY_MAX_CHARS)

    def test_policy_status_values_are_declared_wherever_the_contract_is_stated(self):
        """`policy_status` is a reporting contract, so every document that states
        it has to state the same five values."""
        documents = {"schema.md": SCHEMA_DOC.read_text(encoding="utf-8")}
        for skill, path in KIMI_ADAPTERS.items():
            documents[f"{skill} kimi adapter"] = path.read_text(encoding="utf-8")
        for label, text in documents.items():
            for status in SPEC["policy_status_values"]:
                self.assertIn(status, text, f"{label} omits {status}")


if __name__ == "__main__":
    unittest.main()
