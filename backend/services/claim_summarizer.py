"""Claim-level, evidence-linked summaries for one source document.

This module is intentionally extractive. It never rewrites source claims into
stronger scientific conclusions and never marks extracted evidence as verified.
"""

import hashlib
import re
from typing import Any

from backend.services.evidence_extractor import _split_sentences


CLAIM_TYPES = {
    "experimental_observation",
    "experimental_result",
    "methodological_statement",
    "discussion_interpretation",
    "conclusion",
    "limitation",
    "abstract_statement",
}

SECTION_CLAIM_TYPES = {
    "methodology_methods": "methodological_statement",
    "experimental_setup": "methodological_statement",
    "results": "experimental_result",
    "results_and_discussion": "experimental_result",
    "discussion": "discussion_interpretation",
    "conclusion": "conclusion",
    "limitations": "limitation",
    "abstract": "abstract_statement",
}

MEASUREMENT_TERMS = re.compile(
    r"\b(?:measured|measurement|observed|observation|rate|concentration|"
    r"temperature|pressure|velocity|value|was|were)\b",
    re.IGNORECASE,
)
_ARTIFACT_PATTERN = re.compile(
    r"(?:\bN\d{2}\s*[- ]\s*\d{3,}\b|"
    r"\b(?:page|fig(?:ure)?|table|ref(?:erence)?s?)\s*\.?\s*\d+\b|"
    r"\s{2,}[A-Za-z]{1,3}\s{2,})",
    re.IGNORECASE,
)
_HEADER_PATTERN = re.compile(
    r"^(?:solid surface combustion experiment|"
    r"experimental verification of material flammability|"
    r"flame spread in a .* environment|"
    r"(?:results?|conclusions?|references?|introduction|abstract))$",
    re.IGNORECASE,
)


def _source(document: dict[str, Any], document_id, nasa_id, source_url):
    return {
        "document_id": document_id or document.get("document_id"),
        "nasa_id": nasa_id or document.get("nasa_id"),
        "source_url": (
            source_url
            or document.get("citation_url")
            or document.get("source_url")
        ),
        "source_title": document.get("source_title"),
    }


def _section_provenance(section: dict[str, Any], source: dict[str, Any]):
    return {
        "source_document_id": source.get("document_id"),
        "nasa_id": source.get("nasa_id"),
        "source_url": source.get("source_url"),
        "page_numbers": list(section.get("page_numbers") or []),
        "section_name": section.get("section_name"),
        "evidence_type": {
            "abstract": "abstract_statement",
            "methodology_methods": "experimental_methods",
            "experimental_setup": "experimental_setup",
            "results": "experimental_results",
            "results_and_discussion": "results_and_discussion_statement",
            "discussion": "discussion_interpretation",
            "conclusion": "conclusion_statement",
            "limitations": "limitation_statement",
        }.get(section.get("section_name"), "unclassified_source_text"),
    }


def _claim_type(section_name: str, sentence: str) -> str | None:
    if section_name == "results":
        return (
            "experimental_result"
            if MEASUREMENT_TERMS.search(sentence)
            else "experimental_observation"
        )
    return SECTION_CLAIM_TYPES.get(section_name)


def _claim(
    sentence: str,
    section: dict[str, Any],
    source: dict[str, Any],
) -> dict[str, Any] | None:
    original_excerpt = sentence.strip()
    excerpt = " ".join(sentence.split()).strip()
    if not excerpt:
        return None
    title = str(source.get("source_title") or "").strip()
    if (
        not original_excerpt
        or excerpt.casefold() == title.casefold()
        or _HEADER_PATTERN.fullmatch(excerpt)
        or _ARTIFACT_PATTERN.search(excerpt)
        or not re.search(r"\b(?:is|are|was|were|has|have|show|shows|"
                         r"found|observed|measured|indicate|indicates|"
                         r"occurs|occurred|tested|uses|used|reported|"
                         r"examined|examine|conclude|concludes|predicted|"
                         r"predicts)\b",
                         excerpt, re.IGNORECASE)
    ):
        return None

    claim_type = _claim_type(section.get("section_name"), excerpt)
    if claim_type not in CLAIM_TYPES:
        return None

    provenance = _section_provenance(section, source)
    uncertain = bool(section.get("detection_uncertain"))
    if claim_type in {"abstract_statement", "discussion_interpretation", "conclusion"}:
        uncertain = True

    evidence = {
        **provenance,
        "exact_supporting_text": original_excerpt,
        "extraction_method": "section_aware_extractive_claim",
        "verification_status": "not_scientifically_verified",
        "uncertain": uncertain,
    }
    return {
        "claim_text": excerpt,
        "claim_type": claim_type,
        **provenance,
        "exact_supporting_excerpt": original_excerpt,
        "extraction_method": evidence["extraction_method"],
        "verification_status": evidence["verification_status"],
        "uncertain": uncertain,
        "supporting_evidence": [evidence],
        "scientific_findings_verified": False,
    }


