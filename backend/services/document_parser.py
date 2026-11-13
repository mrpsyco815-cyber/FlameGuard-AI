
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

SECTION_ALIASES = {
    "abstract": ("abstract",),
    "introduction": ("introduction",),
    "background_related_work": (
        "background",
        "related work",
        "related literature",
        "literature review",
    ),
    "methodology_methods": (
        "methodology",
        "methods",
        "materials and methods",
        "experimental methods",
    ),
    "experimental_setup": (
        "experimental setup",
        "experiment setup",
        "experimental apparatus",
        "experimental procedure",
    ),
    "results": ("results", "experimental results"),
    "discussion": ("discussion",),
    "conclusion": ("conclusion", "conclusions"),
    "limitations": (
        "limitations",
        "limitations and uncertainties",
        "uncertainty and limitations",
    ),
    "references": (
        "references",
        "bibliography",
        "references cited",
    ),
}

_SECTION_ALIAS_LOOKUP = {
    alias: section_name
    for section_name, aliases in SECTION_ALIASES.items()
    for alias in aliases
}


def _normalize_heading(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().casefold())


def _heading_candidate(line: str) -> dict[str, Any] | None:
    """Return a conservative section-heading candidate for one text line."""
    stripped = re.sub(r"\s+", " ", line.strip())
    if not stripped or len(stripped) > 100:
        return None

    match = re.match(
        r"^(?P<number>\d+(?:\.\d+)*(?:[.)])?)?\s*(?P<label>.+?)\s*[:\-]?$",
        stripped,
    )
    if not match:
        return None

    label = match.group("label").strip(" :-")
    normalized = _normalize_heading(label)
    if normalized in _SECTION_ALIAS_LOOKUP:
        section_name = _SECTION_ALIAS_LOOKUP[normalized]
    elif normalized in {"results and discussion", "discussion and results"}:
        section_name = "results_and_discussion"
    else:
        return None

    number = match.group("number")
    level = number.rstrip(".)").count(".") + 1 if number else 1
    uncertain = section_name == "results_and_discussion"
    return {
        "heading": stripped,
        "section_name": section_name,
        "section_level": level,
        "detection_method": "exact_heading_alias",
        "uncertain": uncertain,
        "uncertainty_reason": (
            "Combined Results/Discussion heading cannot be assigned to "
            "one canonical section."
            if uncertain
            else None
        ),
    }


def _find_section_heading(line: str) -> dict[str, Any] | None:
    """Avoid treating ordinary sentence lines as section headings."""
    candidate = _heading_candidate(line)
    if not candidate:
        return None

    stripped = line.strip()
    if len(stripped.split()) > 8:
        return None
    if stripped.endswith((".", "!", "?")):
        return None
    return candidate


