import json
from collections import Counter
from pathlib import Path
from typing import Any

from backend.services.query_understanding import parse_query, score_text
from backend.services.ranking_contract import build_ranking_contract


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "bass2"
    / "FlameGuard_BASSII_Experimental_Dataset.json"
)


def load_bass2_dataset() -> dict[str, Any]:
    """Load the raw BASS-II JSON without changing source values."""

    if not DATASET_FILE.exists():
        raise FileNotFoundError(
            f"BASS-II dataset not found: {DATASET_FILE}"
        )

    with DATASET_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("BASS-II JSON must contain an object.")

    columns = data.get("columns")
    records = data.get("records")

    if not isinstance(columns, list) or len(columns) != 17:
        raise ValueError("Expected exactly 17 dataset columns.")

    if not isinstance(records, list):
        raise ValueError("'records' must be a list.")

    if data.get("record_count") != len(records):
        raise ValueError(
            "Declared record_count does not match actual records."
        )

    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            raise ValueError(f"Record {index} is not a JSON object.")

        missing = [column for column in columns if column not in record]

        if missing:
            raise ValueError(
                f"Record {index} is missing columns: {missing}"
            )

    return data


def get_bass2_summary() -> dict[str, Any]:
    """Return structural summary and basic quality counts."""

    data = load_bass2_dataset()
    records = data["records"]
    columns = data["columns"]

    pi_counts = Counter(
        str(record.get("PI", ""))
        for record in records
    )

    identifiers = [
        (str(record.get("PI", "")), str(record.get("Test #", "")))
        for record in records
    ]

    duplicate_ids = [
        {"PI": pi, "Test #": test_id}
        for (pi, test_id), count in Counter(identifiers).items()
        if count > 1
    ]

    blank_cells = sum(
        1
        for record in records
        for column in columns
        if record.get(column) == ""
    )

    literal_none_cells = sum(
        1
        for record in records
        for column in columns
        if isinstance(record.get(column), str)
        and record[column].strip().lower() == "none"
    )

    return {
        "dataset_name": data.get("dataset_name"),
        "record_count": len(records),
        "declared_record_count": data.get("record_count"),
        "column_count": len(columns),
        "pi_counts": dict(pi_counts),
        "blank_cells": blank_cells,
        "literal_none_cells": literal_none_cells,
        "duplicate_identifiers": duplicate_ids,
        "quality_flags_count": len(data.get("quality_flags", [])),
        "source_values_modified": False,
        "scientific_findings_verified": False,
    }


def search_bass2_records(
    query: str,
    limit: int = 10,
    pi: str | None = None,
    fuel: str | None = None,
    initial_oxygen: float | None = None,
    final_oxygen: float | None = None,
    numeric_field: str | None = None,
    numeric_value: float | None = None,
    numeric_tolerance: float = 0.0,
) -> list[dict[str, Any]]:
    """Search raw BASS-II records using transparent keyword matching."""

    if limit < 1 or limit > 100:
        raise ValueError("limit must be between 1 and 100.")
    if numeric_tolerance < 0:
        raise ValueError("numeric_tolerance must be non-negative.")
    supported_numeric_fields = {
        "Calibrated  initial O2 % by vol ",
        "Calibrated final O2 % by vol",
        "Initial CO2 % by vol",
        "Final CO2 % by vol",
        "Initial CO (ppm)",
        "Final CO (ppm)",
        "Total Frames Shot",
        "Fan display",
        "Air display",
        "Flow restrictor",
    }
    if numeric_field and numeric_field not in supported_numeric_fields:
        raise ValueError(
            "numeric_field must be one of the supported BASS-II numeric columns."
        )
    if numeric_field and numeric_value is None:
        raise ValueError("numeric_value is required with numeric_field.")
    if numeric_value is not None and not numeric_field:
        raise ValueError("numeric_field is required with numeric_value.")

    data = load_bass2_dataset()
    scientific_query = None
    if query.strip():
        scientific_query = parse_query(query)
    if (
        scientific_query is None
        and not pi
        and not fuel
        and initial_oxygen is None
        and final_oxygen is None
        and numeric_field is None
        and numeric_value is None
    ):
        return []

    results = []

    for record in data["records"]:
        record_pi = str(record.get("PI", ""))

        if pi and record_pi.casefold() != pi.casefold():
            continue

        material = str(record.get("Fuel Sample Material", ""))

        if fuel and fuel.casefold() not in material.casefold():
            continue
        if not _matches_numeric(
            record.get("Calibrated  initial O2 % by vol "),
            initial_oxygen,
            numeric_tolerance,
        ):
            continue
        if not _matches_numeric(
            record.get("Calibrated final O2 % by vol"),
            final_oxygen,
            numeric_tolerance,
        ):
            continue
        if numeric_field and not _matches_numeric(
            record.get(numeric_field), numeric_value, numeric_tolerance
        ):
            continue

        searchable_text = " ".join(
            str(record.get(column, ""))
            for column in data["columns"]
        ).lower()

        relevance = (
            score_text(scientific_query, searchable_text)
            if scientific_query else
            {"score": 0.0, "matched_terms": [], "matching_reasons": []}
        )
        if scientific_query and not relevance["matched_terms"]:
            continue

        result = {
            "record": record,
            "source_type": "bass_ii",
            "matched_terms": relevance["matched_terms"],
            "relevance_score": relevance["score"],
            "relevance_components": relevance,
            "matching_reasons": relevance["matching_reasons"],
        }
        result["ranking_contract"] = build_ranking_contract(
            query=scientific_query or "",
            original_score=relevance["score"],
            record={
                "source_id": f"BASS2:{record.get('PI')}:{record.get('Test #')}",
                "source_type": "bass_ii",
                "exact_source_excerpt": searchable_text,
                "evidence_type": "bass2_experimental_metadata",
                "citation_url": record.get("Source URL"),
            },
            source_text=searchable_text,
            evidence_scope_name="experimental_metadata",
        )
        results.append(result)

    results.sort(
        key=lambda item: (
            item["relevance_score"],
            len(item["matched_terms"]),
        ),
        reverse=True,
    )

    return results[:limit]


def _matches_numeric(raw_value: Any, expected: float | None, tolerance: float) -> bool:
    if expected is None:
        return True
    try:
        actual = float(raw_value)
    except (TypeError, ValueError):
        return False
    return abs(actual - expected) <= tolerance
