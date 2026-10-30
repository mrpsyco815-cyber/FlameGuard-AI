import unittest
from unittest.mock import Mock, patch

from backend.services.mission_research import (
    _build_search_query,
    _deduplicate_passages,
)
from backend.services.nasa_online import search_nasa_online


class TestMissionSearchContext(unittest.TestCase):
    def test_search_query_includes_mission_fuel_and_environment(self):
        result = _build_search_query(
            "flame spread",
            mission="Moon",
            fuel="PMMA",
            environment_context={"gravity": "lunar", "pressure": "low"},
        )
        self.assertEqual(
            result,
            "flame spread Moon PMMA gravity lunar pressure low",
        )

    def test_deduplication_keeps_all_source_provenance(self):
        common = {
            "source_id": "NASA-123",
            "pdf_page_number": 4,
            "exact_source_excerpt": "Flame spread under microgravity.",
            "query_match_score": 0.5,
            "citation_url": "https://ntrs.nasa.gov/citations/123",
        }
        results = _deduplicate_passages([
            {
                **common,
                "source_dataset": "subhan_verified_core",
                "source_owner": "Subhan",
                "record_id": "SUBHAN-1",
            },
            {
                **common,
                "source_dataset": "nasa_primary_store",
                "source_owner": "FlameGuard",
                "record_id": "NASA-LOCAL-1",
            },
        ])
        self.assertEqual(len(results), 1)
        self.assertEqual(
            set(results[0]["source_presence"]),
            {"subhan_verified_core", "nasa_primary_store"},
        )
        self.assertEqual(len(results[0]["source_provenance"]), 2)


class TestNasaOnlineRetrievalMetadata(unittest.TestCase):
    @patch("backend.services.nasa_online.requests.get")
    def test_ntrs_results_include_retrieval_timestamp_and_scope(self, get):
        response = Mock()
        response.json.return_value = {
            "results": [{
                "id": "20240001234",
                "title": "NASA combustion research",
                "abstract": "An abstract.",
                "authorAffiliations": [],
                "publications": [],
                "center": {},
                "disseminated": "DOCUMENT_AND_METADATA",
            }]
        }
        response.raise_for_status.return_value = None
        get.return_value = response

        result = search_nasa_online("combustion", 5)
        item = result["results"][0]

        self.assertTrue(result["retrieved_at_utc"].endswith("Z"))
        self.assertEqual(item["retrieved_at_utc"], result["retrieved_at_utc"])
        self.assertEqual(
            item["evidence_scope"],
            "bibliographic_metadata_and_abstract_only",
        )
        self.assertFalse(item["full_text_retrieved"])
        self.assertFalse(item["scientific_findings_verified"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
