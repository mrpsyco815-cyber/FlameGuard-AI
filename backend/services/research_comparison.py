"""Conservative condition-aware comparison of source documents."""

from typing import Any

from backend.services.evidence_extractor import extract_structured_findings


CONDITION_DIMENSIONS = (
    "material_fuel",
    "gravity_condition",
    "oxygen_concentration",
    "initial_oxygen_concentration",
    "final_oxygen_concentration",
    "pressure",
    "temperature",
    "flow_condition",
    "experimental_setup",
)


def _norm(value: Any) -> str:
    return " ".join(str(value or "").casefold().split())


def _source(document: dict[str, Any]) -> dict[str, Any]:
    return {
        "document_id": document.get("document_id"),
        "nasa_id": document.get("nasa_id"),
        "source_url": document.get("source_url") or document.get("citation_url"),
        "source_title": document.get("source_title"),
        "source_type": document.get("source_type"),
        "evidence_classification": document.get("evidence_classification"),
        "verification_status": document.get(
            "verification_status", "not_scientifically_verified"
        ),
        "review_status": document.get("review_status", "not_recorded"),
    }


def _findings(document: dict[str, Any]) -> dict[str, Any]:
    existing = document.get("structured_findings")
    if isinstance(existing, dict):
        return existing
    return extract_structured_findings(
        document,
        document_id=document.get("document_id"),
        nasa_id=document.get("nasa_id"),
        source_url=document.get("source_url") or document.get("citation_url"),
    )


def _values(document: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    findings = _findings(document)
    fields = findings.get("fields") or {}
    source_conditions = document.get("conditions") or {}
    values: dict[str, list[dict[str, Any]]] = {}
    for dimension in CONDITION_DIMENSIONS:
        candidates = (
            source_conditions.get(dimension)
            or (fields.get(dimension) or {}).get("values")
            or []
        )
        values[dimension] = [
            item if isinstance(item, dict) else {
                "value": item,
                "raw_value": item,
                "unit": None,
            }
            for item in candidates
            if item not in (None, "")
        ]
    return values


def _signature(item: dict[str, Any]) -> tuple[str, str]:
    return (
        _norm(item.get("value") or item.get("raw_value")),
        _norm(item.get("unit")),
    )


def _field_comparison(
    dimension: str,
    left: list[dict[str, Any]],
    right: list[dict[str, Any]],
) -> dict[str, Any]:
    if not left and not right:
        status = "unknown"
    elif not left or not right:
        status = "partial_match"
    else:
        left_signatures = {_signature(item) for item in left}
        right_signatures = {_signature(item) for item in right}
        if left_signatures.intersection(right_signatures):
            status = "exact_match"
        elif any(
            _norm(item.get("value") or item.get("raw_value"))
            == _norm(other.get("value") or other.get("raw_value"))
            and _norm(item.get("unit")) != _norm(other.get("unit"))
            for item in left for other in right
        ):
            status = "mismatch"
        else:
            status = "mismatch"
    return {
        "dimension": dimension,
        "status": status,
        "first_source_values": left,
        "second_source_values": right,
        "missing_information": (
            [dimension] if status in {"unknown", "partial_match"} else []
        ),
    }


def compare_documents(documents: list[dict[str, Any]]) -> dict[str, Any]:
    """Compare every document pair without inferring equivalence or causality."""
    if not isinstance(documents, list):
        raise ValueError("documents must be a list.")
    valid = [item for item in documents if isinstance(item, dict)]
    sources = [_source(item) for item in valid]
    normalized = [_values(item) for item in valid]
    comparisons = []
    comparable_sources = []
    non_comparable_sources = []

    for index, first in enumerate(valid):
        for second_index in range(index + 1, len(valid)):
            second = valid[second_index]
            fields = [
                _field_comparison(
                    dimension,
                    normalized[index].get(dimension, []),
                    normalized[second_index].get(dimension, []),
                )
                for dimension in CONDITION_DIMENSIONS
            ]
            statuses = {field["status"] for field in fields}
            if "mismatch" in statuses:
                overall = "mismatch"
            elif "partial_match" in statuses:
                overall = "partial_match"
            elif "exact_match" in statuses and "unknown" not in statuses:
                overall = "exact_match"
            elif "exact_match" in statuses:
                overall = "compatible"
            else:
                overall = "unknown"
            comparison = {
                "first_source": _source(first),
                "second_source": _source(second),
                "overall_status": overall,
                "condition_comparisons": fields,
                "missing_information": sorted({
                    name
                    for field in fields
                    for name in field["missing_information"]
                }),
                "comparison_rationale": (
                    "Values are compared only by explicit reported value/unit "
                    "signatures; missing values remain unknown and no unit "
                    "conversion is performed."
                ),
                "independence_status": "unknown",
                "scientific_findings_verified": False,
            }
            comparisons.append(comparison)
            if overall in {"exact_match", "compatible"}:
                comparable_sources.append(comparison)
            else:
                non_comparable_sources.append(comparison)

    return {
        "comparable_sources": comparable_sources,
        "non_comparable_sources": non_comparable_sources,
        "condition_comparisons": comparisons,
        "comparison_limitations": [
            "No unit conversion or material equivalence is inferred.",
            "Different documents are not assumed to represent independent experiments.",
            "Abstracts, metadata, simulations, and interpretations are not experimental observations.",
        ],
        "sources": sources,
        "scientific_findings_verified": False,
    }
