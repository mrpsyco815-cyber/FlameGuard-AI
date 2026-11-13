import unittest

from backend.services.ranking_contract import (
    annotate_duplicate_sources,
    build_ranking_contract,
    condition_match,
    evidence_scope,
    provenance_completeness,
    source_identity,
)


class TestRankingContract(unittest.TestCase):
    def record(self, **values):
        return {
            "source_id": "NASA-1",
            "citation_url": "https://ntrs.nasa.gov/citations/1",
            "pdf_page_number": 2,
            "exact_source_excerpt": values.pop("text", ""),
            **values,
        }

    def test_exact_partial_mismatch_and_unknown_conditions(self):
        exact = condition_match(
            "PMMA microgravity at 21 percent oxygen",
            "PMMA flame spread in microgravity at 21 percent oxygen.",
        )
        self.assertEqual(exact["overall"], "exact")

        partial = condition_match(
            "PMMA microgravity at 21 percent oxygen and 100 kPa pressure",
            "PMMA flame spread in microgravity at 21 percent oxygen.",
        )
        self.assertEqual(partial["overall"], "partial")
        self.assertIn("pressure", partial["missing_information"])

        mismatch = condition_match(
            "PMMA microgravity at 21 percent oxygen",
            "PMMA flame spread in normal gravity at 30 percent oxygen.",
        )
        self.assertEqual(mismatch["overall"], "mismatch")

        unknown = condition_match(
            "PMMA microgravity",
            "Flame spread was measured in a laboratory.",
        )
        self.assertEqual(unknown["overall"], "unknown")

    def test_evidence_scope_is_explicit(self):
        self.assertEqual(
            evidence_scope({"evidence_type": "bibliographic_metadata"}),
            "metadata",
        )
        self.assertEqual(
            evidence_scope({
                "evidence_type": "bibliographic_metadata_and_abstract"
            }),
            "abstract",
        )
        self.assertEqual(
            evidence_scope({"evidence_type": "experimental_results"}),
            "experimental_results",
        )

    def test_contract_preserves_original_score_and_explains_missing_data(self):
        result = build_ranking_contract(
            query="PMMA microgravity 21 percent oxygen",
            original_score=0.73,
            record=self.record(text="PMMA flame spread in microgravity."),
            source_text="PMMA flame spread in microgravity.",
        )
        self.assertEqual(result["original_score"], 0.73)
        self.assertTrue(result["score_semantics"].startswith("source-specific"))
        self.assertIn("oxygen_concentration", result["missing_information"])
        self.assertTrue(result["explanations"])
        self.assertFalse(result["scientific_findings_verified"])

    def test_reviewed_evidence_is_not_auto_verified(self):
        result = build_ranking_contract(
            query="flame spread",
            original_score=0.8,
            record={
                "source_id": "reviewed-1",
                "source_url": "https://example.test/1",
                "exact_source_excerpt": "Flame spread observation.",
                "evidence_type": "independently_reviewed_evidence",
                "review_status": "accepted",
                "scientific_findings_verified": False,
            },
            source_text="Flame spread observation.",
        )
        self.assertEqual(
            result["evidence_scope"], "independently_reviewed_evidence"
        )
        self.assertFalse(result["scientific_findings_verified"])

    def test_provenance_distinguishes_missing_and_not_applicable(self):
        complete = provenance_completeness({
            "source_id": "NASA-1",
            "nasa_id": "1",
            "citation_url": "https://ntrs.nasa.gov/citations/1",
            "exact_source_excerpt": "Observed result.",
            "pdf_page_number": 4,
            "section_name": "Results",
            "evidence_type": "experimental_results",
            "retrieved_at": "2026-10-31T00:00:00Z",
            "review_status": "not_scientifically_reviewed",
        }, "nasa_extracted_passage")
        self.assertEqual(complete["missing_fields"], [])
        self.assertEqual(complete["fields"]["nasa_id"]["status"], "present")

        incomplete = provenance_completeness({
            "source_id": "ntrs-1",
            "abstract": "Metadata only.",
        }, "nasa_ntrs")
        self.assertIn("source_url", incomplete["missing_fields"])
        self.assertIn("page_number_or_range", incomplete["not_applicable_fields"])
        self.assertIn("section_name", incomplete["not_applicable_fields"])

        bass = provenance_completeness({
            "source_id": "BASS2:PI:1",
            "exact_source_excerpt": "Fuel record",
            "evidence_type": "experimental_metadata",
        }, "bass_ii")
        self.assertIn("nasa_id", bass["not_applicable_fields"])

    def test_duplicate_grouping_uses_stable_ids_not_titles(self):
        records = annotate_duplicate_sources([
            {"nasa_id": "100", "title": "Shared title"},
            {"nasa_id": "100", "title": "Different passage"},
            {"nasa_id": "101", "title": "Shared title"},
            {"title": "Shared title"},
        ])
        self.assertTrue(records[0]["duplicate_source"]["is_duplicate"])
        self.assertEqual(records[0]["duplicate_source"]["group_size"], 2)
        self.assertEqual(
            records[0]["duplicate_source"]["independence_status"],
            "unknown",
        )
        self.assertFalse(records[2]["duplicate_source"]["is_duplicate"])
        self.assertIsNone(source_identity(records[3])["group_key"])
        self.assertIn("stable nasa_id", records[0]["duplicate_source"]["explanation"])

    def test_contract_exposes_source_type_and_preserves_score(self):
        result = build_ranking_contract(
            query="flame spread",
            original_score=0.41,
            record={
                "source_id": "BASS2:PI:1",
                "source_type": "bass_ii",
                "exact_source_excerpt": "Flame spread record.",
                "evidence_type": "experimental_metadata",
            },
            source_text="Flame spread record.",
        )
        self.assertEqual(result["original_score"], 0.41)
        self.assertEqual(result["source_type"], "bass_ii")
        self.assertEqual(result["evidence_scope"], "experimental_metadata")
        self.assertIn("source_identity", result)

    def test_nested_local_provenance_is_normalized_without_invention(self):
        result = build_ranking_contract(
            query="flame spread in microgravity",
            original_score=0.9,
            record={
                "source_type": "local_nasa_passage",
                "source": {
                    "source_id": "123",
                    "citation_url": "https://ntrs.nasa.gov/citations/123",
                    "pdf_page_number": 4,
                },
                "classification": {
                    "evidence_role": "experimental_result",
                    "review_status": "requires_manual_review",
                },
                "review": {
                    "source_review_status": "requires_manual_review",
                },
                "exact_source_excerpt": "Flame spread in microgravity.",
            },
            source_text="Flame spread in microgravity.",
        )
        fields = result["provenance"]["fields"]
        self.assertEqual(fields["nasa_id"]["value"], "123")
        self.assertEqual(fields["source_url"]["value"], "https://ntrs.nasa.gov/citations/123")
        self.assertEqual(fields["page_number_or_range"]["value"], 4)
        self.assertEqual(fields["evidence_type"]["value"], "experimental_result")
        self.assertEqual(fields["retrieval_date"]["status"], "missing")


if __name__ == "__main__":
    unittest.main()
