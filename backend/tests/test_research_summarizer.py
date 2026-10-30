import json
import tempfile
import unittest
from pathlib import Path

from backend.services.research_summarizer import build_evidence_brief


class TestResearchSummarizer(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.store_path = Path(self.temp_dir.name) / "test_store.json"

        self.experiment_text = (
            "The experimental flame spread rate decreased as "
            "the concurrent flow velocity decreased."
        )
        self.simulation_text = (
            "The simulation model reproduced flame spread behavior "
            "at lower ambient pressure."
        )

        records = [
            {
                "record_id": "NASA-EXP-001",
                "record_type": "nasa_passage",
                "source": {
                    "source_id": "20000024924",
                    "title": "Experimental Flame Study",
                    "citation_url": "https://ntrs.nasa.gov/citations/20000024924",
                    "pdf_page_number": 5,
                },
                "content": {"text": self.experiment_text},
                "classification": {
                    "evidence_role": "experimental_quantitative_result",
                    "evidence_modality": "experiment",
                    "research_context": "spaceflight_or_microgravity",
                    "context_requirement": "page_context_supplied",
                    "classification_version": "3.4",
                    "review_status": "requires_manual_review",
                    "scientific_findings_verified": False,
                },
                "review": {
                    "source_review_status": "requires_manual_review",
                    "scientific_findings_verified": False,
                },
            },
            {
                "record_id": "NASA-SIM-001",
                "record_type": "nasa_passage",
                "source": {
                    "source_id": "20210017787",
                    "title": "Simulation Flame Study",
                    "citation_url": "https://ntrs.nasa.gov/citations/20210017787",
                    "pdf_page_number": 6,
                },
                "content": {"text": self.simulation_text},
                "classification": {
                    "evidence_role": "simulation_result",
                    "evidence_modality": "simulation",
                    "classification_version": "3.4",
                    "review_status": "requires_manual_review",
                    "scientific_findings_verified": False,
                },
                "review": {
                    "source_review_status": "requires_manual_review",
                    "scientific_findings_verified": False,
                },
            },
            {
                "record_id": "NASA-BG-001",
                "record_type": "nasa_passage",
                "source": {
                    "source_id": "20000024924",
                    "title": "Background passage",
                    "citation_url": "https://ntrs.nasa.gov/citations/20000024924",
                    "pdf_page_number": 2,
                },
                "content": {"text": "Background information about flame spread."},
                "classification": {
                    "evidence_role": "background",
                    "evidence_modality": "unknown",
                    "scientific_findings_verified": False,
                },
                "review": {"scientific_findings_verified": False},
            },
            {
                "record_id": "BASS2-001",
                "record_type": "bass2_experimental_record",
                "source": {"source_id": "B1"},
                "content": {"raw_record": {"Fuel Sample Material": "PMMA"}},
            },
        ]

        self.store_path.write_text(
            json.dumps({"records": records}),
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_finds_candidate_experimental_evidence(self):
        result = build_evidence_brief(
            self.store_path, "flame spread flow velocity"
        )
        ids = [item["record_id"] for item in result["results"]]
        self.assertIn("NASA-EXP-001", ids)

    def test_excludes_background_from_candidate_findings(self):
        result = build_evidence_brief(self.store_path, "flame spread")
        ids = [item["record_id"] for item in result["results"]]
        self.assertNotIn("NASA-BG-001", ids)

    def test_keeps_simulation_separate_from_experiment(self):
        result = build_evidence_brief(self.store_path, "flame spread")
        by_id = {item["record_id"]: item for item in result["results"]}

        self.assertEqual(
            by_id["NASA-EXP-001"]["evidence_modality"], "experiment"
        )
        self.assertEqual(
            by_id["NASA-SIM-001"]["evidence_modality"], "simulation"
        )

    def test_preserves_citation_and_exact_excerpt(self):
        result = build_evidence_brief(
            self.store_path, "flame spread flow velocity"
        )
        item = next(
            item for item in result["results"]
            if item["record_id"] == "NASA-EXP-001"
        )

        self.assertEqual(item["pdf_page_number"], 5)
        self.assertEqual(
            item["citation_url"],
            "https://ntrs.nasa.gov/citations/20000024924",
        )
        self.assertEqual(item["exact_source_excerpt"], self.experiment_text)

    def test_does_not_claim_scientific_verification(self):
        result = build_evidence_brief(self.store_path, "flame spread")
        for item in result["results"]:
            self.assertFalse(item["scientific_findings_verified"])

    def test_bass2_records_are_not_mixed_into_passage_search(self):
        result = build_evidence_brief(self.store_path, "flame spread")
        ids = [item["record_id"] for item in result["results"]]
        self.assertNotIn("BASS2-001", ids)

    def test_ranking_is_described_as_lexical_only(self):
        result = build_evidence_brief(
            self.store_path, "flame spread flow velocity"
        )
        self.assertEqual(
            result["retrieval_method"], "lexical_token_overlap"
        )
        self.assertIn("not a measure of scientific quality", result["ranking_note"])

    def test_rejects_empty_query(self):
        with self.assertRaises(ValueError):
            build_evidence_brief(self.store_path, "   ")

    def test_rejects_invalid_limit(self):
        with self.assertRaises(ValueError):
            build_evidence_brief(self.store_path, "flame", limit=0)


if __name__ == "__main__":
    unittest.main()
