import json
import tempfile
import unittest
from pathlib import Path

from backend.services.mission_intelligence import build_mission_intelligence


def make_record(record_id, role, modality, text):
    return {
        "record_id": record_id,
        "record_type": "nasa_passage",
        "source": {
            "source_id": "NASA-TEST",
            "title": "Test NASA source",
            "citation_url": "https://ntrs.nasa.gov/citations/123",
            "pdf_page_number": 5,
        },
        "content": {"text": text},
        "classification": {
            "evidence_role": role,
            "evidence_modality": modality,
            "scientific_findings_verified": False,
        },
        "review": {
            "source_review_status": "requires_manual_review",
            "scientific_findings_verified": False,
        },
    }


class TestMissionIntelligence(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.store_path = Path(self.temp_dir.name) / "store.json"

        records = [
            make_record(
                "EXP-1",
                "experimental_quantitative_result",
                "experiment",
                "Flame spread rate changes with flow velocity in microgravity.",
            ),
            make_record(
                "SIM-1",
                "simulation_result",
                "simulation",
                "Simulation qualitatively reproduces flame spread behaviour.",
            ),
            make_record(
                "BG-1",
                "background",
                "unknown",
                "General history of NASA space exploration.",
            ),
        ]

        self.store_path.write_text(
            json.dumps({"records": records}),
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_separates_experimental_and_simulation(self):
        result = build_mission_intelligence(
            mission="spacecraft",
            query="flame spread microgravity",
            store_path=self.store_path,
        )
        self.assertEqual(
            [x["record_id"] for x in result["evidence"]["experimental"]],
            ["EXP-1"],
        )
        self.assertEqual(
            [x["record_id"] for x in result["evidence"]["simulation"]],
            ["SIM-1"],
        )

    def test_does_not_return_background_as_result(self):
        result = build_mission_intelligence(
            mission="spacecraft",
            query="NASA space exploration",
            store_path=self.store_path,
        )
        ids = [
            item["record_id"]
            for group in ("experimental", "simulation")
            for item in result["evidence"][group]
        ]
        self.assertNotIn("BG-1", ids)

    def test_does_not_claim_scientific_verification(self):
        result = build_mission_intelligence(
            mission="spacecraft",
            query="flame spread microgravity",
            store_path=self.store_path,
        )
        for group in ("experimental", "simulation"):
            for item in result["evidence"][group]:
                self.assertFalse(item["scientific_findings_verified"])

    def test_unverified_evidence_cannot_generate_recommendation(self):
        result = build_mission_intelligence(
            mission="spacecraft",
            query="flame spread microgravity",
            fuel="PMMA",
            oxygen_concentration="21 percent",
            gravity_condition="microgravity",
            store_path=self.store_path,
        )
        self.assertEqual(
            result["recommendations"][0]["recommendation"],
            "Insufficient verified evidence to support a mission-specific recommendation.",
        )
        self.assertIsNone(result["recommendations"][0]["supporting_source_id"])
        self.assertIn("certified safety decisions", " ".join(result["limitations"]))

    def test_invalid_mission_is_rejected(self):
        with self.assertRaises(ValueError):
            build_mission_intelligence(
                mission="jupiter",
                query="flame spread",
                store_path=self.store_path,
            )

    def test_empty_query_is_rejected(self):
        with self.assertRaises(ValueError):
            build_mission_intelligence(
                mission="moon",
                query=" ",
                store_path=self.store_path,
            )


if __name__ == "__main__":
    unittest.main()
