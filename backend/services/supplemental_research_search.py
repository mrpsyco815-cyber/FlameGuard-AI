from pathlib import Path
import re

from backend.services.nasa_ingestion import load_supplemental_collection
from backend.services.research_summarizer import tokenize


ELIGIBLE_ROLES = {
    "experimental_quantitative_result",
    "experimental_observation",
    "experimental_comparative_result",
    "simulation_result",
    "mixed_comparison",
    "interpretation",
    "scientific_limitation",
    "simulation_limitation",
}


def search_supplemental_research(query, limit=100, project_root: Path | None = None):
    """Search live NASA papers imported into the review-pending collection."""
    query_terms = tokenize(query)
    if not query_terms:
        return []

    collection = load_supplemental_collection(project_root)
    results = []

    for record in collection.get("records", []):
        if not isinstance(record, dict):
            continue
        classification = record.get("classification") or {}
        role = classification.get("evidence_role", "unclassified")
        if role not in ELIGIBLE_ROLES:
            continue

        content = record.get("content") or {}
        excerpt = content.get("text") or ""
        if not isinstance(excerpt, str) or not excerpt.strip():
            continue

        matched = sorted(query_terms.intersection(tokenize(excerpt)))
        if not matched:
            continue

        source = record.get("source") or {}
        results.append({
            "record_id": record.get("record_id"),
            "source_id": source.get("source_id"),
            "source_title": source.get("title"),
            "citation_url": source.get("citation_url"),
            "pdf_page_number": source.get("pdf_page_number"),
            "evidence_role": role,
            "evidence_modality": classification.get("evidence_modality", "unknown"),
            "classification_review_status": classification.get("review_status", "requires_manual_review"),
            "source_review_status": (record.get("review") or {}).get("source_review_status", "requires_manual_review"),
            "scientific_findings_verified": False,
            "matched_query_terms": matched,
            "query_match_score": round(len(matched) / len(query_terms), 4),
            "exact_source_excerpt": excerpt,
            "source_dataset": "live_nasa_supplemental_collection",
            "source_owner": "NASA NTRS live import",
            "source_presence": ["project_local_supplemental_collection"],
        })

    results.sort(
        key=lambda item: (
            -item["query_match_score"],
            str(item.get("source_id") or ""),
            item.get("pdf_page_number") or 0,
        )
    )
    return results[:limit]
