import json
import re
from pathlib import Path
from typing import Any

from backend.services.query_understanding import parse_query, score_text
from backend.services.ranking_contract import (
    annotate_duplicate_sources,
    build_ranking_contract,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "nasa_combined_evidence.json"
)


def load_nasa_passages() -> dict[str, Any]:
    """Load extracted NASA documents and validate their structure."""

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"NASA combined evidence file not found: {DATA_FILE}"
        )

    with DATA_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("NASA combined evidence must be a JSON object.")

    documents = data.get("documents")

    if not isinstance(documents, list):
        raise ValueError("'documents' must be a list.")

    if data.get("document_count") != len(documents):
        raise ValueError("Document count does not match actual documents.")

    for doc_index, document in enumerate(documents, start=1):
        if not isinstance(document, dict):
            raise ValueError(f"Document {doc_index} is invalid.")

        if not document.get("nasa_id") or not document.get("title"):
            raise ValueError(
                f"Document {doc_index} is missing its NASA ID or title."
            )

        passages = document.get("passages")

        if not isinstance(passages, list):
            raise ValueError(
                f"Document {document['nasa_id']} has invalid passages."
            )

        for passage_index, passage in enumerate(passages, start=1):
            if not isinstance(passage, dict):
                raise ValueError(
                    f"Invalid passage {passage_index} "
                    f"in NASA document {document['nasa_id']}."
                )

            if not isinstance(passage.get("text"), str):
                raise ValueError(
                    f"Passage {passage_index} has no valid text field."
                )

    return data


def make_snippet(text: str, matched_terms: list[str], max_length: int = 320) -> str:
    clean_text = re.sub(r"\s+", " ", text).strip()

    if len(clean_text) <= max_length:
        return clean_text

    lower_text = clean_text.lower()
    positions = [
        lower_text.find(term)
        for term in matched_terms
        if lower_text.find(term) >= 0
    ]

    if positions:
        position = min(positions)
        start = max(0, position - 100)
        end = min(len(clean_text), start + max_length)
        snippet = clean_text[start:end]

        if start > 0:
            snippet = "..." + snippet

        if end < len(clean_text):
            snippet += "..."

        return snippet

    return clean_text[:max_length] + "..."


def search_nasa_passages(
    query: str = "",
    limit: int = 10,
    nasa_id: str | None = None,
    classification: str | None = None,
) -> list[dict[str, Any]]:
    """Search extracted NASA page passages using keyword matching."""

    if limit < 1 or limit > 100:
        raise ValueError("limit must be between 1 and 100.")

    scientific_query = parse_query(query) if query.strip() else None

    if not scientific_query and not nasa_id and not classification:
        return []

    data = load_nasa_passages()
    results = []

    for document in data["documents"]:
        document_id = str(document["nasa_id"])
        document_title = str(document["title"])

        if nasa_id and document_id.casefold() != nasa_id.casefold():
            continue

        for passage in document["passages"]:
            passage_class = str(
                passage.get("classification", "unknown")
            )

            if (
                classification
                and passage_class.casefold() != classification.casefold()
            ):
                continue

            original_text = passage["text"]
            relevance = (
                score_text(scientific_query, original_text)
                if scientific_query else
                {"matched_terms": [], "score": 0.0, "matching_reasons": []}
            )
            matched_terms = relevance["matched_terms"]

            # Do not return a passage just because its document title matches.
            if scientific_query and not matched_terms:
                continue

            exact_phrase_match = (
                bool(scientific_query)
                and scientific_query.normalized in original_text.lower()
            )

            relevance_score = (
                relevance["score"]
            )

            citation_url = (
                passage.get("citation_url")
                or passage.get("source_url")
                or document.get("citation_url")
            )

            result = {
                "nasa_id": document_id,
                "source_type": "nasa_extracted_passage",
                "title": document_title,
                "pdf_page_number": passage.get("pdf_page_number"),
                "citation_url": citation_url,
                "source_field": passage.get("source_field"),
                "snippet": make_snippet(original_text, matched_terms),
                "matched_terms": matched_terms,
                "relevance_score": relevance_score,
                "exact_phrase_match": exact_phrase_match,
                "classification": passage_class,
                "classification_status": passage.get(
                    "classification_status"
                ),
                "classification_basis": passage.get(
                    "classification_basis"
                ),
                "evidence_type": passage.get("evidence_type"),
                "research_status": passage.get("research_status"),
                "experimental_result_status": passage.get(
                    "experimental_result_status"
                ),
                "review_status": passage.get("review_status"),
                "scientific_findings_verified": passage.get(
                    "scientific_findings_verified", False
                ),
                "relevance_components": relevance,
                "matching_reasons": relevance["matching_reasons"],
            }
            result["ranking_contract"] = build_ranking_contract(
                query=scientific_query,
                original_score=relevance_score,
                record=result,
                source_text=original_text,
                evidence_scope_name=passage.get("evidence_type"),
            )
            results.append(result)

    results.sort(
        key=lambda item: (
            item["relevance_score"],
            item["exact_phrase_match"],
            len(item["matched_terms"]),
        ),
        reverse=True,
    )

    results = annotate_duplicate_sources(results)
    for item in results:
        item["ranking_contract"]["duplicate_source"] = item["duplicate_source"]
    return results[:limit]
