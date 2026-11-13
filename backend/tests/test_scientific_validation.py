import json
import tempfile
import unittest
from pathlib import Path

from backend.services.conflict_reporting import build_conflict_report
from backend.services.mission_intelligence import build_mission_intelligence


def nasa_record(record_id, text, modality="experiment", verified=False):
    return {
        "record_id": record_id,
        "record_type": "nasa_passage",
        "source": {
            "source_id": f"NASA-{record_id}",
            "title": f"Source {record_id}",
            "citation_url": f"https://ntrs.nasa.gov/citations/{record_id}",
            "pdf_page_number": 2,
        },
        "content": {"text": text},
        "classification": {
            "evidence_role": "experimental_quantitative_result",
            "evidence_modality": modality,
            "scientific_findings_verified": verified,
            "review_status": "requires_manual_review",
        },
        "review": {
            "source_review_status": "requires_manual_review",
            "scientific_findings_verified": verified,
        },
    }


class TestScientificValidation(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.store_path = Path(self.temp_dir.name) / "store.json"
        records = [
            nasa_record(
                "EXP-1",
                "PMMA flame spread in microgravity under forced flow.",
            ),
            nasa_record(
                "ABS-1",
                "PMMA flame spread abstract in spacecraft.",
                modality="abstract",
            ),
            {
                "record_id": "META-1",
                "record_type": "nasa_ntrs_catalog_metadata",
                "source": {"source_id": "META-1", "title": "Metadata only"},
                "content": {"text": ""},
            },
        ]
        self.store_path.write_text(
            json.dumps({"records": records}), encoding="utf-8"
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def result(self, query, **kwargs):
        return build_mission_intelligence(
            mission="spacecraft",
            query=query,
            store_path=self.store_path,
            **kwargs,
        )

    def test_fully_supported_scenario_preserves_experimental_evidence(self):
        result = self.result(
            "PMMA flame spread microgravity",
            fuel="PMMA",
            gravity_condition="microgravity",
        )
        self.assertTrue(result["evidence"]["experimental"])

    def test_partially_supported_scenario_keeps_missing_conditions_explicit(self):
        result = self.result("PMMA flame spread", fuel="PMMA")
        self.assertNotIn("oxygen_concentration", result["comparison"]["supplied_conditions"])

    def test_missing_conditions_do_not_get_defaulted(self):
        result = self.result("PMMA flame spread")
        self.assertIsNone(result["mission_scenario"]["oxygen_concentration"])
        self.assertIsNone(result["mission_scenario"]["environment"])

    def test_no_matching_evidence_returns_insufficiency(self):
        result = self.result("marine biology")
        self.assertEqual(
            result["recommendations"][0]["evidence_strength"],
            "insufficient_verified_evidence",
        )

    def test_conflict_requires_comparable_structured_claims(self):
        report = build_conflict_report([
            {"source_id": "A", "parameter": "spread_rate", "value": 1, "unit": "mm/s",
             "conditions": {"fuel": "PMMA"}},
            {"source_id": "B", "parameter": "spread_rate", "value": 2, "unit": "mm/s",
             "conditions": {"fuel": "PMMA"}},
        ])
        self.assertEqual(report["count"], 1)
        self.assertEqual(report["conflicts"][0]["conflict_status"], "unresolved_disagreement")

    def test_material_mismatch_cannot_create_verified_recommendation(self):
        result = self.result("polyethylene flame spread", fuel="polyethylene")
        self.assertEqual(
            result["recommendations"][0]["evidence_strength"],
            "insufficient_verified_evidence",
        )

    def test_environment_parameter_is_preserved_for_review(self):
        result = self.result("PMMA flame spread", environment="lunar habitat")
        self.assertEqual(
            result["comparison"]["supplied_conditions"]["environment"],
            "lunar habitat",
        )

    def test_metadata_only_record_is_not_experimental_evidence(self):
        result = self.result("metadata only")
        ids = [item["record_id"] for item in result["evidence"]["experimental"]]
        self.assertNotIn("META-1", ids)

    def test_abstract_only_evidence_remains_unverified(self):
        result = self.result("PMMA flame spread abstract")
        abstract = next(
            item for item in result["evidence"]["experimental"]
            if item["record_id"] == "ABS-1"
        )
        self.assertEqual(abstract["evidence_modality"], "abstract")
        self.assertFalse(abstract["scientific_findings_verified"])

    def test_source_link_and_excerpt_are_preserved(self):
        result = self.result("PMMA flame spread microgravity")
        item = next(
            item for item in result["evidence"]["experimental"]
            if item["record_id"] == "EXP-1"
        )
        self.assertEqual(
            item["citation_url"],
            "https://ntrs.nasa.gov/citations/EXP-1",
        )
        self.assertIn("PMMA flame spread", item["exact_source_excerpt"])


if __name__ == "__main__":
    unittest.main()
