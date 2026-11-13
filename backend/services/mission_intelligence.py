import json
import re
from collections import Counter
from pathlib import Path
from typing import Any
from backend.services.ranking_contract import build_ranking_contract


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_STORE_PATH = (
    PROJECT_ROOT / "data" / "processed" / "research_intelligence_store.json"
)

EXPERIMENTAL_ROLES = {
    "experimental_quantitative_result",
    "experimental_observation",
    "experimental_comparative_result",
}

SIMULATION_ROLES = {
    "simulation_result",
    "simulation_limitation",
}

REVIEWED_CONTEXT_ROLES = {
    "experimental_test_scope",
}

SCENARIO_TERMS = {
    "moon": {"lunar", "moon", "lunar surface", "lunar habitat"},
    "mars": {"mars", "martian", "martian atmosphere"},
    "spacecraft": {"spacecraft", "spaceflight", "microgravity", "space station"},
}

STOP_WORDS = {
    "the", "and", "for", "with", "from", "that", "this",
    "was", "were", "are", "is", "into", "during", "than",
}


def _tokens(value: str) -> set[str]:
    return {
        word for word in re.findall(r"[a-z0-9]+", str(value).lower())
        if len(word) > 1 and word not in STOP_WORDS
    }


def _load_records(store_path: str | Path | None = None) -> list[dict[str, Any]]:
    path = Path(store_path) if store_path else DEFAULT_STORE_PATH

    if not path.exists():
        raise FileNotFoundError(f"Research intelligence store not found: {path}")

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Research store contains invalid JSON: {exc}") from exc

    if not isinstance(data, dict) or not isinstance(data.get("records"), list):
        raise ValueError("Invalid research store: expected a records list.")

    return [item for item in data["records"] if isinstance(item, dict)]


def _scenario_terms(mission: str, fuel: str, query: str) -> set[str]:
    terms = set(_tokens(query))
    terms.update(_tokens(fuel))
    terms.update(_tokens(mission))
    terms.update(_tokens(" ".join(SCENARIO_TERMS.get(mission, set()))))
    return terms


def _make_evidence_item(record: dict[str, Any], terms: set[str]) -> dict[str, Any] | None:
    source = record.get("source") or {}
    content = record.get("content") or {}
    classification = record.get("classification") or {}
    review = record.get("review") or {}
    text = content.get("text")

    if not isinstance(text, str) or not text.strip():
        return None

    matched = sorted(terms.intersection(_tokens(text)))
    if not matched:
        return None

    role = classification.get("evidence_role", "unclassified")
    modality = classification.get("evidence_modality", "unknown")

    # Transparent relevance score: proportion of scenario terms found in text.
    score = len(matched) / max(len(terms), 1)

    return {
        "record_id": record.get("record_id"),
        "source_id": source.get("source_id"),
        "source_title": source.get("title"),
        "citation_url": source.get("citation_url"),
        "pdf_page_number": source.get("pdf_page_number"),
        "evidence_role": role,
        "evidence_modality": modality,
        "research_context": classification.get("research_context", "unknown"),
        "review_status": (
            classification.get("review_status")
            or review.get("classification_review_status")
            or review.get("source_review_status")
            or "not_recorded"
        ),
        "scientific_findings_verified": (
            classification.get("scientific_findings_verified") is True
            and review.get("scientific_findings_verified") is True
        ),
        "matched_terms": matched,
        "mission_relevance_score": round(score, 4),
        "ranking_method": "scenario_term_overlap",
        "exact_source_excerpt": text,
    }


def _make_reviewed_context(record: dict[str, Any]) -> dict[str, Any]:
    source = record.get("source") or {}
    content = record.get("content") or {}
    conditions = record.get("conditions") or {}
    classification = record.get("classification") or {}
    review = record.get("review") or {}

    return {
        "record_id": record.get("record_id"),
        "source_id": source.get("source_id"),
        "source_title": source.get("title"),
        "citation_url": source.get("citation_url"),
        "pdf_page_number": source.get("pdf_page_number"),
        "evidence_role": classification.get("evidence_role"),
        "evidence_modality": classification.get("evidence_modality"),
        "review_status": review.get("source_review_status", "not_recorded"),
        "conditions": conditions,
        "exact_source_excerpt": content.get("text"),
        "scientific_findings_verified": (
            review.get("scientific_findings_verified") is True
        ),
        "notice": "Reviewed source context; not independently scientifically verified.",
    }


