import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "1.0"

SOURCE_PATHS = {
    "nasa_combined": "data/processed/nasa_combined_evidence.json",
    "nasa_reviewed": "data/processed/nasa_reviewed_evidence.json",
    "bass2": "data/raw/bass2/FlameGuard_BASSII_Experimental_Dataset.json",
    "v34_audit": "data/processed/nasa_v34_classification_audit.json",
}

OUTPUT_PATH = "data/processed/research_intelligence_store.json"


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Required source file not found: {path}")

    with path.open("r", encoding="utf-8-sig") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError(f"Expected a JSON object in: {path}")

    return data


def load_research_sources(
    project_root: Path | None = None,
) -> dict[str, Any]:
    """Load all original datasets without modifying them."""

    root = project_root or Path(__file__).resolve().parents[2]

    return {
        name: _load_json(root / relative_path)
        for name, relative_path in SOURCE_PATHS.items()
    }


def _audit_lookup(
    audit: dict[str, Any],
) -> tuple[dict[tuple[str, int], dict[str, Any]], list[str]]:

    lookup = {}
    errors = []

    for item in audit.get("records", []):
        nasa_id = item.get("nasa_id")
        record_index = item.get("record_index")

        if not isinstance(nasa_id, str):
            errors.append("Audit record has an invalid NASA ID.")
            continue

        if not isinstance(record_index, int):
            errors.append(
                f"Invalid audit record index for NASA ID {nasa_id}."
            )
            continue

        key = (nasa_id, record_index)

        if key in lookup:
            errors.append(f"Duplicate V3.4 audit key: {key}")
            continue

        lookup[key] = item

    return lookup, errors


def validate_research_sources(
    sources: dict[str, Any],
) -> dict[str, Any]:
    """Validate counts, IDs, classifications and source relationships."""

    errors: list[str] = []
    warnings: list[str] = []

    nasa = sources["nasa_combined"]
    reviewed = sources["nasa_reviewed"]
    bass2 = sources["bass2"]
    audit = sources["v34_audit"]

    documents = nasa.get("documents", [])
    reviewed_records = reviewed.get("evidence", [])
    bass_records = bass2.get("records", [])
    quality_flags = bass2.get("quality_flags", [])
    audit_records = audit.get("records", [])

    actual_passages = sum(
        len(doc.get("passages", []))
        for doc in documents
    )

    if actual_passages != nasa.get("total_passages"):
        errors.append(
            "NASA combined passage count does not match its declared total."
        )

    if len(documents) != nasa.get("document_count"):
        errors.append(
            "NASA document count does not match its declared total."
        )

    if actual_passages != len(audit_records):
        errors.append(
            "NASA passage count and V3.4 audit record count do not match."
        )

    audit_lookup, audit_errors = _audit_lookup(audit)
    errors.extend(audit_errors)

    matched_audit = 0

    for doc in documents:
        nasa_id = doc.get("nasa_id")
        title = doc.get("title")

        if not nasa_id or not title:
            errors.append("A NASA document is missing its ID or title.")
            continue

        for index, passage in enumerate(doc.get("passages", [])):
            key = (nasa_id, index)
            audit_item = audit_lookup.get(key)

            if audit_item is None:
                errors.append(f"Missing V3.4 audit annotation: {key}")
                continue

            if audit_item.get("text") != passage.get("text"):
                errors.append(f"Audit text mismatch: {key}")
                continue

            classification = audit_item.get("classification") or {}

            if not classification:
                errors.append(f"Missing classification data: {key}")
                continue

            if classification.get("scientific_findings_verified") is not False:
                errors.append(
                    f"Unexpected verification status in audit: {key}"
                )

            if classification.get("classification_version") != "3.4":
                errors.append(
                    f"Unexpected classifier version in audit: {key}"
                )

            matched_audit += 1

    reviewed_ids = [
        item.get("evidence_id")
        for item in reviewed_records
    ]

    if len(reviewed_ids) != len(set(reviewed_ids)):
        errors.append("Duplicate manually reviewed evidence IDs detected.")

    if any(not evidence_id for evidence_id in reviewed_ids):
        errors.append("A reviewed evidence record is missing its evidence ID.")

    if bass2.get("record_count") != len(bass_records):
        errors.append("BASS-II declared record count does not match.")

    if bass2.get("column_count") != len(bass2.get("columns", [])):
        errors.append("BASS-II declared column count does not match.")

    bass_keys = []
    bass_key_set = set()

    for record in bass_records:
        pi = record.get("PI")
        test_number = record.get("Test #")

        if not pi or not test_number:
            errors.append("A BASS-II record is missing PI or Test #.")
            continue

        key = (str(pi), str(test_number))

        if key in bass_key_set:
            errors.append(f"Duplicate BASS-II experiment key: {key}")
        else:
            bass_key_set.add(key)
            bass_keys.append(key)

    flags_by_key: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    unmatched_flags = 0

    for flag in quality_flags:
        pi = flag.get("PI")
        test_number = flag.get("Test #")

        if not pi or not test_number:
            unmatched_flags += 1
            continue

        key = (str(pi), str(test_number))

        if key not in bass_key_set:
            unmatched_flags += 1
            continue

        flags_by_key[key].append(flag)

    if unmatched_flags:
        warnings.append(
            f"{unmatched_flags} BASS-II quality flags could not be linked."
        )

    if len(audit_records) != matched_audit:
        warnings.append("Some V3.4 audit records were not linked.")

    counts = {
        "nasa_documents": len(documents),
        "nasa_passages": actual_passages,
        "reviewed_evidence": len(reviewed_records),
        "bass2_experiments": len(bass_records),
        "bass2_quality_flags": len(quality_flags),
        "matched_v34_annotations": matched_audit,
        "matched_bass2_quality_flags": (
            len(quality_flags) - unmatched_flags
        ),
        "unmatched_bass2_quality_flags": unmatched_flags,
        "unique_bass2_experiments": len(bass_key_set),
        "total_expected_unified_records": (
            actual_passages
            + len(reviewed_records)
            + len(bass_records)
        ),
    }

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "counts": counts,
    }


