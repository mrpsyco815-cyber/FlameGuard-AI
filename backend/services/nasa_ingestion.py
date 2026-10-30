import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

from backend.services.document_parser import (
    audit_pdf_identity,
    extract_pdf_pages,
)
from backend.services.evidence_classifier_v3_4 import (
    classify_passage_v3_4,
)
from backend.services.evidence_extractor import extract_page_evidence
from backend.services.nasa_documents import download_nasa_pdf


PROJECT_ROOT = Path(__file__).resolve().parents[2]
COLLECTION_RELATIVE_PATH = (
    Path("data") / "processed" / "supplemental_research_collection.json"
)
NASA_API_BASE = "https://ntrs.nasa.gov/api"
REQUEST_TIMEOUT = 20


def _empty_collection() -> dict[str, Any]:
    return {
        "collection_name": "FlameGuard Supplemental Research Collection",
        "schema_version": "1.0",
        "records": [],
        "documents": [],
    }


def load_supplemental_collection(
    project_root: Path | None = None,
) -> dict[str, Any]:
    root = project_root or PROJECT_ROOT
    path = root / COLLECTION_RELATIVE_PATH

    if not path.exists():
        return _empty_collection()

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Supplemental collection contains invalid JSON: {exc}"
        ) from exc

    if not isinstance(data, dict):
        raise ValueError("Supplemental collection must be a JSON object.")

    if not isinstance(data.get("records"), list):
        raise ValueError("Supplemental collection records must be a list.")

    if not isinstance(data.get("documents"), list):
        raise ValueError("Supplemental collection documents must be a list.")

    record_ids = [
        item.get("record_id")
        for item in data["records"]
        if isinstance(item, dict)
    ]

    if len(record_ids) != len(set(record_ids)):
        raise ValueError("Duplicate record IDs found in supplemental collection.")

    document_ids = [
        str(item.get("nasa_id"))
        for item in data["documents"]
        if isinstance(item, dict) and item.get("nasa_id")
    ]

    if len(document_ids) != len(set(document_ids)):
        raise ValueError("Duplicate NASA document IDs found in supplemental collection.")

    return data


