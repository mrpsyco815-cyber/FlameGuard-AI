import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.main import app
from backend.services.mission_intelligence_orchestrator import (
    build_mission_intelligence_orchestration,
)
from backend.services.review_store import (
    create_review,
    get_review,
    list_reviews,
    review_history,
    update_review,
)


class TestReviewStore(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.db_path = Path(self.directory.name) / "reviews.sqlite3"

    def tearDown(self):
        self.directory.cleanup()

    def test_create_update_history_and_persistence(self):
        review = create_review(
            target_type="claim",
            target_id="NASA-1-claim",
            status="pending",
            reviewer_id="alice",
            db_path=self.db_path,
        )
        self.assertEqual(review["review_status"] if "review_status" in review else review["status"], "pending")
        updated = update_review(
            review["review_id"],
            status="accepted",
            reviewer_notes="Excerpt inspected.",
            db_path=self.db_path,
        )
        self.assertEqual(updated["status"], "accepted")
        self.assertFalse(updated["scientific_findings_verified"])
        self.assertEqual(len(review_history(review["review_id"], db_path=self.db_path)), 2)
        self.assertEqual(len(list_reviews(status="accepted", db_path=self.db_path)), 1)
        self.assertEqual(get_review(review["review_id"], db_path=self.db_path)["revision"], 2)

    def test_invalid_status_and_target_are_rejected(self):
        with self.assertRaises(ValueError):
            create_review(target_type="claim", target_id="x", status="verified", db_path=self.db_path)
        with self.assertRaises(ValueError):
            create_review(target_type="unknown", target_id="x", db_path=self.db_path)
        with self.assertRaises(ValueError):
            create_review(target_type="claim", target_id="bad id", db_path=self.db_path)
        with self.assertRaises(ValueError):
            create_review(target_type="claim", target_id="../db", db_path=self.db_path)

    def test_numeric_nasa_identifier_is_preserved_as_string(self):
        review = create_review(
            target_type="paper",
            target_id="19960008415",
            db_path=self.db_path,
        )
        self.assertEqual(review["target_id"], "19960008415")
        self.assertEqual(
            get_review(review["review_id"], db_path=self.db_path)["target_id"],
            "19960008415",
        )

    def test_identity_is_not_authenticated(self):
        review = create_review(
            target_type="paper",
            target_id="P1",
            reviewer_id="client-user",
            db_path=self.db_path,
        )
        self.assertEqual(
            review["reviewer_identity_status"],
            "unverified_client_supplied",
        )


class TestMissionOrchestration(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.store_path = Path(self.directory.name) / "store.json"
        self.store_path.write_text(json.dumps({"records": []}), encoding="utf-8")
        self.db_path = Path(self.directory.name) / "reviews.sqlite3"

    def tearDown(self):
        self.directory.cleanup()

    @patch("backend.services.mission_intelligence_orchestrator.build_research_comparison")
    def test_empty_workflow_is_conservative(self, compare):
        compare.return_value = {
            "retrieval": {"fallback_triggered": True},
            "evidence": {"papers": [], "claims": []},
            "comparison": {"sources": [], "condition_comparisons": []},
            "conflicts": [],
            "research_gaps": [],
            "suggested_research_questions": [],
        }
        result = build_mission_intelligence_orchestration(
            "flame spread",
            mission_context={"mission": "spacecraft"},
            review_db_path=self.db_path,
            store_path=self.store_path,
        )
        self.assertEqual(
            result["conclusion"],
            "Insufficient verified evidence to support a mission-specific recommendation.",
        )
        self.assertFalse(result["scientific_findings_verified"])

    @patch("backend.services.mission_intelligence_orchestrator.build_research_comparison")
    def test_review_status_and_simulation_are_preserved(self, compare):
        paper = {
            "document_id": "SIM-1",
            "nasa_id": "SIM-1",
            "source_url": "https://example.test/sim",
            "source_type": "local_nasa_passage",
            "evidence_classification": "simulation_result",
            "verification_status": "not_scientifically_verified",
            "review_status": "pending",
            "claims": [{
                "claim_id": "SIM-1-claim",
                "claim_text": "The model predicted a shorter flame.",
                "claim_type": "discussion_interpretation",
                "source_document_id": "SIM-1",
                "nasa_id": "SIM-1",
                "source_url": "https://example.test/sim",
                "exact_supporting_excerpt": "The model predicted a shorter flame.",
                "page_numbers": [2],
                "section_name": "discussion",
                "evidence_type": "discussion_interpretation",
                "verification_status": "not_scientifically_verified",
                "uncertain": True,
            }],
            "structured_findings": {"source": {"document_id": "SIM-1", "nasa_id": "SIM-1", "source_url": "https://example.test/sim"}, "fields": {}},
        }
        compare.return_value = {
            "retrieval": {"fallback_triggered": False},
            "evidence": {"papers": [paper], "claims": paper["claims"]},
            "comparison": {"sources": [paper], "condition_comparisons": []},
            "conflicts": [],
            "research_gaps": [],
            "suggested_research_questions": [],
        }
        create_review(
            target_type="claim",
            target_id="SIM-1-claim",
            status="accepted",
            db_path=self.db_path,
        )
        result = build_mission_intelligence_orchestration(
            "flame",
            mission_context={"mission": "spacecraft"},
            review_db_path=self.db_path,
            store_path=self.store_path,
        )
        self.assertTrue(result["reviews"]["accepted_review_present"])
        self.assertFalse(result["scientific_findings_verified"])
        self.assertIn("Insufficient verified evidence", result["conclusion"])

    @patch("backend.services.mission_intelligence_orchestrator.build_research_comparison")
    def test_numeric_nasa_identifier_review_lookup(self, compare):
        paper = {
            "document_id": 19960008415,
            "nasa_id": 19960008415,
            "claims": [],
            "structured_findings": {"source": {}, "fields": {}},
        }
        compare.return_value = {
            "retrieval": {},
            "evidence": {"papers": [paper], "claims": []},
            "comparison": {"sources": [], "condition_comparisons": []},
            "conflicts": [],
            "research_gaps": [],
            "suggested_research_questions": [],
        }
        create_review(
            target_type="paper",
            target_id="19960008415",
            status="accepted",
            db_path=self.db_path,
        )
        result = build_mission_intelligence_orchestration(
            "flame",
            review_db_path=self.db_path,
        )
        self.assertTrue(result["reviews"]["accepted_review_present"])
        self.assertEqual(
            result["reviews"]["records"][0]["target_id"],
            "19960008415",
        )


class TestPhase3API(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.db_path = Path(self.directory.name) / "reviews.sqlite3"
        self.previous_db_path = getattr(app.state, "review_db_path", None)
        app.state.review_db_path = self.db_path

    def tearDown(self):
        if self.previous_db_path is None:
            try:
                del app.state.review_db_path
            except AttributeError:
                pass
        else:
            app.state.review_db_path = self.previous_db_path
        self.directory.cleanup()

    def test_invalid_mission_request(self):
        client = TestClient(app)
        response = client.post("/research/mission-intelligence", json={})
        self.assertEqual(response.status_code, 400)

    def test_review_api_create_get_update(self):
        client = TestClient(app)
        created = client.post("/research/reviews", json={
            "target_type": "claim",
            "target_id": "api-claim",
            "status": "pending",
        })
        self.assertEqual(created.status_code, 200)
        review_id = created.json()["review_id"]
        fetched = client.get(f"/research/reviews/{review_id}")
        self.assertEqual(fetched.status_code, 200)
        listed = client.get("/research/reviews?target_type=claim&target_id=api-claim")
        self.assertEqual(listed.status_code, 200)
        self.assertEqual(listed.json()["count"], 1)
        updated = client.patch(
            f"/research/reviews/{review_id}",
            json={"status": "accepted"},
        )
        self.assertEqual(updated.status_code, 200)
        self.assertFalse(updated.json()["scientific_findings_verified"])
        history = client.get(f"/research/reviews/{review_id}/history")
        self.assertEqual(history.status_code, 200)
        self.assertEqual(len(history.json()["history"]), 2)

    def test_public_api_rejects_client_database_path(self):
        client = TestClient(app)
        response = client.post("/research/reviews", json={
            "target_type": "claim",
            "target_id": "path-test",
            "db_path": str(self.db_path.parent / "arbitrary.sqlite3"),
        })
        self.assertEqual(response.status_code, 400)
        self.assertFalse((self.db_path.parent / "arbitrary.sqlite3").exists())

    @patch("backend.services.mission_intelligence_orchestrator.build_research_comparison")
    def test_mission_api_accepts_numeric_nasa_ids(self, compare):
        compare.return_value = {
            "retrieval": {},
            "evidence": {
                "papers": [{
                    "document_id": 19960008415,
                    "nasa_id": 19960008415,
                    "claims": [],
                    "structured_findings": {"source": {}, "fields": {}},
                }],
                "claims": [],
            },
            "comparison": {"sources": [], "condition_comparisons": []},
            "conflicts": [],
            "research_gaps": [],
            "suggested_research_questions": [],
        }
        client = TestClient(app)
        response = client.post("/research/mission-intelligence", json={
            "query": "oxygen microgravity",
            "limit": 1,
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["scientific_findings_verified"])
