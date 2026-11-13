import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from backend.main import app
from backend.services.bass2_dataset import search_bass2_records
from backend.services.research_federation import search_research_with_fallback


class TestFallbackCoverageGaps(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.store_path = Path(self.temp_dir.name) / "store.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_records(self, records):
        self.store_path.write_text(json.dumps({"records": records}), encoding="utf-8")

    @patch("backend.services.research_federation.search_nasa_online")
    def test_empty_store_fallback_is_explainable(self, online):
        online.return_value = {"source": "NASA NTRS", "results": [], "count": 0}
        self.write_records([])
        result = search_research_with_fallback(
            "PMMA flame spread microgravity", store_path=self.store_path
        )
        self.assertTrue(result["fallback_triggered"])
        self.assertIn("too_few_local_passages", result["fallback_reason"])
        self.assertEqual(result["counts"]["local_passages_returned"], 0)

    @patch("backend.services.research_federation.search_nasa_online")
    def test_wrong_material_triggers_fallback(self, online):
        online.return_value = {"source": "NASA NTRS", "results": [], "count": 0}
        self.write_records([{
            "record_id": "R1", "record_type": "nasa_passage",
            "source": {"source_id": "S1", "title": "PE"},
            "content": {"text": "Polyethylene flame spread in microgravity."},
            "classification": {"evidence_role": "experimental_observation"},
        }])
        result = search_research_with_fallback(
            "PMMA flame spread microgravity", store_path=self.store_path,
            min_local_passages=0, min_local_sources=0,
        )
        self.assertIn("required_material_not_covered", result["fallback_reason"])

    @patch("backend.services.research_federation.search_nasa_online")
    def test_missing_query_concept_triggers_fallback(self, online):
        online.return_value = {"source": "NASA NTRS", "results": [], "count": 0}
        self.write_records([{
            "record_id": "R1", "record_type": "nasa_passage",
            "source": {"source_id": "S1", "title": "Study"},
            "content": {"text": "PMMA flame spread."},
            "classification": {"evidence_role": "experimental_observation"},
        }])
        result = search_research_with_fallback(
            "PMMA flame spread microgravity", store_path=self.store_path,
            min_local_passages=0, min_local_sources=0,
        )
        self.assertIn("required_scientific_concepts_not_covered",
                      result["fallback_reason"])

    @patch("backend.services.research_federation.search_nasa_online")
    def test_fallback_failure_preserves_local_results(self, online):
        online.return_value = {
            "source": "NASA NTRS", "results": [], "count": 0,
            "error": "unavailable",
        }
        self.write_records([{
            "record_id": "R1", "record_type": "nasa_passage",
            "source": {"source_id": "S1", "title": "Study"},
            "content": {"text": "PMMA flame spread in microgravity."},
            "classification": {"evidence_role": "experimental_observation"},
        }])
        result = search_research_with_fallback(
            "PMMA flame spread", store_path=self.store_path,
            min_local_passages=2,
        )
        self.assertEqual(result["counts"]["local_passages_returned"], 1)
        self.assertEqual(result["online_search"]["status"], "unavailable")

    @patch("backend.services.research_federation.search_nasa_online")
    def test_same_source_retains_distinct_page_provenance(self, online):
        online.return_value = {"source": "NASA NTRS", "results": [], "count": 0}
        self.write_records([
            {
                "record_id": "R1", "record_type": "nasa_passage",
                "source": {"source_id": "S1", "title": "Study", "pdf_page_number": 2},
                "content": {"text": "PMMA flame spread result."},
                "classification": {"evidence_role": "experimental_observation"},
            },
            {
                "record_id": "R2", "record_type": "nasa_passage",
                "source": {"source_id": "S1", "title": "Study", "pdf_page_number": 7},
                "content": {"text": "PMMA flame spread result."},
                "classification": {"evidence_role": "experimental_observation"},
            },
        ])
        result = search_research_with_fallback(
            "PMMA flame spread", store_path=self.store_path,
            min_local_passages=0, min_local_sources=0,
        )
        self.assertEqual(result["combined_sources"][0]["local_pdf_pages"], [2, 7])


class TestBASS2TypedFilters(unittest.TestCase):
    def test_oxygen_filter_and_numeric_filter(self):
        results = search_bass2_records(
            "", fuel="PMMA", initial_oxygen=22.2, numeric_field="Initial CO (ppm)",
            numeric_value=0, numeric_tolerance=0,
        )
        self.assertTrue(results)
        self.assertTrue(all(
            result["record"]["Fuel Sample Material"].lower().find("pmma") >= 0
            for result in results
        ))

    def test_missing_numeric_values_do_not_match(self):
        results = search_bass2_records(
            "", numeric_field="Final CO (ppm)", numeric_value=0
        )
        self.assertTrue(all(
            result["record"]["Final CO (ppm)"] not in ("", "none")
            for result in results
        ))

    def test_unsupported_numeric_column_is_rejected(self):
        with self.assertRaises(ValueError):
            search_bass2_records(
                "", numeric_field="Pressure", numeric_value=1
            )


class TestResearchHTTPAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_valid_bass2_request_exposes_filters(self):
        response = self.client.get(
            "/bass2/search?fuel=PMMA&initial_oxygen=22.2&limit=2"
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["filters"]["initial_oxygen"], 22.2)
        self.assertLessEqual(payload["count"], 2)

    def test_invalid_limit_is_rejected(self):
        response = self.client.get("/bass2/search?limit=0")
        self.assertEqual(response.status_code, 422)

    def test_empty_research_query_is_rejected(self):
        response = self.client.get("/research/search?q=")
        self.assertIn(response.status_code, (400, 422))

    def test_scientifically_empty_online_query_is_rejected(self):
        response = self.client.get("/research/online-search?q=and")
        self.assertEqual(response.status_code, 400)

    @patch("backend.main.search_nasa_online")
    def test_online_unavailable_response_is_explicit(self, online):
        online.return_value = {
            "source": "NASA NTRS", "query": "flame spread",
            "count": 0, "results": [], "error": "unavailable",
        }
        response = self.client.get("/research/online-search?q=flame%20spread")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 0)
        self.assertIn("error", response.json())