def extract_sections_from_pages(
    pages: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Detect conservative research-paper sections from extracted page text.

    This function only structures headings and their source text. It does not
    extract or verify scientific findings.
    """
    section_starts = []
    unclassified = []

    for page_index, page in enumerate(pages):
        page_number = page.get("pdf_page_number")
        page_text = page.get("text") or ""
        if not isinstance(page_text, str) or not page_text.strip():
            continue

        lines = page_text.splitlines()
        for line_index, line in enumerate(lines):
            candidate = _find_section_heading(line)
            if candidate:
                section_starts.append({
                    **candidate,
                    "page_index": page_index,
                    "pdf_page_number": page_number,
                    "line_index": line_index,
                })

    sections = []
    for index, start in enumerate(section_starts):
        next_start = (
            section_starts[index + 1]
            if index + 1 < len(section_starts)
            else None
        )
        start_page_index = start["page_index"]
        end_page_index = (
            next_start["page_index"]
            if next_start
            else len(pages) - 1
        )
        section_lines = []
        section_page_numbers = []

        for page_index in range(start_page_index, end_page_index + 1):
            page = pages[page_index]
            page_number = page.get("pdf_page_number")
            page_text = page.get("text") or ""
            if not isinstance(page_text, str) or not page_text.strip():
                if not next_start or page_index < next_start["page_index"]:
                    if page_number is not None:
                        section_page_numbers.append(page_number)
                continue

            lines = page_text.splitlines()
            first_line = start["line_index"] if page_index == start_page_index else 0
            last_line = (
                next_start["line_index"]
                if next_start and page_index == next_start["page_index"]
                else len(lines)
            )
            content_start = first_line + 1 if page_index == start_page_index else first_line
            section_lines.extend(lines[content_start:last_line])
            has_section_text = any(
                line.strip() for line in lines[content_start:last_line]
            )
            if (
                page_number is not None
                and (
                    not next_start
                    or page_index < next_start["page_index"]
                    or has_section_text
                )
            ):
                section_page_numbers.append(page_number)

        section_text = "\n".join(section_lines).strip()
        sections.append({
            "section_name": start["section_name"],
            "heading": start["heading"],
            "section_level": start["section_level"],
            "text": section_text,
            "page_start": start["pdf_page_number"],
            "page_end": (
                section_page_numbers[-1] if section_page_numbers
                else start["pdf_page_number"]
            ),
            "page_numbers": section_page_numbers,
            "detection_method": start["detection_method"],
            "detection_uncertain": start["uncertain"],
            "uncertainty_reason": start["uncertainty_reason"],
            "scientific_findings_verified": False,
        })

    for page_index, page in enumerate(pages):
        text = page.get("text") or ""
        if not isinstance(text, str) or not text.strip():
            continue

        lines = text.splitlines()
        classified_line_indexes = set()
        for section_index, start in enumerate(section_starts):
            if not start["page_index"] <= page_index:
                continue
            next_start = (
                section_starts[section_index + 1]
                if section_index + 1 < len(section_starts)
                else None
            )
            if next_start and page_index > next_start["page_index"]:
                continue
            if next_start and page_index == next_start["page_index"]:
                last_line = next_start["line_index"]
            else:
                last_line = len(lines)
            first_line = (
                start["line_index"] + 1
                if page_index == start["page_index"]
                else 0
            )
            if first_line < last_line:
                classified_line_indexes.update(range(first_line, last_line))
            if page_index == start["page_index"]:
                classified_line_indexes.add(start["line_index"])

        remaining_lines = [
            line for index, line in enumerate(lines)
            if index not in classified_line_indexes and line.strip()
        ]
        if remaining_lines:
            unclassified.append({
                "text": "\n".join(remaining_lines).strip(),
                "page_start": page.get("pdf_page_number"),
                "page_end": page.get("pdf_page_number"),
                "reason": (
                    "Text is outside a recognized section boundary or uses "
                    "an unrecognized heading."
                ),
            })

    return {
        "sections": sections,
        "section_count": len(sections),
        "unclassified_text": unclassified,
        "section_extraction_status": (
            "sections_detected" if sections else "no_sections_detected"
        ),
        "section_detection_note": (
            "Headings are detected conservatively from exact aliases. "
            "Unrecognized headings and text remain unclassified; section "
            "labels are structural metadata, not scientific findings."
        ),
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

def extract_pdf_pages(
    nasa_id: str,
    pdf_path: str | Path | None = None,
    output_dir: str | Path | None = None,
) -> dict:
    """Extract text page-by-page from a downloaded NASA PDF."""

    if not str(nasa_id).isdigit():
        return {
            "success": False,
            "extraction_status": "invalid_pdf",
            "error": "Invalid NASA ID.",
        }

    project_root = Path(__file__).resolve().parents[2]
    selected_pdf_path = (
        Path(pdf_path)
        if pdf_path is not None
        else project_root / "data" / "raw" / "nasa_pdf" / f"{nasa_id}.pdf"
    )
    selected_output_dir = (
        Path(output_dir)
        if output_dir is not None
        else project_root / "data" / "processed" / "nasa_pdf_pages"
    )
    output_path = selected_output_dir / f"{nasa_id}.json"

    if not selected_pdf_path.is_file():
        return {
            "success": False,
            "extraction_status": "invalid_pdf",
            "error": f"PDF not found: {selected_pdf_path}",
        }

    pages = []

    try:
        with pymupdf.open(selected_pdf_path) as document:
            if document.is_encrypted:
                return {
                    "success": False,
                    "extraction_status": "invalid_pdf",
                    "error": "The PDF is encrypted and needs separate handling.",
                }

            if len(document) == 0:
                return {
                    "success": False,
                    "extraction_status": "invalid_pdf",
                    "error": "PDF contains no pages.",
                }

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

            pages_with_text = sum(1 for page in pages if page["text"])
            pages_without_text = len(pages) - pages_with_text
            if pages_with_text == 0:
                extraction_status = "no_extractable_text"
                extraction_message = (
                    "OCR required or text extraction unavailable."
                )
            elif pages_without_text:
                extraction_status = "partial_extraction"
                extraction_message = (
                    "One or more PDF pages contained no extractable text."
                )
            else:
                extraction_status = "success"
                extraction_message = None

            result = {
                "success": True,
                "extraction_status": extraction_status,
                "extraction_message": extraction_message,
                "nasa_id": nasa_id,
                "title": document.metadata.get("title"),
                "pdf_page_count": len(document),
                "pages_with_extracted_text": pages_with_text,
                "pages_without_extracted_text": pages_without_text,
                "total_extracted_characters": sum(
                    page["character_count"] for page in pages
                ),
                "pdf_path": str(selected_pdf_path),
                "citation_url": (
                    f"https://ntrs.nasa.gov/citations/{nasa_id}"
                ),
                "scientific_findings_verified": False,
                "pages": pages,
            }
            result.update(extract_sections_from_pages(pages))
            from backend.services.evidence_extractor import (
                extract_structured_findings,
            )
            result["structured_findings"] = extract_structured_findings(
                result,
                document_id=f"NASA-{nasa_id}",
                nasa_id=nasa_id,
                source_url=result["citation_url"],
            )
            from backend.services.claim_summarizer import build_paper_summary
            result["claim_summary"] = build_paper_summary(
                result,
                document_id=f"NASA-{nasa_id}",
                nasa_id=nasa_id,
                source_url=result["citation_url"],
            )

        selected_output_dir.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(result, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        result["saved_json_path"] = str(output_path)
        return result

    except (OSError, ValueError, RuntimeError, pymupdf.FileDataError) as exc:
        return {
            "success": False,
            "extraction_status": "invalid_pdf",
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
