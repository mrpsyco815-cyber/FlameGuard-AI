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

    def test_prefers_distinct_sources_before_repeating_a_source(self):
        data = json.loads(self.store_path.read_text(encoding="utf-8"))
        data["records"].append({
            "record_id": "NASA-OTHER-001",
            "record_type": "nasa_passage",
            "source": {
                "source_id": "20300000001",
                "title": "Independent Flame Study",
                "citation_url": "https://ntrs.nasa.gov/citations/20300000001",
                "pdf_page_number": 1,
            },
            "content": {"text": "Experimental flame spread flow velocity result."},
            "classification": {
                "evidence_role": "experimental_observation",
                "evidence_modality": "experiment",
                "scientific_findings_verified": False,
            },
            "review": {"scientific_findings_verified": False},
        })
        self.store_path.write_text(json.dumps(data), encoding="utf-8")

        result = build_evidence_brief(
            self.store_path, "flame spread flow velocity", limit=2
        )
        self.assertEqual(
            len({item["source_id"] for item in result["results"]}), 2
        )

    def test_rejects_empty_query(self):
        with self.assertRaises(ValueError):
            build_evidence_brief(self.store_path, "   ")

    def test_rejects_invalid_limit(self):
        with self.assertRaises(ValueError):
            build_evidence_brief(self.store_path, "flame", limit=0)



    def test_search_includes_supplemental_nasa_passages(self):
        supplemental_path = (
            self.store_path.parent / "supplemental_research_collection.json"
        )
        supplemental_record = {
            "record_id": "NASA-ONLINE-PASSAGE-999999-0001-001",
            "record_type": "nasa_passage",
            "source": {
                "source_id": "999999",
                "title": "Supplemental NASA Flame Study",
                "citation_url": "https://ntrs.nasa.gov/citations/999999",
                "pdf_page_number": 3,
            },
            "content": {
                "text": "Microgravity flame spread changed under low oxygen conditions."
            },
            "classification": {
                "evidence_role": "experimental_observation",
                "evidence_modality": "experiment",
                "classification_version": "3.4",
                "review_status": "requires_manual_review",
                "scientific_findings_verified": False,
            },
            "review": {
                "source_review_status": "requires_manual_review",
                "scientific_findings_verified": False,
            },
            "provenance": {"import_origin": "live_nasa_ntrs"},
        }
        supplemental_path.write_text(
            json.dumps({
                "collection_name": "Test supplemental collection",
                "schema_version": "1.0",
                "documents": [],
                "records": [supplemental_record],
            }),
            encoding="utf-8",
        )

        result = build_evidence_brief(
            self.store_path,
            "microgravity flame spread oxygen",
        )
        item = next(
            item for item in result["results"]
            if item["record_id"] == supplemental_record["record_id"]
        )

        self.assertEqual(
            item["record_origin"],
            "supplemental_research_collection",
        )
        self.assertEqual(item["import_origin"], "live_nasa_ntrs")
        self.assertEqual(item["source_id"], "999999")
        self.assertEqual(item["pdf_page_number"], 3)
        self.assertFalse(item["scientific_findings_verified"])
        self.assertEqual(
            result["search_audit"]["supplemental_nasa_passages_examined"],
            1,
        )

if __name__ == "__main__":
    unittest.main()
