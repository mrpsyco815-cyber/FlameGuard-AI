"""Evidence-grounded research gap and conservative conflict analysis."""

from typing import Any

from backend.services.research_comparison import CONDITION_DIMENSIONS


INSUFFICIENT_RECOMMENDATION = (
    "Insufficient verified evidence to support a mission-specific recommendation."
)


def _claim_ids(document: dict[str, Any]) -> list[str]:
    return [
        claim["claim_id"]
        for claim in document.get("claims", [])
        if claim.get("claim_id")
    ]


def _gap(
    gap_id: str,
    gap_type: str,
    description: str,
    document: dict[str, Any],
    missing: list[str],
    evidence_scope: str,
) -> dict[str, Any]:
    return {
        "gap_id": gap_id,
        "gap_type": gap_type,
        "description": description,
        "related_conditions": missing,
        "supporting_source_ids": [
            value for value in (
                document.get("document_id"), document.get("nasa_id")
            ) if value
        ],
        "supporting_claim_ids": _claim_ids(document),
        "missing_information": missing,
        "evidence_scope": evidence_scope,
        "confidence_basis": (
            "The condition is absent from the retrieved source representation; "
            "this does not establish that it is absent from the original study."
        ),
        "review_status": document.get("review_status", "not_recorded"),
    }


def build_research_gaps(
    documents: list[dict[str, Any]],
    comparison: dict[str, Any],
) -> dict[str, Any]:
    gaps = []
    questions = []
    for index, document in enumerate(documents):
        missing = []
        for field in CONDITION_DIMENSIONS:
            values = (document.get("conditions") or {}).get(field)
            if values is None:
                values = []
            if not values:
                missing.append(field)
        if missing:
            scope = (
                "abstract_only"
                if document.get("source_type") == "nasa_ntrs"
                else "retrieved_source_representation"
            )
            gap = _gap(
                f"gap-{index + 1:03d}",
                "condition_not_reported",
                "One or more requested comparison conditions were not reported "
                "in the retrieved source representation.",
                document,
                missing,
                scope,
            )
            gaps.append(gap)
            for field in missing:
                questions.append({
                    "question": (
                        f"Which retrieved studies report {field.replace('_', ' ')} "
                        "under comparable experimental conditions?"
                    ),
                    "gap_ids": [gap["gap_id"]],
                    "supporting_source_ids": gap["supporting_source_ids"],
                })

    if len(comparison.get("comparable_sources", [])) == 0 and len(documents) > 1:
        gap = {
            "gap_id": f"gap-{len(gaps) + 1:03d}",
            "gap_type": "insufficient_comparable_experiments",
            "description": (
                "The retrieved documents do not contain a pair with sufficiently "
                "compatible reported conditions."
            ),
            "related_conditions": [],
            "supporting_source_ids": [
                item.get("document_id") or item.get("nasa_id")
                for item in documents
                if item.get("document_id") or item.get("nasa_id")
            ],
            "supporting_claim_ids": [
                claim_id for document in documents
                for claim_id in _claim_ids(document)
            ],
            "missing_information": ["comparable_condition_set"],
            "evidence_scope": "retrieved_source_representation",
            "confidence_basis": (
                "No comparable pair was found by explicit value/unit matching."
            ),
            "review_status": "requires_scientific_review",
        }
        gaps.append(gap)
        questions.append({
            "question": (
                "Which fuel materials have comparable experimental observations "
                "under the same reported oxygen, gravity, pressure, temperature, "
                "flow, and setup conditions?"
            ),
            "gap_ids": [gap["gap_id"]],
            "supporting_source_ids": gap["supporting_source_ids"],
        })

    return {
        "research_gaps": gaps,
        "suggested_research_questions": questions,
        "limitations": [
            "A gap means information was absent from retrieved records, not that the scientific literature lacks it.",
            "No confidence percentages or scientific certainty scores are inferred.",
        ],
        "recommendation": INSUFFICIENT_RECOMMENDATION,
    }


def build_conflict_intelligence(
    comparison: dict[str, Any],
    documents: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Classify condition differences and comparable value differences conservatively."""
    conflicts = []
    document_by_id = {
        item.get("document_id") or item.get("nasa_id"): item
        for item in (documents or [])
        if isinstance(item, dict)
    }
    for pair in comparison.get("condition_comparisons", []):
        statuses = {
            field["status"] for field in pair.get("condition_comparisons", [])
        }
        if "mismatch" in statuses:
            classification = "not_comparable"
        elif "partial_match" in statuses or "unknown" in statuses:
            classification = "insufficient_information"
        else:
            classification = "potential_difference"
        if classification != "potential_difference":
            conflicts.append({
                "classification": classification,
                "first_finding": pair["first_source"],
                "second_finding": pair["second_source"],
                "condition_comparisons": pair["condition_comparisons"],
                "comparison_rationale": pair["comparison_rationale"],
                "missing_information": pair["missing_information"],
                "verification_status": "not_scientifically_verified",
                "review_status": "requires_scientific_review",
            })
            continue

        first_id = (
            pair["first_source"].get("document_id")
            or pair["first_source"].get("nasa_id")
        )
        second_id = (
            pair["second_source"].get("document_id")
            or pair["second_source"].get("nasa_id")
        )
        first_findings = (
            (document_by_id.get(first_id, {}).get("structured_findings") or {})
            .get("fields", {})
        )
        second_findings = (
            (document_by_id.get(second_id, {}).get("structured_findings") or {})
            .get("fields", {})
        )
        emitted_measurement_conflict = False
        for field in ("measurement", "oxygen_concentration", "pressure",
                      "temperature", "flow_condition"):
            left = first_findings.get(field, {}).get("values", [])
            right = second_findings.get(field, {}).get("values", [])
            for left_value in left:
                for right_value in right:
                    if (
                        str(left_value.get("unit") or "").casefold()
                        == str(right_value.get("unit") or "").casefold()
                        and left_value.get("value") != right_value.get("value")
                    ):
                        conflicts.append({
                            "classification": "potential_difference",
                            "parameter": field,
                            "first_finding": left_value,
                            "second_finding": right_value,
                            "first_source": pair["first_source"],
                            "second_source": pair["second_source"],
                            "condition_comparisons": pair["condition_comparisons"],
                            "comparison_rationale": (
                                "Comparable reported conditions contain different "
                                "values with matching units; this is a potential "
                                "difference requiring scientific review."
                            ),
                            "missing_information": pair["missing_information"],
                            "verification_status": "not_scientifically_verified",
                            "review_status": "requires_scientific_review",
                        })
                        emitted_measurement_conflict = True
        if not emitted_measurement_conflict:
            conflicts.append({
                "classification": "potential_difference",
                "first_finding": pair["first_source"],
                "second_finding": pair["second_source"],
                "condition_comparisons": pair["condition_comparisons"],
                "comparison_rationale": pair["comparison_rationale"],
                "missing_information": pair["missing_information"],
                "verification_status": "not_scientifically_verified",
                "review_status": "requires_scientific_review",
            })
    return conflicts
