from collections import Counter
from pathlib import Path

from backend.services.bass2_dataset import search_bass2_records
from backend.services.nasa_online import search_nasa_online
from backend.services.research_summarizer import build_evidence_brief, tokenize
from backend.services.subhan_research import search_subhan_research
from backend.services.supplemental_research_search import search_supplemental_research


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_STORE_PATH = PROJECT_ROOT / "data" / "processed" / "research_intelligence_store.json"
DEFAULT_MIN_LOCAL_PASSAGES = 3
DEFAULT_MIN_LOCAL_SOURCES = 2
DEFAULT_MIN_QUERY_TERM_COVERAGE = 0.6


def _build_search_query(query, mission=None, fuel=None, environment_context=None):
    """Add user-supplied mission context to retrieval without changing the raw question."""
    parts = [query.strip()]
    for value in (mission, fuel, environment_context):
        if isinstance(value, str) and value.strip():
            parts.append(value.strip())
        elif isinstance(value, dict):
            parts.extend(
                f"{key} {value_part}"
                for key, value_part in value.items()
                if value_part is not None and str(value_part).strip()
            )
    return " ".join(dict.fromkeys(parts))


def _provenance_entry(item):
    return {
        "source_dataset": item.get("source_dataset"),
        "source_owner": item.get("source_owner"),
        "source_id": item.get("source_id"),
        "record_id": item.get("record_id"),
        "citation_url": item.get("citation_url") or item.get("source_url"),
        "pdf_page_number": item.get("pdf_page_number"),
        "retrieved_at_utc": item.get("retrieved_at_utc"),
    }


def _add_provenance(target, item):
    entry = _provenance_entry(item)
    entries = target.setdefault("source_provenance", [])
    if entry not in entries:
        entries.append(entry)
    presence = item.get("source_dataset") or item.get("source") or "unknown_source"
    target.setdefault("source_presence", [])
    if presence not in target["source_presence"]:
        target["source_presence"].append(presence)


