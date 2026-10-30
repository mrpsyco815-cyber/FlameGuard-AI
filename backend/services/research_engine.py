
import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "processed" / "research_records.json"


def load_research_records() -> list[dict[str, Any]]:
    """Load research records from the project's JSON dataset."""
    if not DATA_FILE.exists():
        return []

    with DATA_FILE.open("r", encoding="utf-8-sig") as file:
        records = json.load(file)

    if not isinstance(records, list):
        raise ValueError("Research dataset must be a JSON list.")

    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Every research record must be a JSON object.")
        if not record.get("study_id"):
            raise ValueError("Every research record needs a study_id.")
        if not record.get("title"):
            raise ValueError("Every research record needs a title.")

    return records

def search_research(query: str, limit: int = 5) -> list[dict[str, Any]]:
    """Rank local research records by simple keyword relevance."""
    if not query or not query.strip():
        return []

    if limit < 1:
        return []

    records = load_research_records()
    query_terms = set(query.lower().split())
    results = []

    searchable_fields = (
        "title",
        "abstract",
        "investigation",
        "research_objective",
        "reported_findings",
        "evidence_passages",
    )

    for record in records:
        searchable_text = " ".join(
            str(record.get(field, ""))
            for field in searchable_fields
        ).lower()

        matched_terms = [
            term for term in query_terms
            if term in searchable_text
        ]

        if not matched_terms:
            continue

        result = record.copy()
        result["relevance_score"] = round(
            len(matched_terms) / len(query_terms), 3
        )
        result["matched_terms"] = matched_terms
        results.append(result)

    results.sort(
        key=lambda item: item["relevance_score"],
        reverse=True,
    )

    return results[:limit]
