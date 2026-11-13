"""Human-review queue generation for extracted scientific evidence."""

from typing import Any

from backend.services.claim_summarizer import extract_claims


REVIEW_DECISIONS = (
    "accepted",
    "rejected",
    "needs_correction",
    "insufficient_evidence",
)


def build_review_queue(
    document: dict[str, Any],
    *,
    reviewer_id: str | None = None,
) -> dict[str, Any]:
    """Create review items without changing verification status."""
    summary = document.get("claim_summary") or {}
    claims = summary.get("claims") or extract_claims(
        document,
        document_id=document.get("document_id"),
        nasa_id=document.get("nasa_id"),
        source_url=document.get("source_url") or document.get("citation_url"),
    ).get("claims", [])
    items = []
    for index, claim in enumerate(claims, start=1):
        evidence = claim.get("supporting_evidence") or [{}]
        first_evidence = evidence[0]
        items.append({
            "review_item_id": f"review-{index:03d}",
            "claim_id": claim.get("claim_id") or f"claim-{index:03d}",
            "claim_text": claim.get("claim_text"),
            "claim_type": claim.get("claim_type"),
            "source_document_id": claim.get("source_document_id"),
            "nasa_id": claim.get("nasa_id"),
            "source_url": claim.get("source_url"),
            "exact_supporting_excerpt": claim.get(
                "exact_supporting_excerpt",
                first_evidence.get("exact_supporting_text"),
            ),
            "supporting_excerpts": [
                item.get("exact_supporting_text")
                for item in evidence
                if item.get("exact_supporting_text")
            ],
            "page_numbers": list(claim.get("page_numbers") or []),
            "section_name": claim.get("section_name"),
            "evidence_type": claim.get("evidence_type"),
            "uncertain": bool(claim.get("uncertain", True)),
            "verification_status": claim.get(
                "verification_status", "not_scientifically_verified"
            ),
            "reviewer_id": reviewer_id,
            "reviewer_decision": None,
            "reviewer_notes": None,
        })

    return {
        "schema_version": "1.0",
        "review_status": "pending_review",
        "allowed_decisions": list(REVIEW_DECISIONS),
        "items": items,
        "scientific_findings_verified": False,
        "review_note": (
            "Reviewer decisions are recorded separately; extraction never "
            "automatically marks evidence as scientifically verified."
        ),
    }


def record_review_decision(
    review_queue: dict[str, Any],
    review_item_id: str,
    decision: str,
    *,
    reviewer_id: str,
    notes: str | None = None,
) -> dict[str, Any]:
    """Return a copied queue with one explicit human decision recorded."""
    if decision not in REVIEW_DECISIONS:
        raise ValueError(f"Unsupported review decision: {decision}")
    if not isinstance(reviewer_id, str) or not reviewer_id.strip():
        raise ValueError("reviewer_id is required.")

    result = {
        **review_queue,
        "items": [dict(item) for item in review_queue.get("items", [])],
    }
    selected = next(
        (
            item for item in result["items"]
            if item.get("review_item_id") == review_item_id
        ),
        None,
    )
    if selected is None:
        raise ValueError(f"Review item not found: {review_item_id}")
    selected["reviewer_id"] = reviewer_id
    selected["reviewer_decision"] = decision
    selected["reviewer_notes"] = notes
    result["review_status"] = (
        "reviewed"
        if all(item.get("reviewer_decision") for item in result["items"])
        else "pending_review"
    )
    result["scientific_findings_verified"] = False
    return result
