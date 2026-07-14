import unittest

import validate_repo


class RepositoryContractTest(unittest.TestCase):
    def test_repository_contract_has_no_errors(self):
        self.assertEqual([], validate_repo.validate_repository())

    def test_catalog_counts_are_canonical(self):
        rows = validate_repo.catalog()
        counts = {
            kind: sum(row[1] == kind for row in rows)
            for kind in ("full", "diagnostic", "deferred", "boundary")
        }
        self.assertEqual(36, len(rows))
        self.assertEqual(
            {"full": 19, "diagnostic": 10, "deferred": 4, "boundary": 3},
            counts,
        )

    def test_go_mappings_reference_known_unique_general_ids(self):
        known = {row[0] for row in validate_repo.catalog()}
        rows = validate_repo.mapping_rows()
        general = [row[1] for row in rows]
        self.assertTrue(general)
        self.assertTrue(set(general).issubset(known))
        self.assertEqual(len(general), len(set(general)))

    def test_repository_documentation_is_english_only(self):
        errors = [
            error
            for error in validate_repo.validate_repository()
            if "documentation must be English" in error
        ]
        self.assertEqual([], errors)


if __name__ == "__main__":
    unittest.main()
