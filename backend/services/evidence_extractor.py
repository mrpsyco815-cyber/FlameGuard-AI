
import re
import json
from pathlib import Path
from typing import Any


def _tokenize(text: str) -> set[str]:
    """Normalize text into searchable terms."""
    return set(re.findall(r"[a-z0-9]+", (text or "").lower()))


def _split_sentences(text: str) -> list[str]:
    """Split source text into candidate passages."""
    return [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", (text or "").strip())
        if sentence.strip()
    ]


def extract_evidence(
    record: dict[str, Any],
    query: str = "",
) -> dict[str, Any]:
    """
    Extract traceable text passages from available record fields.

    Extracted passages are not independently verified scientific findings.
    """
    source_passages = []

    title = record.get("title")
    abstract = record.get("abstract")
    query_terms = _tokenize(query)

    if title:
        matched_terms = sorted(query_terms & _tokenize(title))

        if not query_terms or matched_terms:
            source_passages.append({
                "text": title,
                "source_field": "title",
                "source_url": record.get("source_url"),
                "evidence_type": "bibliographic_metadata",
                "matched_terms": matched_terms,
            })

    if abstract:
        for sentence in _split_sentences(abstract):
            matched_terms = sorted(
                query_terms & _tokenize(sentence)
            )

            if not query_terms or matched_terms:
                source_passages.append({
                    "text": sentence,
                    "source_field": "abstract",
                    "source_url": record.get("source_url"),
                    "evidence_type": "source_text",
                    "matched_terms": matched_terms,
                })

    for field in ("evidence_passages", "reported_findings"):
        values = record.get(field) or []

        if isinstance(values, str):
            values = [values]

        for value in values:
            if not isinstance(value, str) or not value.strip():
                continue

            matched_terms = sorted(
                query_terms & _tokenize(value)
            )

            if not query_terms or matched_terms:
                source_passages.append({
                    "text": value.strip(),
                    "source_field": field,
                    "source_url": record.get("source_url"),
                    "evidence_type": (
                        "demo_only"
                        if record.get("verification_status") == "demo_only"
                        else "provided_structured_text"
                    ),
                    "matched_terms": matched_terms,
                })

    unique_passages = []
    seen = set()

    for passage in source_passages:
        key = (passage["source_field"], passage["text"])

        if key not in seen:
            seen.add(key)
            unique_passages.append(passage)

    limitations = []

    if not abstract:
        limitations.append(
            "No abstract text is available in this record."
        )

    if not record.get("source_url"):
        limitations.append(
            "No source URL is available for traceability."
        )

    if record.get("dissemination_status") == "METADATA_ONLY":
        limitations.append(
            "NASA marks this record as metadata-only; "
            "full-text availability has not been confirmed."
        )
    elif not record.get("full_text"):
        limitations.append(
            "Full text has not been supplied; passages come "
            "only from available record fields."
        )

    if record.get("verification_status") == "demo_only":
        limitations.append(
            "This is a demo record, not scientific evidence."
        )

    return {
        "study_id": record.get("study_id") or record.get("nasa_id"),
        "title": title,
        "source_url": record.get("source_url"),
        "query": query,
        "passage_count": len(unique_passages),
        "passages": unique_passages,
        "full_text_reviewed": bool(record.get("full_text")),
        "scientific_findings_verified": False,
        "limitations": limitations,
    }


def _classify_page_context(page_text: str) -> dict[str, str]:
    """
    Infer research status from explicit page-heading phrases.

    This is a heuristic classification, not scientific verification.
    """
    text = " ".join((page_text or "").lower().split())

    rules = [
        (
            ("completed content",),
            "completed_research",
            "Page heading identifies completed content."
        ),
        (
            ("current content",),
            "current_research",
            "Page heading identifies current content."
        ),
        (
            ("proposed content",),
            "proposed_investigation",
            "Page heading identifies proposed content."
        ),
        (
            ("future investigations",),
            "future_investigation",
            "Page heading identifies future investigations."
        ),
        (
            (
                "fire / flammability applications",
                "fire/flammability applications",
            ),
            "fire_safety_principle",
            "Page heading identifies fire and flammability applications."
        ),
    ]

    for phrases, status, basis in rules:
        if any(phrase in text for phrase in phrases):
            return {
                "research_status": status,
                "classification_basis": basis,
                "classification_status": "heuristic_page_context",
            }

    return {
        "research_status": "unclassified",
        "classification_basis": "No recognized page heading found.",
        "classification_status": "requires_manual_review",
    }


def extract_page_evidence(
    nasa_id: str,
    query: str = "",
) -> dict[str, Any]:
    """
    Extract candidate passages from saved NASA PDF page text.

    Preserves source page numbers and citation URLs.
    Research status is inferred from page-level headings only.
    """
    if not str(nasa_id).isdigit():
        raise ValueError("NASA ID must contain digits only.")

    project_root = Path(__file__).resolve().parents[2]

    json_path = (
        project_root
        / "data"
        / "processed"
        / "nasa_pdf_pages"
        / f"{nasa_id}.json"
    )

    if not json_path.exists():
        raise FileNotFoundError(
            f"PDF page extraction JSON not found: {json_path}"
        )

    with json_path.open("r", encoding="utf-8") as file:
        document = json.load(file)

    query_terms = _tokenize(query)

    passages = []
    page_classifications = []

    for page in document.get("pages", []):
        page_number = page.get("pdf_page_number")
        page_text = page.get("text", "")

        if not isinstance(page_text, str) or not page_text.strip():
            continue

        context = _classify_page_context(page_text)

        page_classifications.append({
            "pdf_page_number": page_number,
            **context,
        })

        sentences = _split_sentences(page_text)

        for sentence in sentences:
            matched_terms = sorted(
                query_terms & _tokenize(sentence)
            )

            if query_terms and not matched_terms:
                continue

            passages.append({
                "text": sentence.strip(),
                "source_field": "pdf_page_text",
                "pdf_page_number": page_number,
                "source_url": document.get("citation_url"),
                "matched_terms": matched_terms,
                "evidence_type": "extracted_source_text",
                "research_status": context["research_status"],
                "classification_basis": context["classification_basis"],
                "classification_status": context["classification_status"],
                "experimental_result_status": "not_established",
                "scientific_findings_verified": False,
            })

    return {
        "nasa_id": nasa_id,
        "title": document.get("title"),
        "source_url": document.get("citation_url"),
        "query": query,
        "pdf_page_count": document.get("pdf_page_count"),
        "pages_with_extracted_text": document.get(
            "pages_with_extracted_text"
        ),
        "passage_count": len(passages),
        "passages": passages,
        "page_classifications": page_classifications,
        "full_text_reviewed": True,
        "scientific_findings_verified": False,
        "limitations": [
            "Research status is inferred from page-level headings.",
            "Page classification is heuristic and requires review.",
            "Experimental results are not established by this extraction.",
            "Sentence splitting may separate headings, bullets, or tables.",
            "A missing query match does not prove absence of relevant evidence.",
            "Original PDF pages must be reviewed before scientific conclusions.",
        ],
    }
