"""Condition-aware synthesis for multiple source documents.

The service is deliberately conservative: it groups papers only when every
condition required by the comparison is explicitly reported and equal in the
source wording/value/unit representation. It does not infer equivalence or
scientific causality.
"""

import re
from collections import defaultdict
from typing import Any

from backend.services.claim_summarizer import extract_claims
from backend.services.evidence_extractor import extract_structured_findings


CONDITION_FIELDS = (
    "material_fuel",
    "gravity_condition",
    "oxygen_concentration",
    "pressure",
    "temperature",
    "flow_condition",
    "experimental_setup",
)

MEASUREMENT_FIELDS = {
    "measurement",
    "oxygen_concentration",
    "pressure",
    "temperature",
    "flow_condition",
}

UNSUPPORTED_SYNTHESIS = (
    "Insufficient verified evidence to support a cross-study conclusion."
)


def _norm(value: Any) -> str:
    return " ".join(str(value or "").casefold().split())


def _value_signature(value: dict[str, Any]) -> tuple[str, str, str]:
    return (
        _norm(value.get("value") or value.get("raw_value")),
        _norm(value.get("unit")),
        _norm(value.get("raw_value")),
    )


def _document_id(document: dict[str, Any], index: int) -> str:
    return str(
        document.get("document_id")
        or (document.get("structured_findings") or {}).get("source", {}).get(
            "document_id"
        )
        or document.get("nasa_id")
        or f"document-{index + 1}"
    )


def _findings(document: dict[str, Any]) -> dict[str, Any]:
    findings = document.get("structured_findings")
    if isinstance(findings, dict):
        return findings
    return extract_structured_findings(
        document,
        document_id=document.get("document_id"),
        nasa_id=document.get("nasa_id"),
        source_url=document.get("source_url") or document.get("citation_url"),
    )


def _claims(document: dict[str, Any]) -> list[dict[str, Any]]:
    summary = document.get("claim_summary")
    if isinstance(summary, dict) and isinstance(summary.get("claims"), list):
        claims = summary["claims"]
    else:
        claims = extract_claims(
            document,
            document_id=document.get("document_id"),
            nasa_id=document.get("nasa_id"),
            source_url=document.get("source_url") or document.get("citation_url"),
        )["claims"]

    result = []
    for index, claim in enumerate(claims, start=1):
        item = dict(claim)
        item.setdefault("claim_id", f"claim-{index:03d}")
        result.append(item)
    return result


def _setup_values(document: dict[str, Any]) -> list[dict[str, Any]]:
    values = []
    for claim in _claims(document):
        if claim.get("claim_type") != "methodological_statement":
            continue
        values.append({
            "value": claim.get("claim_text"),
            "raw_value": claim.get("claim_text"),
            "unit": None,
            "exact_supporting_text": claim.get(
                "exact_supporting_excerpt", claim.get("claim_text")
            ),
            "source_document_id": claim.get("source_document_id"),
            "nasa_id": claim.get("nasa_id"),
            "source_url": claim.get("source_url"),
            "page_numbers": claim.get("page_numbers", []),
            "section_name": claim.get("section_name"),
            "evidence_type": claim.get("evidence_type"),
            "verification_status": claim.get(
                "verification_status", "not_scientifically_verified"
            ),
            "uncertain": claim.get("uncertain", True),
        })
    return values


def _condition_values(
    document: dict[str, Any],
    findings: dict[str, Any],
) -> dict[str, list[dict[str, Any]]]:
    fields = findings.get("fields") or {}
    values = {}
    for field in CONDITION_FIELDS:
        if field == "experimental_setup":
            field_values = _setup_values(document)
        else:
            entry = fields.get(field) or {}
            field_values = entry.get("values") or []
        values[field] = [
            item for item in field_values if isinstance(item, dict)
        ]
    return values


def _condition_signature(
    condition_values: dict[str, list[dict[str, Any]]],
) -> tuple[tuple[str, tuple[tuple[str, str, str], ...]], ...]:
    return tuple(
        (
            field,
            tuple(sorted(_value_signature(value) for value in values)),
        )
        for field, values in condition_values.items()
    )


def _provenance(claim: dict[str, Any]) -> dict[str, Any]:
    return {
        "claim_id": claim.get("claim_id"),
        "source_document_id": claim.get("source_document_id"),
        "nasa_id": claim.get("nasa_id"),
        "source_url": claim.get("source_url"),
        "exact_supporting_excerpt": claim.get(
            "exact_supporting_excerpt",
            claim.get("exact_supporting_text", claim.get("claim_text")),
        ),
        "page_numbers": list(claim.get("page_numbers") or []),
        "section_name": claim.get("section_name"),
        "evidence_type": claim.get("evidence_type"),
        "experimental_conditions": claim.get("experimental_conditions"),
        "verification_status": claim.get(
            "verification_status", "not_scientifically_verified"
        ),
        "uncertain": bool(claim.get("uncertain", True)),
    }


def _with_conditions(
    provenance: dict[str, Any],
    group: dict[str, Any],
) -> dict[str, Any]:
    result = dict(provenance)
    result["experimental_conditions"] = group["conditions"]
    return result


def _paper_entry(document: dict[str, Any], index: int) -> dict[str, Any]:
    findings = _findings(document)
    claims = _claims(document)
    source = findings.get("source") or {}
    condition_values = _condition_values(document, findings)
    return {
        "document_id": _document_id(document, index),
        "nasa_id": source.get("nasa_id") or document.get("nasa_id"),
        "source_url": (
            source.get("source_url")
            or document.get("source_url")
            or document.get("citation_url")
        ),
        "conditions": condition_values,
        "condition_signature": _condition_signature(condition_values),
        "claims": claims,
        "findings": findings,
    }


