import tempfile
import unittest
from pathlib import Path

import pymupdf

from backend.services.document_parser import (
    extract_pdf_pages,
    extract_sections_from_pages,
)


class TestSectionExtractionStep3(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.pdf_path = self.root / "sections.pdf"

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_pdf(self, pages):
        document = pymupdf.open()
        for text in pages:
            page = document.new_page()
            page.insert_textbox((50, 50, 550, 780), text)
        document.save(self.pdf_path)
        document.close()

    def test_standard_structure_preserves_order_and_content(self):
        pages = [
            {
                "pdf_page_number": 1,
                "text": (
                    "Title and author information.\n"
                    "Abstract\nAbstract text.\n"
                    "1. Introduction\nIntroduction text."
                ),
            },
            {
                "pdf_page_number": 2,
                "text": "Methods\nMethods text.\nResults\nResults text.",
            },
            {
                "pdf_page_number": 3,
                "text": "Discussion\nDiscussion text.\nConclusion\nConclusion text.",
            },
            {
                "pdf_page_number": 4,
                "text": "References\nReference entry.",
            },
        ]

        result = extract_sections_from_pages(pages)
        names = [section["section_name"] for section in result["sections"]]

        self.assertEqual(
            names,
            [
                "abstract",
                "introduction",
                "methodology_methods",
                "results",
                "discussion",
                "conclusion",
                "references",
            ],
        )
        self.assertEqual(result["sections"][0]["page_start"], 1)
        self.assertEqual(result["sections"][-1]["page_end"], 4)
        self.assertIn("Abstract text.", result["sections"][0]["text"])
        self.assertIn("Results text.", result["sections"][3]["text"])

    def test_heading_capitalization_and_numbered_subsections(self):
        pages = [{
            "pdf_page_number": 1,
            "text": (
                "2. BACKGROUND\nBackground text.\n"
                "3.2 Experimental Setup\nSetup text.\n"
                "3.3 EXPERIMENTAL METHODS\nMethods text."
            ),
        }]

        result = extract_sections_from_pages(pages)
        self.assertEqual(
            [section["section_name"] for section in result["sections"]],
            [
                "background_related_work",
                "experimental_setup",
                "methodology_methods",
            ],
        )
        self.assertEqual(result["sections"][1]["section_level"], 2)
        self.assertEqual(result["sections"][1]["heading"], "3.2 Experimental Setup")

    def test_sections_span_pages_and_include_empty_pages_in_page_span(self):
        pages = [
            {"pdf_page_number": 1, "text": "Introduction\nFirst part."},
            {"pdf_page_number": 2, "text": ""},
            {"pdf_page_number": 3, "text": "Second part."},
            {"pdf_page_number": 4, "text": "Results\nResult text."},
        ]

        result = extract_sections_from_pages(pages)
        introduction = result["sections"][0]

        self.assertEqual(introduction["page_start"], 1)
        self.assertEqual(introduction["page_end"], 3)
        self.assertEqual(introduction["page_numbers"], [1, 2, 3])
        self.assertIn("First part.", introduction["text"])
        self.assertIn("Second part.", introduction["text"])

    def test_missing_sections_are_absent(self):
        result = extract_sections_from_pages([{
            "pdf_page_number": 1,
            "text": "Abstract\nOnly abstract text.",
        }])

        self.assertEqual(result["section_count"], 1)
        self.assertNotIn(
            "results",
            [section["section_name"] for section in result["sections"]],
        )

    def test_multiple_subsections_are_kept_in_order(self):
        result = extract_sections_from_pages([{
            "pdf_page_number": 1,
            "text": (
                "3 Methods\nOverview.\n"
                "3.1 Experimental Setup\nSetup.\n"
                "3.2 Methods\nProcedure."
            ),
        }])

        self.assertEqual(
            [section["heading"] for section in result["sections"]],
            ["3 Methods", "3.1 Experimental Setup", "3.2 Methods"],
        )

    def test_references_are_detected(self):
        result = extract_sections_from_pages([{
            "pdf_page_number": 1,
            "text": "References\n[1] Source entry.",
        }])

        self.assertEqual(result["sections"][0]["section_name"], "references")
        self.assertEqual(result["sections"][0]["text"], "[1] Source entry.")

    def test_combined_heading_is_flagged_uncertain(self):
        result = extract_sections_from_pages([{
            "pdf_page_number": 1,
            "text": "Results and Discussion\nCombined text.",
        }])

        section = result["sections"][0]
        self.assertEqual(section["section_name"], "results_and_discussion")
        self.assertTrue(section["detection_uncertain"])
        self.assertTrue(section["uncertainty_reason"])

    def test_unclassified_text_is_preserved(self):
        result = extract_sections_from_pages([{
            "pdf_page_number": 1,
            "text": (
                "Document title and author.\n"
                "Introduction\n"
                "Introduction text."
            ),
        }])

        self.assertTrue(result["unclassified_text"])
        self.assertIn(
            "Document title and author.",
            result["unclassified_text"][0]["text"],
        )

    def test_pdf_pipeline_adds_sections_without_changing_pages(self):
        self.write_pdf([
            "Abstract\nAbstract text.",
            "",
            "Conclusion\nConclusion text.",
        ])

        result = extract_pdf_pages(
            "123",
            pdf_path=self.pdf_path,
            output_dir=self.root / "output",
        )

        self.assertEqual(result["extraction_status"], "partial_extraction")
        self.assertEqual(
            [page["pdf_page_number"] for page in result["pages"]],
            [1, 2, 3],
        )
        self.assertEqual(
            [section["section_name"] for section in result["sections"]],
            ["abstract", "conclusion"],
        )
        self.assertEqual(result["sections"][0]["page_start"], 1)
        self.assertEqual(result["sections"][1]["page_start"], 3)

