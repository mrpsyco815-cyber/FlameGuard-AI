"""Review-aware orchestration of retrieval, comparison, gaps, and mission briefs."""

from pathlib import Path
from typing import Any

from backend.services.bass2_dataset import (
    get_bass2_summary,
    load_bass2_dataset,
    search_bass2_records,
)
from backend.services.mission_research_brief import build_mission_research_brief
from backend.services.query_understanding import parse_query
from backend.services.research_gap_analysis import build_conflict_intelligence
from backend.services.research_insights import (
    INSUFFICIENT_RECOMMENDATION,
    build_research_comparison,
)
from backend.services.review_store import list_reviews


def _bass2_context(query: str, limit: int) -> dict[str, Any]:
    dataset = load_bass2_dataset()
    parsed = parse_query(query)
    filters: dict[str, Any] = {}
    material = next(iter(parsed.materials), None)
    if material:
        filters["fuel"] = material
    records = search_bass2_records(
        query=query if not material else "",
        fuel=material,
        limit=min(limit, 20),
    )
    return {
        "dataset_available": True,
        "search_status": "completed",
        "applied_filters": filters,
        "total_matching_records": len(records),
        "returned_records": records,
        "dataset_summary": get_bass2_summary(),
        "dataset_name": dataset.get("dataset_name"),
        "source": dataset.get("source"),
        "field_names": dataset.get("columns", []),
        "condition_summary": {
            "initial_oxygen_field": "Calibrated  initial O2 % by vol ",
            "final_oxygen_field": "Calibrated final O2 % by vol",
            "available_condition_fields": [
                "Fuel Sample Material",
                "Flow restrictor",
                "Fan display",
                "Air display",
                "Total Frames Shot",
                "Calibrated  initial O2 % by vol ",
                "Calibrated final O2 % by vol",
            ],
        },
        "limitations": [
            "BASS-II records provide condition and instrument metadata, not a verified flame-spread or extinction outcome.",
            "Gravity, pressure, temperature, flame-spread-rate, and extinction-outcome fields are not present in this dataset.",
            "Initial and final oxygen values are preserved as separate raw dataset fields.",
        ],
        "scientific_findings_verified": False,
    }


def build_mission_intelligence_orchestration(
    query: str,
    *,
    mission_context: dict[str, Any] | None = None,
    limit: int = 10,
    review_status: str | None = None,
    review_db_path: str | Path | None = None,
    store_path: str | Path | None = None,
) -> dict[str, Any]:
    if not isinstance(mission_context, dict):
        mission_context = {}
    comparison = build_research_comparison(
        query,
        limit=limit,
        store_path=store_path,
    )
    bass2_evidence = _bass2_context(query, limit)
    documents = comparison.get("evidence", {}).get("papers", [])
    brief = build_mission_research_brief(
        mission_context,
        documents,
        synthesis=None,
    )
    paper_ids = [
        str(item.get("document_id") or item.get("nasa_id"))
        for item in documents
        if item.get("document_id") or item.get("nasa_id")
    ]
    claim_ids = [
        str(claim.get("claim_id"))
        for document in documents
        for claim in document.get("claims", [])
        if claim.get("claim_id")
    ]
    reviews = []
    for target_id in paper_ids:
        reviews.extend(list_reviews(
            target_type="paper",
            target_id=target_id,
            status=review_status,
            limit=100,
            db_path=review_db_path,
        ))
    for target_id in claim_ids:
        reviews.extend(list_reviews(
            target_type="claim",
            target_id=target_id,
            status=review_status,
            limit=100,
            db_path=review_db_path,
        ))
    has_accepted = any(item["status"] == "accepted" for item in reviews)
    return {
        "schema_version": "1.0",
        "query": query,
        "mission_context": mission_context,
        "retrieval": comparison.get("retrieval", {}),
        "evidence": comparison.get("evidence", {}),
        "comparison": comparison.get("comparison", {}),
        "conflicts": comparison.get("conflicts", []),
        "research_gaps": comparison.get("research_gaps", []),
        "suggested_research_questions": comparison.get(
            "suggested_research_questions", []
        ),
        "bass2_evidence": bass2_evidence,
        "reviews": {
            "records": reviews,
            "accepted_review_present": has_accepted,
            "authentication_status": "not_available",
        },
        "mission_research_brief": brief,
        "conclusion": INSUFFICIENT_RECOMMENDATION,
        "scientific_findings_verified": False,
        "limitations": [
            "Review decisions are persisted but reviewer identity is not authenticated.",
            "Accepted review status is not scientific certification or universal verification.",
            "The orchestration does not generate operational fire-safety instructions.",
        ],
    }
