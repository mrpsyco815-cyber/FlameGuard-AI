import json
import re
from functools import lru_cache
from collections import Counter
from pathlib import Path

from backend.services.query_understanding import parse_query, score_text
from backend.services.ranking_contract import (
    annotate_duplicate_sources,
    build_ranking_contract,
)

ELIGIBLE_EVIDENCE_ROLES = {
    "experimental_quantitative_result",
    "experimental_observation",
    "experimental_comparative_result",
    "simulation_result",
    "mixed_comparison",
    "interpretation",
    "scientific_limitation",
    "simulation_limitation",
}

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_STORE_PATH = PROJECT_ROOT / "data" / "processed" / "research_intelligence_store.json"
DEFAULT_SUPPLEMENTAL_PATH = PROJECT_ROOT / "data" / "processed" / "supplemental_research_collection.json"

STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for",
    "from", "in", "is", "it", "of", "on", "or", "that", "the",
    "their", "this", "to", "was", "were", "what", "when", "with",
}


def tokenize(text):
    """Provide the legacy token interface used by remote research services."""
    words = re.findall(r"[a-z0-9]+", str(text).lower())
    return {word for word in words if len(word) > 1 and word not in STOP_WORDS}


@lru_cache(maxsize=8)
def _load_store_cached(path_string, modified_ns, file_size):
    path = Path(path_string)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Research intelligence store contains invalid JSON: {exc}") from exc

    if not isinstance(data, dict) or not isinstance(data.get("records"), list):
        raise ValueError("Invalid research store: expected a records list.")

    return data


def load_store(store_path):
    path = Path(store_path)

    if not path.exists():
        raise FileNotFoundError(f"Research intelligence store not found: {path}")

    metadata = path.stat()
    return _load_store_cached(
        str(path.resolve()),
        metadata.st_mtime_ns,
        metadata.st_size,
    )


def _review_status(record, classification):
    review = record.get("review") or {}

    return (
        classification.get("review_status")
        or review.get("classification_review_status")
        or review.get("source_review_status")
        or "not_recorded"
    )


def _make_result(record, scientific_query, record_origin):
    source = record.get("source") or {}
    content = record.get("content") or {}
    classification = record.get("classification") or {}
    review = record.get("review") or {}

    excerpt = content.get("text")
    if not isinstance(excerpt, str) or not excerpt.strip():
        return None

    relevance = score_text(scientific_query, excerpt)
    if not relevance["matched_terms"]:
        return None

    result = {
        "record_id": record.get("record_id"),
        "record_origin": record_origin,
        "import_origin": (record.get("provenance") or {}).get("import_origin"),
        "source_id": source.get("source_id"),
        "nasa_id": source.get("source_id"),
        "source_title": source.get("title"),
        "citation_url": source.get("citation_url"),
        "source_url": source.get("citation_url"),
        "pdf_page_number": source.get("pdf_page_number"),
        "evidence_role": classification.get("evidence_role", "unclassified"),
        "evidence_modality": classification.get("evidence_modality", "unknown"),
        "research_context": classification.get("research_context", "unknown"),
        "context_requirement": classification.get("context_requirement"),
        "classification_version": classification.get("classification_version"),
        "classification_review_status": _review_status(record, classification),
        "source_review_status": review.get("source_review_status", "not_recorded"),
        "evidence_type": (
            classification.get("evidence_role")
            or classification.get("evidence_modality")
        ),
        "scientific_findings_verified": (
            classification.get("scientific_findings_verified") is True
            and review.get("scientific_findings_verified") is True
        ),
        "matched_query_terms": relevance["matched_terms"],
        "query_match_score": relevance["score"],
        "relevance_components": relevance,
        "matching_reasons": relevance["matching_reasons"],
        "exact_source_excerpt": excerpt,
    }
    result["ranking_contract"] = build_ranking_contract(
        query=scientific_query,
        original_score=relevance["score"],
        record={
            **source,
            "source_id": source.get("source_id"),
            "nasa_id": source.get("source_id"),
            "source_type": "local_nasa_passage",
            "citation_url": source.get("citation_url"),
            "source_url": source.get("citation_url"),
            "pdf_page_number": source.get("pdf_page_number"),
            "exact_source_excerpt": excerpt,
            "evidence_type": classification.get("evidence_type"),
            "evidence_modality": classification.get("evidence_modality"),
            "classification": classification,
            "review": review,
            "provenance": record.get("provenance"),
            "scientific_findings_verified": result[
                "scientific_findings_verified"
            ],
        },
        source_text=excerpt,
    )
    return result


def _diversify_results(results, limit):
    """Prefer one high-ranked passage per source before filling the limit."""
    if len(results) <= limit:
        return results

    diversified = []
    deferred = []
    seen_sources = set()
    for item in results:
        source_id = (
            item.get("ranking_contract", {})
            .get("source_identity", {})
            .get("group_key")
            or item.get("source_id")
            or item.get("citation_url")
        )
        if source_id not in seen_sources:
            diversified.append(item)
            seen_sources.add(source_id)
        else:
            deferred.append(item)
        if len(diversified) == limit:
            return diversified

    return diversified + deferred[:limit - len(diversified)]


