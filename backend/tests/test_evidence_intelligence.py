import unittest

from backend.services.evidence_intelligence import (
    build_evidence_intelligence,
    score_mission_relevance,
)


class TestEvidenceIntelligence(unittest.TestCase):
    def test_fuel_and_mission_context_affect_retrieval_rank(self):
        item = {
            "matched_query_terms": ["flame", "spread"],
            "source_title": "BASS-II PMMA flame spread in microgravity",
            "experiment_context": "PMMA rod, ISS, microgravity spacecraft test",
            "moon_mars_rank": 1,
            "moon_mars_rank_reason": "Curated Moon/Mars applicability note.",
            "citation_url": "https://ntrs.nasa.gov/citations/12345678901",
            "pdf_page_number": 18,
        }
        scored = score_mission_relevance(
            item, "flame spread", mission="moon", fuel="PMMA"
        )
        self.assertGreater(scored["score_components"]["mission_context"], 0)
        self.assertGreater(scored["score_components"]["fuel_match"], 0)
        self.assertFalse(scored["is_scientific_quality_score"])
        self.assertFalse(scored["is_safety_score"])

    def test_no_fuel_filter_does_not_award_fuel_points(self):
        scored = score_mission_relevance(
            {"matched_query_terms": ["flame"], "exact_source_excerpt": "flame"},
            "flame", mission="spacecraft",
        )
        self.assertEqual(scored["score_components"]["fuel_match"], 0)

    def test_experimental_and_simulation_results_stay_separate(self):
        result = build_evidence_intelligence(
            local_evidence=[
                {
                    "source_id": "1",
                    "evidence_modality": "experiment",
                    "matched_query_terms": ["flame"],
                    "exact_source_excerpt": "Experimental flame spread.",
                    "citation_url": "https://ntrs.nasa.gov/citations/1",
                    "pdf_page_number": 2,
                },
                {
                    "source_id": "2",
                    "evidence_modality": "simulation",
                    "matched_query_terms": ["flame"],
                    "exact_source_excerpt": "Simulation of flame spread.",
                    "citation_url": "https://ntrs.nasa.gov/citations/2",
                    "pdf_page_number": 5,
                },
            ],
            online_metadata=[],
            bass2_results=[],
            query="flame",
            mission="spacecraft",
        )
        self.assertEqual(result["comparison"]["experimental_passage_count"], 1)
        self.assertEqual(result["comparison"]["simulation_passage_count"], 1)
        self.assertTrue(result["comparison"]["experimental_and_simulation_are_kept_separate"])

    def test_metadata_only_results_are_identified_as_evidence_gap(self):
        result = build_evidence_intelligence(
            local_evidence=[],
            online_metadata=[{"title": "NASA abstract only"}],
            bass2_results=[],
            query="smoke detector",
        )
        self.assertTrue(any("metadata/abstracts" in gap for gap in result["evidence_gaps"]))
        self.assertEqual(result["comparison"]["ntrs_metadata_only_record_count"], 1)

    def test_relevance_score_is_not_presented_as_scientific_certainty(self):
        result = build_evidence_intelligence(
            local_evidence=[{
                "matched_query_terms": ["oxygen"],
                "exact_source_excerpt": "Oxygen level in the test.",
            }],
            online_metadata=[],
            bass2_results=[],
            query="oxygen",
        )
        self.assertIn("not scientific quality", result["ranking_disclaimer"])
        self.assertEqual(
            result["ranked_evidence"][0]["mission_relevance"]["score_label"],
            "transparent retrieval relevance (0-100)",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
