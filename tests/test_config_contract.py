import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "plugins/gopher/skills/config/templates/default.gopher-plugin.toml"
SCHEMA_DOC = ROOT / "plugins/gopher/skills/config/references/schema.md"
VALIDATION_DOC = ROOT / "plugins/gopher/skills/config/references/validation.md"
CONFIG_SKILL = ROOT / "plugins/gopher/skills/config/SKILL.md"
BOOTSTRAP_DOC = ROOT / "plugins/gopher/skills/config/references/bootstrap.md"
EXPLAIN_DOC = ROOT / "plugins/gopher/skills/config/references/explain.md"

CANONICAL_TABLES = (
    "gopher", "project", "complexity", "test-quality", "modernize", "refactor", "tools",
    "doctor", "fuzz", "architecture", "agents", "developer",
)

AGENT_ROLES = ("developer", "architect", "reviewer")
AGENT_MODELS = ("shipped", "inherit", "haiku", "sonnet", "opus")
AGENT_EFFORTS = ("shipped", "inherit", "low", "medium", "high", "xhigh")
AGENT_AUTHORIZATIONS = ("handback", "request-approval", "inherit-session")
AGENT_DIVERGENCE_MODES = ("report", "block")
DEVELOPER_IDIOM_POLICIES = ("latest-compatible", "project-aligned", "explicit-only")
DEVELOPER_TEST_WORKFLOWS = ("adaptive-tdd", "strict-tdd", "test-after")

QUALITY_LAB_FAMILIES = (
    "deterministic-concurrency", "integration", "contract", "hermetic", "flake",
    "race-leak", "golden", "property", "metamorphic", "differential",
    "model-state", "mutation",
)


def load_template():
    with TEMPLATE.open("rb") as handle:
        return tomllib.load(handle)


