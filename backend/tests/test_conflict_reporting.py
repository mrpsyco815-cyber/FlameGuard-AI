import unittest

from backend.services.conflict_reporting import build_conflict_report


class TestConflictReporting(unittest.TestCase):
    def test_comparable_disagreement_is_traceable(self):
        report = build_conflict_report([
            {
                "source_id": "A", "source_url": "https://example/a",
                "pdf_page_number": 3, "parameter": "spread_rate",
                "value": 1.0, "unit": "cm/s",
                "conditions": {"oxygen": "21%"},
            },
            {
                "source_id": "B", "source_url": "https://example/b",
                "pdf_page_number": 8, "parameter": "spread_rate",
                "value": 2.0, "unit": "cm/s",
                "conditions": {"oxygen": "21%"},
            },
        ])
        self.assertEqual(report["count"], 1)
        conflict = report["conflicts"][0]
        self.assertEqual(conflict["conflict_status"], "unresolved_disagreement")
        self.assertEqual(conflict["source_a"]["page"], 3)
        self.assertEqual(conflict["source_b"]["source_id"], "B")

    def test_unstructured_passages_are_not_invented_as_conflicts(self):
        report = build_conflict_report([
            {"source_id": "A", "exact_source_excerpt": "spread increased"},
            {"source_id": "B", "exact_source_excerpt": "spread decreased"},
        ])
        self.assertEqual(report["count"], 0)
        self.assertTrue(report["limitations"])
