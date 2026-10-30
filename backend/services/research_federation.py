from collections import Counter
from pathlib import Path

from backend.services.nasa_online import search_nasa_online
from backend.services.research_summarizer import build_evidence_brief


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_STORE_PATH = (
    PROJECT_ROOT / "data" / "processed" / "research_intelligence_store.json"
)

DEFAULT_MIN_LOCAL_PASSAGES = 3
DEFAULT_MIN_LOCAL_SOURCES = 2


def _source_key(nasa_id, citation_url):
    if nasa_id is not None and str(nasa_id).strip():
        return f"id:{str(nasa_id).strip().casefold()}"

    if citation_url:
        return f"url:{str(citation_url).strip().casefold()}"

    return None


def _build_combined_sources(local_results, online_results):
    sources = {}

    for item in local_results:
        nasa_id = item.get("source_id")
        citation_url = item.get("citation_url")
        key = _source_key(nasa_id, citation_url)

        if not key:
            continue

        if key not in sources:
            sources[key] = {
                "nasa_id": nasa_id,
                "title": item.get("source_title"),
                "citation_url": citation_url,
                "source_presence": [],
                "local_passage_count": 0,
                "local_record_ids": [],
                "local_pdf_pages": [],
                "local_evidence_roles": [],
                "local_evidence_modalities": [],
                "ntrs_metadata": None,
            }

        source = sources[key]

        local_origin = (
            "supplemental_research_collection"
            if item.get("record_origin") == "supplemental_research_collection"
            else "local_research_intelligence_store"
        )
        if local_origin not in source["source_presence"]:
            source["source_presence"].append(local_origin)

        source["local_passage_count"] += 1

        if item.get("record_id"):
            source["local_record_ids"].append(item["record_id"])

        if item.get("pdf_page_number") is not None:
            source["local_pdf_pages"].append(item["pdf_page_number"])

        role = item.get("evidence_role")
        if role and role not in source["local_evidence_roles"]:
            source["local_evidence_roles"].append(role)

        modality = item.get("evidence_modality")
        if modality and modality not in source["local_evidence_modalities"]:
            source["local_evidence_modalities"].append(modality)

    new_online_sources = 0
    merged_online_sources = 0

    for item in online_results:
        nasa_id = item.get("nasa_id")
        citation_url = item.get("source_url")
        key = _source_key(nasa_id, citation_url)

        if not key:
            continue

        if key in sources:
            source = sources[key]
            merged_online_sources += 1
        else:
            source = {
                "nasa_id": nasa_id,
                "title": item.get("title"),
                "citation_url": citation_url,
                "source_presence": [],
                "local_passage_count": 0,
                "local_record_ids": [],
                "local_pdf_pages": [],
                "local_evidence_roles": [],
                "local_evidence_modalities": [],
                "ntrs_metadata": None,
            }
            sources[key] = source
            new_online_sources += 1

        if "nasa_ntrs_online" not in source["source_presence"]:
            source["source_presence"].append("nasa_ntrs_online")

        if not source.get("title"):
            source["title"] = item.get("title")

        if not source.get("citation_url"):
            source["citation_url"] = citation_url

        source["ntrs_metadata"] = {
            "abstract": item.get("abstract"),
            "authors": item.get("authors") or [],
            "publication_date": item.get("publication_date"),
            "keywords": item.get("keywords") or [],
            "subject_categories": item.get("subject_categories") or [],
            "document_type": item.get("document_type"),
            "dissemination_status": item.get("dissemination_status"),
            "document_available": item.get("document_available", False),
            "verification_status": item.get(
                "verification_status", "metadata_retrieved"
            ),
            "evidence_scope": "bibliographic_metadata_and_abstract_only",
            "scientific_findings_verified": False,
        }

    combined = list(sources.values())

    for source in combined:
        source["local_record_ids"] = sorted(set(source["local_record_ids"]))
        source["local_pdf_pages"] = sorted(set(source["local_pdf_pages"]))
        source["local_evidence_roles"] = sorted(
            source["local_evidence_roles"]
        )
        source["local_evidence_modalities"] = sorted(
            source["local_evidence_modalities"]
        )

    combined.sort(
        key=lambda item: (
            0 if item["local_passage_count"] else 1,
            str(item.get("nasa_id") or ""),
        )
    )

    return combined, new_online_sources, merged_online_sources


