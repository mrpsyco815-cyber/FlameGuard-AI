from collections import Counter

from backend.services.nasa_online import search_nasa_online
from backend.services.research_summarizer import DEFAULT_STORE_PATH, build_evidence_brief
from backend.services.subhan_research import search_subhan_research


DEFAULT_MIN_LOCAL_PASSAGES = 3
DEFAULT_MIN_LOCAL_SOURCES = 2


def _deduplicate_passages(items):
    unique = {}
    for item in items:
        excerpt = " ".join(str(item.get("exact_source_excerpt") or "").casefold().split())
        source_id = str(item.get("source_id") or "")
        page = str(item.get("pdf_page_number") or "")
        key = (source_id.casefold(), page, excerpt)
        if key not in unique:
            unique[key] = dict(item)
            unique[key]["source_presence"] = [item.get("source_dataset", "existing_local_store")]
        else:
            current = unique[key]
            presence = item.get("source_dataset", "existing_local_store")
            if presence not in current["source_presence"]:
                current["source_presence"].append(presence)
    results = list(unique.values())
    results.sort(
        key=lambda item: (
            -float(item.get("query_match_score") or 0),
            str(item.get("source_id") or ""),
            item.get("pdf_page_number") or 0,
        )
    )
    return results


def search_mission_research(
    query,
    limit=10,
    legacy_store_path=None,
    subhan_core_path=None,
    subhan_passages_path=None,
    subhan_extended_path=None,
    min_local_passages=DEFAULT_MIN_LOCAL_PASSAGES,
    min_local_sources=DEFAULT_MIN_LOCAL_SOURCES,
):
    """Search Subhan's local data first, then local NASA passages, then NTRS."""
    if not isinstance(query, str) or len(query.strip()) < 2:
        raise ValueError("Query must contain at least two characters.")
    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 100:
        raise ValueError("limit must be an integer between 1 and 100.")

    subhan = search_subhan_research(
        query,
        limit=limit,
        core_path=subhan_core_path,
        passages_path=subhan_passages_path,
        extended_path=subhan_extended_path,
    )

    legacy_brief = build_evidence_brief(
        legacy_store_path or DEFAULT_STORE_PATH,
        query,
        limit=100,
    )
    legacy_results = []
    for item in legacy_brief.get("results", []):
        legacy_results.append({
            **item,
            "source_dataset": "existing_local_nasa_research_store",
            "source_owner": "FlameGuard project",
        })

    subhan_results = subhan["verified_core_evidence"]
    combined_local = _deduplicate_passages(subhan_results + legacy_results)
    local_source_ids = {
        str(item.get("source_id"))
        for item in combined_local
        if item.get("source_id")
    }

    reasons = []
    if len(combined_local) < min_local_passages:
        reasons.append("too_few_local_evidence_passages")
    if len(local_source_ids) < min_local_sources:
        reasons.append("insufficient_distinct_local_source_coverage")

    fallback_triggered = bool(reasons)
    online_search = {
        "performed": False,
        "source": "NASA NTRS",
        "status": "not_needed_local_coverage_sufficient",
        "query": query,
        "count": 0,
        "results": [],
        "content_scope": "not_searched",
    }

    if fallback_triggered:
        raw_online = search_nasa_online(query, limit)
        online_results = raw_online.get("results", [])
        if not isinstance(online_results, list):
            online_results = []
        online_search = {
            "performed": True,
            "source": raw_online.get("source", "NASA NTRS"),
            "status": "unavailable" if raw_online.get("error") else "completed",
            "query": query,
            "count": len(online_results),
            "results": [
                {
                    **item,
                    "record_type": "nasa_ntrs_catalog_metadata",
                    "source_presence": ["nasa_ntrs_online"],
                    "evidence_scope": "bibliographic_metadata_and_abstract_only",
                    "full_text_retrieved": False,
                    "scientific_findings_verified": False,
                }
                for item in online_results
            ],
            "content_scope": "bibliographic_metadata_and_abstract_only",
        }
        if raw_online.get("error"):
            online_search["error"] = raw_online["error"]

    role_counts = Counter(item.get("evidence_role", "unclassified") for item in combined_local[:limit])
    modality_counts = Counter(item.get("evidence_modality", "unknown") for item in combined_local[:limit])

    return {
        "query": query,
        "search_strategy": "subhan_local_first_then_project_local_then_nasa_ntrs",
        "fallback_triggered": fallback_triggered,
        "fallback_reason": reasons,
        "local_coverage": {
            "passage_count_before_display_limit": len(combined_local),
            "distinct_source_count": len(local_source_ids),
            "minimum_passages": min_local_passages,
            "minimum_distinct_sources": min_local_sources,
            "evidence_role_counts": dict(role_counts),
            "evidence_modality_counts": dict(modality_counts),
        },
        "local_evidence": combined_local[:limit],
        "subhan_data": {
            "core_record_count": subhan["core_record_count"],
            "core_passage_count": subhan["core_passage_count"],
            "matched_core_passages": subhan["verified_core_evidence_count"],
            "verified_core_results": subhan["verified_core_evidence"][:limit],
            "preliminary_index_match_count": subhan["preliminary_index_match_count"],
            "preliminary_index_matches": subhan["preliminary_index_matches"][:limit],
            "data_quality": subhan["data_quality"],
            "notice": subhan["notice"],
        },
        "existing_local_store": {
            "candidate_passage_count": legacy_brief["summary"]["candidate_passage_count"],
            "source_document_count": legacy_brief["summary"]["source_document_count"],
            "retrieval_method": legacy_brief["retrieval_method"],
        },
        "online_search": online_search,
        "counts": {
            "subhan_verified_core_matches": subhan["verified_core_evidence_count"],
            "existing_local_matches": len(legacy_results),
            "combined_unique_local_passages": len(combined_local),
            "online_ntrs_metadata_records": online_search["count"],
        },
        "limitations": [
            "Subhan's 10-record verified core contains 68 PDF-page-checked passages; independent scientific verification is not claimed.",
            "Subhan's 176-entry extended index is preliminary and is never treated as verified evidence.",
            "NASA NTRS fallback currently returns catalog metadata and abstracts; it does not claim to have retrieved or analysed full-text PDFs.",
            "Online discoveries are not automatically added to the permanent local dataset.",
            "Lexical match scores indicate word overlap, not scientific quality, confidence, or mission safety.",
            "This search is a research aid, not an operational fire-safety certification or safe/unsafe prediction.",
        ],
    }
