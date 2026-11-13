"""Unified, source-linked research insights assembled from existing services."""

from collections import OrderedDict
from pathlib import Path
from typing import Any

from backend.services.claim_summarizer import build_paper_summary
from backend.services.evidence_extractor import extract_structured_findings
from backend.services.research_comparison import compare_documents
from backend.services.research_gap_analysis import (
    build_conflict_intelligence,
    build_research_gaps,
)
from backend.services.research_federation import (
    DEFAULT_MIN_LOCAL_PASSAGES,
    DEFAULT_MIN_LOCAL_SOURCES,
    search_research_with_fallback,
)


INSUFFICIENT_RECOMMENDATION = (
    "Insufficient verified evidence to support a mission-specific recommendation."
)

_ROLE_SECTIONS = {
    "experimental_quantitative_result": "results",
    "experimental_observation": "results",
    "experimental_comparative_result": "results",
    "simulation_result": "discussion",
    "simulation_limitation": "limitations",
    "interpretation": "discussion",
    "scientific_limitation": "limitations",
    "mixed_comparison": "results_and_discussion",
}


def _source_key(item: dict[str, Any]) -> str:
    source_id = item.get("source_id") or item.get("nasa_id")
    if source_id not in (None, ""):
        return f"id:{source_id}"
    url = item.get("citation_url") or item.get("source_url")
    if url:
        return f"url:{url.strip().casefold().rstrip('/')}"
    record_id = item.get("record_id")
    return f"record:{record_id}" if record_id else "record:unknown"


def _local_document(item: dict[str, Any]) -> dict[str, Any]:
    role = item.get("evidence_role", "unclassified")
    section_name = _ROLE_SECTIONS.get(role)
    if section_name is None:
        section_name = "unclassified"
    return {
        "document_id": item.get("source_id"),
        "nasa_id": item.get("source_id"),
        "source_url": item.get("citation_url") or item.get("source_url"),
        "source_title": item.get("source_title"),
        "source_type": "local_nasa_passage",
        "evidence_classification": role,
        "verification_status": item.get(
            "classification_review_status", "not_scientifically_verified"
        ),
        "review_status": item.get(
            "source_review_status",
            item.get("classification_review_status", "not_recorded"),
        ),
        "scientific_findings_verified": (
            item.get("scientific_findings_verified") is True
        ),
        "sections": [{
            "section_name": section_name,
            "text": item.get("exact_source_excerpt") or "",
            "page_numbers": (
                [item["pdf_page_number"]]
                if item.get("pdf_page_number") is not None else []
            ),
        }],
    }


def _online_document(item: dict[str, Any]) -> dict[str, Any]:
    abstract = item.get("abstract") or ""
    return {
        "document_id": item.get("nasa_id"),
        "nasa_id": item.get("nasa_id"),
        "source_url": item.get("source_url"),
        "source_title": item.get("title"),
        "source_type": "nasa_ntrs",
        "evidence_classification": "bibliographic_metadata_and_abstract",
        "verification_status": item.get(
            "verification_status", "metadata_retrieved"
        ),
        "review_status": item.get(
            "review_status", "not_scientifically_reviewed"
        ),
        "scientific_findings_verified": False,
        "sections": [{
            "section_name": "abstract",
            "text": abstract,
            "page_numbers": [],
        }] if abstract else [],
    }