def _refresh_local_brief(local_brief, display_limit):
    all_results = local_brief["results"]
    matched_count = len(all_results)
    displayed_results = all_results[:display_limit]

    local_brief["results"] = displayed_results

    role_counts = Counter(
        item["evidence_role"] for item in displayed_results
    )
    modality_counts = Counter(
        item["evidence_modality"] for item in displayed_results
    )
    source_count = len({
        item["source_id"]
        for item in displayed_results
        if item.get("source_id")
    })

    local_brief["summary"] = {
        "overview": (
            f"Displaying {len(displayed_results)} local candidate passages "
            f"from {source_count} NASA source document(s)."
        ),
        "candidate_passage_count": len(displayed_results),
        "source_document_count": source_count,
        "evidence_role_counts": dict(role_counts),
        "evidence_modality_counts": dict(modality_counts),
    }

    local_brief["search_audit"]["matched_passage_count_before_display_limit"] = (
        matched_count
    )
    local_brief["search_audit"]["display_limit"] = display_limit


def search_research_with_fallback(
    query,
    limit=10,
    store_path=None,
    min_local_passages=DEFAULT_MIN_LOCAL_PASSAGES,
    min_local_sources=DEFAULT_MIN_LOCAL_SOURCES,
):
    if not isinstance(query, str) or len(query.strip()) < 2:
        raise ValueError("Query must contain at least two characters.")

    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 100:
        raise ValueError("limit must be an integer between 1 and 100.")

    if not isinstance(min_local_passages, int) or min_local_passages < 0:
        raise ValueError("min_local_passages must be a non-negative integer.")

    if not isinstance(min_local_sources, int) or min_local_sources < 0:
        raise ValueError("min_local_sources must be a non-negative integer.")

    selected_store = Path(store_path) if store_path else DEFAULT_STORE_PATH

    # Probe enough records to assess local coverage even when the requested
    # display limit is smaller than the fallback threshold.
    probe_limit = max(limit, min_local_passages, 1)
    probe_limit = min(probe_limit, 100)

    local_brief = build_evidence_brief(
        selected_store,
        query,
        limit=probe_limit,
    )

    probe_results = local_brief["results"]
    local_source_ids = {
        item["source_id"]
        for item in probe_results
        if item.get("source_id")
    }

    insufficient_reasons = []

    if len(probe_results) < min_local_passages:
        insufficient_reasons.append("too_few_local_passages")

    if len(local_source_ids) < min_local_sources:
        insufficient_reasons.append("insufficient_local_source_coverage")

    fallback_triggered = bool(insufficient_reasons)

    _refresh_local_brief(local_brief, limit)
    local_results = local_brief["results"]

    online_response = {
        "performed": False,
        "source": "NASA NTRS",
        "query": query,
        "count": 0,
        "results": [],
        "content_scope": "not_searched",
    }

    if fallback_triggered:
        raw_online = search_nasa_online(query, limit)

        online_items = raw_online.get("results", [])
        if not isinstance(online_items, list):
            online_items = []

        online_response = {
            "performed": True,
            "source": raw_online.get("source", "NASA NTRS"),
            "query": query,
            "count": len(online_items),
            "results": [
                {
                    **item,
                    "record_type": "nasa_ntrs_catalog_metadata",
                    "evidence_scope": "bibliographic_metadata_and_abstract_only",
                    "scientific_findings_verified": False,
                }
                for item in online_items
            ],
            "content_scope": "bibliographic_metadata_and_abstract_only",
        }

        if raw_online.get("error"):
            online_response["error"] = raw_online["error"]
            online_response["status"] = "unavailable"
        else:
            online_response["status"] = "completed"

    online_items = online_response["results"]

    combined_sources, new_online_count, merged_online_count = (
        _build_combined_sources(local_results, online_items)
    )

    return {
        "query": query,
        "search_strategy": "local_first_with_nasa_ntrs_fallback",
        "fallback_triggered": fallback_triggered,
        "fallback_reason": insufficient_reasons,
        "fallback_thresholds": {
            "minimum_local_passages": min_local_passages,
            "minimum_distinct_local_sources": min_local_sources,
        },
        "local_evidence_brief": local_brief,
        "online_search": online_response,
        "combined_sources": combined_sources,
        "counts": {
            "local_passages_returned": len(local_results),
            "local_sources_returned": len(local_source_ids),
            "online_metadata_records": len(online_items),
            "new_online_sources_discovered": new_online_count,
            "online_sources_merged_with_local": merged_online_count,
            "unique_combined_sources": len(combined_sources),
        },
        "notices": [
            "Local passages retain their original record IDs, citations, and PDF pages.",
            "NASA NTRS fallback results are catalog metadata and abstracts, not full-text scientific findings.",
            "Online metadata is not independently scientifically verified.",
            "Local V3.4 classifications remain heuristic and require review.",
            "Query matching scores measure lexical overlap, not scientific quality or mission relevance.",
            "Online discoveries are returned for this search; they are not automatically inserted into the persistent research store.",
        ],
    }
