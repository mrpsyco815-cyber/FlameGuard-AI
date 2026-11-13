import requests
from datetime import datetime, timezone

from backend.services.query_understanding import (
    MATERIALS,
    parse_query,
    score_text,
)
from backend.services.ranking_contract import (
    annotate_duplicate_sources,
    build_ranking_contract,
)

NASA_NTRS_SEARCH_URL = "https://ntrs.nasa.gov/api/citations/search"

_NASA_QUERY_CONCEPTS = (
    ("oxygen concentration", "oxygen concentration"),
    ("flame spread", "flame spread"),
    ("flame extinction", "extinction"),
    ("microgravity", "microgravity"),
    ("combustion", "combustion"),
    ("fire detection", "fire detection"),
    ("fire suppression", "fire suppression"),
    ("fire hazard", "fire hazard"),
)
MAX_FALLBACK_ATTEMPTS = 3


def build_nasa_fallback_queries(query: str) -> list[str]:
    """Return bounded, concept-specific NASA queries in priority order."""
    parsed = parse_query(query)
    focused = build_nasa_query(query)
    queries = [focused]
    if len(parsed.normalized) <= 200:
        return queries
    candidates = [
        "oxygen concentration microgravity combustion",
        "microgravity flame spread",
        "flame extinction oxygen",
        "BASS-II combustion experiments",
        "spacecraft material flammability",
    ]
    for candidate in candidates:
        if candidate not in queries:
            queries.append(candidate)
    return queries[:MAX_FALLBACK_ATTEMPTS]


def build_nasa_query(query: str) -> str:
    """Build a concise NASA query from explicit parsed scientific concepts."""
    parsed = parse_query(query)
    if len(parsed.tokens) <= 6 and len(parsed.normalized.split()) <= 6:
        return parsed.normalized
    terms = []
    for concept, output in _NASA_QUERY_CONCEPTS:
        if concept in parsed.concepts or concept in parsed.phenomena:
            terms.append(output)

    for material in parsed.materials:
        aliases = [
            alias for alias, canonical in MATERIALS.items()
            if canonical == material
        ]
        if any(
            f" {alias} " in f" {parsed.normalized} "
            for alias in aliases
        ) and material not in terms:
            terms.append(material)

    for condition in parsed.conditions:
        if condition in {"microgravity", "low pressure", "spaceflight"}:
            if condition not in terms:
                terms.append(condition)

    for unit in parsed.units:
        if unit not in terms:
            terms.append(unit)

    return " ".join(dict.fromkeys(terms)) or parsed.normalized