def _make_bass2_context(record: dict[str, Any]) -> dict[str, Any]:
    source = record.get("source") or {}
    content = record.get("content") or {}
    conditions = record.get("conditions") or {}
    quality = record.get("quality") or {}
    review = record.get("review") or {}

    return {
        "record_id": record.get("record_id"),
        "source_id": source.get("source_id"),
        "dataset": source.get("source_system"),
        "principal_investigator": source.get("principal_investigator"),
        "fuel_material_raw": content.get("fuel_material_raw"),
        "conditions_raw": conditions,
        "quality_flags": quality.get("flags", []),
        "source_review_status": review.get("source_review_status"),
        "scientific_findings_verified": (
            review.get("scientific_findings_verified") is True
        ),
        "notice": (
            "BASS-II environmental and experiment metadata. "
            "Do not interpret this record alone as a flame-spread result."
        ),
    }


def build_mission_intelligence(
    mission: str,
    query: str,
    fuel: str = "",
    limit: int = 10,
    store_path: str | Path | None = None,
    oxygen_concentration: str = "",
    flow_condition: str = "",
    gravity_condition: str = "",
    environment: str = "",
) -> dict[str, Any]:
    allowed_missions = {"moon", "mars", "spacecraft"}

    if mission not in allowed_missions:
        raise ValueError("mission must be moon, mars, or spacecraft.")

    if not isinstance(query, str) or len(query.strip()) < 2:
        raise ValueError("query must contain at least two characters.")

    if not isinstance(fuel, str) or len(fuel) > 120:
        raise ValueError("fuel must be a string of at most 120 characters.")
    for name, value in (
        ("oxygen_concentration", oxygen_concentration),
        ("flow_condition", flow_condition),
        ("gravity_condition", gravity_condition),
        ("environment", environment),
    ):
        if not isinstance(value, str) or len(value) > 120:
            raise ValueError(f"{name} must be a string of at most 120 characters.")

    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 50:
        raise ValueError("limit must be an integer between 1 and 50.")

    records = _load_records(store_path)
    terms = _scenario_terms(mission, fuel, query)
    supplied_conditions = {
        key: value for key, value in {
            "oxygen_concentration": oxygen_concentration,
            "flow_condition": flow_condition,
            "gravity_condition": gravity_condition,
            "environment": environment,
        }.items() if value.strip()
    }

    experiments = []
    simulations = []
    reviewed_context = []
    bass2_context = []

    for record in records:
        record_type = record.get("record_type")
        classification = record.get("classification") or {}
        role = classification.get("evidence_role")

        if record_type == "nasa_passage":
            item = _make_evidence_item(record, terms)
            if item is None:
                continue
            item["ranking_contract"] = build_ranking_contract(
                query=query,
                original_score=item["mission_relevance_score"],
                record={
                    **item,
                    "exact_source_excerpt": item["exact_source_excerpt"],
                    "evidence_type": item["evidence_modality"],
                    "source_type": "mission_intelligence",
                },
                source_text=item["exact_source_excerpt"],
            )
            if role in EXPERIMENTAL_ROLES:
                experiments.append(item)
            elif role in SIMULATION_ROLES:
                simulations.append(item)

        elif record_type == "reviewed_nasa_evidence":
            if role in REVIEWED_CONTEXT_ROLES:
                reviewed_context.append(_make_reviewed_context(record))

        elif record_type == "bass2_experimental_record":
            bass2_context.append(_make_bass2_context(record))

    sort_key = lambda item: (
        -item["mission_relevance_score"],
        str(item.get("source_id") or ""),
        item.get("pdf_page_number") or 0,
        str(item.get("record_id") or ""),
    )
    experiments.sort(key=sort_key)
    simulations.sort(key=sort_key)

    experiments = experiments[:limit]
    simulations = simulations[:limit]

    role_counts = Counter(
        (r.get("classification") or {}).get("evidence_role", "unclassified")
        for r in records if r.get("record_type") == "nasa_passage"
    )

    # These are evidence-linked observations, not operational safety instructions.
    insights = []
    if experiments:
        insights.append({
            "topic": "Experimental evidence",
            "observation": (
                f"{len(experiments)} matching experimental passage(s) "
                "were retrieved for this query and mission scenario."
            ),
            "source_record_ids": [item["record_id"] for item in experiments],
            "status": "evidence_retrieved",
        })
    else:
        insights.append({
            "topic": "Experimental evidence",
            "observation": "No matching experimental passages were retrieved.",
            "source_record_ids": [],
            "status": "insufficient_matching_evidence",
        })

    if simulations:
        insights.append({
            "topic": "Simulation evidence",
            "observation": (
                f"{len(simulations)} matching simulation passage(s) "
                "were retrieved. These are model results, not direct measurements."
            ),
            "source_record_ids": [item["record_id"] for item in simulations],
            "status": "simulation_evidence_retrieved",
        })

    recommendations = []
    for item in experiments:
        if not item["scientific_findings_verified"]:
            continue
        recommendations.append({
            "recommendation": (
                "Use this evidence as a mission-specific research input; "
                "do not treat it as a certified safety limit."
            ),
            "supporting_source_id": item["source_id"],
            "source_title": item["source_title"],
            "source_url": item["citation_url"],
            "passage": item["exact_source_excerpt"],
            "evidence_type": item["evidence_modality"],
            "experimental_conditions": supplied_conditions,
            "applicability_limitations": (
                "Applicability requires qualified engineering review of material, "
                "environment, and experimental-condition compatibility."
            ),
            "evidence_strength": "source record explicitly marked scientifically verified",
            "review_status": item["review_status"],
        })
    if not recommendations:
        recommendations = [{
            "recommendation": (
                "Insufficient verified evidence to support a mission-specific "
                "recommendation."
            ),
            "supporting_source_id": None,
            "source_title": None,
            "source_url": None,
            "passage": None,
            "evidence_type": None,
            "experimental_conditions": supplied_conditions,
            "applicability_limitations": (
                "Retrieved evidence is absent, incompatible, or not marked "
                "scientifically verified."
            ),
            "evidence_strength": "insufficient_verified_evidence",
            "review_status": "not_scientifically_reviewed",
        }]

    return {
        "project": "FlameGuard AI",
        "mission_scenario": {
            "mission": mission,
            "query": query,
            "fuel": fuel or None,
            "oxygen_concentration": oxygen_concentration or None,
            "flow_condition": flow_condition or None,
            "gravity_condition": gravity_condition or None,
            "environment": environment or None,
        },
        "retrieval": {
            "method": "scenario_term_overlap",
            "scenario_terms": sorted(terms),
            "ranking_note": (
                "Scores measure word overlap with the scenario query. "
                "They do not measure scientific quality, certainty, or safety."
            ),
        },
        "evidence": {
            "experimental": experiments,
            "simulation": simulations,
            "reviewed_context": reviewed_context[:limit],
            "bass2_context": bass2_context[:limit],
        },
        "comparison": {
            "experimental_passage_count": len(experiments),
            "simulation_passage_count": len(simulations),
            "comparison_note": (
                "Experimental passages and simulation passages are kept separate. "
                "This endpoint does not infer agreement or disagreement automatically."
            ),
            "supplied_conditions": supplied_conditions,
            "compatibility_status": (
                "requires_qualified_scientific_review"
                if experiments or simulations or reviewed_context or bass2_context
                else "no_matching_evidence"
            ),
        },
        "recommendations": recommendations,
        "safety_insights": insights,
        "coverage": {
            "total_store_records": len(records),
            "nasa_passage_role_inventory": dict(role_counts),
            "matched_experimental_passages": len(experiments),
            "matched_simulation_passages": len(simulations),
        },
        "limitations": [
            "This service uses deterministic keyword overlap, not an LLM.",
            "Mission relevance scores are not scientific-quality scores.",
            "NASA V3.4 evidence classifications are heuristic and may require manual review.",
            "Scientific findings are not independently verified by this service.",
            "Some NASA passage records have no structured experimental conditions.",
            "BASS-II metadata is contextual and is not automatically a flame-spread result.",
            "No operational fire-safety instruction or certified safety guarantee is produced.",
            "These outputs are research-support insights and must not be treated "
            "as certified safety decisions or substitutes for qualified engineering review.",
        ],
    }
