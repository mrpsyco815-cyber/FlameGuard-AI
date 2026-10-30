from datetime import datetime, timezone

import requests


NASA_NTRS_SEARCH_URL = "https://ntrs.nasa.gov/api/citations/search"


def _utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def search_nasa_online(query: str, limit: int = 5) -> dict:
    """Search NASA NTRS and return catalogue metadata with retrieval provenance."""
    query = query.strip()

    if len(query) < 2:
        return {
            "source": "NASA NTRS",
            "query": query,
            "count": 0,
            "results": [],
        }

    try:
        response = requests.get(
            NASA_NTRS_SEARCH_URL,
            params={"q": query, "page.size": limit},
            timeout=20,
        )
        response.raise_for_status()
        payload = response.json()
        records = payload.get("results", [])
        retrieved_at_utc = _utc_now()
        results = []

        for record in records[:limit]:
            nasa_id = record.get("id")
            author_affiliations = record.get("authorAffiliations") or []
            authors = []

            for item in author_affiliations:
                meta = item.get("meta") or {}
                author = meta.get("author") or {}
                organization = meta.get("organization") or {}
                name = author.get("name")
                if name:
                    authors.append({
                        "name": name,
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

            results.append({
                "title": record.get("title"),
                "abstract": record.get("abstract"),
                "nasa_id": nasa_id,
                "source_url": (
                    f"https://ntrs.nasa.gov/citations/{nasa_id}"
                    if nasa_id is not None
                    else None
                ),
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
                "retrieved_at_utc": retrieved_at_utc,
                "evidence_scope": "bibliographic_metadata_and_abstract_only",
                "full_text_retrieved": False,
                "scientific_findings_verified": False,
            })

        return {
            "source": "NASA NTRS",
            "query": query,
            "count": len(results),
            "retrieved_at_utc": retrieved_at_utc,
            "results": results,
        }

    except requests.RequestException:
        return {
            "source": "NASA NTRS",
            "query": query,
            "count": 0,
            "results": [],
            "error": "NASA online search is temporarily unavailable.",
        }

    except (ValueError, AttributeError, TypeError):
        return {
            "source": "NASA NTRS",
            "query": query,
            "count": 0,
            "results": [],
            "error": "NASA returned an unexpected response.",
        }
