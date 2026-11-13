import unittest

from backend.services.research_comparison import compare_documents
from backend.services.research_gap_analysis import (
    build_conflict_intelligence,
    build_research_gaps,
)


def paper(name, *, material="PMMA", oxygen="21", gravity="microgravity",
          pressure="100", temperature="300", flow="10", unit="cm/s",
          source_type="local_nasa_passage"):
    conditions = {
        "material_fuel": [{"value": material, "unit": None}],
        "oxygen_concentration": [{"value": oxygen, "unit": "%"}],
        "initial_oxygen_concentration": [{"value": oxygen, "unit": "%"}],
        "final_oxygen_concentration": [{"value": oxygen, "unit": "%"}],
        "gravity_condition": [{"value": gravity, "unit": None}],
        "pressure": [{"value": pressure, "unit": "kPa"}],
        "temperature": [{"value": temperature, "unit": "K"}],
        "flow_condition": [{"value": flow, "unit": unit}],
        "experimental_setup": [{"value": "apparatus-A", "unit": None}],
    }
    return {
        "document_id": name,
        "nasa_id": name,
        "source_url": f"https://example.test/{name}",
        "source_type": source_type,
        "evidence_classification": (
            "bibliographic_metadata_and_abstract"
            if source_type == "nasa_ntrs" else "experimental_results"
        ),
        "review_status": "requires_manual_review",
        "conditions": conditions,
        "claims": [{
            "claim_id": f"{name}-claim",
            "exact_supporting_excerpt": "The reported observation was recorded.",
        }],
    }


class TestResearchComparison(unittest.TestCase):
    def test_exact_conditions_are_comparable(self):
        result = compare_documents([paper("A"), paper("B")])
        self.assertEqual(len(result["comparable_sources"]), 1)
        self.assertEqual(
            result["condition_comparisons"][0]["overall_status"],
            "exact_match",
        )

    def test_oxygen_material_and_unit_differences_are_not_matches(self):
        oxygen = compare_documents([paper("A"), paper("B", oxygen="25")])
        material = compare_documents([paper("A"), paper("B", material="PE")])
        units = compare_documents([paper("A"), paper("B", flow="0.01", unit="m/s")])
        self.assertEqual(oxygen["condition_comparisons"][0]["overall_status"], "mismatch")
        self.assertEqual(material["condition_comparisons"][0]["overall_status"], "mismatch")
        self.assertEqual(units["condition_comparisons"][0]["overall_status"], "mismatch")

    def test_missing_conditions_remain_unknown_or_partial(self):
        incomplete = paper("B")
        incomplete["conditions"].pop("gravity_condition")
        incomplete["conditions"].pop("temperature")
        incomplete["conditions"].pop("pressure")
        result = compare_documents([paper("A"), incomplete])
        statuses = {
            item["dimension"]: item["status"]
            for item in result["condition_comparisons"][0]["condition_comparisons"]
        }
        self.assertEqual(statuses["gravity_condition"], "partial_match")
        self.assertEqual(statuses["temperature"], "partial_match")
        self.assertEqual(statuses["pressure"], "partial_match")

    def test_model_and_abstract_sources_are_not_experiments(self):
        result = compare_documents([
            paper("A"),
            paper("B", source_type="nasa_ntrs"),
        ])
        self.assertFalse(result["scientific_findings_verified"])
        self.assertEqual(
            result["sources"][1]["evidence_classification"],
            "bibliographic_metadata_and_abstract",
        )

    def test_conflict_classification_is_conservative(self):
        comparison = compare_documents([paper("A"), paper("B", oxygen="25")])
        conflicts = build_conflict_intelligence(comparison)
        self.assertEqual(conflicts[0]["classification"], "not_comparable")
        self.assertEqual(
            conflicts[0]["verification_status"],
            "not_scientifically_verified",
        )

    def test_comparable_measurements_report_potential_difference(self):
        first = paper("A")
        second = paper("B")
        first["structured_findings"] = {
            "fields": {
                "measurement": {"values": [{
                    "value": "0.3", "unit": "mm/s",
                    "exact_supporting_text": "Rate was 0.3 mm/s.",
                }]}
            }
        }
        second["structured_findings"] = {
            "fields": {
                "measurement": {"values": [{
                    "value": "0.5", "unit": "mm/s",
                    "exact_supporting_text": "Rate was 0.5 mm/s.",
                }]}
            }
        }
        comparison = compare_documents([first, second])
        conflicts = build_conflict_intelligence(comparison, [first, second])
        self.assertEqual(conflicts[0]["classification"], "potential_difference")
        self.assertEqual(conflicts[0]["parameter"], "measurement")
        self.assertIn("exact_supporting_text", conflicts[0]["first_finding"])

    def test_gaps_and_questions_trace_to_sources(self):
        incomplete = paper("A")
        incomplete["conditions"].pop("temperature")
        comparison = compare_documents([incomplete])
        result = build_research_gaps([incomplete], comparison)
        self.assertTrue(result["research_gaps"])
        gap = result["research_gaps"][0]
        self.assertIn("A", gap["supporting_source_ids"])
        self.assertIn(gap["gap_id"], result["suggested_research_questions"][0]["gap_ids"])

    def test_empty_evidence_is_safe(self):
        comparison = compare_documents([])
        result = build_research_gaps([], comparison)
        self.assertEqual(result["research_gaps"], [])
        self.assertFalse(comparison["scientific_findings_verified"])
