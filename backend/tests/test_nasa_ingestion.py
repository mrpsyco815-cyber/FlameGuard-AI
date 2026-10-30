import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from backend.services import nasa_ingestion


class TestNASAIngestion(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

        self.metadata = {
            "id": "20080034883",
            "title": "Microgravity Flame Spread in Exploration Atmospheres",
            "abstract": "Research on pressure, oxygen, and flame spread.",
            "authorAffiliations": [],
            "publications": [],
            "disseminated": "DOCUMENT_AND_METADATA",
            "copyright": None,
        }

    def tearDown(self):
        self.temp_dir.cleanup()

    def configure_successful_import(self):
        response = Mock()
        response.json.return_value = self.metadata
        response.raise_for_status.return_value = None

        pages = {
            "success": True,
            "nasa_id": "20080034883",
            "title": self.metadata["title"],
            "pdf_path": "data/raw/nasa_pdf/20080034883.pdf",
            "pdf_page_count": 2,
            "pages_with_extracted_text": 1,
            "pages_without_extracted_text": 1,
            "pages": [
                {
                    "pdf_page_number": 1,
                    "text": (
                        "Experimental flame spread changed with "
                        "the ambient pressure. "
                        "Oxygen concentration affected the flame behaviour."
                    ),
                },
                {
                    "pdf_page_number": 2,
                    "text": "",
                },
            ],
        }

        return response, pages

    @patch("backend.services.nasa_ingestion.classify_passage_v3_4")
    @patch("backend.services.nasa_ingestion.extract_pdf_pages")
    @patch("backend.services.nasa_ingestion.audit_pdf_identity")
    @patch("backend.services.nasa_ingestion.download_nasa_pdf")
    @patch("backend.services.nasa_ingestion.requests.get")
    def test_imports_pdf_passages_and_preserves_provenance(
        self,
        get_request,
        download_pdf,
        identity_audit,
        extract_pages,
        classify,
    ):
        response, pages = self.configure_successful_import()
        get_request.return_value = response
        download_pdf.return_value = {"success": True}
        identity_audit.return_value = {
            "success": True,
            "visible_title_matches_api": True,
            "identity_audit_status": "identity_consistent",
        }
        extract_pages.return_value = pages
        classify.return_value = {
            "evidence_role": "experimental_quantitative_result",
            "evidence_modality": "experiment",
            "classification_version": "3.4",
            "scientific_findings_verified": False,
        }

        result = nasa_ingestion.import_nasa_document(
            "20080034883",
            project_root=self.root,
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["status"], "imported_pending_review")
        self.assertEqual(result["passage_count"], 2)
        self.assertEqual(result["empty_pages"], 1)

        collection_path = (
            self.root / nasa_ingestion.COLLECTION_RELATIVE_PATH
        )
        collection = json.loads(
            collection_path.read_text(encoding="utf-8")
        )

        self.assertEqual(len(collection["documents"]), 1)
        self.assertEqual(len(collection["records"]), 2)

        record = collection["records"][0]
        self.assertEqual(record["source"]["source_id"], "20080034883")
        self.assertEqual(record["source"]["pdf_page_number"], 1)
        self.assertEqual(
            record["review"]["source_review_status"],
            "requires_manual_review",
        )
        self.assertFalse(record["review"]["scientific_findings_verified"])
        self.assertEqual(
            record["provenance"]["import_origin"],
            "live_nasa_ntrs",
        )

    @patch("backend.services.nasa_ingestion.requests.get")
    def test_invalid_pdf_identity_prevents_ingestion(self, get_request):
        response, _ = self.configure_successful_import()
        get_request.return_value = response

        with patch(
            "backend.services.nasa_ingestion.download_nasa_pdf",
            return_value={"success": True},
        ), patch(
            "backend.services.nasa_ingestion.audit_pdf_identity",
            return_value={
                "success": True,
                "visible_title_matches_api": False,
                "identity_audit_status": "manual_review_required",
            },
        ), patch(
            "backend.services.nasa_ingestion.extract_pdf_pages"
        ) as extract_pages:
            result = nasa_ingestion.import_nasa_document(
                "20080034883",
                project_root=self.root,
            )

        self.assertFalse(result["success"])
        self.assertEqual(
            result["status"],
            "pdf_identity_requires_manual_review",
        )
        extract_pages.assert_not_called()

        collection_path = (
            self.root / nasa_ingestion.COLLECTION_RELATIVE_PATH
        )
        self.assertFalse(collection_path.exists())

    def test_same_nasa_document_is_not_imported_twice(self):
        collection_path = (
            self.root / nasa_ingestion.COLLECTION_RELATIVE_PATH
        )
        collection_path.parent.mkdir(parents=True, exist_ok=True)
        collection_path.write_text(
            json.dumps({
                "collection_name": "Test",
                "schema_version": "1.0",
                "documents": [{
                    "nasa_id": "20080034883",
                    "title": "Previously imported study",
                    "passage_count": 12,
                }],
                "records": [],
            }),
            encoding="utf-8",
        )

        with patch(
            "backend.services.nasa_ingestion.requests.get"
        ) as get_request:
            result = nasa_ingestion.import_nasa_document(
                "20080034883",
                project_root=self.root,
            )

        self.assertTrue(result["success"])
        self.assertEqual(result["status"], "already_imported")
        get_request.assert_not_called()

    def test_rejects_invalid_nasa_id(self):
        result = nasa_ingestion.import_nasa_document(
            "../bad-id",
            project_root=self.root,
        )
        self.assertFalse(result["success"])
        self.assertEqual(result["status"], "invalid_nasa_id")


if __name__ == "__main__":
    unittest.main()