def search_nasa_online(query: str, limit: int = 5) -> dict:
    """Search NASA NTRS and return normalized bibliographic metadata."""

    if not isinstance(query, str) or len(query.strip()) < 2:
        return {
            "source": "NASA NTRS",
            "source_type": "nasa_ntrs",
            "query": query,
            "count": 0,
            "results": [],
        }

    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 100:
        raise ValueError("limit must be an integer between 1 and 100.")
    parsed_query = parse_query(query)
    normalized_query = parsed_query.normalized
    retrieval_timestamp = datetime.now(timezone.utc).isoformat()

    def request_query(search_query: str) -> tuple[list[dict], str | None]:
        response = requests.get(
            NASA_NTRS_SEARCH_URL,
            params={"q": search_query, "page.size": limit, "page": 1},
            timeout=20,
        )
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, dict):
            raise ValueError("NASA response must be an object.")
        records = payload.get("results", [])
        if not isinstance(records, list):
            raise ValueError("NASA response results must be a list.")
        return records, None

    def normalize_records(records: list[dict]) -> list[dict]:
        normalized = []
        seen_keys = set()
        for record in records:
            nasa_id = record.get("id")
            source_url = record.get("url") or (
                f"https://ntrs.nasa.gov/citations/{nasa_id}"
                if nasa_id is not None else None
            )
            key = (
                f"id:{str(nasa_id).strip()}" if nasa_id is not None
                else f"url:{source_url}" if source_url
                else f"record:{record.get('title')}:{record.get('abstract')}"
            )
            if key in seen_keys:
                continue
            seen_keys.add(key)
            abstract = record.get("abstract") or ""
            relevance = score_text(
                parsed_query,
                f"{record.get('title') or ''} {abstract}",
            )
            author_affiliations = record.get("authorAffiliations") or []
            authors = []
            for item in author_affiliations:
                meta = item.get("meta") or {}
                author = meta.get("author") or {}
                organization = meta.get("organization") or {}
                if author.get("name"):
                    authors.append({
                        "name": author["name"],
                        "affiliation": organization.get("name"),
                    })
            publications = record.get("publications") or []
            publication_date = next(
                (
                    publication.get("publicationDate")
                    for publication in publications
                    if publication.get("publicationDate")
                ),
                None,
            )
            center = record.get("center") or {}
            normalized.append({
                "title": record.get("title"),
                "abstract": record.get("abstract"),
                "nasa_id": nasa_id,
                "source_url": source_url,
                "source": "NASA NTRS",
                "authors": authors,
                "publication_date": publication_date,
                "keywords": record.get("keywords") or [],
                "subject_categories": record.get("subjectCategories") or [],
                "document_type": record.get("stiTypeDetails") or record.get("stiType"),
                "dissemination_status": record.get("disseminated"),
                "document_available": record.get("disseminated") == "DOCUMENT_AND_METADATA",
                "center": center.get("name"),
                "verification_status": "metadata_retrieved",
                "evidence_type": "bibliographic_metadata_and_abstract",
                "full_text_retrieved": False,
                "scientific_findings_verified": False,
                "review_status": "not_scientifically_reviewed",
                "relevance_score": relevance["score"],
                "matching_reasons": relevance["matching_reasons"],
                "retrieval_timestamp": retrieval_timestamp,
                "retrieved_at": retrieval_timestamp,
            })
        normalized.sort(key=lambda item: item["relevance_score"], reverse=True)
        normalized = annotate_duplicate_sources(normalized[:limit])
        for item in normalized:
            item["ranking_contract"] = build_ranking_contract(
                query=parsed_query,
                original_score=item["relevance_score"],
                record=item,
                source_text=f"{item.get('title') or ''} {item.get('abstract') or ''}",
                evidence_scope_name="abstract",
            )
            item["ranking_contract"]["duplicate_source"] = item["duplicate_source"]
        return normalized

    try:
        records, _ = request_query(normalized_query)
        results = normalize_records(records)

        response_result = {
            "source": "NASA NTRS",
            "query": query,
            "normalized_query": normalized_query,
            "count": len(results),
            "results": results,
            "retrieval_timestamp": retrieval_timestamp,
            "retrieved_at": retrieval_timestamp,
        }
        response_result.update({
            "original_query": query,
            "nasa_query": normalized_query,
            "fallback_attempted": False,
            "fallback_reason": None,
            "original_result_count": len(results),
            "fallback_result_count": 0,
        })
        if results:
            return response_result

        fallback_queries = [
            item for item in build_nasa_fallback_queries(query)
            if item != normalized_query
        ]
        if not fallback_queries:
            return response_result

        attempts = []
        merged = []
        seen_ids = set()
        for fallback_query in fallback_queries:
            try:
                fallback_records, _ = request_query(fallback_query)
                fallback_results = normalize_records(fallback_records)
                attempts.append({
                    "query": fallback_query,
                    "status": "completed",
                    "result_count": len(fallback_results),
                    "reason": (
                        "relevant_records_returned"
                        if fallback_results else "zero_results"
                    ),
                })
                for item in fallback_results:
                    key = str(item.get("nasa_id") or item.get("source_url"))
                    if key not in seen_ids:
                        seen_ids.add(key)
                        merged.append(item)
                if len(merged) >= limit:
                    break
            except requests.RequestException as exc:
                attempts.append({
                    "query": fallback_query,
                    "status": "network_error",
                    "result_count": 0,
                    "reason": str(exc),
                })
            except (ValueError, TypeError) as exc:
                attempts.append({
                    "query": fallback_query,
                    "status": "invalid_response",
                    "result_count": 0,
                    "reason": str(exc),
                })
        merged = merged[:limit]
        response_result.update({
            "results": merged,
            "count": len(merged),
            "nasa_query": attempts[0]["query"] if attempts else normalized_query,
            "fallback_attempted": bool(attempts),
            "fallback_reason": "original_query_returned_zero_results",
            "original_result_count": 0,
            "fallback_result_count": len(merged),
            "fallback_attempts": attempts,
        })
        return response_result

    except requests.RequestException:
        return {
            "source": "NASA NTRS",
            "query": query,
            "normalized_query": normalized_query,
            "count": 0,
            "results": [],
            "retrieval_timestamp": retrieval_timestamp,
            "retrieved_at": retrieval_timestamp,
            "error": "NASA online search is temporarily unavailable.",
            "original_query": query,
            "nasa_query": normalized_query,
            "fallback_attempted": False,
            "fallback_reason": "technical_error",
            "original_result_count": 0,
            "fallback_result_count": 0,
        }

    except (ValueError, AttributeError, TypeError):
        return {
            "source": "NASA NTRS",
            "query": query,
            "normalized_query": normalized_query,
            "count": 0,
            "results": [],
            "retrieval_timestamp": retrieval_timestamp,
            "error": "NASA returned an unexpected response.",
            "original_query": query,
            "nasa_query": normalized_query,
            "fallback_attempted": False,
            "fallback_reason": "technical_error",
            "original_result_count": 0,
            "fallback_result_count": 0,
        }