def _group_documents(local_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: OrderedDict[str, dict[str, Any]] = OrderedDict()
    for item in local_results:
        key = _source_key(item)
        document = grouped.setdefault(key, _local_document(item))
        document["sections"].extend(_local_document(item)["sections"])
    return list(grouped.values())


def _paper_insight(document: dict[str, Any]) -> dict[str, Any]:
    summary = build_paper_summary(
        document,
        document_id=document.get("document_id"),
        nasa_id=document.get("nasa_id"),
        source_url=document.get("source_url"),
    )
    claims = []
    for claim in summary["claims"]:
        enriched = dict(claim)
        enriched["source_type"] = document.get("source_type")
        enriched["source_title"] = document.get("source_title")
        enriched["evidence_classification"] = document.get(
            "evidence_classification"
        )
        enriched["source_verification_status"] = document.get(
            "verification_status"
        )
        enriched["review_status"] = document.get("review_status")
        claims.append(enriched)
    summary["claims"] = claims
    return {
        "document_id": document.get("document_id"),
        "nasa_id": document.get("nasa_id"),
        "source_url": document.get("source_url"),
        "source_title": document.get("source_title"),
        "source_type": document.get("source_type"),
        "evidence_classification": document.get("evidence_classification"),
        "verification_status": document.get("verification_status"),
        "review_status": document.get("review_status"),
        "scientific_findings_verified": False,
        "summary": summary,
        "claims": claims,
        "structured_findings": extract_structured_findings(
            document,
            document_id=document.get("document_id"),
            nasa_id=document.get("nasa_id"),
            source_url=document.get("source_url"),
        ),
        "provenance": {
            "source_document_id": document.get("document_id"),
            "nasa_id": document.get("nasa_id"),
            "source_url": document.get("source_url"),
            "page_numbers": sorted({
                page
                for section in document.get("sections", [])
                for page in section.get("page_numbers", [])
            }),
            "sections": sorted({
                section.get("section_name")
                for section in document.get("sections", [])
                if section.get("section_name")
            }),
            "review_status": document.get("review_status"),
        },
    }


def build_research_insights(
    query: str,
    *,
    limit: int = 10,
    store_path: str | Path | None = None,
) -> dict[str, Any]:
    """Run local-first retrieval and return source-linked extractive insights."""
    if not isinstance(query, str) or len(query.strip()) < 2:
        raise ValueError("query must contain at least two characters.")
    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 100:
        raise ValueError("limit must be an integer between 1 and 100.")

    federation = search_research_with_fallback(
        query,
        limit=limit,
        store_path=store_path,
        min_local_passages=DEFAULT_MIN_LOCAL_PASSAGES,
        min_local_sources=DEFAULT_MIN_LOCAL_SOURCES,
    )
    local_results = (
        federation.get("local_evidence_brief", {}).get("results", [])
    )
    online = federation.get("online_search", {})
    online_results = online.get("results", [])
    if not isinstance(local_results, list):
        local_results = []
    if not isinstance(online_results, list):
        online_results = []

    documents = _group_documents(local_results)
    documents.extend(
        _online_document(item)
        for item in online_results
        if isinstance(item, dict)
    )
    papers = [_paper_insight(document) for document in documents]
    claims = [
        claim
        for paper in papers
        for claim in paper["claims"]
    ]

    return {
        "schema_version": "1.0",
        "query": query,
        "retrieval": {
            "strategy": federation.get("search_strategy"),
            "fallback_triggered": federation.get("fallback_triggered", False),
            "fallback_reason": federation.get("fallback_reason", []),
            "missing_query_concepts": federation.get(
                "missing_query_concepts", []
            ),
            "online_search": {
                key: online.get(key)
                for key in (
                    "performed", "status", "original_query", "nasa_query",
                    "fallback_attempted", "fallback_reason",
                    "original_result_count", "fallback_result_count",
                    "count", "content_scope", "error",
                )
                if key in online
            },
            "counts": federation.get("counts", {}),
        },
        "evidence": {
            "paper_count": len(papers),
            "claim_count": len(claims),
            "papers": papers,
            "claims": claims,
        },
        "conflict_report": federation.get("conflict_report", {
            "conflicts": [],
            "count": 0,
            "limitations": [
                "No conflict report was available from retrieval."
            ],
        }),
        "recommendation": INSUFFICIENT_RECOMMENDATION,
        "scientific_findings_verified": False,
        "notices": [
            "Claims are extractive and source-linked; they are not independently scientifically verified.",
            "NASA metadata and abstracts remain bibliographic or abstract evidence, not full-text findings.",
            "Simulation and model records are not experimental observations.",
            "Different passages or papers are not treated as independent experiments.",
            "This endpoint is research support, not an autonomous fire-safety authority.",
        ],
        "limitations": [
            "Only records returned by the existing local-first federation are processed.",
            "Claim extraction is section-aware and pattern-based, not scientific fact-checking.",
            "Missing provenance remains missing and is not inferred.",
        ],
    }


def build_research_comparison(
    query: str,
    *,
    limit: int = 10,
    store_path: str | Path | None = None,
) -> dict[str, Any]:
    """Retrieve Phase 1 evidence and add condition/gap analysis."""
    insights = build_research_insights(
        query,
        limit=limit,
        store_path=store_path,
    )
    papers = insights["evidence"]["papers"]
    comparison = compare_documents(papers)
    gaps = build_research_gaps(papers, comparison)
    conflicts = build_conflict_intelligence(comparison, papers)
    return {
        "schema_version": "1.0",
        "query": query,
        "retrieval": insights["retrieval"],
        "evidence": insights["evidence"],
        "comparison": comparison,
        "conflicts": conflicts,
        "research_gaps": gaps["research_gaps"],
        "suggested_research_questions": gaps[
            "suggested_research_questions"
        ],
        "comparison_limitations": (
            comparison["comparison_limitations"] + gaps["limitations"]
        ),
        "recommendation": gaps["recommendation"],
        "scientific_findings_verified": False,
    }
