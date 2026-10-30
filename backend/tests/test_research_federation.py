import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from backend.services.research_federation import (
    search_research_with_fallback,
)


class TestResearchFederation(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.store_path = Path(self.temp_dir.name) / "store.json"
        self.write_store(3)

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_store(self, matching_records):
        records = []

        for index in range(matching_records):
            nasa_id = "NASA-A" if index < 2 else "NASA-B"
            source_id = "20000024924" if index < 2 else "20210017787"

            records.append({
                "record_id": f"PASSAGE-{index}",
                "record_type": "nasa_passage",
                "source": {
                    "source_id": source_id,
                    "title": f"Study {source_id}",
                    "citation_url": f"https://ntrs.nasa.gov/citations/{source_id}",
                    "pdf_page_number": index + 1,
                },
                "content": {
                    "text": (
                        f"Experimental flame spread result number {index} "
                        "under low pressure conditions."
                    )
                },
                "classification": {
                    "evidence_role": "experimental_quantitative_result",
                    "evidence_modality": "experiment",
                    "research_context": "spaceflight_or_microgravity",
                    "classification_version": "3.4",
                    "review_status": "requires_manual_review",
                    "scientific_findings_verified": False,
                },
                "review": {
                    "source_review_status": "requires_manual_review",
                    "scientific_findings_verified": False,
                },
            })

        self.store_path.write_text(
            json.dumps({"records": records}),
            encoding="utf-8",
        )

    def online_payload(self):
        return {
            "source": "NASA NTRS",
            "query": "flame spread",
            "count": 2,
            "results": [
                {
                    "nasa_id": "20000024924",
                    "title": "Study 20000024924",
                    "abstract": "NASA catalog abstract for an existing local source.",
                    "source_url": "https://ntrs.nasa.gov/citations/20000024924",
                    "authors": [],
                    "keywords": ["flame"],
                    "verification_status": "metadata_retrieved",
                },
                {
                    "nasa_id": "99999999999",
                    "title": "New NASA catalog study",
                    "abstract": "A newly discovered catalog abstract.",
                    "source_url": "https://ntrs.nasa.gov/citations/99999999999",
                    "authors": [],
                    "keywords": ["combustion"],
                    "verification_status": "metadata_retrieved",
                },
            ],
        }

    @patch("backend.services.research_federation.search_nasa_online")
    def test_sufficient_local_coverage_skips_online_search(self, online_search):
        result = search_research_with_fallback(
            "flame spread",
            limit=10,
            store_path=self.store_path,
        )

        online_search.assert_not_called()
        self.assertFalse(result["fallback_triggered"])
        self.assertEqual(result["counts"]["local_passages_returned"], 3)
        self.assertFalse(result["online_search"]["performed"])

    @patch("backend.services.research_federation.search_nasa_online")
    def test_insufficient_local_passages_triggers_fallback(self, online_search):
        self.write_store(1)
        online_search.return_value = self.online_payload()

        result = search_research_with_fallback(
            "flame spread",
            store_path=self.store_path,
        )

        online_search.assert_called_once()
        self.assertTrue(result["fallback_triggered"])
        self.assertIn("too_few_local_passages", result["fallback_reason"])

    @patch("backend.services.research_federation.search_nasa_online")
    def test_one_local_source_triggers_coverage_fallback(self, online_search):
        self.write_store(3)

        # Make all local records belong to one NASA document.
        data = json.loads(self.store_path.read_text(encoding="utf-8"))
        for record in data["records"]:
            record["source"]["source_id"] = "20000024924"
            record["source"]["citation_url"] = (
                "https://ntrs.nasa.gov/citations/20000024924"
            )
        self.store_path.write_text(json.dumps(data), encoding="utf-8")

        online_search.return_value = self.online_payload()

        result = search_research_with_fallback(
            "flame spread",
            store_path=self.store_path,
        )

        online_search.assert_called_once()
        self.assertIn(
            "insufficient_local_source_coverage",
            result["fallback_reason"],
        )

    @patch("backend.services.research_federation.search_nasa_online")
    def test_online_sources_merge_and_deduplicate_by_nasa_id(self, online_search):
        self.write_store(1)
        online_search.return_value = self.online_payload()

        result = search_research_with_fallback(
            "flame spread",
            store_path=self.store_path,
        )

        ids = [item["nasa_id"] for item in result["combined_sources"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(result["combined_sources"]), 2)

        existing = next(
            item for item in result["combined_sources"]
            if item["nasa_id"] == "20000024924"
        )
        self.assertIn(
            "local_research_intelligence_store",
            existing["source_presence"],
        )
        self.assertIn("nasa_ntrs_online", existing["source_presence"])
        self.assertIsNotNone(existing["ntrs_metadata"])

    @patch("backend.services.research_federation.search_nasa_online")
    def test_new_online_source_is_marked_metadata_only(self, online_search):
        self.write_store(1)
        online_search.return_value = self.online_payload()

        result = search_research_with_fallback(
            "flame spread",
            store_path=self.store_path,
        )

        new_source = next(
            item for item in result["combined_sources"]
            if item["nasa_id"] == "99999999999"
        )
        self.assertEqual(new_source["local_passage_count"], 0)
        self.assertEqual(
            new_source["ntrs_metadata"]["evidence_scope"],
            "bibliographic_metadata_and_abstract_only",
        )
        self.assertFalse(
            new_source["ntrs_metadata"]["scientific_findings_verified"]
        )
        self.assertEqual(result["counts"]["new_online_sources_discovered"], 1)

    @patch("backend.services.research_federation.search_nasa_online")
    def test_online_failure_keeps_local_results(self, online_search):
        self.write_store(1)
        online_search.return_value = {
            "source": "NASA NTRS",
            "query": "flame spread",
            "count": 0,
            "results": [],
            "error": "NASA online search is temporarily unavailable.",
        }

        result = search_research_with_fallback(
            "flame spread",
            store_path=self.store_path,
        )

        self.assertTrue(result["fallback_triggered"])
        self.assertEqual(result["counts"]["local_passages_returned"], 1)
        self.assertEqual(result["online_search"]["status"], "unavailable")
        self.assertEqual(len(result["combined_sources"]), 1)

    def test_invalid_limits_are_rejected(self):
        with self.assertRaises(ValueError):
            search_research_with_fallback(
                "flame spread",
                limit=0,
                store_path=self.store_path,
            )


if __name__ == "__main__":
    unittest.main()