def _deduplicate_passages(items):
    """Deduplicate identical source/page excerpts while retaining every provenance record."""
    unique = {}
    for item in items:
        excerpt = " ".join(str(item.get("exact_source_excerpt") or "").casefold().split())
        source_id = str(item.get("source_id") or item.get("citation_url") or item.get("record_id") or "")
        page = str(item.get("pdf_page_number") or "")
        key = (source_id.casefold(), page, excerpt)
        if key not in unique:
            unique[key] = dict(item)
            unique[key]["source_presence"] = []
            unique[key]["source_provenance"] = []
        _add_provenance(unique[key], item)

    results = list(unique.values())
    # This is lexical retrieval ordering only; scientific evidence ranking is a later phase.
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
    fuel=None,
    mission=None,
    environment_context=None,
    min_local_passages=DEFAULT_MIN_LOCAL_PASSAGES,
    min_local_sources=DEFAULT_MIN_LOCAL_SOURCES,
    min_query_term_coverage=DEFAULT_MIN_QUERY_TERM_COVERAGE,
):
    """Federated retrieval: Subhan + project-local NASA/BASS-II, then NTRS on thin coverage."""
    if not isinstance(query, str) or len(query.strip()) < 2:
        raise ValueError("Query must contain at least two characters.")
    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 100:
        raise ValueError("limit must be an integer between 1 and 100.")
    if not 0 <= min_query_term_coverage <= 1:
        raise ValueError("min_query_term_coverage must be between 0 and 1.")
    if mission is not None and (not isinstance(mission, str) or len(mission) > 80):
        raise ValueError("mission must be a string of at most 80 characters.")
    if environment_context is not None and not isinstance(environment_context, (str, dict)):
        raise ValueError("environment_context must be a string or an object.")
    if isinstance(environment_context, str) and len(environment_context) > 500:
        raise ValueError("environment_context must not exceed 500 characters.")

    search_query = _build_search_query(query, mission, fuel, environment_context)

    # 1. Search Subhan's verified passages and preliminary discovery index separately.
    subhan = search_subhan_research(
        search_query,
        limit=limit,
        core_path=subhan_core_path,
        passages_path=subhan_passages_path,
        extended_path=subhan_extended_path,
    )

    # 2. Search the existing NASA primary research store.
    legacy_brief = build_evidence_brief(
        legacy_store_path or DEFAULT_STORE_PATH,
        search_query,
        limit=100,
    )
    legacy_results = [
        {
            **item,
            "source_dataset": "existing_local_nasa_research_store",
            "source_owner": "FlameGuard project",
        }
        for item in legacy_brief.get("results", [])
    ]

    # 3. Search previously imported NASA passages (review status remains attached).
    supplemental_results = search_supplemental_research(search_query, limit=100)
    combined_local = _deduplicate_passages(
        subhan["verified_core_evidence"] + legacy_results + supplemental_results
    )
    local_source_ids = {
        str(item.get("source_id"))
        for item in combined_local
        if item.get("source_id")
    }

    query_terms = tokenize(search_query)
    matched_terms = {
        term
        for item in combined_local
        for term in (item.get("matched_query_terms") or [])
    }
    query_term_coverage = len(matched_terms) / max(len(query_terms), 1)

    reasons = []
    if len(combined_local) < min_local_passages:
        reasons.append("too_few_local_evidence_passages")
    if len(local_source_ids) < min_local_sources:
        reasons.append("insufficient_distinct_local_source_coverage")
    if query_term_coverage < min_query_term_coverage:
        reasons.append("insufficient_query_term_coverage")

    # 4. BASS-II is searched as structured experimental context, never mixed into PDF passages.
    bass2_matches = search_bass2_records(query=query, limit=limit, fuel=fuel)

    # 5. Search the official NASA NTRS catalogue only when local evidence is insufficient.
    fallback_triggered = bool(reasons)
    online_search = {
        "performed": False,
        "source": "NASA NTRS",
        "status": "not_needed_local_coverage_sufficient",
        "query": search_query,
        "count": 0,
        "results": [],
        "content_scope": "not_searched",
    }

    if fallback_triggered:
        raw_online = search_nasa_online(search_query, limit)
        online_results = raw_online.get("results", [])
        if not isinstance(online_results, list):
            online_results = []

        online_metadata = [
            {
                **item,
                "record_type": "nasa_ntrs_catalog_metadata",
                "source_presence": ["nasa_ntrs_online"],
                "source_provenance": [{
                    "source_dataset": "nasa_ntrs_online",
                    "source_owner": "NASA",
                    "source_id": item.get("nasa_id"),
                    "record_id": item.get("nasa_id"),
                    "citation_url": item.get("source_url"),
                    "pdf_page_number": None,
                    "retrieved_at_utc": item.get("retrieved_at_utc"),
                }],
                "evidence_scope": "bibliographic_metadata_and_abstract_only",
                "full_text_retrieved": False,
                "scientific_findings_verified": False,
            }
            for item in online_results
        ]

        local_by_source = {
            str(item.get("source_id")): item
            for item in combined_local
            if item.get("source_id")
        }
        unique_online_metadata = []
        for metadata in online_metadata:
            nasa_id = str(metadata.get("nasa_id") or "")
            local_match = local_by_source.get(nasa_id)
            if local_match:
                local_match["online_catalog_metadata"] = metadata
                _add_provenance(local_match, {
                    "source_dataset": "nasa_ntrs_online",
                    "source_owner": "NASA",
                    "source_id": nasa_id,
                    "record_id": nasa_id,
                    "source_url": metadata.get("source_url"),
                    "retrieved_at_utc": metadata.get("retrieved_at_utc"),
                })
            else:
                unique_online_metadata.append(metadata)

        online_search = {
            "performed": True,
            "source": raw_online.get("source", "NASA NTRS"),
            "status": "unavailable" if raw_online.get("error") else "completed",
            "query": search_query,
            "count": len(unique_online_metadata),
            "results": unique_online_metadata,
            "content_scope": "bibliographic_metadata_and_abstract_only",
        }
        if raw_online.get("error"):
            online_search["error"] = raw_online["error"]

    role_counts = Counter(
        item.get("evidence_role", "unclassified")
        for item in combined_local[:limit]
    )
    modality_counts = Counter(
        item.get("evidence_modality", "unknown")
        for item in combined_local[:limit]
    )

    return {
        "query": query,
        "search_query": search_query,
        "search_context": {
            "mission": mission,
            "fuel": fuel,
            "environment": environment_context,
        },
        "search_strategy": "subhan_local_first_then_project_local_then_nasa_ntrs",
        "fallback_triggered": fallback_triggered,
        "fallback_reason": reasons,
        "local_coverage": {
            "passage_count_before_display_limit": len(combined_local),
            "distinct_source_count": len(local_source_ids),
            "query_term_coverage": round(query_term_coverage, 4),
            "minimum_passages": min_local_passages,
            "minimum_distinct_sources": min_local_sources,
            "minimum_query_term_coverage": min_query_term_coverage,
            "evidence_role_counts": dict(role_counts),
            "evidence_modality_counts": dict(modality_counts),
        },
        "local_evidence": combined_local[:limit],
        "bass2_structured_experimental_data": {
            "query_relevant_record_count": len(bass2_matches),
            "results": [
                {
                    **item,
                    "source_owner": "FlameGuard BASS-II dataset",
                    "source_dataset": "BASS-II structured experimental dataset",
                    "scientific_findings_verified": False,
                    "raw_values_preserved": True,
                }
                for item in bass2_matches
            ],
            "notice": "BASS-II rows are raw structured experiment records. Original values are preserved; quality flags and units require inspection before comparison.",
        },
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
            "supplemental_live_nasa_matches": len(supplemental_results),
        },
        "online_search": online_search,
        "counts": {
            "subhan_verified_core_matches": subhan["verified_core_evidence_count"],
            "existing_local_matches": len(legacy_results),
            "supplemental_live_nasa_matches": len(supplemental_results),
            "combined_unique_local_passages": len(combined_local),
            "query_relevant_bass2_records": len(bass2_matches),
            "online_ntrs_unique_metadata_records": online_search["count"],
        },
        "limitations": [
            "Subhan verified-core passages were checked against stated PDF pages; independent scientific verification is not claimed.",
            "Subhan extended-index entries are discovery metadata only and are never presented as verified findings.",
            "NASA NTRS fallback returns catalogue metadata and abstracts, not analysed full-text PDFs.",
            "NTRS metadata matching an existing source is attached as provenance rather than duplicated as a second finding.",
            "BASS-II structured rows remain separate from PDF evidence passages; original values are not modified.",
            "NASA documents require explicit import; imported passages remain review-pending and are searchable on later requests.",
            "Lexical match scores indicate word overlap only, not scientific quality, confidence, or mission safety.",
            "This search is a research aid, not an operational fire-safety certification or safe/unsafe prediction.",
        ],
    }
