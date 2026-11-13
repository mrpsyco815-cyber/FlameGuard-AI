"""Traceable comparison of explicitly structured research claims.

Free-form passages are not converted into scientific claims here. A conflict
is reported only when callers provide comparable parameter/value/unit records.
"""

from collections import defaultdict
from typing import Any


def build_conflict_report(records: list[dict[str, Any]]) -> dict[str, Any]:
    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    limitations = []

    for record in records:
        parameter = record.get("claim_parameter") or record.get("parameter")
        value = record.get("claim_value") if "claim_value" in record else record.get("value")
        if not parameter or value is None:
            continue
        conditions = record.get("conditions") or {}
        condition_key = repr(sorted(conditions.items()))
        unit = str(record.get("unit") or "")
        groups[(str(parameter), unit, condition_key)].append(record)

    comparisons: list[dict[str, Any]] = []
    by_condition: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for (parameter, unit, condition_key), group in groups.items():
        by_condition[(parameter, unit, condition_key)].extend(group)

    for (parameter, unit, condition_key), group in by_condition.items():
        values = {repr(item.get("claim_value", item.get("value"))) for item in group}
        source_ids = {str(item.get("source_id") or "") for item in group}
        if len(values) < 2 or len(source_ids) < 2:
            continue
        for index, first in enumerate(group):
            for second in group[index + 1:]:
                if first.get("source_id") == second.get("source_id"):
                    continue
                comparisons.append({
                    "parameter": parameter,
                    "source_a": _source_details(first),
                    "source_b": _source_details(second),
                    "conditions": first.get("conditions") or {},
                    "value_a": first.get("claim_value", first.get("value")),
                    "value_b": second.get("claim_value", second.get("value")),
                    "unit": unit or None,
                    "conflict_status": "unresolved_disagreement",
                    "review_status": "requires_scientific_review",
                })

    if not comparisons:
        limitations.append(
            "No conflict is reported unless comparable parameter, value, unit, "
            "condition, and source fields are explicitly supplied."
        )
    return {
        "conflicts": comparisons,
        "count": len(comparisons),
        "limitations": limitations,
    }


def _source_details(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_id": record.get("source_id"),
        "source_url": record.get("source_url") or record.get("citation_url"),
        "title": record.get("title") or record.get("source_title"),
        "page": record.get("page") or record.get("pdf_page_number"),
        "evidence_type": record.get("evidence_type"),
        "review_status": record.get("review_status", "not_recorded"),
    }