def _save_collection(
    collection: dict[str, Any],
    project_root: Path | None = None,
) -> Path:
    root = project_root or PROJECT_ROOT
    output_path = root / COLLECTION_RELATIVE_PATH
    output_path.parent.mkdir(parents=True, exist_ok=True)

    temporary_path = output_path.with_name(
        output_path.name + ".tmp"
    )

    try:
        temporary_path.write_text(
            json.dumps(collection, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        temporary_path.replace(output_path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()

    return output_path


def _extract_authors(metadata: dict[str, Any]) -> list[dict[str, Any]]:
    authors = []

    for item in metadata.get("authorAffiliations") or []:
        meta = item.get("meta") or {}
        author = meta.get("author") or {}
        organization = meta.get("organization") or {}

        name = author.get("name")
        if name:
            authors.append({
                "name": name,
                "affiliation": organization.get("name"),
            })

    return authors


def _fetch_citation(nasa_id: str) -> dict[str, Any]:
    url = f"{NASA_API_BASE}/citations/{nasa_id}"

    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    metadata = response.json()

    if not isinstance(metadata, dict):
        raise ValueError("NASA citation response was not a JSON object.")

    returned_id = str(metadata.get("id") or "")

    if returned_id != nasa_id:
        raise ValueError(
            f"NASA citation ID mismatch: requested {nasa_id}, "
            f"received {returned_id or 'missing'}."
        )

    if not isinstance(metadata.get("title"), str) or not metadata["title"].strip():
        raise ValueError("NASA citation metadata is missing its title.")

    return metadata


def import_nasa_document(
    nasa_id: str,
    project_root: Path | None = None,
) -> dict[str, Any]:
    """
    Download, identity-check, extract and add one NASA NTRS PDF.

    Imported passages remain pending manual review.
    Original research source files and V3.4 audit files are not modified.
    """

    if not isinstance(nasa_id, str) or not nasa_id.isdigit():
        return {
            "success": False,
            "status": "invalid_nasa_id",
            "error": "NASA ID must contain digits only.",
        }

    root = project_root or PROJECT_ROOT

    try:
        collection = load_supplemental_collection(root)
    except (OSError, ValueError) as exc:
        return {
            "success": False,
            "status": "collection_error",
            "error": str(exc),
        }

    # Do not duplicate a paper already present in the audited primary dataset.
    primary_dataset_path = (
        root / "data" / "processed" / "nasa_combined_evidence.json"
    )
    if primary_dataset_path.exists():
        try:
            primary_dataset = json.loads(
                primary_dataset_path.read_text(encoding="utf-8-sig")
            )
        except (OSError, json.JSONDecodeError) as exc:
            return {
                "success": False,
                "status": "primary_dataset_read_failed",
                "nasa_id": nasa_id,
                "error": str(exc),
            }

        primary_ids = {
            str(document.get("nasa_id"))
            for document in primary_dataset.get("documents", [])
            if isinstance(document, dict) and document.get("nasa_id")
        }
        if nasa_id in primary_ids:
            return {
                "success": True,
                "status": "already_in_primary_collection",
                "nasa_id": nasa_id,
                "title": next(
                    (
                        document.get("title")
                        for document in primary_dataset.get("documents", [])
                        if isinstance(document, dict)
                        and str(document.get("nasa_id")) == nasa_id
                    ),
                    None,
                ),
                "passage_count": 0,
                "collection_path": str(primary_dataset_path),
            }

    existing_document = next(
        (
            document
            for document in collection["documents"]
            if str(document.get("nasa_id")) == nasa_id
        ),
        None,
    )

    if existing_document:
        return {
            "success": True,
            "status": "already_imported",
            "nasa_id": nasa_id,
            "title": existing_document.get("title"),
            "passage_count": existing_document.get("passage_count", 0),
            "collection_path": str(root / COLLECTION_RELATIVE_PATH),
        }

    try:
        metadata = _fetch_citation(nasa_id)
    except (requests.RequestException, ValueError, TypeError) as exc:
        return {
            "success": False,
            "status": "citation_lookup_failed",
            "nasa_id": nasa_id,
            "error": str(exc),
        }

    citation_url = f"https://ntrs.nasa.gov/citations/{nasa_id}"

    # Only import the PDF when NASA provides it through its existing
    # validated download service.
    download_result = download_nasa_pdf(nasa_id)

    if not download_result.get("success"):
        return {
            "success": False,
            "status": "pdf_unavailable",
            "nasa_id": nasa_id,
            "title": metadata["title"],
            "citation_url": citation_url,
            "error": download_result.get(
                "error", "NASA PDF download was unsuccessful."
            ),
            "metadata_only": True,
        }

    identity = audit_pdf_identity(nasa_id)

    if not identity.get("success"):
        return {
            "success": False,
            "status": "pdf_identity_audit_failed",
            "nasa_id": nasa_id,
            "title": metadata["title"],
            "citation_url": citation_url,
            "error": identity.get("error"),
        }

    if not identity.get("visible_title_matches_api"):
        return {
            "success": False,
            "status": "pdf_identity_requires_manual_review",
            "nasa_id": nasa_id,
            "title": metadata["title"],
            "citation_url": citation_url,
            "identity_audit": identity,
            "error": (
                "The PDF first page did not confirm the NASA catalogue title. "
                "No passages were added to the collection."
            ),
        }

    extraction = extract_pdf_pages(nasa_id)

    if not extraction.get("success"):
        return {
            "success": False,
            "status": "pdf_text_extraction_failed",
            "nasa_id": nasa_id,
            "title": metadata["title"],
            "citation_url": citation_url,
            "error": extraction.get("error"),
        }

    pages = extraction.get("pages") or []
    if not pages:
        return {
            "success": False,
            "status": "no_pdf_pages",
            "nasa_id": nasa_id,
            "title": metadata["title"],
            "citation_url": citation_url,
            "error": "No PDF pages were extracted.",
        }

    retrieved_at = datetime.now(timezone.utc).isoformat()
    authors = _extract_authors(metadata)
    new_records = []
    empty_page_count = sum(
        1 for page in pages
        if not str(page.get("text") or "").strip()
    )

    try:
        extracted_evidence = extract_page_evidence(nasa_id)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return {
            "success": False,
            "status": "evidence_extraction_failed",
            "nasa_id": nasa_id,
            "title": metadata["title"],
            "citation_url": citation_url,
            "error": str(exc),
        }

    candidate_passages = extracted_evidence.get("passages") or []
    if not candidate_passages:
        return {
            "success": False,
            "status": "no_text_passages",
            "nasa_id": nasa_id,
            "title": metadata["title"],
            "citation_url": citation_url,
            "error": "The page evidence extractor returned no candidate passages.",
            "empty_pages": empty_page_count,
        }

    page_text_lookup = {
        page.get("pdf_page_number"): page.get("text") or ""
        for page in pages
    }
    page_counters = {}

    for passage in candidate_passages:
        page_number = passage.get("pdf_page_number")
        sentence = passage.get("text")

        if (
            not isinstance(page_number, int)
            or page_number < 1
            or not isinstance(sentence, str)
            or not sentence.strip()
        ):
            continue

        page_counters[page_number] = page_counters.get(page_number, 0) + 1
        sentence_index = page_counters[page_number]
        page_text = page_text_lookup.get(page_number, "")

        classification = classify_passage_v3_4(
            {
                "text": sentence,
                "pdf_page_number": page_number,
            },
            page_context=page_text,
        )

        classification = dict(classification)
        classification["classification_version"] = "3.4"
        classification["review_status"] = "requires_manual_review"
        classification["scientific_findings_verified"] = False

        record_id = (
            f"NASA-ONLINE-PASSAGE-{nasa_id}-"
            f"{page_number:04d}-{sentence_index:03d}"
        )

        new_records.append({
                "record_id": record_id,
                "record_type": "nasa_passage",
                "source": {
                    "source_system": "NASA NTRS",
                    "source_id": nasa_id,
                    "title": metadata["title"],
                    "citation_url": citation_url,
                    "pdf_page_number": page_number,
                },
                "content": {
                    "text": sentence,
                    "source_field": "pdf_page_text",
                    "evidence_type": "extracted_source_text",
                },
                "conditions": None,
                "classification": classification,
                "source_metadata": {
                    "import_origin": "live_nasa_ntrs",
                    "retrieved_at_utc": retrieved_at,
                    "publication_date": next(
                        (
                            item.get("publicationDate")
                            for item in metadata.get("publications") or []
                            if item.get("publicationDate")
                        ),
                        None,
                    ),
                    "authors": authors,
                    "abstract_available": bool(metadata.get("abstract")),
                    "research_status": passage.get("research_status"),
                    "page_context_classification_status": passage.get(
                        "classification_status"
                    ),
                    "page_context_classification_basis": passage.get(
                        "classification_basis"
                    ),
                    "copyright_metadata": metadata.get("copyright"),
                    "dissemination_status": metadata.get("disseminated"),
                },
                "review": {
                    "source_review_status": "requires_manual_review",
                    "classification_review_status": "requires_manual_review",
                    "scientific_findings_verified": False,
                },
                "provenance": {
                    "import_origin": "live_nasa_ntrs",
                    "nasa_id": nasa_id,
                    "pdf_page_number": page_number,
                    "passage_index_on_page": sentence_index,
                    "research_status": passage.get("research_status"),
                    "pdf_path": extraction.get("pdf_path"),
                    "identity_audit_status": identity.get(
                        "identity_audit_status"
                    ),
                    "source_text_preserved": True,
                    "retrieved_at_utc": retrieved_at,
                },
            })

    if not new_records:
        return {
            "success": False,
            "status": "no_text_passages",
            "nasa_id": nasa_id,
            "title": metadata["title"],
            "citation_url": citation_url,
            "error": (
                "PDF was retrieved, but no usable text passages were extracted. "
                "No document was inserted into the collection."
            ),
            "empty_pages": empty_page_count,
        }

    existing_ids = {
        record.get("record_id")
        for record in collection["records"]
        if isinstance(record, dict)
    }

    new_ids = [record["record_id"] for record in new_records]

    if len(new_ids) != len(set(new_ids)):
        return {
            "success": False,
            "status": "generated_duplicate_ids",
            "nasa_id": nasa_id,
            "error": "Duplicate passage IDs were generated; nothing was saved.",
        }

    collisions = existing_ids.intersection(new_ids)

    if collisions:
        return {
            "success": False,
            "status": "record_id_collision",
            "nasa_id": nasa_id,
            "error": (
                f"Existing passage IDs collide with new records: "
                f"{sorted(collisions)[:5]}"
            ),
        }

    document_entry = {
        "nasa_id": nasa_id,
        "title": metadata["title"],
        "citation_url": citation_url,
        "import_origin": "live_nasa_ntrs",
        "retrieved_at_utc": retrieved_at,
        "publication_date": next(
            (
                item.get("publicationDate")
                for item in metadata.get("publications") or []
                if item.get("publicationDate")
            ),
            None,
        ),
        "authors": authors,
        "pdf_path": extraction.get("pdf_path"),
        "pdf_page_count": extraction.get("pdf_page_count"),
        "pages_with_extracted_text": extraction.get(
            "pages_with_extracted_text"
        ),
        "pages_without_extracted_text": extraction.get(
            "pages_without_extracted_text"
        ),
        "passage_count": len(new_records),
        "identity_audit_status": identity.get("identity_audit_status"),
        "identity_audit": identity,
        "source_review_status": "requires_manual_review",
        "scientific_findings_verified": False,
    }

    # Append only. Existing documents and passages remain unchanged.
    collection["records"].extend(new_records)
    collection["documents"].append(document_entry)

    try:
        output_path = _save_collection(collection, root)
    except OSError as exc:
        return {
            "success": False,
            "status": "collection_save_failed",
            "nasa_id": nasa_id,
            "error": str(exc),
        }

    return {
        "success": True,
        "status": "imported_pending_review",
        "nasa_id": nasa_id,
        "title": metadata["title"],
        "citation_url": citation_url,
        "passage_count": len(new_records),
        "document_page_count": extraction.get("pdf_page_count"),
        "empty_pages": empty_page_count,
        "identity_audit_status": identity.get("identity_audit_status"),
        "source_review_status": "requires_manual_review",
        "scientific_findings_verified": False,
        "collection_path": str(output_path),
    }
