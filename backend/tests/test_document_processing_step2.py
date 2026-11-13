import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import pymupdf

from backend.services.document_parser import extract_pdf_pages
from backend.services.nasa_online import search_nasa_online


class TestPDFExtractionDiagnostics(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.pdf_path = self.root / "sample.pdf"
        self.output_dir = self.root / "pages"

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_pdf(self, pages):
        document = pymupdf.open()
        for text in pages:
            page = document.new_page()
            if text:
                page.insert_text((72, 72), text)
        document.save(self.pdf_path)
        document.close()

    def test_valid_multipage_pdf_preserves_order_and_pages(self):
        self.write_pdf(["first page", "second page", "third page"])

        result = extract_pdf_pages(
            "123",
            pdf_path=self.pdf_path,
            output_dir=self.output_dir,
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["extraction_status"], "success")
        self.assertEqual(result["pdf_page_count"], 3)
        self.assertEqual(result["pages_with_extracted_text"], 3)
        self.assertEqual(
            [page["pdf_page_number"] for page in result["pages"]],
            [1, 2, 3],
        )
        self.assertEqual(
            [page["text"] for page in result["pages"]],
            ["first page", "second page", "third page"],
        )
        self.assertEqual(result["citation_url"], "https://ntrs.nasa.gov/citations/123")

    def test_empty_page_is_reported_as_partial_extraction(self):
        self.write_pdf(["first page", "", "third page"])

        result = extract_pdf_pages(
            "123",
            pdf_path=self.pdf_path,
            output_dir=self.output_dir,
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["extraction_status"], "partial_extraction")
        self.assertEqual(result["pages_with_extracted_text"], 2)
        self.assertEqual(result["pages_without_extracted_text"], 1)
        self.assertEqual(result["pages"][1]["text_extraction_status"], "no_text_extracted")
        self.assertEqual(result["pages"][1]["pdf_page_number"], 2)

    def test_valid_pdf_with_no_text_reports_ocr_required(self):
        self.write_pdf(["", ""])

        result = extract_pdf_pages(
            "123",
            pdf_path=self.pdf_path,
            output_dir=self.output_dir,
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["extraction_status"], "no_extractable_text")
        self.assertEqual(
            result["extraction_message"],
            "OCR required or text extraction unavailable.",
        )
        self.assertEqual(result["pages_with_extracted_text"], 0)

    def test_malformed_pdf_fails_as_invalid_pdf(self):
        self.pdf_path.write_bytes(b"%PDF-corrupt")

        result = extract_pdf_pages(
            "123",
            pdf_path=self.pdf_path,
            output_dir=self.output_dir,
        )

        self.assertFalse(result["success"])
        self.assertEqual(result["extraction_status"], "invalid_pdf")
        self.assertTrue(result["error"])

    def test_missing_pdf_is_explicit(self):
        result = extract_pdf_pages(
            "123",
            pdf_path=self.root / "missing.pdf",
            output_dir=self.output_dir,
        )

        self.assertFalse(result["success"])
        self.assertEqual(result["extraction_status"], "invalid_pdf")
        self.assertIn("PDF not found", result["error"])


class TestAbstractOnlyScope(unittest.TestCase):
    @patch("backend.services.nasa_online.requests.get")
    def test_abstract_only_record_is_not_full_text(self, get):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "results": [{
                "id": "123",
                "title": "Abstract-only study",
                "abstract": "A study abstract.",
            }]
        }
        get.return_value = response

        result = search_nasa_online("study", limit=1)
        item = result["results"][0]

        self.assertEqual(item["evidence_type"], "bibliographic_metadata_and_abstract")
        self.assertFalse(item["full_text_retrieved"])
        self.assertFalse(item["scientific_findings_verified"])
        self.assertEqual(item["nasa_id"], "123")
        self.assertEqual(item["source_url"], "https://ntrs.nasa.gov/citations/123")
