import unittest

from backend.services.claim_summarizer import (
    build_paper_summary,
    extract_claims,
)


class TestClaimSummarizerStep5(unittest.TestCase):
    def document(self):
        return {
            "nasa_id": "123",
            "citation_url": "https://ntrs.nasa.gov/citations/123",
            "sections": [
                {
                    "section_name": "abstract",
                    "text": "The study examined PMMA flame spread in microgravity.",
                    "page_numbers": [1],
                },
                {
                    "section_name": "experimental_setup",
                    "text": (
                        "PMMA samples were tested at 21 percent oxygen "
                        "and 10 cm/s flow."
                    ),
                    "page_numbers": [2, 3],
                },
                {
                    "section_name": "results",
                    "text": (
                        "The flame spread rate was 0.3 mm/s. "
                        "The observed flame became shorter."
                    ),
                    "page_numbers": [4],
                },
                {
                    "section_name": "discussion",
                    "text": "These results may indicate a flow effect.",
                    "page_numbers": [5],
                },
                {
                    "section_name": "conclusion",
                    "text": "The authors conclude that flow influenced spread.",
                    "page_numbers": [6],
                },
                {
                    "section_name": "limitations",
                    "text": "Measurement uncertainty was not reported.",
                    "page_numbers": [7],
                },
                {
                    "section_name": "introduction",
                    "text": "Combustion is important for spacecraft safety.",
                    "page_numbers": [1],
                },
            ],
        }

    def test_extracts_supported_claims_with_exact_provenance(self):
        result = extract_claims(self.document(), document_id="NASA-123")
        claim = next(
            item for item in result["claims"]
            if "0.3 mm/s" in item["claim_text"]
        )
        self.assertEqual(claim["claim_type"], "experimental_result")
        self.assertEqual(claim["source_document_id"], "NASA-123")
        self.assertEqual(claim["nasa_id"], "123")
        self.assertEqual(claim["page_numbers"], [4])
        self.assertEqual(claim["exact_supporting_excerpt"], claim["claim_text"])
        self.assertEqual(
            claim["verification_status"],
            "not_scientifically_verified",
        )

    def test_discussion_and_conclusion_are_not_results(self):
        result = extract_claims(self.document())
        types = {
            claim["claim_type"]
            for claim in result["claims"]
            if "flow" in claim["claim_text"].lower()
        }
        self.assertIn("discussion_interpretation", types)
        self.assertIn("conclusion", types)
        self.assertNotIn("experimental_result", types)
        self.assertTrue(all(
            claim["uncertain"]
            for claim in result["claims"]
            if claim["claim_type"] in {
                "discussion_interpretation", "conclusion"
            }
        ))

    def test_abstract_is_distinguished_from_experimental_evidence(self):
        result = extract_claims(self.document())
        abstract = next(
            claim for claim in result["claims"]
            if claim["claim_type"] == "abstract_statement"
        )
        self.assertEqual(abstract["evidence_type"], "abstract_statement")
        self.assertNotEqual(abstract["claim_type"], "experimental_result")

    def test_intro_text_is_rejected_as_claim_evidence(self):
        result = extract_claims(self.document())
        self.assertTrue(any(
            "Combustion is important" in item["text"]
            for item in result["rejected_claims"]
        ))
        self.assertFalse(any(
            "Combustion is important" in claim["claim_text"]
            for claim in result["claims"]
        ))

    def test_summary_statements_link_to_claims_and_reports_gaps(self):
        result = build_paper_summary(self.document(), document_id="NASA-123")
        claim_ids = {
            claim["claim_id"] for claim in result["claims"]
        }
        for statements in result["summary"].values():
            for statement in statements:
                self.assertTrue(set(statement["claim_ids"]) <= claim_ids)
                self.assertTrue(statement["evidence_sufficient"])
        self.assertFalse(any(
            gap["summary_field"] == "evidence_gaps"
            for gap in result["evidence_gaps"]
        ))
        self.assertFalse(result["scientific_findings_verified"])

    def test_empty_sections_never_create_unsupported_claims(self):
        result = extract_claims({
            "sections": [
                {
                    "section_name": "results",
                    "text": "",
                    "page_numbers": [1],
                },
            ],
        })
        self.assertEqual(result["claim_count"], 0)

    def test_uncertain_section_provenance_is_preserved(self):
        result = extract_claims({
            "sections": [{
                "section_name": "results_and_discussion",
                "text": "The result may indicate a flow effect.",
                "page_numbers": [2],
                "detection_uncertain": True,
            }],
        })
        self.assertEqual(result["claim_count"], 1)
        self.assertTrue(result["claims"][0]["uncertain"])
        self.assertEqual(
            result["claims"][0]["evidence_type"],
            "results_and_discussion_statement",
        )

    def test_multiple_excerpts_can_support_one_claim(self):
        result = extract_claims(
            self.document(),
            additional_evidence=[{
                "claim_text": "The observed flame became shorter.",
                "exact_supporting_excerpt": (
                    "The observed flame became shorter under reduced gravity."
                ),
                "page_numbers": [8],
                "section_name": "results",
                "evidence_type": "experimental_results",
            }],
        )
        claim = next(
            item for item in result["claims"]
            if item["claim_text"] == "The observed flame became shorter."
        )
        self.assertEqual(len(claim["supporting_evidence"]), 2)
        self.assertEqual(
            claim["supporting_evidence"][1]["page_numbers"], [8]
        )


if __name__ == "__main__":
    unittest.main()
