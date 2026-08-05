import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "plugins/gopher/skills/config/templates/default.gopher-plugin.toml"
SCHEMA_DOC = ROOT / "plugins/gopher/skills/config/references/schema.md"
VALIDATION_DOC = ROOT / "plugins/gopher/skills/config/references/validation.md"

CANONICAL_TABLES = (
    "gopher", "project", "complexity", "test-quality", "modernize", "refactor", "tools",
    "doctor", "fuzz", "architecture",
)

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
        self.assertEqual(2, data["gopher"]["schema_version"])
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


if __name__ == "__main__":
    unittest.main()
