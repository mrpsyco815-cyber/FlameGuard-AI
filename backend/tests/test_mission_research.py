import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from backend.services.mission_research import search_mission_research
from backend.services.subhan_research import search_subhan_research


class TestSubhanResearchIntegration(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.core = self.root / "core.json"
        self.passages = self.root / "passages.json"
        self.extended = self.root / "extended.json"
        self.legacy = self.root / "legacy.json"

        core = [{
            "study_id": "saffire-vi-2024",
            "title": "Preliminary Results from the Saffire VI Experiment",
            "investigation": "SAFFIRE-VI",
            "source_url": "https://ntrs.nasa.gov/api/citations/20240002981/downloads/file.pdf",
            "verification_status": "verified_from_opened_pdf",
        }]
        passages = {
            "records_with_evidence": 1,
            "total_passages": 3,
            "evidence_passages": [
                {
                    "study_id": "saffire-vi-2024",
                    "title": "Preliminary Results from the Saffire VI Experiment",
                    "investigation": "SAFFIRE-VI",
                    "evidence_text": "Smoke detection alarm threshold was achieved at 981 seconds.",
                    "source_url": "https://ntrs.nasa.gov/api/citations/20240002981/downloads/file.pdf",
                    "file_name": "saffire-vi.pdf",
                    "page": 6,
                    "section_or_table": "Conclusion",
                    "experiment_context": "Saffire VI, microgravity.",
                },
                {
                    "study_id": "saffire-vi-2024",
                    "title": "Preliminary Results from the Saffire VI Experiment",
                    "investigation": "SAFFIRE-VI",
                    "evidence_text": "Microgravity flame spread and carbon dioxide increased during the spacecraft fire experiment.",
                    "source_url": "https://ntrs.nasa.gov/api/citations/20240002981/downloads/file.pdf",
                    "file_name": "saffire-vi.pdf",
                    "page": 2,
                    "section_or_table": "Introduction",
                    "experiment_context": "Saffire VI, microgravity.",
                },
                {
                    "study_id": "saffire-vi-2024",
                    "title": "Preliminary Results from the Saffire VI Experiment",
                    "investigation": "SAFFIRE-VI",
                    "evidence_text": "Microgravity flame spread test conditions were documented.",
                    "source_url": "https://ntrs.nasa.gov/api/citations/20240002981/downloads/file.pdf",
                    "file_name": "saffire-vi.pdf",
                    "page": 9,
                    "section_or_table": "Test conditions",
                    "experiment_context": "Saffire VI, microgravity.",
                },
                {
                    "study_id": "saffire-vi-2024",
                    "title": "Preliminary Results from the Saffire VI Experiment",
                    "investigation": "SAFFIRE-VI",
                    "evidence_text": "Microgravity flame spread test conditions were documented.",
                    "source_url": "https://ntrs.nasa.gov/api/citations/20240002981/downloads/file.pdf",
                    "file_name": "saffire-vi.pdf",
                    "page": 9,
                    "section_or_table": "Test conditions",
                    "experiment_context": "Saffire VI, microgravity.",
                },
            ],
        }
        extended = [{
            "study_id": "prelim-001",
            "title": "Microgravity flame spread overview",
            "investigation": "ISS research",
            "plain_summary": "Preliminary summary of flame spread behaviour.",
            "source_url": "https://ntrs.nasa.gov/citations/99999999999",
            "verification_status": "preliminary",
            "evidence_passages": [],
            "missing_fields": ["PDF not opened"],
        }]
        legacy = {"records": [{
            "record_id": "LEGACY-001",
            "record_type": "nasa_passage",
            "source": {
                "source_id": "20150023100",
                "title": "Legacy NASA research",
                "citation_url": "https://ntrs.nasa.gov/citations/20150023100",
                "pdf_page_number": 4,
            },
            "content": {"text": "Microgravity flame spread experimental observation."},
            "classification": {
                "evidence_role": "experimental_observation",
                "evidence_modality": "experiment",
                "scientific_findings_verified": False,
            },
            "review": {"scientific_findings_verified": False},
        }]}
        self.core.write_text(json.dumps(core), encoding="utf-8")
        self.passages.write_text(json.dumps(passages), encoding="utf-8")
        self.extended.write_text(json.dumps(extended), encoding="utf-8")
        self.legacy.write_text(json.dumps(legacy), encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def subhan_args(self):
        return {
            "core_path": self.core,
            "passages_path": self.passages,
            "extended_path": self.extended,
        }

    def mission_subhan_args(self):
        return {
            "subhan_core_path": self.core,
            "subhan_passages_path": self.passages,
            "subhan_extended_path": self.extended,
        }

    def test_subhan_pdf_passage_citation_and_page_are_preserved(self):
        result = search_subhan_research("smoke alarm 981 seconds", **self.subhan_args())
        self.assertEqual(result["verified_core_evidence_count"], 1)
        item = result["verified_core_evidence"][0]
        self.assertEqual(item["pdf_page_number"], 6)
        self.assertIn("20240002981", item["citation_url"])
        self.assertEqual(item["source_owner"], "Subhan Malik")
        self.assertFalse(item["scientific_findings_verified"])

    def test_extended_records_are_discovery_only(self):
        result = search_subhan_research("microgravity flame spread", **self.subhan_args())
        self.assertEqual(result["preliminary_index_match_count"], 1)
        item = result["preliminary_index_matches"][0]
        self.assertEqual(item["record_scope"], "discovery_metadata_only_not_verified_evidence")
        self.assertEqual(item["evidence_passage_count"], 0)

    @patch("backend.services.mission_research.search_nasa_online")
    def test_nasa_fallback_runs_when_local_coverage_is_thin(self, online):
        online.return_value = {
            "source": "NASA NTRS",
            "results": [{
                "nasa_id": "12345678901",
                "title": "NASA online catalog result",
                "abstract": "NASA abstract metadata only.",
                "source_url": "https://ntrs.nasa.gov/citations/12345678901",
                "document_available": True,
            }],
        }
        result = search_mission_research(
            "smoke alarm 981 seconds",
            legacy_store_path=self.legacy,
            **self.mission_subhan_args(),
        )
        online.assert_called_once()
        self.assertTrue(result["fallback_triggered"])
        self.assertTrue(result["online_search"]["performed"])
        self.assertEqual(
            result["online_search"]["results"][0]["evidence_scope"],
            "bibliographic_metadata_and_abstract_only",
        )
        self.assertFalse(result["online_search"]["results"][0]["full_text_retrieved"])
        self.assertTrue(result["online_search"]["results"][0]["import_available"])
        self.assertEqual(
            result["online_search"]["results"][0]["full_text_import_endpoint"],
            "/research/import/12345678901",
        )

    @patch("backend.services.mission_research.search_nasa_online")
    def test_sufficient_local_coverage_skips_nasa_fallback(self, online):
        result = search_mission_research(
            "microgravity flame",
            legacy_store_path=self.legacy,
            **self.mission_subhan_args(),
        )
        online.assert_not_called()
        self.assertFalse(result["fallback_triggered"])
        self.assertGreaterEqual(
            result["local_coverage"]["distinct_source_count"], 2
        )

    @patch("backend.services.mission_research.search_bass2_records")
    @patch("backend.services.mission_research.search_nasa_online")
    def test_online_metadata_is_attached_to_matching_local_source(self, online, bass2):
        online.return_value = {
            "source": "NASA NTRS",
            "results": [{
                "nasa_id": "20240002981",
                "title": "Preliminary Results from the Saffire VI Experiment",
                "abstract": "NASA catalogue abstract.",
                "source_url": "https://ntrs.nasa.gov/citations/20240002981",
            }],
        }
        bass2.return_value = []
        result = search_mission_research(
            "smoke alarm 981 seconds",
            legacy_store_path=self.legacy,
            **self.mission_subhan_args(),
        )
        self.assertTrue(result["fallback_triggered"])
        self.assertEqual(result["online_search"]["count"], 0)
        matching = next(
            item for item in result["local_evidence"]
            if item["source_id"] == "20240002981"
        )
        self.assertIn("online_catalog_metadata", matching)
        self.assertIn("nasa_ntrs_online", matching["source_presence"])

    @patch("backend.services.mission_research.search_bass2_records")
    def test_bass2_search_uses_query_and_fuel_filter(self, bass2):
        bass2.return_value = [{
            "record": {"Fuel Sample Material": "PMMA"},
            "matched_terms": ["pmma"],
            "relevance_score": 1.0,
        }]
        result = search_mission_research(
            "PMMA flame",
            fuel="PMMA",
            legacy_store_path=self.legacy,
            **self.mission_subhan_args(),
        )
        bass2.assert_called_once_with(query="PMMA flame", limit=10, fuel="PMMA")
        self.assertEqual(
            result["bass2_structured_experimental_data"]["query_relevant_record_count"],
            1,
        )

    def test_rejects_empty_or_unsearchable_query(self):
        with self.assertRaises(ValueError):
            search_subhan_research("  ", **self.subhan_args())


if __name__ == "__main__":
    unittest.main(verbosity=2)
