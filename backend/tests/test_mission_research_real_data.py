import unittest
from unittest.mock import patch

from backend.services.mission_research import search_mission_research


class TestMissionResearchAgainstProjectDatasets(unittest.TestCase):
    @patch("backend.services.mission_research.search_nasa_online")
    def test_flame_spread_query_uses_project_local_sources_first(self, online):
        online.side_effect = AssertionError(
            "NASA online fallback should not run when local coverage is sufficient."
        )
        result = search_mission_research(
            "flame spread microgravity",
            mission="spacecraft",
            fuel="PMMA",
            limit=10,
        )

        self.assertEqual(result["subhan_data"]["core_record_count"], 10)
        self.assertEqual(result["subhan_data"]["core_passage_count"], 68)
        self.assertGreater(result["counts"]["combined_unique_local_passages"], 0)
        self.assertFalse(result["fallback_triggered"])
        self.assertTrue(result["evidence_intelligence"]["ranked_evidence"])
        self.assertIn("condition_comparison", result)
        self.assertTrue(
            all(
                item.get("citation_url") and item.get("pdf_page_number") is not None
                for item in result["subhan_data"]["verified_core_results"]
            )
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
