"""Shared, non-calibrated metadata contract for scientific ranking results."""

import re
from collections import Counter
from typing import Any
from urllib.parse import urlsplit, urlunsplit

from backend.services.query_understanding import (
    MATERIALS,
    ScientificQuery,
    parse_query,
)


RANKING_CONTRACT_VERSION = "1.0"
CONDITION_FIELDS = (
    "material_fuel",
    "gravity",
    "oxygen_concentration",
    "pressure",
    "temperature",
    "flow_condition",
    "experimental_setup",
)

_VALUE_UNIT = r"(?P<value>\d+(?:\.\d+)?)\s*(?P<unit>%|percent|ppm|kPa|Pa|bar|atm|K|m/s|cm/s|mm/s)"


def _norm(value: Any) -> str:
    return " ".join(str(value or "").casefold().split())


def _source_text(record_text: str | None) -> str:
    return _norm(record_text)


def _query_condition_values(query: ScientificQuery) -> dict[str, list[str]]:
    normalized = query.normalized
    result: dict[str, list[str]] = {}
    if query.materials:
        result["material_fuel"] = list(query.materials)
    if any(term in normalized for term in ("microgravity", "reduced gravity", "low gravity", "normal gravity")):
        result["gravity"] = [
            term for term in (
                "microgravity", "reduced gravity", "low gravity", "normal gravity"
            ) if term in normalized
        ]
    if "oxygen" in normalized or "o2" in normalized:
        oxygen = re.findall(
            r"\d+(?:\.\d+)?\s*(?:%|percent|ppm)(?:[^.\n]{0,40})(?:oxygen|o2)"
            r"|(?:oxygen|o2)(?:[^.\n]{0,40})\d+(?:\.\d+)?\s*(?:%|percent|ppm)",
            normalized,
            flags=re.IGNORECASE,
        )
        result["oxygen_concentration"] = oxygen
        if not result["oxygen_concentration"] and any(
            term in normalized for term in ("concentration", "percentage", "percent")
        ):
            result["oxygen_concentration"] = ["reported"]
    for field, labels in {
        "pressure": ("pressure",),
        "temperature": ("temperature", "thermal"),
        "flow_condition": ("flow", "velocity", "airflow"),
    }.items():
        if any(label in normalized for label in labels):
            result[field] = [normalized]
    if "experimental setup" in normalized or "experimental procedure" in normalized:
        result["experimental_setup"] = ["reported"]
    return result


def _source_condition_values(text: str) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    lowered = _source_text(text)
    for field, patterns in {
        "material_fuel": (
            r"\bpmma\b", r"\bpolymethyl methacrylate\b", r"\bpolyethylene\b",
            r"\bpolypropylene\b", r"\bsilicone\b", r"\bsolid fuel\b",
        ),
        "gravity": (
            r"\bmicrogravity\b", r"\breduced gravity\b", r"\blow gravity\b",
            r"\bnormal gravity\b", r"\bterrestrial gravity\b",
        ),
    }.items():
        result[field] = [
            match.group(0)
            for pattern in patterns
            for match in re.finditer(pattern, lowered, re.IGNORECASE)
        ]
    for field, pattern in {
        "oxygen_concentration": (
            r"\d+(?:\.\d+)?\s*(?:%|percent|ppm)(?:[^.\n]{0,40})(?:oxygen|o2)"
            r"|(?:oxygen|o2)(?:[^.\n]{0,40})\d+(?:\.\d+)?\s*(?:%|percent|ppm)"
        ),
        "pressure": r"(?:pressure|pressurized)[^.\n]{0,30}?" + _VALUE_UNIT,
        "temperature": r"(?:temperature|thermal)[^.\n]{0,30}?" + _VALUE_UNIT,
        "flow_condition": r"(?:flow|velocity|airflow)[^.\n]{0,30}?" + _VALUE_UNIT,
    }.items():
        result[field] = [
            match.group(0)
            for match in re.finditer(pattern, lowered, re.IGNORECASE)
        ]
    if re.search(r"\b(?:experimental setup|experimental procedure|methods?)\b", lowered):
        result["experimental_setup"] = ["reported"]
    return result


