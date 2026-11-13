import tempfile
import time
import unittest
from pathlib import Path

import pymupdf

from backend.services.claim_summarizer import extract_claims
from backend.services.document_parser import extract_pdf_pages
from backend.services.human_review import (
    build_review_queue,
    record_review_decision,
)
from backend.services.mission_research_brief import build_mission_research_brief
from backend.services.scientific_synthesis import synthesize_documents


def write_pdf(path: Path, pages: list[str]) -> None:
    document = pymupdf.open()
    for text in pages:
        page = document.new_page()
        for line_index, line in enumerate(text.splitlines()):
            page.insert_text((72, 72 + line_index * 18), line)
    document.save(path)
    document.close()


def mission_context():
    return {
        "research_question": "How does PMMA flame spread under the supplied conditions?",
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


class TestSummarizationEndToEndStep8(unittest.TestCase):
    def make_pdf(self, directory, name, measurement="0.3"):
        path = Path(directory) / f"{name}.pdf"
        write_pdf(path, [
            "Abstract\nThe study examined PMMA flame spread.",
            (
                "Experimental Setup\n"
                "PMMA samples were tested in microgravity at 21 percent oxygen.\n"
                "Ambient pressure 100 kPa.\n"
                "Temperature 300 K.\n"
                "Forced flow velocity was 10 cm/s."
            ),
            (
                "Results\n"
                f"The flame spread rate was {measurement} mm/s.\n"
                "The observed flame became shorter."
            ),
            (
                "Discussion\nThese results may indicate a flow effect.\n"
                "Conclusion\nThe authors conclude that flow influenced spread."
            ),
        ])
        return path

    def test_pdf_to_mission_brief_preserves_pipeline_and_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            first = extract_pdf_pages(
                "801",
                self.make_pdf(directory, "first"),
                Path(directory) / "out",
            )
            second = extract_pdf_pages(
                "802",
                self.make_pdf(directory, "second", "0.5"),
                Path(directory) / "out",
            )
            self.assertTrue(first["success"])
            self.assertEqual(first["extraction_status"], "success")
            self.assertTrue(first["sections"])
            self.assertTrue(first["structured_findings"]["evidence"])
            self.assertTrue(first["claim_summary"]["claims"])

            synthesis = synthesize_documents([first, second])
            self.assertTrue(synthesis["comparable_study_groups"])
            self.assertTrue(synthesis["potential_disagreements"])
            disagreement = synthesis["potential_disagreements"][0]
            self.assertEqual(
                disagreement["supporting_claims"][0]["page_numbers"], [3]
            )
            self.assertIn("mm/s", disagreement["supporting_claims"][0][
                "exact_supporting_excerpt"
            ])

            brief = build_mission_research_brief(
                mission_context(),
                [first, second],
                synthesis=synthesis,
            )
            self.assertEqual(len(brief["comparable_studies"]), 2)
            self.assertTrue(brief["scientific_observations"])
            self.assertFalse(brief["scientific_findings_verified"])
            self.assertIn("source_document_id", brief["source_references"][0])
            self.assertTrue(
                brief["comparable_studies"][0]["supporting_claim_ids"]
            )

    def test_human_review_queue_is_explicit_and_never_verifies(self):
        document = {
            "claim_summary": {
                "claims": [{
                    "claim_id": "claim-001",
                    "claim_text": "The flame spread rate was 0.3 mm/s.",
                    "claim_type": "experimental_result",
                    "source_document_id": "NASA-801",
                    "nasa_id": "801",
                    "source_url": "https://ntrs.nasa.gov/citations/801",
                    "exact_supporting_excerpt": (
                        "The flame spread rate was 0.3 mm/s."
                    ),
                    "page_numbers": [3],
                    "section_name": "results",
                    "evidence_type": "experimental_results",
                    "uncertain": False,
                    "verification_status": "not_scientifically_verified",
                    "supporting_evidence": [{
                        "exact_supporting_text": (
                            "The flame spread rate was 0.3 mm/s."
                        ),
                    }],
                }],
            },
        }
        queue = build_review_queue(document, reviewer_id="reviewer-a")
        self.assertEqual(queue["review_status"], "pending_review")
        self.assertEqual(queue["items"][0]["reviewer_decision"], None)
        reviewed = record_review_decision(
            queue,
            "review-001",
            "accepted",
            reviewer_id="reviewer-a",
            notes="Evidence excerpt inspected.",
        )
        self.assertEqual(reviewed["review_status"], "reviewed")
        self.assertFalse(reviewed["scientific_findings_verified"])

    def test_human_review_queue_can_start_from_raw_parsed_document(self):
        document = {
            "document_id": "NASA-805",
            "nasa_id": "805",
            "citation_url": "https://ntrs.nasa.gov/citations/805",
            "sections": [{
                "section_name": "results",
                "text": "The flame spread rate was 0.3 mm/s.",
                "page_numbers": [2],
            }],
        }
        queue = build_review_queue(document)
        self.assertEqual(len(queue["items"]), 1)
        self.assertEqual(queue["items"][0]["page_numbers"], [2])
        self.assertFalse(queue["scientific_findings_verified"])

    def test_abstract_only_and_missing_conditions_do_not_create_exact_match(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "abstract.pdf"
            write_pdf(path, [
                "Abstract\nThe study examined PMMA combustion in microgravity."
            ])
            document = extract_pdf_pages(
                "803", path, Path(directory) / "out"
            )
            brief = build_mission_research_brief(
                mission_context(), [document]
            )
            self.assertFalse(brief["comparable_studies"])
            self.assertEqual(
                brief["partially_comparable_studies"][0]["comparison"],
                "partial_match",
            )
            self.assertFalse(brief["scientific_observations"])

    def test_pipeline_latency_is_measured_not_asserted_against_target(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.make_pdf(directory, "timed")
            start = time.perf_counter()
            document = extract_pdf_pages(
                "804", path, Path(directory) / "out"
            )
            extraction_seconds = time.perf_counter() - start
            start = time.perf_counter()
            extract_claims(document)
            claim_seconds = time.perf_counter() - start
            start = time.perf_counter()
            synthesize_documents([document])
            synthesis_seconds = time.perf_counter() - start
            start = time.perf_counter()
            build_mission_research_brief(mission_context(), [document])
            brief_seconds = time.perf_counter() - start
            self.assertTrue(document["success"])
            self.assertGreaterEqual(extraction_seconds, 0)
            self.assertGreaterEqual(claim_seconds, 0)
            self.assertGreaterEqual(synthesis_seconds, 0)
            self.assertGreaterEqual(brief_seconds, 0)


if __name__ == "__main__":
    unittest.main()
