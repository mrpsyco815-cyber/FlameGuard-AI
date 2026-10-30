import re
from typing import Any


def _terms(value: Any) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", str(value or "").casefold()))


def _item_context(item: dict[str, Any]) -> str:
    parts = [
        item.get("source_title"),
        item.get("research_context"),
        item.get("context_requirement"),
        item.get("experiment_context"),
        item.get("platform_type"),
        item.get("moon_mars_rank_reason"),
    ]
    conditions = item.get("experiment_conditions") or {}
    if isinstance(conditions, dict):
        parts.extend(str(value) for value in conditions.values())
    comparison = item.get("comparison_keys") or {}
    if isinstance(comparison, dict):
        parts.extend(str(value) for value in comparison.values())
    return " ".join(str(part or "") for part in parts)


def score_mission_relevance(
    item: dict[str, Any],
    query: str,
    mission: str = "spacecraft",
    fuel: str | None = None,
) -> dict[str, Any]:
    """Transparent retrieval relevance rubric; not scientific quality or safety."""
    query_terms = _terms(query)
    matched = set(item.get("matched_query_terms") or [])
    if not matched:
        matched = query_terms.intersection(_terms(item.get("exact_source_excerpt")))
    lexical = len(matched) / max(len(query_terms), 1)

    context_text = _item_context(item)
    context_terms = _terms(context_text)
    mission_terms = {
        "moon": {"moon", "lunar", "lunar_surface", "lander", "habitat"},
        "mars": {"mars", "martian", "planetary", "transit", "habitat"},
        "spacecraft": {"spacecraft", "iss", "spaceflight", "orbital", "crew"},
    }[mission]
    mission_hits = sorted(mission_terms.intersection(context_terms))
    curated_rank = item.get("moon_mars_rank")
    mission_score = 0.0

    if mission in {"moon", "mars"} and isinstance(curated_rank, int):
        mission_score = {1: 25.0, 2: 18.0, 3: 10.0}.get(curated_rank, 0.0)
    elif mission_hits:
        mission_score = min(25.0, 10.0 + 5.0 * len(mission_hits))

    fuel_score = 0.0
    fuel_hits = []
    if fuel and fuel.strip():
        fuel_terms = _terms(fuel)
        fuel_hits = sorted(fuel_terms.intersection(context_terms))
        if fuel_hits:
            fuel_score = min(15.0, 7.5 + 7.5 * len(fuel_hits) / max(len(fuel_terms), 1))

    has_citation = bool(item.get("citation_url") or item.get("source_url"))
    has_page = item.get("pdf_page_number") is not None
    provenance_score = (5.0 if has_citation else 0.0) + (5.0 if has_page else 0.0)

    score = round(
        lexical * 50.0 + mission_score + fuel_score + provenance_score,
        2,
    )
    reasons = [
        f"Query-term coverage: {len(matched)}/{len(query_terms)}",
    ]
    if mission_score:
        reasons.append("Mission-context match: " + ", ".join(mission_hits or [f"curated priority {curated_rank}"]))
    else:
        reasons.append("No explicit mission-context match found")
    if fuel:
        reasons.append(
            "Fuel/material match: " + (", ".join(fuel_hits) if fuel_hits else "not found")
        )
    reasons.append(
        "Page-level citation available" if has_citation and has_page
        else "Page-level citation incomplete"
    )

    return {
        "mission_relevance_score": score,
        "score_label": "transparent retrieval relevance (0-100)",
        "score_components": {
            "query_match": round(lexical * 50.0, 2),
            "mission_context": round(mission_score, 2),
            "fuel_match": round(fuel_score, 2),
            "citation_provenance": round(provenance_score, 2),
        },
        "ranking_reasons": reasons,
        "matched_mission_terms": mission_hits,
        "matched_fuel_terms": fuel_hits,
        "is_scientific_quality_score": False,
        "is_safety_score": False,
    }


