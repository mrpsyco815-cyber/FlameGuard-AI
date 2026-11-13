import unittest
from unittest.mock import Mock, patch

from backend.services.nasa_online import build_nasa_query, search_nasa_online


class TestNASAOnline(unittest.TestCase):
    def test_builds_concise_scientific_query(self):
        query = (
            "How does oxygen concentration affect flame spread and flame "
            "extinction in microgravity combustion experiments, and what "
            "evidence from NASA research and BASS-II experiments supports "
            "these observations?"
        )
        self.assertEqual(
            build_nasa_query(query),
            "oxygen concentration flame spread extinction microgravity combustion",
        )

    def test_keeps_concise_query_unchanged(self):
        self.assertEqual(
            build_nasa_query("microgravity flame spread"),
            "microgravity flame spread",
        )

    @patch("backend.services.nasa_online.requests.get")
    def test_normalizes_metadata_without_claiming_verification(self, get):
        response = Mock()
        response.json.return_value = {
            "results": [{
                "id": "123",
                "title": "PMMA flame spread",
                "abstract": "Flame spread at reduced gravity.",
                "authorAffiliations": [],
                "publications": [{"publicationDate": "2020"}],
                "keywords": ["combustion"],
                "subjectCategories": ["fire safety"],
                "stiType": "Technical Paper",
            }]
        }
        response.raise_for_status.return_value = None
        get.return_value = response
        result = search_nasa_online("microgravity flame spread", limit=1)
        item = result["results"][0]
        self.assertEqual(result["normalized_query"], "microgravity flame spread")
        self.assertEqual(item["nasa_id"], "123")
        self.assertFalse(item["full_text_retrieved"])
        self.assertFalse(item["scientific_findings_verified"])
        self.assertEqual(item["evidence_type"], "bibliographic_metadata_and_abstract")
        self.assertTrue(item["retrieval_timestamp"])
        self.assertEqual(item["retrieved_at"], item["retrieval_timestamp"])
        self.assertEqual(item["source_url"], "https://ntrs.nasa.gov/citations/123")
        self.assertFalse(result["fallback_attempted"])
        self.assertEqual(result["original_result_count"], 1)

    @patch("backend.services.nasa_online.requests.get")
    def test_duplicate_nasa_records_are_removed(self, get):
        response = Mock()
        response.json.return_value = {
            "results": [
                {"id": "123", "title": "PMMA flame spread", "abstract": "flame spread"},
                {"id": "123", "title": "PMMA flame spread duplicate", "abstract": "flame spread"},
            ]
        }
        response.raise_for_status.return_value = None
        get.return_value = response
        result = search_nasa_online("flame spread", limit=5)
        self.assertEqual(len(result["results"]), 1)

    @patch("backend.services.nasa_online.requests.get")
    def test_http_failure_is_explicit(self, get):
        import requests
        get.side_effect = requests.Timeout()
        result = search_nasa_online("flame spread")
        self.assertEqual(result["count"], 0)
        self.assertIn("error", result)
        self.assertFalse(result["fallback_attempted"])

    @patch("backend.services.nasa_online.requests.get")
    def test_zero_results_retry_with_focused_query(self, get):
        empty = Mock()
        empty.json.return_value = {"results": []}
        empty.raise_for_status.return_value = None
        populated = Mock()
        populated.json.return_value = {
            "results": [{
                "id": "456",
                "title": "Microgravity flame extinction",
                "abstract": "Oxygen concentration affects extinction.",
            }]
        }
        populated.raise_for_status.return_value = None
        get.side_effect = [empty, populated]

        query = (
            "How does oxygen concentration affect flame spread and flame "
            "extinction in microgravity combustion experiments?"
        )
        result = search_nasa_online(query, limit=5)

        self.assertEqual(result["count"], 1)
        self.assertTrue(result["fallback_attempted"])
        self.assertEqual(result["original_result_count"], 0)
        self.assertEqual(result["fallback_result_count"], 1)
        self.assertEqual(
            result["nasa_query"],
            "oxygen concentration flame spread extinction microgravity combustion",
        )
        self.assertEqual(get.call_count, 2)
        self.assertEqual(
            get.call_args_list[1].kwargs["params"]["q"],
            result["nasa_query"],
        )

    @patch("backend.services.nasa_online.requests.get")
    def test_focused_retry_also_empty(self, get):
        response = Mock()
        response.json.return_value = {"results": []}
        response.raise_for_status.return_value = None
        get.return_value = response

        result = search_nasa_online(
            "How does oxygen concentration affect flame extinction in microgravity?",
            limit=5,
        )

        self.assertEqual(result["count"], 0)
        self.assertTrue(result["fallback_attempted"])
        self.assertEqual(result["fallback_result_count"], 0)
        self.assertEqual(get.call_count, 2)

    @patch("backend.services.nasa_online.requests.get")
    def test_identical_focused_query_is_not_retried(self, get):
        response = Mock()
        response.json.return_value = {"results": []}
        response.raise_for_status.return_value = None
        get.return_value = response

        result = search_nasa_online("microgravity flame spread", limit=5)

        self.assertEqual(result["count"], 0)
        self.assertFalse(result["fallback_attempted"])
        self.assertEqual(get.call_count, 1)
