
import re
from pathlib import Path
from typing import Any
import json
import pymupdf

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_TEXT_DIR = PROJECT_ROOT / "data" / "raw" / "nasa_text"


TOPIC_PATTERNS = {
    "methods": r"\bmethod(?:s|ology)?\b|experimental setup|experimental procedure",
    "results": r"\bresults?\b|observations?|measurements?",
    "limitations": r"\blimitations?\b|uncertaint(?:y|ies)|sources of error",
    "fire_safety": r"spacecraft fire safety|fire safety|flammability",
    "combustion": r"\bcombustion\b|\bflames?\b|\bburning\b",
    "microgravity": r"\bmicrogravity\b|\bzero[- ]gravity\b",
    "smoldering": r"\bsmolder(?:ing)?\b|\bsmoulder(?:ing)?\b",
    "oxygen": r"\boxygen\b|\boxidizer\b",
}


def load_nasa_text(nasa_id: str) -> dict[str, Any]:
    """Load a previously downloaded NASA converted-text file."""
    if not nasa_id or not nasa_id.isdigit():
        return {
            "success": False,
            "error": "NASA ID must contain digits only.",
        }

    path = RAW_TEXT_DIR / f"{nasa_id}.txt"

    if not path.is_file():
        return {
            "success": False,
            "error": f"Downloaded text file not found: {path}",
        }

    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return {
            "success": False,
            "error": f"Could not read document text: {exc}",
        }

    if not text.strip():
        return {
            "success": False,
            "error": "The document text file is empty.",
        }

    return {
        "success": True,
        "nasa_id": nasa_id,
        "path": str(path),
        "text": text,
        "character_count": len(text),
    }


def split_into_slides(text: str) -> list[dict[str, Any]]:
    """
    Split converted presentation text using standalone numeric lines.

    This is a heuristic: numeric lines may occasionally be content rather
    than slide numbers. Original PDF pages should be checked when precision
    matters.
    """
    lines = text.splitlines()
    slides = []
    current_lines = []
    current_number = None

    def save_current():
        content = "\n".join(current_lines).strip()
        if content:
            slides.append({
                "slide_number": current_number,
                "text": content,
            })

    for line in lines:
        stripped = line.strip()

        # Treat a standalone number as a likely slide boundary only
        # when it is surrounded by blank lines.
        if (
            stripped.isdigit()
            and len(stripped) <= 3
            and (not current_lines or not current_lines[-1].strip())
        ):
            next_nonempty = next(
                (
                    item.strip()
                    for item in lines[lines.index(line) + 1:]
                    if item.strip()
                ),
                "",
            )

            if next_nonempty and len(next_nonempty) > 0:
                save_current()
                current_lines = []
                current_number = int(stripped)
                continue

        current_lines.append(line)

    save_current()

    # If no slide boundaries were recognized, return the document as one block.
    if not slides and text.strip():
        slides = [{"slide_number": None, "text": text.strip()}]

    return slides


def analyze_slide_text(slide_text: str) -> dict[str, Any]:
    """Identify candidate topics without claiming they are verified findings."""
    matches = []

    for topic, pattern in TOPIC_PATTERNS.items():
        if re.search(pattern, slide_text, flags=re.IGNORECASE):
            matches.append(topic)

    return {
        "candidate_topics": matches,
        "contains_candidate_methods_terms": "methods" in matches,
        "contains_candidate_results_terms": "results" in matches,
        "scientific_findings_verified": False,
    }


def parse_nasa_document(nasa_id: str) -> dict[str, Any]:
    """Load a NASA text file and return slide-level searchable records."""
    loaded = load_nasa_text(nasa_id)

    if not loaded["success"]:
        return loaded

    slides = split_into_slides(loaded["text"])

    parsed_slides = []

    for index, slide in enumerate(slides, start=1):
        parsed_slides.append({
            "record_id": f"{nasa_id}-BLOCK-{index:03d}",
            "nasa_id": nasa_id,
            "slide_number": slide["slide_number"],
            "text": slide["text"],
            "analysis": analyze_slide_text(slide["text"]),
            "source_url": f"https://ntrs.nasa.gov/citations/{nasa_id}",
        })

    return {
        "success": True,
        "nasa_id": nasa_id,
        "source_url": f"https://ntrs.nasa.gov/citations/{nasa_id}",
        "document_path": loaded["path"],
        "character_count": loaded["character_count"],
        "block_count": len(parsed_slides),
        "blocks": parsed_slides,
        "parser_note": (
            "Topic labels are keyword-based candidates, not verified "
            "scientific findings. Numeric slide boundaries are heuristic."
        ),
    }

