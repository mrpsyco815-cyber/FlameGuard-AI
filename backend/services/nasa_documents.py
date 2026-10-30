
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

import requests


NASA_API_BASE = "https://ntrs.nasa.gov/api"
NASA_SITE_BASE = "https://ntrs.nasa.gov"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_TEXT_DIR = PROJECT_ROOT / "data" / "raw" / "nasa_text"

MAX_DOWNLOAD_BYTES = 20 * 1024 * 1024  # 20 MB
TIMEOUT_SECONDS = 30


def _is_valid_nasa_download_url(url: str, nasa_id: str) -> bool:
    """Allow download URLs only from the expected NASA citation endpoint."""
    expected_prefix = (
        f"{NASA_SITE_BASE}/api/citations/{nasa_id}/downloads/"
    )

    return url.startswith(expected_prefix)


def get_nasa_downloads(nasa_id: str) -> dict[str, Any]:
    """
    Retrieve the available download formats listed by NASA NTRS.

    This checks metadata about available files. It does not download
    or verify the contents of the actual document.
    """
    if not nasa_id or not nasa_id.isdigit():
        return {
            "success": False,
            "nasa_id": nasa_id,
            "downloads": [],
            "error": "NASA ID must contain digits only.",
        }

    endpoint = f"{NASA_API_BASE}/citations/{nasa_id}/downloads"

    try:
        response = requests.get(
            endpoint,
            timeout=TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        payload = response.json()

        if not isinstance(payload, list):
            raise ValueError("Unexpected NASA downloads response format.")

        downloads = []

        for item in payload:
            if not isinstance(item, dict):
                continue

            links = item.get("links") or {}

            text_path = links.get("fulltext")
            pdf_path = links.get("pdf")

            text_url = (
                urljoin(NASA_SITE_BASE, text_path)
                if isinstance(text_path, str)
                and text_path.startswith(
                    f"/api/citations/{nasa_id}/downloads/"
                )
                else None
            )

            pdf_url = (
                urljoin(NASA_SITE_BASE, pdf_path)
                if isinstance(pdf_path, str)
                and pdf_path.startswith(
                    f"/api/citations/{nasa_id}/downloads/"
                )
                else None
            )

            downloads.append({
                "name": item.get("name"),
                "mimetype": item.get("mimetype"),
                "draft": item.get("draft"),
                "text_url": text_url,
                "pdf_url": pdf_url,
            })

        return {
            "success": True,
            "nasa_id": nasa_id,
            "downloads": downloads,
            "error": None,
        }

    except (requests.RequestException, ValueError) as exc:
        return {
            "success": False,
            "nasa_id": nasa_id,
            "downloads": [],
            "error": str(exc),
        }


def download_nasa_fulltext(
    nasa_id: str,
    max_bytes: int = MAX_DOWNLOAD_BYTES,
) -> dict[str, Any]:
    """
    Download NASA's converted text file and save it locally.

    A successful download means text was retrieved and saved.
    It does not mean scientific claims have been verified.
    """
    if not nasa_id or not nasa_id.isdigit():
        return {
            "success": False,
            "nasa_id": nasa_id,
            "error": "NASA ID must contain digits only.",
        }

    if max_bytes <= 0:
        return {
            "success": False,
            "nasa_id": nasa_id,
            "error": "max_bytes must be greater than zero.",
        }

    # Discover the actual converted-text link rather than assuming
    # every NASA record has a .txt file.
    availability = get_nasa_downloads(nasa_id)

    if not availability["success"]:
        return {
            "success": False,
            "nasa_id": nasa_id,
            "error": availability["error"],
        }

    text_url = next(
        (
            item["text_url"]
            for item in availability["downloads"]
            if item.get("text_url")
        ),
        None,
    )

    if not text_url or not _is_valid_nasa_download_url(
        text_url, nasa_id
    ):
        return {
            "success": False,
            "nasa_id": nasa_id,
            "error": (
                "No valid converted-text download is listed for this "
                "NASA record."
            ),
            "pdf_available": any(
                item.get("pdf_url")
                for item in availability["downloads"]
            ),
        }

    try:
        with requests.get(
            text_url,
            timeout=TIMEOUT_SECONDS,
            stream=True,
        ) as response:
            response.raise_for_status()

            content_type = response.headers.get(
                "Content-Type", ""
            ).lower()

            if not (
                "text/" in content_type
                or "application/octet-stream" in content_type
            ):
                return {
                    "success": False,
                    "nasa_id": nasa_id,
                    "error": (
                        "Unexpected response content type: "
                        f"{content_type or 'unknown'}"
                    ),
                }

            declared_size = response.headers.get("Content-Length")

            if declared_size:
                try:
                    if int(declared_size) > max_bytes:
                        return {
                            "success": False,
                            "nasa_id": nasa_id,
                            "error": (
                                "NASA text file exceeds the configured "
                                "download size limit."
                            ),
                        }
                except ValueError:
                    pass

            chunks = []
            total_bytes = 0

            for chunk in response.iter_content(
                chunk_size=64 * 1024
            ):
                if not chunk:
                    continue

                total_bytes += len(chunk)

                if total_bytes > max_bytes:
                    return {
                        "success": False,
                        "nasa_id": nasa_id,
                        "error": (
                            "Download stopped because the text file "
                            "exceeded the configured size limit."
                        ),
                    }

                chunks.append(chunk)

        raw_text = b"".join(chunks)

        if not raw_text:
            return {
                "success": False,
                "nasa_id": nasa_id,
                "error": "NASA returned an empty text file.",
            }

        text = raw_text.decode(
            "utf-8",
            errors="replace",
        ).strip()

        if not text:
            return {
                "success": False,
                "nasa_id": nasa_id,
                "error": "The downloaded file contains no readable text.",
            }

        # Avoid saving an HTML error page as if it were a research paper.
        if text[:500].lstrip().lower().startswith(
            ("<!doctype html", "<html")
        ):
            return {
                "success": False,
                "nasa_id": nasa_id,
                "error": (
                    "NASA returned HTML instead of converted research text."
                ),
            }

        RAW_TEXT_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path = RAW_TEXT_DIR / f"{nasa_id}.txt"
        output_path.write_text(
            text,
            encoding="utf-8",
        )

        return {
            "success": True,
            "nasa_id": nasa_id,
            "saved_path": str(output_path),
            "downloaded_bytes": total_bytes,
            "character_count": len(text),
            "full_text_retrieved": True,
            "scientific_findings_verified": False,
            "error": None,
        }

    except (
        requests.RequestException,
        OSError,
        ValueError,
    ) as exc:
        return {
            "success": False,
            "nasa_id": nasa_id,
            "error": str(exc),
        }

def download_nasa_pdf(
    nasa_id: str,
    max_bytes: int = MAX_DOWNLOAD_BYTES,
) -> dict[str, Any]:
    """Download an official NASA NTRS PDF with basic safety checks."""

    if not nasa_id.isdigit():
        return {"success": False, "error": "Invalid NASA ID."}

    if max_bytes <= 0:
        return {"success": False, "error": "max_bytes must be positive."}

    downloads = get_nasa_downloads(nasa_id)

    if not downloads.get("success"):
        return {
            "success": False,
            "error": downloads.get("error", "Could not retrieve NASA downloads."),
        }

    pdf_url = next(
        (
            item.get("pdf_url")
            for item in downloads.get("downloads", [])
            if item.get("pdf_url")
        ),
        None,
    )

    if not pdf_url or not _is_valid_nasa_download_url(pdf_url, nasa_id):
        return {
            "success": False,
            "error": "No valid official NASA PDF download URL found.",
        }

    pdf_dir = PROJECT_ROOT / "data" / "raw" / "nasa_pdf"
    pdf_dir.mkdir(parents=True, exist_ok=True)

    output_path = pdf_dir / f"{nasa_id}.pdf"
    temp_path = pdf_dir / f"{nasa_id}.pdf.part"
    downloaded_bytes = 0

    try:
        with requests.get(
            pdf_url,
            stream=True,
            timeout=TIMEOUT_SECONDS,
            allow_redirects=False,
        ) as response:
            response.raise_for_status()

            content_type = response.headers.get("Content-Type", "").lower()
            content_length = response.headers.get("Content-Length")

            if content_type and "pdf" not in content_type and "octet-stream" not in content_type:
                return {
                    "success": False,
                    "error": f"Unexpected content type: {content_type}",
                }

            if content_length:
                try:
                    if int(content_length) > max_bytes:
                        return {
                            "success": False,
                            "error": "PDF exceeds the download size limit.",
                        }
                except ValueError:
                    pass

            with temp_path.open("wb") as file:
                for chunk in response.iter_content(chunk_size=64 * 1024):
                    if not chunk:
                        continue

                    downloaded_bytes += len(chunk)

                    if downloaded_bytes > max_bytes:
                        return {
                            "success": False,
                            "error": "PDF exceeded the download size limit.",
                        }

                    file.write(chunk)

        with temp_path.open("rb") as file:
            signature = file.read(5)

        if signature != b"%PDF-":
            return {
                "success": False,
                "error": "Downloaded file does not have a valid PDF signature.",
            }

        temp_path.replace(output_path)

        return {
            "success": True,
            "nasa_id": nasa_id,
            "saved_path": str(output_path),
            "downloaded_bytes": downloaded_bytes,
            "pdf_url": pdf_url,
            "citation_url": f"{NASA_SITE_BASE}/citations/{nasa_id}",
            "pdf_retrieved": True,
            "scientific_findings_verified": False,
        }

    except (requests.RequestException, OSError) as exc:
        return {
            "success": False,
            "error": f"PDF download failed: {exc}",
        }

    finally:
        if temp_path.exists():
            temp_path.unlink()