def normalize_nasa_passages(
    sources: dict[str, Any],
    audit_lookup: dict[tuple[str, int], dict[str, Any]],
) -> list[dict[str, Any]]:
    """Normalize NASA passages and attach their matching V3.4 annotations."""

    records = []
    nasa = sources["nasa_combined"]

    for doc in nasa.get("documents", []):
        nasa_id = doc["nasa_id"]

        for index, passage in enumerate(doc.get("passages", [])):
            annotation = audit_lookup[(nasa_id, index)]
            classification = dict(annotation["classification"])

            citation_url = (
                passage.get("citation_url")
                or passage.get("source_url")
                or doc.get("citation_url")
            )

            records.append({
                "record_id": f"NASA-PASSAGE-{nasa_id}-{index:04d}",
                "record_type": "nasa_passage",
                "source": {
                    "source_system": "NASA NTRS",
                    "source_id": nasa_id,
                    "title": doc.get("title"),
                    "citation_url": citation_url,
                    "pdf_page_number": passage.get("pdf_page_number"),
                },
                "content": {
                    "text": passage.get("text"),
                    "source_field": passage.get("source_field"),
                    "evidence_type": passage.get("evidence_type"),
                },
                "conditions": None,
                "classification": classification,
                "source_metadata": {
                    "matched_terms": passage.get("matched_terms", []),
                    "research_status": passage.get("research_status"),
                    "experimental_result_status": passage.get(
                        "experimental_result_status"
                    ),
                    "original_classification": passage.get("classification"),
                    "original_classification_basis": passage.get(
                        "classification_basis"
                    ),
                },
                "review": {
                    "source_review_status": passage.get("review_status"),
                    "classification_review_status": classification.get(
                        "review_status"
                    ),
                    "scientific_findings_verified": False,
                },
                "provenance": {
                    "record_index": index,
                    "audit_version": classification.get(
                        "classification_version"
                    ),
                    "source_text_preserved": True,
                },
            })

    return records


def normalize_reviewed_evidence(
    sources: dict[str, Any],
) -> list[dict[str, Any]]:
    """Preserve manually reviewed evidence and its original conditions."""

    records = []

    for item in sources["nasa_reviewed"].get("evidence", []):
        records.append({
            "record_id": f"REVIEWED-{item['evidence_id']}",
            "record_type": "reviewed_nasa_evidence",
            "source": {
                "source_system": "NASA NTRS",
                "source_id": item.get("nasa_id"),
                "title": item.get("title"),
                "citation_url": item.get("citation_url"),
                "pdf_page_number": item.get("pdf_page_number"),
            },
            "content": {
                "text": item.get("finding"),
                "evidence_class": item.get("evidence_class"),
            },
            "conditions": {
                "raw_values": dict(item.get("conditions") or {}),
                "values_normalized": False,
            },
            "classification": {
                "evidence_role": item.get("evidence_class"),
                "evidence_modality": "unknown",
                "classification_basis": "Manually reviewed paper-reported evidence.",
            },
            "source_metadata": {},
            "review": {
                "source_review_status": item.get("review_status"),
                "scientific_findings_verified": False,
            },
            "provenance": {
                "evidence_id": item.get("evidence_id"),
                "source_record_preserved": True,
            },
        })

    return records


