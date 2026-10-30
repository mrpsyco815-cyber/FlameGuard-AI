import unittest
from unittest.mock import patch

from backend.services.supplemental_research_search import search_supplemental_research


class TestSupplementalResearchSearch(unittest.TestCase):
    @patch("backend.services.supplemental_research_search.load_supplemental_collection")
    def test_returns_page_cited_pending_review_passages(self, loader):
        loader.return_value = {
            "records": [{
                "record_id": "NASA-ONLINE-PASSAGE-12345678901-0004-001",
                "source": {
                    "source_id": "12345678901",
                    "title": "NASA Microgravity Flame Study",
                    "citation_url": "https://ntrs.nasa.gov/citations/12345678901",
                    "pdf_page_number": 4,
                },
                "content": {
                    "text": "Experimental flame spread rate decreased in microgravity."
                },
                "classification": {
                    "evidence_role": "experimental_quantitative_result",
                    "evidence_modality": "experiment",
                    "review_status": "requires_manual_review",
                },
                "review": {
                    "source_review_status": "requires_manual_review",
                    "scientific_findings_verified": False,
                },
            }]
        }
        results = search_supplemental_research("flame spread microgravity")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["pdf_page_number"], 4)
        self.assertEqual(results[0]["source_id"], "12345678901")
        self.assertFalse(results[0]["scientific_findings_verified"])
        self.assertEqual(
            results[0]["source_dataset"],
            "live_nasa_supplemental_collection",
        )

    @patch("backend.services.supplemental_research_search.load_supplemental_collection")
    def test_excludes_background_and_unmatched_passages(self, loader):
        loader.return_value = {
            "records": [
                {
                    "record_id": "BG-1",
                    "source": {"source_id": "1"},
                    "content": {"text": "Microgravity flame background overview."},
                    "classification": {"evidence_role": "background"},
                },
                {
                    "record_id": "EXP-2",
                    "source": {"source_id": "2"},
                    "content": {"text": "Carbon dioxide concentration measurement."},
                    "classification": {"evidence_role": "experimental_observation"},
                },
            ]
        }
        self.assertEqual(search_supplemental_research("flame spread"), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
