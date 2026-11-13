
import json
import re
from pathlib import Path
from typing import Any
from backend.services.ranking_contract import (
    annotate_duplicate_sources,
    build_ranking_contract,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

EVIDENCE_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "nasa_reviewed_evidence.json"
)


def load_reviewed_evidence() -> list[dict[str, Any]]:
    if not EVIDENCE_FILE.exists():
        return []

    with EVIDENCE_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("Reviewed evidence file must be a JSON object.")

    records = data.get("evidence", [])

    if not isinstance(records, list):
        raise ValueError("'evidence' must be a JSON list.")

    return [
        record for record in records
        if isinstance(record, dict)
        and record.get("evidence_id")
        and record.get("finding")
    ]


def search_nasa_evidence(
    query: str,
    limit: int = 5,
) -> list[dict[str, Any]]:

    if not query or not query.strip():
        return []

    if limit < 1:
        return []

    records = load_reviewed_evidence()

    terms = set(re.findall(r"[a-z0-9]+", query.lower()))

    if not terms:
        return []

    results = []

    searchable_fields = (
        "title",
        "finding",
        "evidence_class",
        "nasa_id",
    )

    for record in records:
        searchable_text = " ".join(
            str(record.get(field, ""))
            for field in searchable_fields
        ).lower()

        searchable_terms = set(
            re.findall(r"[a-z0-9]+", searchable_text)
        )

        matched_terms = terms.intersection(searchable_terms)

        if not matched_terms:
            continue

        result = {
            "evidence_id": record.get("evidence_id"),
            "nasa_id": record.get("nasa_id"),
            "title": record.get("title"),
            "finding": record.get("finding"),
            "evidence_class": record.get("evidence_class"),
            "pdf_page_number": record.get("pdf_page_number"),
            "citation_url": record.get("citation_url"),
            "review_status": record.get("review_status"),
            "scientific_findings_verified": record.get(
                "scientific_findings_verified", False
            ),
            "matched_terms": sorted(matched_terms),
            "relevance_score": round(
                len(matched_terms) / len(terms), 3
            ),
            "source_type": "reviewed_evidence",
        }
        result["ranking_contract"] = build_ranking_contract(
            query=query,
            original_score=result["relevance_score"],
            record={
                **result,
                "exact_source_excerpt": record.get("finding"),
                "evidence_type": "independently_reviewed_evidence",
            },
            source_text=str(record.get("finding") or ""),
            evidence_scope_name="independently_reviewed_evidence",
        )

        results.append(result)

    results.sort(
        key=lambda item: item["relevance_score"],
        reverse=True,
    )

    results = annotate_duplicate_sources(results)
    for item in results:
        item["ranking_contract"]["duplicate_source"] = item["duplicate_source"]
    return results[:limit]