def condition_match(
    query: ScientificQuery | str,
    source_text: str,
) -> dict[str, Any]:
    """Compare only explicitly requested conditions; unknown is not a match."""
    parsed = (
        parse_query(query)
        if isinstance(query, str) and query.strip()
        else query if isinstance(query, ScientificQuery) else None
    )
    requested = _query_condition_values(parsed) if parsed else {}
    reported = _source_condition_values(source_text)
    fields: dict[str, dict[str, Any]] = {}

    for field, requested_values in requested.items():
        reported_values = reported.get(field, [])
        if not reported_values:
            status = "unknown"
        elif field == "material_fuel":
            requested_canonical = {
                MATERIALS.get(value, value) for value in requested_values
            }
            reported_canonical = {
                MATERIALS.get(_norm(value), _norm(value))
                for value in reported_values
            }
            status = (
                "exact" if requested_canonical.intersection(reported_canonical)
                else "mismatch"
            )
        elif field in {"gravity", "experimental_setup"}:
            status = (
                "exact"
                if any(_norm(value) in _norm(item) for value in requested_values for item in reported_values)
                else "mismatch"
            )
        else:
            requested_numbers = re.findall(r"\d+(?:\.\d+)?\s*(?:%|percent|ppm|kpa|pa|bar|atm|k|m/s|cm/s|mm/s)", " ".join(requested_values))
            reported_numbers = re.findall(r"\d+(?:\.\d+)?\s*(?:%|percent|ppm|kpa|pa|bar|atm|k|m/s|cm/s|mm/s)", " ".join(reported_values))
            status = (
                "exact" if requested_numbers and set(requested_numbers).intersection(reported_numbers)
                else "mismatch" if requested_numbers and reported_numbers
                else "unknown"
            )
        fields[field] = {
            "status": status,
            "requested": requested_values,
            "reported": reported_values,
        }

    statuses = [item["status"] for item in fields.values()]
    if not statuses:
        overall = "unknown"
    elif "mismatch" in statuses:
        overall = "mismatch"
    elif "exact" in statuses and "unknown" in statuses:
        overall = "partial"
    elif all(status == "exact" for status in statuses):
        overall = "exact"
    else:
        overall = "unknown"

    missing = [
        field for field, item in fields.items() if item["status"] == "unknown"
    ]
    explanations = [
        f"{field}: {item['status']}"
        for field, item in fields.items()
    ]
    return {
        "overall": overall,
        "fields": fields,
        "missing_information": missing,
        "explanations": explanations,
    }


def evidence_scope(record: dict[str, Any]) -> str:
    explicit = _norm(record.get("evidence_type"))
    if explicit in {"bibliographic_metadata", "metadata"}:
        return "metadata"
    if "abstract" in explicit:
        return "abstract"
    if explicit in {
        "experimental_methods", "experimental_setup", "experimental_results",
        "experimental_metadata",
        "discussion_interpretation", "conclusion_statement",
        "limitation_statement", "independently_reviewed_evidence",
    }:
        return explicit
    if record.get("scientific_findings_verified") is True and record.get("review_status") in {
        "accepted", "reviewed", "independently_reviewed"
    }:
        return "independently_reviewed_evidence"
    if record.get("abstract") and not record.get("full_text_retrieved", False):
        return "abstract"
    content = record.get("content")
    if (
        (isinstance(content, dict) and content.get("text"))
        or record.get("exact_source_excerpt")
    ):
        return "reported_source_text"
    return "unknown"


