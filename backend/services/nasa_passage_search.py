import json
import re
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "nasa_combined_evidence.json"
)


def tokenize(value: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", value.lower())


def load_nasa_passages() -> dict[str, Any]:
    """Load extracted NASA documents and validate their structure."""

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"NASA combined evidence file not found: {DATA_FILE}"
        )

    raw_content = DATA_FILE.read_text(encoding="utf-8")
    if not raw_content.strip():
        # No combined NASA passages have been loaded yet.
        return {"document_count": 0, "documents": []}

    try:
        data = json.loads(raw_content)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"NASA combined evidence contains invalid JSON: {exc}"
        ) from exc

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
    clean_text = re.sub(r"\\s+", " ", text).strip()

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

    query_terms = list(dict.fromkeys(tokenize(query)))

    if not query_terms and not nasa_id and not classification:
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
            passage_terms = set(tokenize(original_text))

            matched_terms = [
                term for term in query_terms
                if term in passage_terms
            ]

            # Do not return a passage just because its document title matches.
            if query_terms and not matched_terms:
                continue

            normalized_text = " ".join(tokenize(original_text))
            normalized_query = " ".join(query_terms)

            exact_phrase_match = (
                bool(normalized_query)
                and normalized_query in normalized_text
            )

            relevance_score = (
                round(len(matched_terms) / len(query_terms), 3)
                if query_terms else 0.0
            )

            citation_url = (
                passage.get("citation_url")
                or passage.get("source_url")
                or document.get("citation_url")
            )

            results.append({
                "nasa_id": document_id,
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
            })

    results.sort(
        key=lambda item: (
            item["relevance_score"],
            item["exact_phrase_match"],
            len(item["matched_terms"]),
        ),
        reverse=True,
    )

    return results[:limit]
