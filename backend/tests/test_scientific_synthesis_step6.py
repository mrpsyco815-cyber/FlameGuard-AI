import unittest

from backend.services.scientific_synthesis import synthesize_documents


def paper(
    document_id,
    oxygen="21 percent",
    gravity="microgravity",
    material="PMMA",
    measurement="0.3",
    nasa_id=None,
):
    return {
        "document_id": document_id,
        "nasa_id": nasa_id or document_id,
        "citation_url": f"https://example.test/{document_id}",
        "sections": [
            {
                "section_name": "experimental_setup",
                "text": (
                    f"{material} samples were tested in {gravity} at "
                    f"{oxygen} oxygen. Ambient pressure 100 kPa, "
                    "temperature 300 K. "
                    "Forced flow velocity was 10 cm/s."
                ),
                "page_numbers": [2],
            },
            {
                "section_name": "results",
                "text": (
                    f"The flame spread rate was {measurement} mm/s. "
                    "The observed flame became shorter."
                ),
                "page_numbers": [4],
            },
        ],
    }


class TestScientificSynthesisStep6(unittest.TestCase):
    def test_comparable_conditions_create_group_and_shared_observation(self):
        result = synthesize_documents([
            paper("A", nasa_id="101"),
            paper("B", nasa_id="102"),
        ], research_topic="microgravity flame spread")
        self.assertEqual(len(result["comparable_study_groups"]), 1)
        self.assertTrue(result["shared_observations"])
        self.assertEqual(
            result["shared_observations"][0]["evidence_status"],
            "comparable_findings",
        )
        self.assertFalse(result["scientific_findings_verified"])

    def test_different_oxygen_is_not_comparable(self):
        result = synthesize_documents([
            paper("A", oxygen="21 percent"),
            paper("B", oxygen="30 percent"),
        ])
        self.assertFalse(result["comparable_study_groups"])
        self.assertEqual(result["differences"][0]["label"],
                         "different_experimental_conditions")
        self.assertIn("oxygen_concentration", result["differences"][0]["reason"])

    def test_different_gravity_is_not_comparable(self):
        result = synthesize_documents([
            paper("A", gravity="microgravity"),
            paper("B", gravity="normal gravity"),
        ])
        self.assertFalse(result["comparable_study_groups"])
        self.assertIn("gravity_condition", result["differences"][0]["reason"])

    def test_missing_condition_is_not_treated_as_equal(self):
        incomplete = paper("B")
        incomplete["sections"][0]["text"] = (
            "PMMA samples were tested in microgravity at 21 percent oxygen."
        )
        result = synthesize_documents([paper("A"), incomplete])
        self.assertFalse(result["comparable_study_groups"])
        self.assertIn(
            "pressure not reported in both studies",
            result["differences"][0]["reason"],
        )
        self.assertTrue(result["evidence_gaps"])

    def test_different_material_is_not_comparable(self):
        result = synthesize_documents([
            paper("A", material="PMMA"),
            paper("B", material="polyethylene"),
        ])
        self.assertFalse(result["comparable_study_groups"])
        self.assertIn("material_fuel", result["differences"][0]["reason"])

    def test_original_units_and_provenance_are_preserved(self):
        result = synthesize_documents([
            paper("A", nasa_id="101"),
            paper("B", nasa_id="102"),
        ])
        disagreement = synthesize_documents([
            paper("A", measurement="0.3", nasa_id="101"),
            paper("B", measurement="0.5", nasa_id="102"),
        ])["potential_disagreements"]
        self.assertTrue(disagreement)
        item = disagreement[0]["supporting_claims"][0]
        self.assertEqual(item["nasa_id"], "101")
        self.assertIn("mm/s", item["exact_supporting_excerpt"])
        self.assertEqual(item["page_numbers"], [4])

    def test_potential_disagreement_requires_comparable_conditions(self):
        result = synthesize_documents([
            paper("A", measurement="0.3"),
            paper("B", measurement="0.5", oxygen="30 percent"),
        ])
        self.assertFalse(result["potential_disagreements"])
        self.assertFalse(result["comparable_study_groups"])

    def test_unsupported_cross_study_conclusion_is_rejected(self):
        result = synthesize_documents([paper("A")])
        self.assertEqual(
            result["evidence_gaps"][0]["statement"],
            "Insufficient verified evidence to support a cross-study conclusion.",
        )
        self.assertEqual(result["evidence_gaps"][0]["claim_ids"], [])

    def test_invalid_input_is_rejected(self):
        with self.assertRaises(ValueError):
            synthesize_documents({})


if __name__ == "__main__":
    unittest.main()