def _source_type(record: dict[str, Any]) -> str:
    explicit = record.get("source_type") or record.get("source")
    if isinstance(explicit, dict):
        explicit = explicit.get("source_system")
    if explicit:
        return _norm(explicit).replace(" ", "_")
    if record.get("nasa_id") or record.get("citation_url"):
        return "nasa"
    if record.get("record", {}).get("Test #") is not None:
        return "bass_ii"
    if record.get("review_status") or record.get("finding"):
        return "reviewed_evidence"
    return "local_research"


def _provenance_value(record: dict[str, Any], name: str) -> Any:
    source = record.get("source") if isinstance(record.get("source"), dict) else {}
    classification = (
        record.get("classification")
        if isinstance(record.get("classification"), dict)
        else {}
    )
    review = record.get("review") if isinstance(record.get("review"), dict) else {}
    provenance = (
        record.get("provenance")
        if isinstance(record.get("provenance"), dict)
        else {}
    )
    aliases = {
        "source_document_id": (
            "source_document_id", "document_id", "source_id",
            ("source", "source_id"),
        ),
        "nasa_id": ("nasa_id", ("source", "source_id")),
        "source_url": (
            "source_url", "citation_url", "url",
            ("source", "citation_url"),
        ),
        "exact_supporting_excerpt": (
            "exact_supporting_excerpt", "exact_source_excerpt", "excerpt",
            "snippet", "finding", "abstract",
        ),
        "page_number_or_range": (
            "page_number_or_range", "pdf_page_number", "page_number",
            "page_span",
            ("source", "pdf_page_number"),
            ("source", "page_number"),
        ),
        "section_name": ("section_name", "section", "section_heading"),
        "evidence_type": (
            "evidence_type", "evidence_modality",
            ("classification", "evidence_role"),
            ("classification", "evidence_modality"),
        ),
        "retrieval_date": (
            "retrieval_date", "retrieval_timestamp", "retrieved_at",
            ("provenance", "retrieval_date"),
            ("provenance", "retrieved_at"),
        ),
        "review_status": (
            "review_status", "verification_status",
            ("review", "source_review_status"),
            ("classification", "review_status"),
        ),
    }
    for alias in aliases[name]:
        if isinstance(alias, tuple):
            containers = {
                "source": source,
                "classification": classification,
                "review": review,
                "provenance": provenance,
            }
            value = containers.get(alias[0], {}).get(alias[1])
        else:
            value = record.get(alias)
        if value not in (None, ""):
            return value
    return None


def provenance_completeness(
    record: dict[str, Any],
    source_type: str | None = None,
) -> dict[str, Any]:
    source_kind = source_type or _source_type(record)
    not_applicable = {"section_name"} if source_kind in {
        "nasa_ntrs", "nasa", "bass_ii", "bass2", "bass_ii_metadata",
    } and not record.get("section_name") and not record.get("section") else set()
    if source_kind in {"nasa_ntrs", "metadata", "abstract"}:
        not_applicable.add("page_number_or_range")
    if source_kind in {"bass_ii", "bass2", "bass_ii_metadata"}:
        not_applicable.update({"nasa_id", "page_number_or_range", "section_name"})

    fields = {}
    for name in (
        "source_document_id", "nasa_id", "source_url",
        "exact_supporting_excerpt", "page_number_or_range", "section_name",
        "evidence_type", "retrieval_date", "review_status",
    ):
        value = _provenance_value(record, name)
        status = "not_applicable" if name in not_applicable else (
            "present" if value not in (None, "") else "missing"
        )
        fields[name] = {"status": status, "value": value}

    present = [name for name, item in fields.items() if item["status"] == "present"]
    missing = [name for name, item in fields.items() if item["status"] == "missing"]
    unavailable = [
        name for name, item in fields.items() if item["status"] == "not_applicable"
    ]
    explanations = [
        f"{name}: {item['status']}" for name, item in fields.items()
    ]
    return {
        "source_type": source_kind,
        "fields": fields,
        "present_fields": present,
        "missing_fields": missing,
        "not_applicable_fields": unavailable,
        "complete": not missing,
        "complete_applicable_fields": not missing and bool(present),
        "explanations": explanations,
    }