def normalize_bass2_records(
    sources: dict[str, Any],
) -> list[dict[str, Any]]:
    """Preserve BASS-II raw strings and attach matching quality flags."""

    dataset = sources["bass2"]

    flags_by_key: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)

    for flag in dataset.get("quality_flags", []):
        key = (
            str(flag.get("PI") or ""),
            str(flag.get("Test #") or ""),
        )
        flags_by_key[key].append(dict(flag))

    records = []

    for raw_record in dataset.get("records", []):
        pi = str(raw_record.get("PI") or "")
        test_number = str(raw_record.get("Test #") or "")
        key = (pi, test_number)

        records.append({
            "record_id": f"BASS2-{pi}-{test_number}",
            "record_type": "bass2_experimental_record",
            "source": {
                "source_system": "NASA PSI-25 BASS-II",
                "source_id": test_number,
                "title": dataset.get("dataset_name"),
                "dataset_source": dataset.get("source"),
                "principal_investigator": pi,
            },
            "content": {
                "experiment_date_raw": raw_record.get("Date"),
                "fuel_material_raw": raw_record.get("Fuel Sample Material"),
                "raw_record": dict(raw_record),
            },
            "conditions": {
                "oxygen_initial_percent_raw": raw_record.get(
                    "Calibrated  initial O2 % by vol "
                ),
                "oxygen_final_percent_raw": raw_record.get(
                    "Calibrated final O2 % by vol"
                ),
                "flow_restrictor_raw": raw_record.get("Flow restrictor"),
                "fan_display_raw": raw_record.get("Fan display"),
                "air_display_raw": raw_record.get("Air display"),
                "raw_values_preserved": True,
                "numeric_normalization_performed": False,
            },
            "classification": {
                "evidence_role": "experimental_dataset_record",
                "evidence_modality": "experiment",
                "classification_basis": (
                    "Structured record from the NASA PSI-25 BASS-II dataset."
                ),
            },
            "source_metadata": {
                "original_columns": list(dataset.get("columns", [])),
                "dataset_column_count": dataset.get("column_count"),
            },
            "quality": {
                "flags": flags_by_key.get(key, []),
                "flag_count": len(flags_by_key.get(key, [])),
            },
            "review": {
                "source_review_status": (
                    "source_transcription_structurally_checked"
                ),
                "scientific_findings_verified": False,
            },
            "provenance": {
                "principal_investigator": pi,
                "test_number": test_number,
                "source_record_preserved": True,
            },
        })

    return records


def build_research_intelligence_store(
    sources: dict[str, Any],
) -> dict[str, Any]:
    """Build a unified store after validating all source relationships."""

    validation = validate_research_sources(sources)

    if not validation["valid"]:
        raise ValueError(
            "Research source validation failed: "
            + " | ".join(validation["errors"])
        )

    audit_lookup, _ = _audit_lookup(sources["v34_audit"])

    nasa_records = normalize_nasa_passages(sources, audit_lookup)
    reviewed_records = normalize_reviewed_evidence(sources)
    bass2_records = normalize_bass2_records(sources)

    records = nasa_records + reviewed_records + bass2_records

    record_ids = [record["record_id"] for record in records]

    if len(record_ids) != len(set(record_ids)):
        raise ValueError("Duplicate unified record IDs detected.")

    expected = validation["counts"]["total_expected_unified_records"]

    if len(records) != expected:
        raise ValueError(
            f"Unified record count mismatch: expected {expected}, "
            f"received {len(records)}."
        )

    type_counts = Counter(record["record_type"] for record in records)

    return {
        "project": "FlameGuard AI",
        "store_name": "Research Intelligence Store",
        "schema_version": SCHEMA_VERSION,
        "source_inventory": {
            "nasa_documents": validation["counts"]["nasa_documents"],
            "nasa_passages": len(nasa_records),
            "manually_reviewed_evidence": len(reviewed_records),
            "bass2_experimental_records": len(bass2_records),
            "v34_is_annotation_source_not_a_separate_record_set": True,
        },
        "record_count": len(records),
        "record_type_counts": dict(type_counts),
        "scientific_findings_verified": False,
        "validation": validation,
        "records": records,
    }


def save_research_intelligence_store(
    store: dict[str, Any],
    project_root: Path | None = None,
) -> Path:
    """Save the new store without overwriting any source dataset."""

    root = project_root or Path(__file__).resolve().parents[2]
    output_path = root / OUTPUT_PATH

    output_path.parent.mkdir(parents=True, exist_ok=True)

    temporary_path = output_path.with_suffix(".json.tmp")

    with temporary_path.open("w", encoding="utf-8") as f:
        json.dump(store, f, ensure_ascii=False, indent=2)

    temporary_path.replace(output_path)

    return output_path


def build_and_save_research_intelligence_store(
    project_root: Path | None = None,
) -> dict[str, Any]:
    root = project_root or Path(__file__).resolve().parents[2]

    sources = load_research_sources(root)
    store = build_research_intelligence_store(sources)
    output_path = save_research_intelligence_store(store, root)

    return {
        "output_path": str(output_path),
        "record_count": store["record_count"],
        "record_type_counts": store["record_type_counts"],
        "validation": store["validation"],
        "scientific_findings_verified": False,
    }