def extract_claims(
    document: dict[str, Any],
    *,
    document_id: str | None = None,
    nasa_id: str | None = None,
    source_url: str | None = None,
    additional_evidence: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Extract only non-empty claims with exact source excerpts."""
    source = _source(document, document_id, nasa_id, source_url)
    claims: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []

    for section in document.get("sections") or []:
        text = section.get("text") or ""
        if not isinstance(text, str):
            continue
        for sentence in _split_sentences(text):
            candidate = _claim(sentence, section, source)
            if candidate is None:
                if sentence.strip() and section.get("section_name") in {
                    "introduction",
                    "background_related_work",
                    "references",
                }:
                    rejected.append({
                        "text": " ".join(sentence.split()),
                        "reason": "Section is not an eligible claim evidence role.",
                    })
                continue
            key = (
                candidate["claim_type"],
                candidate["claim_text"],
                tuple(candidate["page_numbers"]),
            )
            if not any(
                (item["claim_type"], item["claim_text"], tuple(item["page_numbers"]))
                == key
                for item in claims
            ):
                claims.append(candidate)

    for supporting in additional_evidence or []:
        if not isinstance(supporting, dict):
            continue
        claim_text = " ".join(
            str(supporting.get("claim_text") or "").split()
        ).strip()
        excerpt = " ".join(
            str(
                supporting.get("exact_supporting_excerpt")
                or supporting.get("exact_supporting_text")
                or ""
            ).split()
        ).strip()
        if not claim_text or not excerpt:
            continue
        matching_claim = next(
            (
                claim for claim in claims
                if claim["claim_text"].casefold() == claim_text.casefold()
            ),
            None,
        )
        if matching_claim is None:
            continue
        matching_claim["supporting_evidence"].append({
            "source_document_id": supporting.get(
                "source_document_id", matching_claim["source_document_id"]
            ),
            "nasa_id": supporting.get("nasa_id", matching_claim["nasa_id"]),
            "source_url": supporting.get(
                "source_url", matching_claim["source_url"]
            ),
            "page_numbers": list(
                supporting.get("page_numbers")
                or matching_claim["page_numbers"]
            ),
            "section_name": supporting.get(
                "section_name", matching_claim["section_name"]
            ),
            "evidence_type": supporting.get(
                "evidence_type", matching_claim["evidence_type"]
            ),
            "exact_supporting_text": excerpt,
            "extraction_method": "provided_source_linked_evidence",
            "verification_status": "not_scientifically_verified",
            "uncertain": bool(supporting.get("uncertain", True)),
        })

    return {
        "schema_version": "1.0",
        "source": source,
        "claims": claims,
        "rejected_claims": rejected,
        "claim_count": len(claims),
        "scientific_findings_verified": False,
        "extraction_note": (
            "Claims are source-preserving extracts. They are not independently "
            "scientifically verified."
        ),
    }


def build_paper_summary(
    document: dict[str, Any],
    *,
    document_id: str | None = None,
    nasa_id: str | None = None,
    source_url: str | None = None,
) -> dict[str, Any]:
    """Build a structured summary whose statements reference claim IDs."""
    extracted = extract_claims(
        document,
        document_id=document_id,
        nasa_id=nasa_id,
        source_url=source_url,
    )
    claims = extracted["claims"]
    grouped = {
        "research_objective": [],
        "experimental_context": [],
        "materials_and_conditions": [],
        "main_reported_observations": [],
        "main_interpretations": [],
        "limitations": [],
    }

    for index, claim in enumerate(claims, start=1):
        identity = "|".join([
            str(claim.get("source_document_id") or ""),
            str(claim.get("nasa_id") or ""),
            str(claim.get("source_url") or ""),
            claim["claim_type"],
            claim["claim_text"],
            ",".join(str(page) for page in claim.get("page_numbers", [])),
        ])
        claim["claim_id"] = (
            "claim-" + hashlib.sha256(identity.encode("utf-8")).hexdigest()[:20]
        )
        claim_type = claim["claim_type"]
        if claim_type == "abstract_statement":
            grouped["research_objective"].append(claim["claim_id"])
        elif claim_type == "methodological_statement":
            grouped["experimental_context"].append(claim["claim_id"])
            if re.search(
                r"\b(?:PMMA|polyethylene|polypropylene|fuel|oxygen|gravity|"
                r"pressure|temperature|flow)\b",
                claim["claim_text"],
                re.IGNORECASE,
            ):
                grouped["materials_and_conditions"].append(claim["claim_id"])
        elif claim_type in {"experimental_observation", "experimental_result"}:
            grouped["main_reported_observations"].append(claim["claim_id"])
        elif claim_type in {"discussion_interpretation", "conclusion"}:
            grouped["main_interpretations"].append(claim["claim_id"])
        elif claim_type == "limitation":
            grouped["limitations"].append(claim["claim_id"])

    statements = {}
    for name, claim_ids in grouped.items():
        statements[name] = [
            {
                "statement": next(
                    item["claim_text"] for item in claims
                    if item["claim_id"] == claim_id
                ),
                "claim_ids": [claim_id],
                "evidence_sufficient": True,
            }
            for claim_id in claim_ids
        ]

    evidence_gaps = []
    for name, values in statements.items():
        if not values:
            evidence_gaps.append({
                "summary_field": name,
                "statement": "Insufficient verified evidence to support this statement.",
                "claim_ids": [],
                "evidence_sufficient": False,
            })

    return {
        "schema_version": "1.0",
        "source": extracted["source"],
        "claims": claims,
        "summary": statements,
        "evidence_gaps": evidence_gaps,
        "scientific_findings_verified": False,
        "verification_note": (
            "This summary is extractive and source-linked; it is not scientific "
            "verification or a safety decision."
        ),
    }
