"""Condition-aware mission research briefs.

This layer organizes source-linked research for a supplied mission context. It
does not make operational recommendations or treat differing conditions as
validation of mission conditions.
"""

from typing import Any

from backend.services.scientific_synthesis import (
    CONDITION_FIELDS,
    _claims,
    _condition_values,
    _findings,
)


MISSION_FIELDS = (
    "material_fuel",
    "gravity_condition",
    "oxygen_concentration",
    "pressure",
    "temperature",
    "flow_condition",
    "experimental_setup",
)

INSUFFICIENT_RECOMMENDATION = (
    "Insufficient verified evidence to support a mission-specific recommendation."
)


def _norm(value: Any) -> str:
    return " ".join(str(value or "").casefold().split())


def _reported_forms(value: dict[str, Any]) -> set[str]:
    forms = {
        _norm(value.get("value")),
        _norm(value.get("raw_value")),
    }
    numeric = _norm(value.get("value"))
    unit = _norm(value.get("unit"))
    if numeric and unit:
        forms.add(f"{numeric} {unit}")
    return {item for item in forms if item}


def _mission_value_forms(value: Any) -> set[str]:
    return {_norm(value)} if _norm(value) else set()


def _condition_match(
    mission_value: Any,
    reported: list[dict[str, Any]],
) -> str:
    mission_forms = _mission_value_forms(mission_value)
    if not mission_forms:
        return "unknown"
    if not reported:
        return "unknown"
    if any(mission_forms.intersection(_reported_forms(item)) for item in reported):
        return "match"
    return "different"


def _claim_provenance(claim: dict[str, Any]) -> dict[str, Any]:
    return {
        "claim_id": claim.get("claim_id"),
        "source_document_id": claim.get("source_document_id"),
        "nasa_id": claim.get("nasa_id"),
        "source_url": claim.get("source_url"),
        "claim_text": claim.get("claim_text"),
        "exact_supporting_excerpt": claim.get(
            "exact_supporting_excerpt",
            claim.get("exact_supporting_text", claim.get("claim_text")),
        ),
        "page_numbers": list(claim.get("page_numbers") or []),
        "section_name": claim.get("section_name"),
        "evidence_type": claim.get("evidence_type"),
        "verification_status": claim.get(
            "verification_status", "not_scientifically_verified"
        ),
        "uncertain": bool(claim.get("uncertain", True)),
    }


def _mission_conditions(context: dict[str, Any]) -> dict[str, str]:
    aliases = {
        "fuel": "material_fuel",
        "material": "material_fuel",
        "fuel_material": "material_fuel",
    }
    result = {}
    for key, value in context.items():
        target = aliases.get(key, key)
        if target in MISSION_FIELDS and isinstance(value, str) and value.strip():
            result[target] = value.strip()
    return result


def _classify_paper(
    document: dict[str, Any],
    index: int,
    mission_conditions: dict[str, str],
) -> dict[str, Any]:
    findings = _findings(document)
    conditions = _condition_values(document, findings)
    claims = _claims(document)
    source = findings.get("source") or {}
    document_id = str(
        document.get("document_id")
        or source.get("document_id")
        or document.get("nasa_id")
        or f"document-{index + 1}"
    )

    field_matches = {
        field: _condition_match(
            mission_conditions.get(field),
            conditions.get(field) or [],
        )
        for field in MISSION_FIELDS
    }
    matched = [field for field, status in field_matches.items() if status == "match"]
    different = [
        field for field, status in field_matches.items() if status == "different"
    ]
    unknown = [
        field for field, status in field_matches.items() if status == "unknown"
    ]

    if not field_matches or (not matched and not different):
        comparison = "unknown_conditions"
    elif different:
        comparison = "different_conditions"
    elif unknown:
        comparison = "partial_match"
    else:
        comparison = "exact_match"

    observations = [
        _claim_provenance(claim)
        for claim in claims
        if claim.get("claim_type") in {
            "experimental_observation", "experimental_result"
        }
    ]
    interpretations = [
        _claim_provenance(claim)
        for claim in claims
        if claim.get("claim_type") in {"discussion_interpretation", "conclusion"}
    ]
    explanation = {
        "exact_match": "All supplied mission conditions were explicitly reported and matched.",
        "partial_match": "Some supplied mission conditions matched; remaining supplied conditions were not reported.",
        "different_conditions": "At least one supplied mission condition differed from the reported study condition.",
        "unknown_conditions": "No sufficient condition comparison could be established from the supplied mission context and source.",
    }[comparison]

    return {
        "document_id": document_id,
        "nasa_id": source.get("nasa_id") or document.get("nasa_id"),
        "source_url": (
            source.get("source_url")
            or document.get("source_url")
            or document.get("citation_url")
        ),
        "comparison": comparison,
        "comparison_explanation": explanation,
        "condition_matches": field_matches,
        "matched_condition_fields": matched,
        "different_condition_fields": different,
        "unknown_condition_fields": unknown,
        "reported_conditions": conditions,
        "scientific_observations": observations,
        "interpretations_and_conclusions": interpretations,
        "claims": [
            _claim_provenance(claim) for claim in claims
        ],
        "supporting_claim_ids": [
            claim.get("claim_id") for claim in claims if claim.get("claim_id")
        ],
        "verification_status": "not_scientifically_verified",
        "uncertain": True,
    }


