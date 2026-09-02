import unittest

import run_forward_tests


class ForwardCorpusTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = run_forward_tests.load_json(run_forward_tests.CASES_PATH)
        cls.cases = cls.payload["cases"]
        cls.configs = {harness: run_forward_tests.load_json(run_forward_tests.ROOT / f"tests/{harness}/config.json") for harness in run_forward_tests.HARNESSES}

    def test_corpus_schema_and_owner_coverage(self):
        self.assertEqual([], run_forward_tests.validate_corpus(self.payload))
        self.assertEqual(120, len(self.cases))
        for harness, config in self.configs.items():
            self.assertEqual(harness, config["harness"])
            selector = "@alvadorncorp/gopher" if harness == "opencode" else "gopher@alvadorncorp"
            self.assertEqual(selector, config["selector"])
            self.assertTrue(config["requires_local_install"])
            self.assertEqual(f"python3 tests/run_forward_tests.py --harness {harness}", config["runner"])

    def test_review_modes_cover_full_subset_and_preflight(self):
        ids = {case["id"] for case in self.cases}
        self.assertTrue({"review-full", "review-subset-exact", "review-no-mode"}.issubset(ids))

    def test_pattern_decisions_cover_required_baselines(self):
        ids = {case["id"] for case in self.cases}
        required = {"constructor-two-optionals", "functional-options-sdk", "config-from-yaml", "optional-map-lookup", "result-everywhere", "function-strategy", "reject-singleton", "reject-premature-interface", "reject-unmeasured-pool"}
        self.assertTrue(required.issubset(ids))

    def test_required_owner_set_is_derived_from_the_layout_fixture(self):
        owners = run_forward_tests.required_owners()
        layout = run_forward_tests.load_json(run_forward_tests.LAYOUT_PATH)
        self.assertEqual(len(layout["skills"]), len(owners))
        self.assertTrue(all(owner.startswith("gopher:") for owner in owners))

    def test_capability_peers_own_positive_and_boundary_cases(self):
        selected = [case["expected"]["selected_skill"] for case in self.cases]
        tags = {case["id"]: set(case["tags"]) for case in self.cases}
        for owner in ("doctor", "resilience", "observability", "codegen", "cgo", "fuzz"):
            self.assertIn(f"gopher:{owner}", selected, f"no case selects gopher:{owner}")
            self.assertTrue(
                any(owner in case_tags and "negative" in case_tags for case_tags in tags.values()),
                f"gopher:{owner} has no negative boundary case",
            )

    def test_expected_comparison_is_exact_for_declared_fields(self):
        actual = {"selected_skill": "gopher:review", "selected_lenses": ["tests", "security"], "extra": 1}
        expected = {"selected_skill": "gopher:review", "selected_lenses": ["tests", "security"]}
        self.assertEqual([], run_forward_tests.compare_expected(actual, expected))


if __name__ == "__main__":
    unittest.main()
