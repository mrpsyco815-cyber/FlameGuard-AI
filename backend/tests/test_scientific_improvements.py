import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from backend.services.claim_summarizer import build_paper_summary
from backend.services.mission_intelligence_orchestrator import (
    build_mission_intelligence_orchestration,
)
from backend.services.nasa_online import search_nasa_online


class TestNASAImprovement(unittest.TestCase):
    @staticmethod
    def response(records):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {"results": records}
        return response

    @patch("backend.services.nasa_online.requests.get")
    def test_long_query_uses_bounded_fallback_attempts_and_deduplicates(self, get):
        get.side_effect = [
            self.response([]),
            self.response([{"id": "1", "title": "oxygen microgravity"}]),
            self.response([{"id": "1", "title": "duplicate"}, {"id": "2", "title": "flame spread"}]),
            self.response([{"id": "3", "title": "extinction oxygen"}]),
        ]
        query = "oxygen concentration and flame spread in microgravity " * 20
        result = search_nasa_online(query, limit=5)
        self.assertTrue(result["fallback_attempted"])
        self.assertLessEqual(len(result["fallback_attempts"]), 3)
        self.assertEqual(result["fallback_result_count"], 3)
        self.assertEqual(
            {item["nasa_id"] for item in result["results"]},
            {"1", "2", "3"},
        )
        self.assertEqual(result["original_query"], query)

    @patch("backend.services.nasa_online.requests.get")
    def test_fallback_records_zero_results_per_attempt(self, get):
        get.side_effect = [
            self.response([]),
            self.response([]),
            self.response([]),
            self.response([]),
        ]
        result = search_nasa_online("oxygen concentration " * 30, limit=5)
        self.assertEqual(result["count"], 0)
        self.assertEqual(
            [item["reason"] for item in result["fallback_attempts"]],
            ["zero_results", "zero_results", "zero_results"],
        )


class TestClaimImprovement(unittest.TestCase):
    def document(self, source_id):
        return {
            "source_title": "A scientific paper",
            "sections": [{
                "section_name": "results",
                "text": (
                    "Solid Surface Combustion Experiment Flame Spread. "
                    "The flame spread rate was 0.3 mm/s. "
                    "N96- 15553 references."
                ),
                "page_numbers": [4],
            }],
            "document_id": source_id,
            "nasa_id": source_id,
            "source_url": f"https://example.test/{source_id}",
        }

    def test_filters_headers_and_artifacts_preserving_valid_excerpt(self):
        result = build_paper_summary(self.document("NASA-A"))
        self.assertEqual(len(result["claims"]), 1)
        claim = result["claims"][0]
        self.assertIn("0.3 mm/s", claim["exact_supporting_excerpt"])
        self.assertEqual(claim["claim_id"][:6], "claim-")

    def test_claim_ids_are_stable_and_source_unique(self):
        first = build_paper_summary(self.document("NASA-A"))["claims"][0]["claim_id"]
        repeat = build_paper_summary(self.document("NASA-A"))["claims"][0]["claim_id"]
        other = build_paper_summary(self.document("NASA-B"))["claims"][0]["claim_id"]
        self.assertEqual(first, repeat)
        self.assertNotEqual(first, other)


class TestMissionBASS2Integration(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.store_path = Path(self.directory.name) / "store.json"
        self.store_path.write_text(json.dumps({"records": []}), encoding="utf-8")
        self.review_path = Path(self.directory.name) / "reviews.sqlite3"

    def tearDown(self):
        self.directory.cleanup()

    @patch("backend.services.mission_intelligence_orchestrator.build_research_comparison")
    def test_mission_response_contains_distinct_bass2_evidence(self, compare):
        compare.return_value = {
            "retrieval": {},
            "evidence": {"papers": [], "claims": []},
            "comparison": {"sources": [], "condition_comparisons": []},
            "conflicts": [],
            "research_gaps": [],
            "suggested_research_questions": [],
        }
        result = build_mission_intelligence_orchestration(
            "oxygen concentration combustion",
            review_db_path=self.review_path,
            store_path=self.store_path,
            limit=3,
        )
        bass2 = result["bass2_evidence"]
        self.assertTrue(bass2["dataset_available"])
        self.assertIn("Calibrated  initial O2 % by vol ", bass2["field_names"])
        self.assertIn("Calibrated final O2 % by vol", bass2["field_names"])
        self.assertFalse(bass2["scientific_findings_verified"])
        self.assertNotIn("gravity_condition", bass2["field_names"])


if __name__ == "__main__":
    unittest.main()