def extract_pdf_pages(nasa_id: str) -> dict:
    """Extract text page-by-page from a downloaded NASA PDF."""

    if not nasa_id.isdigit():
        return {"success": False, "error": "Invalid NASA ID."}

    project_root = Path(__file__).resolve().parents[2]
    pdf_path = project_root / "data" / "raw" / "nasa_pdf" / f"{nasa_id}.pdf"
    output_dir = project_root / "data" / "processed" / "nasa_pdf_pages"
    output_path = output_dir / f"{nasa_id}.json"

    if not pdf_path.is_file():
        return {
            "success": False,
            "error": f"PDF not found: {pdf_path}",
        }

    pages = []

    try:
        with pymupdf.open(pdf_path) as document:
            if document.is_encrypted:
                return {
                    "success": False,
                    "error": "The PDF is encrypted and needs separate handling.",
                }

            if len(document) == 0:
                return {"success": False, "error": "PDF contains no pages."}

            for index, page in enumerate(document):
                page_text = page.get_text("text", sort=True).strip()

                pages.append({
                    "pdf_page_number": index + 1,
                    "text": page_text,
                    "character_count": len(page_text),
                    "word_count": len(page_text.split()),
                    "text_extraction_status": (
                        "text_extracted" if page_text else "no_text_extracted"
                    ),
                    "source_url": (
                        f"https://ntrs.nasa.gov/citations/{nasa_id}"
                    ),
                    "scientific_findings_verified": False,
                })

            result = {
                "success": True,
                "nasa_id": nasa_id,
                "title": document.metadata.get("title"),
                "pdf_page_count": len(document),
                "pages_with_extracted_text": sum(
                    1 for page in pages if page["text"]
                ),
                "pages_without_extracted_text": sum(
                    1 for page in pages if not page["text"]
                ),
                "total_extracted_characters": sum(
                    page["character_count"] for page in pages
                ),
                "pdf_path": str(pdf_path),
                "citation_url": (
                    f"https://ntrs.nasa.gov/citations/{nasa_id}"
                ),
                "scientific_findings_verified": False,
                "pages": pages,
            }

        output_dir.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(result, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        result["saved_json_path"] = str(output_path)
        return result

    except (OSError, ValueError, RuntimeError) as exc:
        return {
            "success": False,
            "error": f"PDF text extraction failed: {exc}",
        }

def audit_pdf_identity(nasa_id: str) -> dict:
    """Compare NASA API metadata with the downloaded PDF's visible first page."""

    import re
    import requests
    import pymupdf

    if not nasa_id.isdigit():
        return {"success": False, "error": "Invalid NASA ID."}

    project_root = Path(__file__).resolve().parents[2]
    pdf_path = (
        project_root / "data" / "raw" / "nasa_pdf" / f"{nasa_id}.pdf"
    )

    if not pdf_path.is_file():
        return {"success": False, "error": f"PDF not found: {pdf_path}"}

    api_url = f"https://ntrs.nasa.gov/api/citations/{nasa_id}"

    try:
        response = requests.get(api_url, timeout=20)
        response.raise_for_status()
        nasa_record = response.json()

        with pymupdf.open(pdf_path) as document:
            if len(document) == 0:
                return {"success": False, "error": "PDF contains no pages."}

            pdf_metadata = document.metadata or {}
            first_page_text = document[0].get_text("text", sort=True).strip()

        api_title = (nasa_record.get("title") or "").strip()
        embedded_title = (pdf_metadata.get("title") or "").strip()

        def normalize(value: str) -> str:
            return re.sub(r"\s+", " ", value).strip().casefold()

        normalized_page = normalize(first_page_text)
        normalized_api_title = normalize(api_title)

        visible_title_matches = bool(
            normalized_api_title
            and normalized_api_title in normalized_page
        )

        embedded_title_matches = bool(
            embedded_title
            and normalize(embedded_title) == normalized_api_title
        )

        if visible_title_matches and not embedded_title_matches:
            status = "embedded_metadata_mismatch"
        elif visible_title_matches and embedded_title_matches:
            status = "identity_consistent"
        else:
            status = "manual_review_required"

        return {
            "success": True,
            "nasa_id": nasa_id,
            "api_title": api_title,
            "api_id": str(nasa_record.get("id", "")),
            "pdf_embedded_title": embedded_title,
            "pdf_embedded_author": pdf_metadata.get("author"),
            "first_page_text_excerpt": first_page_text[:600],
            "visible_title_matches_api": visible_title_matches,
            "embedded_title_matches_api": embedded_title_matches,
            "identity_audit_status": status,
            "citation_url": f"https://ntrs.nasa.gov/citations/{nasa_id}",
            "scientific_findings_verified": False,
        }

    except (requests.RequestException, ValueError, OSError, RuntimeError) as exc:
        return {
            "success": False,
            "error": f"Document identity audit failed: {exc}",
        }