def _normalized_url(value: Any) -> str | None:
    if not value:
        return None
    parsed = urlsplit(str(value).strip())
    if not parsed.scheme or not parsed.netloc:
        return None
    return urlunsplit((parsed.scheme.casefold(), parsed.netloc.casefold(),
                       parsed.path.rstrip("/"), parsed.query, ""))


def source_identity(record: dict[str, Any]) -> dict[str, Any]:
    """Return identity only from stable identifiers; never title similarity."""
    for field in ("nasa_id", "source_document_id", "source_id", "document_id"):
        value = record.get(field)
        if value not in (None, ""):
            return {
                "group_key": f"{field}:{str(value).casefold()}",
                "identity_field": field,
                "identity_value": value,
                "reason": f"shared stable {field}",
            }
    url = _normalized_url(record.get("source_url") or record.get("citation_url"))
    if url:
        return {
            "group_key": f"source_url:{url}",
            "identity_field": "source_url",
            "identity_value": url,
            "reason": "shared normalized source URL",
        }
    return {
        "group_key": None,
        "identity_field": None,
        "identity_value": None,
        "reason": "no stable source identifier available",
    }


def annotate_duplicate_sources(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Annotate records by stable source identity without merging them."""
    identities = [source_identity(record) for record in records]
    counts = Counter(
        identity["group_key"] for identity in identities
        if identity["group_key"] is not None
    )
    occurrences: Counter[str] = Counter()
    annotated = []
    for record, identity in zip(records, identities):
        group_key = identity["group_key"]
        occurrences[group_key] += 1
        group_size = counts.get(group_key, 1)
        item = dict(record)
        item["duplicate_source"] = {
            "group_key": group_key,
            "is_duplicate": group_key is not None and group_size > 1,
            "group_size": group_size,
            "occurrence": occurrences[group_key],
            "independent_evidence": None,
            "independence_status": "unknown",
            "explanation": identity["reason"],
        }
        annotated.append(item)
    return annotated


def build_ranking_contract(
    *,
    query: ScientificQuery | str,
    original_score: float | int,
    record: dict[str, Any],
    source_text: str,
    evidence_scope_name: str | None = None,
) -> dict[str, Any]:
    conditions = condition_match(query, source_text)
    source_type = _source_type(record)
    provenance = provenance_completeness(record, source_type)
    scope = evidence_scope_name or evidence_scope(record)
    identity = source_identity(record)
    explanations = list(conditions["explanations"])
    if provenance["complete"]:
        explanations.append("complete source provenance")
    else:
        explanations.append(
            "missing provenance: " + ", ".join(provenance["missing_fields"])
        )
    explanations.append(f"evidence scope: {scope}")
    return {
        "contract_version": RANKING_CONTRACT_VERSION,
        "original_score": original_score,
        "score_semantics": "source-specific original score; not calibrated across sources",
        "source_type": source_type,
        "source_identity": identity,
        "dimensions": {
            "lexical_relevance": {
                "score": original_score,
                "semantics": "preserved source-specific relevance score",
            },
            "condition_compatibility": conditions["overall"],
            "evidence_scope": scope,
            "provenance_completeness": provenance,
        },
        "condition_match": conditions,
        "evidence_scope": scope,
        "missing_information": conditions["missing_information"] + provenance["missing_fields"],
        "explanations": explanations,
        "provenance": provenance,
        "duplicate_source": {
            "group_key": identity["group_key"],
            "is_duplicate": False,
            "group_size": 1,
            "independent_evidence": None,
            "independence_status": "unknown",
            "explanation": identity["reason"],
        },
        "scientific_findings_verified": record.get(
            "scientific_findings_verified", False
        ) is True,
    }
