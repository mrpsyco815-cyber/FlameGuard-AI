import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.main import app
from backend.services.research_insights import (
    build_research_comparison,
    build_research_insights,
)


class TestResearchInsights(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.store_path = Path(self.temp_dir.name) / "store.json"
        self.store_path.write_text(json.dumps({"records": []}), encoding="utf-8")

    def tearDown(self):
        self.temp_dir.cleanup()

    def federation(self, local=None, online=None, conflict=None):
        return {
            "search_strategy": "local_first_with_nasa_ntrs_fallback",
            "fallback_triggered": bool(online),
            "fallback_reason": ["too_few_local_passages"] if online else [],
            "missing_query_concepts": [],
            "local_evidence_brief": {"results": local or []},
            "online_search": online or {
                "performed": False,
                "count": 0,
                "results": [],
                "content_scope": "not_searched",
                "fallback_attempted": False,
            },
            "conflict_report": conflict or {
                "conflicts": [], "count": 0, "limitations": []
            },
            "counts": {"local_passages_returned": len(local or [])},
        }

    @patch("backend.services.research_insights.search_research_with_fallback")
    def test_end_to_end_provenance_and_classification(self, search):
        search.return_value = self.federation(local=[{
            "record_id": "P-1",
            "source_id": "NASA-1",
            "source_title": "Study",
            "citation_url": "https://ntrs.nasa.gov/citations/NASA-1",
            "pdf_page_number": 4,
            "evidence_role": "experimental_quantitative_result",
            "classification_review_status": "requires_manual_review",
            "exact_source_excerpt": "The flame spread rate was 0.3 mm/s.",
            "scientific_findings_verified": False,
        }])
        result = build_research_insights(
            "flame spread", store_path=self.store_path
        )
        self.assertEqual(result["evidence"]["claim_count"], 1)
        claim = result["evidence"]["claims"][0]
        self.assertEqual(claim["nasa_id"], "NASA-1")
        self.assertEqual(claim["source_url"], "https://ntrs.nasa.gov/citations/NASA-1")
        self.assertEqual(claim["page_numbers"], [4])
        self.assertEqual(claim["evidence_type"], "experimental_results")
        self.assertEqual(claim["review_status"], "requires_manual_review")
        self.assertFalse(claim["scientific_findings_verified"])
        self.assertEqual(result["recommendation"],
                         "Insufficient verified evidence to support a mission-specific recommendation.")

    @patch("backend.services.research_insights.search_research_with_fallback")
    def test_online_fallback_metadata_and_abstract_are_preserved(self, search):
        online = {
            "performed": True,
            "status": "completed",
            "original_query": "long question",
            "nasa_query": "flame spread microgravity",
            "fallback_attempted": True,
            "fallback_reason": "original_query_returned_zero_results",
            "original_result_count": 0,
            "fallback_result_count": 1,
            "count": 1,
            "content_scope": "bibliographic_metadata_and_abstract_only",
            "results": [{
                "nasa_id": "NASA-2",
                "title": "Catalog study",
                "source_url": "https://ntrs.nasa.gov/citations/NASA-2",
                "abstract": "The study examined flame spread.",
                "evidence_type": "bibliographic_metadata_and_abstract",
                "scientific_findings_verified": False,
                "verification_status": "metadata_retrieved",
            }],
        }
        search.return_value = self.federation(online=online)
        result = build_research_insights(
            "long question", store_path=self.store_path
        )
        self.assertEqual(
            result["retrieval"]["online_search"]["nasa_query"],
            "flame spread microgravity",
        )
        paper = result["evidence"]["papers"][0]
        self.assertEqual(paper["evidence_classification"],
                         "bibliographic_metadata_and_abstract")
        self.assertFalse(paper["scientific_findings_verified"])
        self.assertEqual(paper["claims"][0]["claim_type"], "abstract_statement")

    @patch("backend.services.research_insights.search_research_with_fallback")
    def test_zero_evidence_and_conflicts_are_honest(self, search):
        conflict = {
            "conflicts": [{
                "conflict_status": "unresolved_disagreement",
                "review_status": "requires_scientific_review",
            }],
            "count": 1,
            "limitations": [],
        }
        search.return_value = self.federation(conflict=conflict)
        result = build_research_insights(
            "unknown question", store_path=self.store_path
        )
        self.assertEqual(result["evidence"]["paper_count"], 0)
        self.assertEqual(result["evidence"]["claim_count"], 0)
        self.assertEqual(result["conflict_report"]["count"], 1)
        self.assertEqual(
            result["recommendation"],
            "Insufficient verified evidence to support a mission-specific recommendation.",
        )

    @patch("backend.services.research_insights.search_research_with_fallback")
    def test_simulation_is_not_relabelled_as_experiment(self, search):
        search.return_value = self.federation(local=[{
            "record_id": "S-1",
            "source_id": "NASA-SIM",
            "source_title": "Simulation",
            "citation_url": "https://example.test/sim",
            "evidence_role": "simulation_result",
            "exact_source_excerpt": "The model predicted a shorter flame.",
        }])
        result = build_research_insights(
            "flame", store_path=self.store_path
        )
        claim = result["evidence"]["claims"][0]
        self.assertEqual(claim["claim_type"], "discussion_interpretation")
        self.assertEqual(claim["evidence_classification"], "simulation_result")
        self.assertFalse(claim["scientific_findings_verified"])

    @patch("backend.services.research_insights.search_research_with_fallback")
    def test_missing_provenance_is_not_invented(self, search):
        search.return_value = self.federation(local=[{
            "record_id": "P-2",
            "evidence_role": "experimental_observation",
            "exact_source_excerpt": "A flame was observed.",
        }])
        result = build_research_insights(
            "flame", store_path=self.store_path
        )
        claim = result["evidence"]["claims"][0]
        self.assertIsNone(claim["source_document_id"])
        self.assertIsNone(claim["nasa_id"])
        self.assertIsNone(claim["source_url"])
        self.assertEqual(claim["page_numbers"], [])

    @patch("backend.services.research_insights.search_research_with_fallback")
    def test_unclassified_content_does_not_create_unsupported_claim(self, search):
        search.return_value = self.federation(local=[{
            "record_id": "P-3",
            "source_id": "NASA-3",
            "evidence_role": "unclassified",
            "exact_source_excerpt": "Background text describes flame spread.",
        }])
        result = build_research_insights(
            "flame spread", store_path=self.store_path
        )
        self.assertEqual(result["evidence"]["claim_count"], 0)
        self.assertEqual(result["evidence"]["papers"][0]["claims"], [])


class TestResearchInsightsHTTP(unittest.TestCase):
    @patch("backend.main.build_research_insights")
    def test_successful_request_returns_unified_contract(self, build):
        build.return_value = {
            "schema_version": "1.0",
            "query": "flame spread",
            "evidence": {"papers": [], "claims": []},
        }
        client = TestClient(app)
        response = client.post(
            "/research/insights",
            json={"query": "flame spread", "limit": 2},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["schema_version"], "1.0")
        build.assert_called_once_with("flame spread", limit=2)

    def test_existing_endpoint_and_new_endpoint_contracts(self):
        client = TestClient(app)
        response = client.post("/research/insights", json={"query": "x"})
        self.assertEqual(response.status_code, 400)
        health = client.get("/health")
        self.assertEqual(health.status_code, 200)

    @patch("backend.main.build_research_comparison")
    def test_comparison_endpoint_is_additive(self, build):
        build.return_value = {
            "schema_version": "1.0",
            "query": "flame spread",
            "comparison": {"comparable_sources": []},
            "scientific_findings_verified": False,
        }
        client = TestClient(app)
        response = client.post(
            "/research/insights/compare",
            json={"query": "flame spread", "limit": 2},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["schema_version"], "1.0")
        build.assert_called_once_with("flame spread", limit=2)
