import json
import re
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CORE_PATH = PROJECT_ROOT / "data" / "processed" / "subhan_verified_core.json"
DEFAULT_PASSAGES_PATH = PROJECT_ROOT / "data" / "evidence" / "subhan_evidence_passages.json"
DEFAULT_EXTENDED_PATH = PROJECT_ROOT / "data" / "processed" / "subhan_extended_preliminary.json"

STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
    "in", "is", "it", "of", "on", "or", "that", "the", "their", "this",
    "to", "was", "were", "what", "when", "with", "how", "which",
}


def _tokens(value: Any) -> set[str]:
    words = re.findall(r"[a-z0-9]+", str(value or "").casefold())
    return {word for word in words if len(word) > 1 and word not in STOP_WORDS}


def _load_json(path: Path, expected_type):
    if not path.exists():
        raise FileNotFoundError(f"Subhan research data file not found: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in Subhan research data: {path}") from exc
    if not isinstance(value, expected_type):
        raise ValueError(f"Unexpected data structure in Subhan research file: {path}")
    return value


def search_subhan_research(
    query: str,
    limit: int = 10,
    core_path: str | Path | None = None,
    passages_path: str | Path | None = None,
    extended_path: str | Path | None = None,
) -> dict[str, Any]:
    """Search Subhan's PDF-checked core evidence and preliminary index separately."""
    if not isinstance(query, str) or len(query.strip()) < 2:
        raise ValueError("Query must contain at least two characters.")
    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 100:
        raise ValueError("limit must be an integer between 1 and 100.")

    terms = _tokens(query)
    if not terms:
        raise ValueError("Query must contain at least one meaningful search term.")

    core_file = Path(core_path) if core_path else DEFAULT_CORE_PATH
    passages_file = Path(passages_path) if passages_path else DEFAULT_PASSAGES_PATH
    extended_file = Path(extended_path) if extended_path else DEFAULT_EXTENDED_PATH

    core_records = _load_json(core_file, list)
    passage_payload = _load_json(passages_file, dict)
    extended_records = _load_json(extended_file, list)

    core_by_id = {
        str(record.get("study_id")): record
        for record in core_records
        if isinstance(record, dict) and record.get("study_id")
    }

    evidence_results = []
    for passage in passage_payload.get("evidence_passages", []):
        if not isinstance(passage, dict):
            continue
        excerpt = passage.get("evidence_text") or passage.get("text") or ""
        matched = sorted(terms.intersection(_tokens(excerpt)))
        if not matched:
            continue

        study_id = str(passage.get("study_id") or "")
        study = core_by_id.get(study_id, {})
        source_url = passage.get("source_url") or study.get("source_url")
        evidence_results.append({
            "record_id": f"SUBHAN-EVIDENCE-{study_id}-{passage.get('page', 'NA')}-{len(evidence_results) + 1}",
            "study_id": study_id,
            "source_id": (re.search(r"/(?:api/)?citations/(\d+)", str(source_url or "")) or [None, study_id])[1],
            "source_title": passage.get("title") or study.get("title"),
            "investigation": passage.get("investigation") or study.get("investigation"),
            "moon_mars_rank": study.get("moon_mars_rank"),
            "moon_mars_rank_reason": study.get("moon_mars_rank_reason"),
            "platform_type": study.get("platform_type"),
            "experiment_conditions": study.get("experiment_conditions"),
            "comparison_keys": study.get("comparison_keys"),
            "citation_url": source_url,
            "source_url": source_url,
            "file_name": passage.get("file_name") or study.get("file_name"),
            "pdf_page_number": passage.get("page"),
            "section_or_table": passage.get("section_or_table"),
            "experiment_context": passage.get("experiment_context"),
            "evidence_role": "source_checked_evidence_passage",
            "evidence_modality": "experiment",
            "source_owner": "Subhan Malik",
            "source_dataset": "Subhan verified core v2",
            "verification_status": study.get("verification_status", "verified_from_opened_pdf"),
            "scientific_findings_verified": False,
            "matched_query_terms": matched,
            "query_match_score": round(len(matched) / len(terms), 4),
            "exact_source_excerpt": excerpt,
        })

    evidence_results.sort(
        key=lambda item: (
            -item["query_match_score"],
            str(item.get("source_id") or ""),
            item.get("pdf_page_number") or 0,
        )
    )

    preliminary_results = []
    for record in extended_records:
        if not isinstance(record, dict):
            continue
        searchable = " ".join(str(record.get(field) or "") for field in (
            "study_id", "title", "investigation", "plain_summary",
            "publication_details", "comparison_keys",
        ))
        matched = sorted(terms.intersection(_tokens(searchable)))
        if not matched:
            continue
        preliminary_results.append({
            "study_id": record.get("study_id"),
            "title": record.get("title"),
            "investigation": record.get("investigation"),
            "plain_summary": record.get("plain_summary"),
            "source_url": record.get("source_url"),
            "verification_status": record.get("verification_status", "preliminary"),
            "missing_fields": record.get("missing_fields", []),
            "evidence_passage_count": len(record.get("evidence_passages") or []),
            "source_owner": "Subhan Malik",
            "source_dataset": "Subhan extended research index v2",
            "record_scope": "discovery_metadata_only_not_verified_evidence",
            "scientific_findings_verified": False,
            "matched_query_terms": matched,
            "query_match_score": round(len(matched) / len(terms), 4),
        })

    preliminary_results.sort(
        key=lambda item: (
            -item["query_match_score"],
            str(item.get("study_id") or ""),
        )
    )

    return {
        "source": "Subhan Malik research handover",
        "query": query,
        "core_record_count": len(core_records),
        "core_passage_count": passage_payload.get("total_passages", len(passage_payload.get("evidence_passages", []))),
        "verified_core_evidence_count": len(evidence_results),
        "verified_core_evidence": evidence_results[:limit],
        "preliminary_index_match_count": len(preliminary_results),
        "preliminary_index_matches": preliminary_results[:limit],
        "data_quality": {
            "core_status": "verified_from_opened_pdf",
            "core_record_count": len(core_records),
            "core_passage_inventory": passage_payload.get("total_passages"),
            "extended_record_count": len(extended_records),
            "extended_status": "preliminary_not_verified_and_not_176_unique_studies",
            "whole_psi_datasets_downloaded": False,
            "scientific_findings_verified": False,
        },
        "notice": (
            "Verified-core passages were checked against the stated PDF page by the data contributor; "
            "this does not constitute independent scientific verification. Extended-index entries are "
            "discovery metadata only and must not be presented as verified findings."
        ),
    }
