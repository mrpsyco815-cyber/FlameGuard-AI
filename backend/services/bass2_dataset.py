import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


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
) -> list[dict[str, Any]]:
    """Search raw BASS-II records using transparent keyword matching."""

    if limit < 1 or limit > 100:
        raise ValueError("limit must be between 1 and 100.")

    data = load_bass2_dataset()
    query_terms = set(re.findall(r"[a-z0-9]+", query.lower()))

    if not query_terms and not pi and not fuel:
        return []

    results = []

    for record in data["records"]:
        record_pi = str(record.get("PI", ""))

        if pi and record_pi.casefold() != pi.casefold():
            continue

        material = str(record.get("Fuel Sample Material", ""))

        if fuel and fuel.casefold() not in material.casefold():
            continue

        searchable_text = " ".join(
            str(record.get(column, ""))
            for column in data["columns"]
        ).lower()

        searchable_terms = set(
            re.findall(r"[a-z0-9]+", searchable_text)
        )

        matched_terms = query_terms.intersection(searchable_terms)

        if query_terms and not matched_terms:
            continue

        score = (
            round(len(matched_terms) / len(query_terms), 3)
            if query_terms else 0.0
        )

        results.append({
            "record": record,
            "matched_terms": sorted(matched_terms),
            "relevance_score": score,
        })

    results.sort(
        key=lambda item: (
            item["relevance_score"],
            len(item["matched_terms"]),
        ),
        reverse=True,
    )

    return results[:limit]
