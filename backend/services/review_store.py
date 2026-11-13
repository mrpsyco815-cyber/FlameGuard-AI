"""SQLite-backed append-only human review records."""

import re
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REVIEW_STATUSES = (
    "pending",
    "accepted",
    "rejected",
    "needs_correction",
    "insufficient_evidence",
)
TARGET_TYPES = (
    "paper",
    "claim",
    "structured_finding",
    "comparison",
    "conflict",
    "research_gap",
    "mission_brief",
)
_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,199}$")
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REVIEW_DB = PROJECT_ROOT / "data" / "processed" / "research_reviews.sqlite3"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _validate_target(target_type: str, target_id: str) -> None:
    if target_type not in TARGET_TYPES:
        raise ValueError(f"target_type must be one of: {', '.join(TARGET_TYPES)}.")
    if not isinstance(target_id, str) or not _ID_PATTERN.fullmatch(target_id):
        raise ValueError("target_id must be a non-empty safe identifier.")


def validate_review_id(review_id: str) -> str:
    """Validate a review identifier without accepting filesystem-like input."""
    if not isinstance(review_id, str) or not _ID_PATTERN.fullmatch(review_id):
        raise ValueError("review_id must be a safe identifier.")
    return review_id


def _validate_status(status: str) -> None:
    if status not in REVIEW_STATUSES:
        raise ValueError(f"status must be one of: {', '.join(REVIEW_STATUSES)}.")