def build_mission_research_brief(
    mission_context: dict[str, Any],
    documents: list[dict[str, Any]],
    *,
    synthesis: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build an evidence-linked research brief for explicitly supplied conditions."""
    if not isinstance(mission_context, dict):
        raise ValueError("mission_context must be a mapping.")
    if not isinstance(documents, list):
        raise ValueError("documents must be a list.")

    objective = str(
        mission_context.get("research_objective")
        or mission_context.get("research_question")
        or ""
    ).strip()
    question = str(
        mission_context.get("specific_research_question")
        or mission_context.get("research_question")
        or objective
        or ""
    ).strip()
    conditions = _mission_conditions(mission_context)
    papers = [
        _classify_paper(document, index, conditions)
        for index, document in enumerate(documents)
        if isinstance(document, dict)
    ]

    exact = [paper for paper in papers if paper["comparison"] == "exact_match"]
    partial = [paper for paper in papers if paper["comparison"] == "partial_match"]
    different = [
        paper for paper in papers
        if paper["comparison"] == "different_conditions"
    ]
    unknown = [
        paper for paper in papers
        if paper["comparison"] == "unknown_conditions"
    ]

    evidence_gaps = []
    if not exact:
        evidence_gaps.append({
            "statement": INSUFFICIENT_RECOMMENDATION,
            "reason": "No study was an exact match for all supplied mission conditions.",
            "claim_ids": [],
            "source_document_ids": [paper["document_id"] for paper in papers],
        })
    if not conditions:
        evidence_gaps.append({
            "statement": "Mission conditions were not supplied; condition-specific relevance is unknown.",
            "reason": "No explicit mission condition fields were available.",
            "claim_ids": [],
            "source_document_ids": [],
        })

    synthesis_groups = []
    if isinstance(synthesis, dict):
        synthesis_groups = [
            group for group in synthesis.get("comparable_study_groups", [])
            if isinstance(group, dict)
        ]

    all_claims = [
        claim for paper in papers for claim in paper["claims"]
    ]
    source_references = [
        {
            "source_document_id": claim["source_document_id"],
            "nasa_id": claim["nasa_id"],
            "source_url": claim["source_url"],
            "claim_id": claim["claim_id"],
            "page_numbers": claim["page_numbers"],
            "exact_supporting_excerpt": claim["exact_supporting_excerpt"],
        }
        for claim in all_claims
    ]

    return {
        "schema_version": "1.0",
        "brief_type": "mission_research_support",
        "research_question": question,
        "research_objective": objective,
        "supplied_mission_conditions": conditions,
        "relevant_nasa_research": papers,
        "comparable_studies": exact,
        "partially_comparable_studies": partial,
        "important_differences": different,
        "unknown_condition_studies": unknown,
        "scientific_observations": [
            observation
            for paper in papers
            for observation in paper["scientific_observations"]
        ],
        "interpretations_and_conclusions": [
            interpretation
            for paper in papers
            for interpretation in paper["interpretations_and_conclusions"]
        ],
        "evidence_gaps": evidence_gaps,
        "limitations_and_uncertainty": [
            "This is a research-support brief, not a certified spacecraft safety assessment.",
            "Different experimental conditions do not directly validate mission conditions.",
            "All extracted claims remain not scientifically verified.",
            "No operational recommendation is generated by this service.",
        ],
        "further_research_needed": [
            "Obtain source evidence for every unknown mission condition.",
            "Have qualified scientific and engineering reviewers assess applicability.",
        ],
        "source_references": source_references,
        "synthesis_groups_used": synthesis_groups,
        "scientific_findings_verified": False,
    }