def build_evidence_brief(store_path=None, query="", limit=20):
    if not isinstance(query, str) or not query.strip():
        raise ValueError("A non-empty research query is required.")

    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 100:
        raise ValueError("limit must be an integer between 1 and 100.")

    scientific_query = parse_query(query)

    selected_store = Path(store_path) if store_path else DEFAULT_STORE_PATH
    store = load_store(selected_store)
    primary_records = [
        record for record in store["records"]
        if record.get("record_type") == "nasa_passage"
    ]

    supplemental_path = selected_store.parent / "supplemental_research_collection.json"
    supplemental_records = []
    if supplemental_path.exists():
        try:
            supplemental = json.loads(
                supplemental_path.read_text(encoding="utf-8")
            )
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Supplemental research collection contains invalid JSON: {exc}"
            ) from exc

        if not isinstance(supplemental, dict) or not isinstance(
            supplemental.get("records"), list
        ):
            raise ValueError(
                "Invalid supplemental collection: expected a records list."
            )

        supplemental_records = [
            record for record in supplemental["records"]
            if isinstance(record, dict)
            and record.get("record_type") == "nasa_passage"
        ]

    all_records = (
        [(record, "primary_research_intelligence_store") for record in primary_records]
        + [(record, "supplemental_research_collection") for record in supplemental_records]
    )

    all_role_counts = Counter()
    eligible_role_counts = Counter()
    results = []
    seen_record_ids = set()

    for record, record_origin in all_records:
        record_id = record.get("record_id")
        if record_id and record_id in seen_record_ids:
            continue
        if record_id:
            seen_record_ids.add(record_id)

        classification = record.get("classification") or {}
        role = classification.get("evidence_role", "unclassified")
        all_role_counts[role] += 1

        if role not in ELIGIBLE_EVIDENCE_ROLES:
            continue

        eligible_role_counts[role] += 1

        result = _make_result(record, scientific_query, record_origin)
        if result:
            results.append(result)

    results.sort(
        key=lambda item: (
            -item["query_match_score"],
            -len(item["matching_reasons"]),
            str(item.get("source_id") or ""),
            item.get("pdf_page_number") or 0,
            str(item.get("record_id") or ""),
        )
    )

    results = annotate_duplicate_sources(results)
    for item in results:
        item["ranking_contract"]["duplicate_source"] = item["duplicate_source"]

    pre_diversification_count = len(results)
    distinct_sources_before_display = len({
        item["source_id"] for item in results if item.get("source_id")
    })
    results = _diversify_results(results, limit)

    modality_counts = Counter(
        item["evidence_modality"] for item in results
    )
    matched_role_counts = Counter(
        item["evidence_role"] for item in results
    )

    source_count = len({
        item["source_id"] for item in results if item.get("source_id")
    })

    overview = (
        f"Retrieved {len(results)} candidate evidence passages "
        f"from {source_count} NASA source document(s)."
    )

    return {
        "engine": "FlameGuard Extractive Evidence Brief",
        "engine_version": "1.0",
        "query": query,
        "retrieval_method": "lexical_token_overlap",
        "ranking_note": (
            "Ranking combines normalized scientific terms, defensible "
            "concepts, materials, conditions, and numeric matches. It is "
            "not a measure of scientific quality, certainty, or evidence strength."
        ),
        "summary": {
            "overview": overview,
            "candidate_passage_count": len(results),
            "source_document_count": source_count,
            "evidence_role_counts": dict(matched_role_counts),
            "evidence_modality_counts": dict(modality_counts),
        },
        "search_audit": {
            "nasa_passages_examined": len(primary_records) + len(supplemental_records),
            "primary_nasa_passages_examined": len(primary_records),
            "supplemental_nasa_passages_examined": len(supplemental_records),
            "eligible_role_counts": dict(eligible_role_counts),
            "all_nasa_role_counts": dict(all_role_counts),
            "result_limit": limit,
            "matched_passage_count_before_display_limit": pre_diversification_count,
            "distinct_sources_before_display": distinct_sources_before_display,
            "source_diversification": (
                "one top-ranked passage per source is preferred before "
                "remaining ranked passages fill the display limit"
            ),
        },
        "results": results,
        "limitations": [
            "V3.4 evidence-role labels are heuristic classifications, not scientific verification.",
            "All excerpts remain subject to source and classification review.",
            "Extracted PDF text may contain OCR, formatting, or context errors.",
            "Experimental findings and simulation results are identified separately.",
            "BASS-II structured records are not included in this text-passage search.",
            "Supplemental NASA passages are searched alongside the primary store when available.",
            "This version does not generate scientific conclusions or fire-safety recommendations.",
        ],
    }
