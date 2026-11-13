import unittest

from backend.services.mission_research_brief import (
    INSUFFICIENT_RECOMMENDATION,
    build_mission_research_brief,
)
from backend.tests.test_scientific_synthesis_step6 import paper


class TestMissionResearchBriefStep7(unittest.TestCase):
    def context(self, **overrides):
        value = {
            "research_objective": "Assess flame spread evidence.",
            "specific_research_question": "How does flame spread behave?",
            "fuel_material": "PMMA",
            "gravity_condition": "microgravity",
            "oxygen_concentration": "21 percent",
            "pressure": "100 kPa",
            "temperature": "300 K",
            "flow_condition": "10 cm/s",
            "experimental_setup": (
                "PMMA samples were tested in microgravity at 21 percent oxygen."
            ),
        }
        value.update(overrides)
        return value

    def test_exact_conditions_are_classified_and_traceable(self):
        result = build_mission_research_brief(
            self.context(),
            [paper("A", nasa_id="101")],
        )
        self.assertEqual(len(result["comparable_studies"]), 1)
        study = result["comparable_studies"][0]
        self.assertEqual(study["comparison"], "exact_match")
        self.assertTrue(study["scientific_observations"])
        claim = study["scientific_observations"][0]
        self.assertEqual(claim["nasa_id"], "101")
        self.assertEqual(claim["page_numbers"], [4])
        self.assertIn("mm/s", claim["exact_supporting_excerpt"])

    def test_partial_match_preserves_unknown_conditions(self):
        result = build_mission_research_brief(
            self.context(temperature=""),
            [paper("A")],
        )
        self.assertEqual(len(result["partially_comparable_studies"]), 1)
        study = result["partially_comparable_studies"][0]
        self.assertIn("temperature", study["unknown_condition_fields"])

    def test_different_gravity_and_oxygen_are_not_validation(self):
        result = build_mission_research_brief(
            self.context(),
            [paper("A", gravity="normal gravity", oxygen="30 percent")],
        )
        self.assertEqual(len(result["important_differences"]), 1)
        study = result["important_differences"][0]
        self.assertIn("gravity_condition", study["different_condition_fields"])
        self.assertIn("oxygen_concentration", study["different_condition_fields"])
        self.assertFalse(result["comparable_studies"])

    def test_missing_mission_parameters_remain_unknown(self):
        result = build_mission_research_brief(
            {"research_question": "What is reported?"},
            [paper("A")],
        )
        self.assertEqual(len(result["unknown_condition_studies"]), 1)
        self.assertTrue(result["evidence_gaps"])
        self.assertIn("not supplied", result["evidence_gaps"][1]["statement"])

    def test_missing_research_conditions_are_unknown(self):
        incomplete = paper("A")
        incomplete["sections"][0]["text"] = (
            "PMMA samples were tested in microgravity at 21 percent oxygen."
        )
        result = build_mission_research_brief(self.context(), [incomplete])
        self.assertEqual(len(result["important_differences"]), 0)
        self.assertEqual(len(result["comparable_studies"]), 0)
        self.assertEqual(
            result["relevant_nasa_research"][0]["comparison"],
            "partial_match",
        )

    def test_no_recommendation_is_generated_and_safeguard_is_explicit(self):
        result = build_mission_research_brief(
            self.context(oxygen_concentration="30 percent"),
            [paper("A")],
        )
        self.assertNotIn("recommendation", result)
        self.assertIn(INSUFFICIENT_RECOMMENDATION, {
            gap["statement"] for gap in result["evidence_gaps"]
        })
        self.assertFalse(result["scientific_findings_verified"])

    def test_invalid_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            build_mission_research_brief([], [])
        with self.assertRaises(ValueError):
            build_mission_research_brief({}, {})


if __name__ == "__main__":
    unittest.main()