def _comparison_reason(left: dict[str, list[dict[str, Any]]],
                       right: dict[str, list[dict[str, Any]]]) -> str:
    differences = []
    for field in CONDITION_FIELDS:
        left_values = left.get(field) or []
        right_values = right.get(field) or []
        if not left_values or not right_values:
            differences.append(f"{field} not reported in both studies")
        elif {
            _value_signature(item) for item in left_values
        } != {
            _value_signature(item) for item in right_values
        }:
            differences.append(f"{field} differs")
    return "; ".join(differences) or "Condition signatures differ."


def _claim_key(claim: dict[str, Any]) -> str:
    return re.sub(r"[^a-z0-9%./ -]", "", _norm(claim.get("claim_text")))


def synthesize_documents(
    documents: list[dict[str, Any]],
    *,
    research_topic: str | None = None,
) -> dict[str, Any]:
    """Compare documents only where complete, equal condition signatures exist."""
    if not isinstance(documents, list):
        raise ValueError("documents must be a list.")

    papers = [_paper_entry(document, index)
              for index, document in enumerate(documents)
              if isinstance(document, dict)]
    groups = defaultdict(list)
    for paper in papers:
        if all(paper["conditions"].get(field) for field in CONDITION_FIELDS):
            groups[paper["condition_signature"]].append(paper)

    comparable_groups = []
    for group_index, group in enumerate(groups.values(), start=1):
        if len(group) < 2:
            continue
        comparable_groups.append({
            "group_id": f"group-{group_index:03d}",
            "document_ids": [paper["document_id"] for paper in group],
            "conditions": {
                field: group[0]["conditions"][field]
                for field in CONDITION_FIELDS
            },
            "comparison_status": "comparable",
        })

    shared_observations = []
    disagreements = []
    for group in comparable_groups:
        group_papers = [
            paper for paper in papers
            if paper["document_id"] in group["document_ids"]
        ]
        observations = defaultdict(list)
        for paper in group_papers:
            for claim in paper["claims"]:
                if claim.get("claim_type") not in {
                    "experimental_observation", "experimental_result"
                }:
                    continue
                observations[_claim_key(claim)].append({
                    "document_id": paper["document_id"],
                    "claim": claim,
                })
        for key, items in observations.items():
            if len({item["document_id"] for item in items}) >= 2 and key:
                shared_observations.append({
                    "statement": items[0]["claim"].get("claim_text"),
                    "group_id": group["group_id"],
                    "supporting_claims": [
                        _with_conditions(_provenance(item["claim"]), group)
                        for item in items
                    ],
                    "evidence_status": "comparable_findings",
                    "uncertain": any(
                        item["claim"].get("uncertain", True) for item in items
                    ),
                })

        measurements = defaultdict(list)
        for paper in group_papers:
            for item in (paper["findings"].get("measurements") or []):
                if item.get("field") not in MEASUREMENT_FIELDS:
                    continue
                measurements[(
                    item.get("field"),
                    _norm(item.get("unit")),
                )].append((paper, item))
        for key, items in measurements.items():
            distinct_values = {
                _norm(item.get("value") or item.get("raw_value"))
                for _, item in items
            }
            if len({paper["document_id"] for paper, _ in items}) >= 2 and len(
                distinct_values
            ) > 1:
                disagreements.append({
                    "label": "potential_disagreement",
                    "group_id": group["group_id"],
                    "field": key[0],
                    "unit": key[1] or None,
                    "statement": (
                        "Comparable studies report different values for "
                        f"{key[0]} under matching reported conditions."
                    ),
                    "supporting_claims": [
                        _with_conditions(_provenance(item), group)
                        for _, item in items
                    ],
                    "evidence_status": "potential_disagreement",
                    "uncertain": True,
                })

    non_comparable = []
    for index, left in enumerate(papers):
        for right in papers[index + 1:]:
            if left["condition_signature"] == right["condition_signature"]:
                continue
            non_comparable.append({
                "document_ids": [left["document_id"], right["document_id"]],
                "label": "different_experimental_conditions",
                "reason": _comparison_reason(
                    left["conditions"], right["conditions"]
                ),
                "evidence_status": "non_comparable",
                "uncertain": True,
            })

    evidence_gaps = []
    if not comparable_groups:
        evidence_gaps.append({
            "statement": UNSUPPORTED_SYNTHESIS,
            "claim_ids": [],
            "source_document_ids": [paper["document_id"] for paper in papers],
            "evidence_status": "insufficient_evidence",
        })

    return {
        "schema_version": "1.0",
        "research_topic": research_topic,
        "papers_included": [
            {
                "document_id": paper["document_id"],
                "nasa_id": paper["nasa_id"],
                "source_url": paper["source_url"],
            }
            for paper in papers
        ],
        "comparable_study_groups": comparable_groups,
        "shared_observations": shared_observations,
        "differences": non_comparable,
        "potential_disagreements": disagreements,
        "evidence_gaps": evidence_gaps,
        "limitations": [
            "Comparability requires explicit equality of all supported condition fields.",
            "Original units and source wording are preserved; no conversions occur.",
            "Potential disagreements are not verified scientific contradictions.",
            "This synthesis does not establish causality or safety recommendations.",
        ],
        "scientific_findings_verified": False,
    }
