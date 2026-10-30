from itertools import combinations
from typing import Any


CONDITION_FIELDS = (
    "fuel_or_material",
    "gravity",
    "oxygen",
    "pressure",
    "flow",
)


def _normalize(value: Any) -> str | None:
    if value is None:
        return None
    text = " ".join(str(value).casefold().split())
    return text or None


def build_condition_comparison(
    evidence: list[dict[str, Any]],
    bass2_results: list[dict[str, Any]] | None = None,
    pair_limit: int = 20,
) -> dict[str, Any]:
    """Compare recorded experimental contexts without normalizing raw values."""
    by_source = {}
    for item in evidence:
        source_id = item.get("source_id")
        if not source_id:
            continue
        conditions = item.get("experiment_conditions")
        if not isinstance(conditions, dict) or not conditions:
            continue
        if source_id not in by_source:
            by_source[source_id] = {
                "source_id": source_id,
                "title": item.get("source_title"),
                "citation_url": item.get("citation_url") or item.get("source_url"),
                "pdf_page_number": item.get("pdf_page_number"),
                "experiment_conditions_raw": {
                    field: conditions.get(field)
                    for field in CONDITION_FIELDS
                },
            }

    studies = list(by_source.values())
    pairs = []
    for left, right in combinations(studies, 2):
        matching = []
        differing = []
        missing = []

        for field in CONDITION_FIELDS:
            left_value = _normalize(left["experiment_conditions_raw"].get(field))
            right_value = _normalize(right["experiment_conditions_raw"].get(field))
            if left_value is None or right_value is None:
                missing.append(field)
            elif left_value == right_value:
                matching.append(field)
            else:
                differing.append(field)

        if differing:
            status = "recorded_conditions_differ"
        elif missing:
            status = "insufficient_condition_metadata"
        else:
            status = "recorded_conditions_match_textually"

        pairs.append({
            "left_source_id": left["source_id"],
            "left_title": left["title"],
            "right_source_id": right["source_id"],
            "right_title": right["title"],
            "status": status,
            "matching_fields": matching,
            "differing_fields": differing,
            "missing_fields": missing,
        })

    bass2 = bass2_results or []
    return {
        "condition_fields_checked": list(CONDITION_FIELDS),
        "study_condition_records": studies,
        "study_pair_comparisons": pairs[:pair_limit],
        "study_pair_comparison_count": len(pairs),
        "bass2_structured_record_count": len(bass2),
        "bass2_notice": (
            "BASS-II rows remain raw structured records. This matrix does not "
            "normalize units or calculate cross-study numeric comparisons."
        ),
        "interpretation_limit": (
            "Textually matching recorded conditions do not prove experimental "
            "equivalence. Differing or missing conditions must be reviewed in "
            "the original papers before interpreting differences in outcomes."
        ),
    }
