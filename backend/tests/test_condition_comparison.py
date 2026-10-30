import unittest

from backend.services.condition_comparison import build_condition_comparison


class TestConditionComparison(unittest.TestCase):
    def test_identical_recorded_conditions_are_flagged_as_textual_match(self):
        conditions = {
            "fuel_or_material": "PMMA rod",
            "gravity": "microgravity",
            "oxygen": "21% O2",
            "pressure": "1 atm",
            "flow": "0.4 cm/s",
        }
        evidence = [
            {"source_id": "A", "source_title": "Study A", "experiment_conditions": conditions},
            {"source_id": "B", "source_title": "Study B", "experiment_conditions": dict(conditions)},
        ]
        result = build_condition_comparison(evidence)
        self.assertEqual(
            result["study_pair_comparisons"][0]["status"],
            "recorded_conditions_match_textually",
        )
        self.assertEqual(len(result["study_pair_comparisons"][0]["matching_fields"]), 5)

    def test_different_conditions_are_not_called_directly_comparable(self):
        left = {
            "fuel_or_material": "PMMA",
            "gravity": "microgravity",
            "oxygen": "21%",
            "pressure": "1 atm",
            "flow": "0.4 cm/s",
        }
        right = {**left, "oxygen": "16%"}
        result = build_condition_comparison([
            {"source_id": "A", "experiment_conditions": left},
            {"source_id": "B", "experiment_conditions": right},
        ])
        pair = result["study_pair_comparisons"][0]
        self.assertEqual(pair["status"], "recorded_conditions_differ")
        self.assertIn("oxygen", pair["differing_fields"])

    def test_missing_conditions_are_explicitly_reported(self):
        result = build_condition_comparison([
            {"source_id": "A", "experiment_conditions": {"gravity": "microgravity"}},
            {"source_id": "B", "experiment_conditions": {"gravity": "microgravity"}},
        ])
        pair = result["study_pair_comparisons"][0]
        self.assertEqual(pair["status"], "insufficient_condition_metadata")
        self.assertIn("oxygen", pair["missing_fields"])

    def test_raw_bass2_records_are_not_normalized(self):
        result = build_condition_comparison([], bass2_results=[{"record": {"O2": "none"}}])
        self.assertEqual(result["bass2_structured_record_count"], 1)
        self.assertIn("does not normalize units", result["bass2_notice"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