class ConfigContractTest(unittest.TestCase):
    def test_schema_version_and_canonical_tables(self):
        data = load_template()
        self.assertEqual(4, data["gopher"]["schema_version"])
        self.assertEqual(set(CANONICAL_TABLES), set(data.keys()))

    def test_no_root_loose_or_dotted_keys(self):
        data = load_template()
        for key, value in data.items():
            self.assertIsInstance(value, dict, f"root key {key} is not a table")
        for line in TEMPLATE.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("[") or stripped.startswith("#"):
                continue
            name = stripped.split("=", 1)[0].strip()
            self.assertNotIn(".", name, f"dotted key not allowed: {stripped}")

    def test_value_types_and_ranges(self):
        data = load_template()
        self.assertIsInstance(data["project"]["module_roots"], list)
        self.assertEqual(["./..."], data["project"]["package_patterns"])
        complexity = data["complexity"]
        for key in (
            "cyclomatic_max", "cognitive_max", "maintainability_min",
            "function_lines_max", "file_lines_max",
        ):
            self.assertIsInstance(complexity[key], int)
            self.assertGreater(complexity[key], 0)
        tq = data["test-quality"]
        self.assertTrue(0 <= tq["coverage_target"] <= 100)
        self.assertEqual(0, tq["coverage_regression_max"])
        self.assertTrue(0 <= tq["mutation_target"] <= 100)
        self.assertIsInstance(tq["quality_lab_families"], list)
        self.assertEqual([], tq["quality_lab_families"])
        for family in tq["quality_lab_families"]:
            self.assertIn(family, QUALITY_LAB_FAMILIES)
        self.assertIsInstance(data["modernize"]["apply_fixes"], bool)
        self.assertIsInstance(data["refactor"]["require_passing_baseline"], bool)
        self.assertIsInstance(data["refactor"]["require_behavior_tests"], bool)
        doctor = data["doctor"]
        for key in ("deadline_ms", "max_findings"):
            self.assertIsInstance(doctor[key], int)
            self.assertGreater(doctor[key], 0)
        self.assertEqual(2000, doctor["deadline_ms"])
        self.assertEqual(20, doctor["max_findings"])
        self.assertIsInstance(doctor["required_rules"], list)
        self.assertEqual([], doctor["required_rules"])
        fuzz = data["fuzz"]
        for key in ("local_budget_seconds", "ci_budget_seconds", "repro_runs"):
            self.assertIsInstance(fuzz[key], int)
            self.assertGreater(fuzz[key], 0)
        self.assertEqual(60, fuzz["local_budget_seconds"])
        self.assertEqual(300, fuzz["ci_budget_seconds"])
        self.assertEqual(3, fuzz["repro_runs"])

    def test_agents_policy_types_and_enums(self):
        agents = load_template()["agents"]
        self.assertIsInstance(agents["enabled"], bool)
        self.assertTrue(agents["enabled"])
        self.assertIsInstance(agents["reviewer_max_parallel"], int)
        self.assertTrue(1 <= agents["reviewer_max_parallel"] <= 7)
        self.assertEqual(7, agents["reviewer_max_parallel"])
        for role in AGENT_ROLES:
            self.assertEqual("shipped", agents[f"{role}_model"])
            self.assertEqual("shipped", agents[f"{role}_effort"])
        self.assertEqual("handback", agents["authorization"])
        self.assertEqual("report", agents["policy_divergence"])

    def test_agents_enum_members_are_documented(self):
        """The template pins exactly one member of each `[agents]` enum, so
        testing that member against its own enum proves nothing. The enum is
        only checkable against the document that defines it."""
        doc = SCHEMA_DOC.read_text(encoding="utf-8")
        members = AGENT_MODELS + AGENT_EFFORTS + AGENT_AUTHORIZATIONS + AGENT_DIVERGENCE_MODES
        for member in members:
            self.assertIn(f"`{member}`", doc, f"schema.md omits agents enum member {member}")

    def test_developer_policy_defaults_types_and_enums(self):
        developer = load_template()["developer"]
        self.assertEqual(
            {
                "idiom_policy": "latest-compatible",
                "test_workflow": "adaptive-tdd",
            },
            developer,
        )
        self.assertIsInstance(developer["idiom_policy"], str)
        self.assertIn(developer["idiom_policy"], DEVELOPER_IDIOM_POLICIES)
        self.assertIsInstance(developer["test_workflow"], str)
        self.assertIn(developer["test_workflow"], DEVELOPER_TEST_WORKFLOWS)

    def test_developer_enum_members_are_documented(self):
        doc = SCHEMA_DOC.read_text(encoding="utf-8")
        for member in DEVELOPER_IDIOM_POLICIES + DEVELOPER_TEST_WORKFLOWS:
            self.assertIn(f"`{member}`", doc, f"schema.md omits developer enum member {member}")

    def test_enum_values(self):
        data = load_template()
        self.assertEqual("advisory", data["complexity"]["mode"])
        self.assertEqual("advisory", data["test-quality"]["mutation_mode"])
        self.assertEqual("declared", data["modernize"]["target_go"])
        self.assertFalse(data["modernize"]["apply_fixes"])
        self.assertEqual("none", data["modernize"]["dependency_updates"])
        for tool in ("complexity", "mutation", "modernize"):
            self.assertEqual("auto", data["tools"][tool])
        self.assertEqual("standard", data["doctor"]["profile"])
        self.assertIn(data["doctor"]["profile"], ("quick", "standard", "strict"))
        architecture = data["architecture"]
        self.assertEqual("advisory", architecture["workspace_mode"])
        self.assertEqual("advisory", architecture["tidy_mode"])
        self.assertEqual("independent", architecture["release_mode"])
        self.assertEqual("local-only", architecture["replace_mode"])
        for key in ("workspace_mode", "tidy_mode"):
            self.assertIn(architecture[key], ("off", "advisory", "required"))
        self.assertIn(architecture["release_mode"], ("independent", "grouped"))
        self.assertIn(architecture["replace_mode"], ("forbid", "local-only", "allow"))

    def test_schema_doc_documents_every_table_and_key(self):
        doc = SCHEMA_DOC.read_text(encoding="utf-8")
        data = load_template()
        for table in CANONICAL_TABLES:
            self.assertIn(table, doc, f"schema.md omits table {table}")
        for table, body in data.items():
            for key in body:
                self.assertIn(key, doc, f"schema.md omits key {table}.{key}")

    def test_validation_doc_documents_states(self):
        doc = VALIDATION_DOC.read_text(encoding="utf-8")
        for state in (
            "ABSENT", "VALID", "MIGRATION_AVAILABLE", "INVALID", "UNSUPPORTED_VERSION",
        ):
            self.assertIn(state, doc, f"validation.md omits state {state}")

    def test_schema_v4_developer_policy_is_normative_across_config_workflow(self):
        """Schema 4 must keep legacy contracts usable until a confirmed migration."""
        documents = {
            "SKILL.md": CONFIG_SKILL.read_text(encoding="utf-8"),
            "bootstrap.md": BOOTSTRAP_DOC.read_text(encoding="utf-8"),
            "validation.md": VALIDATION_DOC.read_text(encoding="utf-8"),
            "explain.md": EXPLAIN_DOC.read_text(encoding="utf-8"),
        }
        for name, document in documents.items():
            with self.subTest(document=name):
                self.assertIn("`idiom_policy`", document)
                self.assertIn("`test_workflow`", document)

        bootstrap = documents["bootstrap.md"]
        for version in (1, 2, 3):
            with self.subTest(version=version):
                self.assertIn(f"| `{version}` |", bootstrap)
        self.assertIn("schema_version = 4", bootstrap)
        self.assertIn("[developer]", bootstrap)
        self.assertIn('idiom_policy = "latest-compatible"', bootstrap)
        self.assertIn('test_workflow = "adaptive-tdd"', bootstrap)
        self.assertIn("Preserve every value the user already set", bootstrap)
        self.assertIn("Declining leaves the file untouched", bootstrap)

        validation = documents["validation.md"]
        self.assertIn("`4` is `VALID`", validation)
        self.assertIn("`1`, `2`, and `3` are `MIGRATION_AVAILABLE`", validation)
        self.assertIn("missing `[developer]` table", validation)

        explain = documents["explain.md"]
        self.assertIn("`idiom_policy`", explain)
        self.assertIn("`test_workflow`", explain)
        self.assertIn("latest-compatible", explain)
        self.assertIn("adaptive-tdd", explain)
        self.assertIn("`--explain` writes nothing", explain)


if __name__ == "__main__":
    unittest.main()