def _connect(db_path: str | Path | None) -> sqlite3.Connection:
    selected = Path(db_path) if db_path else DEFAULT_REVIEW_DB
    selected.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(selected)
    connection.row_factory = sqlite3.Row
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS research_reviews (
            review_id TEXT NOT NULL,
            revision INTEGER NOT NULL,
            target_type TEXT NOT NULL,
            target_id TEXT NOT NULL,
            source_document_id TEXT,
            nasa_id TEXT,
            source_url TEXT,
            reviewer_id TEXT,
            reviewer_identity_status TEXT NOT NULL,
            status TEXT NOT NULL,
            reviewer_decision TEXT,
            reviewer_notes TEXT,
            correction_notes TEXT,
            scientific_findings_verified INTEGER NOT NULL DEFAULT 0,
            evidence_scope TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            PRIMARY KEY (review_id, revision)
        )
        """
    )
    connection.commit()
    return connection


def _row(row: sqlite3.Row) -> dict[str, Any]:
    result = dict(row)
    result["scientific_findings_verified"] = bool(
        result["scientific_findings_verified"]
    )
    return result


def create_review(
    *,
    target_type: str,
    target_id: str,
    status: str = "pending",
    source_document_id: str | None = None,
    nasa_id: str | None = None,
    source_url: str | None = None,
    reviewer_id: str | None = None,
    reviewer_notes: str | None = None,
    correction_notes: str | None = None,
    evidence_scope: str | None = None,
    db_path: str | Path | None = None,
) -> dict[str, Any]:
    _validate_target(target_type, target_id)
    _validate_status(status)
    review_id = str(uuid.uuid4())
    timestamp = _now()
    identity_status = (
        "unverified_client_supplied" if reviewer_id else "not_authenticated"
    )
    connection = _connect(db_path)
    try:
        connection.execute(
            """
            INSERT INTO research_reviews (
                review_id, revision, target_type, target_id,
                source_document_id, nasa_id, source_url, reviewer_id,
                reviewer_identity_status, status, reviewer_decision,
                reviewer_notes, correction_notes,
                scientific_findings_verified, evidence_scope,
                created_at, updated_at
            ) VALUES (?, 1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?, ?)
            """,
            (
                review_id, target_type, target_id, source_document_id,
                nasa_id, source_url, reviewer_id, identity_status, status,
                status if status != "pending" else None, reviewer_notes,
                correction_notes, evidence_scope, timestamp, timestamp,
            ),
        )
        connection.commit()
        return get_review(review_id, db_path=db_path)
    finally:
        connection.close()


def get_review(
    review_id: str,
    *,
    db_path: str | Path | None = None,
) -> dict[str, Any] | None:
    validate_review_id(review_id)
    connection = _connect(db_path)
    try:
        row = connection.execute(
            """
            SELECT * FROM research_reviews
            WHERE review_id = ?
            ORDER BY revision DESC LIMIT 1
            """,
            (review_id,),
        ).fetchone()
        return _row(row) if row else None
    finally:
        connection.close()


def list_reviews(
    *,
    target_type: str | None = None,
    target_id: str | None = None,
    status: str | None = None,
    limit: int = 50,
    db_path: str | Path | None = None,
) -> list[dict[str, Any]]:
    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 100:
        raise ValueError("limit must be an integer between 1 and 100.")
    if target_type is not None and target_type not in TARGET_TYPES:
        raise ValueError("Unsupported target_type.")
    if status is not None:
        _validate_status(status)
    clauses = []
    parameters: list[Any] = []
    if target_type:
        clauses.append("target_type = ?")
        parameters.append(target_type)
    if target_id:
        _validate_target(target_type or "claim", target_id)
        clauses.append("target_id = ?")
        parameters.append(target_id)
    if status:
        clauses.append("status = ?")
        parameters.append(status)
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    connection = _connect(db_path)
    try:
        rows = connection.execute(
            f"""
            SELECT review_id, MAX(revision) AS revision
            FROM research_reviews
            {where}
            GROUP BY review_id
            ORDER BY review_id
            LIMIT ?
            """,
            (*parameters, limit),
        ).fetchall()
        return [
            _row(connection.execute(
                "SELECT * FROM research_reviews WHERE review_id = ? AND revision = ?",
                (row["review_id"], row["revision"]),
            ).fetchone())
            for row in rows
        ]
    finally:
        connection.close()


def update_review(
    review_id: str,
    *,
    status: str,
    reviewer_notes: str | None = None,
    correction_notes: str | None = None,
    reviewer_id: str | None = None,
    db_path: str | Path | None = None,
) -> dict[str, Any]:
    current = get_review(review_id, db_path=db_path)
    if current is None:
        raise ValueError("Review not found.")
    _validate_status(status)
    timestamp = _now()
    identity_status = (
        "unverified_client_supplied" if reviewer_id else
        current["reviewer_identity_status"]
    )
    connection = _connect(db_path)
    try:
        connection.execute(
            """
            INSERT INTO research_reviews (
                review_id, revision, target_type, target_id,
                source_document_id, nasa_id, source_url, reviewer_id,
                reviewer_identity_status, status, reviewer_decision,
                reviewer_notes, correction_notes,
                scientific_findings_verified, evidence_scope,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?, ?)
            """,
            (
                review_id, current["revision"] + 1, current["target_type"],
                current["target_id"], current["source_document_id"],
                current["nasa_id"], current["source_url"],
                reviewer_id or current["reviewer_id"], identity_status, status,
                status if status != "pending" else None,
                reviewer_notes if reviewer_notes is not None
                else current["reviewer_notes"],
                correction_notes if correction_notes is not None
                else current["correction_notes"],
                current["evidence_scope"], current["created_at"], timestamp,
            ),
        )
        connection.commit()
        return get_review(review_id, db_path=db_path)
    finally:
        connection.close()


def review_history(
    review_id: str,
    *,
    db_path: str | Path | None = None,
) -> list[dict[str, Any]]:
    if get_review(review_id, db_path=db_path) is None:
        return []
    connection = _connect(db_path)
    try:
        return [
            _row(row) for row in connection.execute(
                """
                SELECT * FROM research_reviews
                WHERE review_id = ? ORDER BY revision
                """,
                (review_id,),
            ).fetchall()
        ]
    finally:
        connection.close()
