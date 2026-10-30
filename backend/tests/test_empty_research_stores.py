import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from backend.services import nasa_passage_search, research_engine, research_summarizer


class TestEmptyResearchStores(unittest.TestCase):
    def test_empty_intelligence_store_returns_empty_brief(self):
        with tempfile.TemporaryDirectory() as directory:
            store_path = Path(directory) / "research_intelligence_store.json"
            store_path.write_text("", encoding="utf-8")

            result = research_summarizer.build_evidence_brief(
                store_path,
                "microgravity flame",
            )

        self.assertEqual(result["results"], [])
        self.assertEqual(result["summary"]["candidate_passage_count"], 0)
        self.assertEqual(result["search_audit"]["nasa_passages_examined"], 0)

    def test_empty_combined_nasa_store_returns_no_passages(self):
        with tempfile.TemporaryDirectory() as directory:
            store_path = Path(directory) / "nasa_combined_evidence.json"
            store_path.write_text("", encoding="utf-8")

            with patch.object(nasa_passage_search, "DATA_FILE", store_path):
                results = nasa_passage_search.search_nasa_passages(
                    query="microgravity flame",
                )

        self.assertEqual(results, [])

    def test_demo_only_records_are_not_returned_by_research_search(self):
        demo_record = {
            "study_id": "DEMO-001",
            "title": "Demo Study: Microgravity Combustion",
            "abstract": "Fictional test record for microgravity combustion.",
            "verification_status": "demo_only",
        }
        real_record = {
            "study_id": "NASA-001",
            "title": "NASA Microgravity Combustion Study",
            "abstract": "A source-backed study of microgravity combustion.",
            "verification_status": "requires_manual_review",
        }

        with tempfile.TemporaryDirectory() as directory:
            data_path = Path(directory) / "research_records.json"
            data_path.write_text(
                json.dumps([demo_record, real_record]),
                encoding="utf-8",
            )

            with patch.object(research_engine, "DATA_FILE", data_path):
                results = research_engine.search_research(
                    "microgravity combustion",
                )

        result_ids = [item["study_id"] for item in results]
        self.assertNotIn("DEMO-001", result_ids)
        self.assertIn("NASA-001", result_ids)


if __name__ == "__main__":
    unittest.main()