def build_evidence_intelligence(
    local_evidence: list[dict[str, Any]],
    online_metadata: list[dict[str, Any]],
    bass2_results: list[dict[str, Any]],
    query: str,
    mission: str = "spacecraft",
    fuel: str | None = None,
    limit: int = 10,
) -> dict[str, Any]:
    """Rank candidate passages and expose comparison coverage and evidence gaps."""
    ranked = []
    for item in local_evidence:
        ranked.append({
            **item,
            "mission_relevance": score_mission_relevance(
                item, query=query, mission=mission, fuel=fuel
            ),
        })

    ranked.sort(
        key=lambda item: (
            -item["mission_relevance"]["mission_relevance_score"],
            str(item.get("source_id") or ""),
            item.get("pdf_page_number") or 0,
        )
    )

    experiments = [
        item for item in ranked
        if item.get("evidence_modality") == "experiment"
    ]
    simulations = [
        item for item in ranked
        if item.get("evidence_modality") == "simulation"
    ]
    unknown = [
        item for item in ranked
        if item.get("evidence_modality") not in {"experiment", "simulation"}
    ]

    missing_conditions = [
        item for item in ranked
        if not item.get("experiment_context")
        and not item.get("research_context")
        and not item.get("context_requirement")
    ]
    missing_pages = [
        item for item in ranked
        if item.get("pdf_page_number") is None
    ]

    gaps = []
    if not ranked:
        gaps.append("No local full-text evidence passages matched the query.")
    if fuel and not any(item["mission_relevance"]["matched_fuel_terms"] for item in ranked):
        gaps.append(f"No retrieved passage explicitly matched fuel/material '{fuel}'.")
    if not experiments:
        gaps.append("No experimental passages were retrieved for this query.")
    if not simulations:
        gaps.append("No simulation passages were retrieved for this query.")
    if missing_conditions:
        gaps.append(f"{len(missing_conditions)} passage(s) lack explicit experiment/context details.")
    if online_metadata:
        gaps.append("NASA NTRS returned catalog metadata/abstracts; these are not full-text findings.")

    top_evidence = []
    for item in ranked[:min(limit, 5)]:
        top_evidence.append({
            "source_title": item.get("source_title"),
            "source_id": item.get("source_id"),
            "citation_url": item.get("citation_url") or item.get("source_url"),
            "pdf_page_number": item.get("pdf_page_number"),
            "evidence_modality": item.get("evidence_modality", "unknown"),
            "excerpt": item.get("exact_source_excerpt"),
            "mission_relevance": item["mission_relevance"],
        })

    return {
        "mission": mission,
        "query": query,
        "fuel_filter": fuel,
        "ranking_method": "transparent_weighted_retrieval_relevance",
        "ranking_disclaimer": (
            "Scores order retrieved material for this query and mission context only. "
            "They are not scientific quality, evidence certainty, operational risk, "
            "or safe/unsafe scores."
        ),
        "ranked_evidence": ranked[:limit],
        "top_evidence_summary": top_evidence,
        "comparison": {
            "experimental_passage_count": len(experiments),
            "simulation_passage_count": len(simulations),
            "unclassified_or_other_passage_count": len(unknown),
            "bass2_structured_record_count": len(bass2_results),
            "ntrs_metadata_only_record_count": len(online_metadata),
            "experimental_and_simulation_are_kept_separate": True,
            "automatic_conflict_detection_performed": False,
        },
        "evidence_gaps": gaps,
        "limitations": [
            "The ranking is a retrieval aid based on lexical overlap, mission-context terms, optional fuel terms, and page-level provenance.",
            "A missing result does not prove that a phenomenon does not occur.",
            "Passage-level context may be incomplete; consult the cited source paper.",
            "NASA NTRS abstracts are not treated as page-level full-text evidence.",
            "BASS-II raw rows are displayed separately and require unit/quality-flag review before numeric comparison.",
        ],
    }
