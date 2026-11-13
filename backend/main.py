from fastapi import FastAPI, Query, HTTPException

from backend.services.nasa_online import search_nasa_online
from backend.services.nasa_evidence_search import search_nasa_evidence
from backend.services.bass2_dataset import get_bass2_summary, search_bass2_records
from backend.services.nasa_passage_search import search_nasa_passages
from backend.services.research_federation import search_research_with_fallback
from backend.services.research_summarizer import (
    DEFAULT_STORE_PATH,
    build_evidence_brief,
)
from backend.services.nasa_ingestion import import_nasa_document
from backend.services.mission_research import search_mission_research
from backend.services.research_insights import (
    build_research_comparison,
    build_research_insights,
)
from backend.services.mission_intelligence_orchestrator import (
    build_mission_intelligence_orchestration,
)
from backend.services.review_store import (
    DEFAULT_REVIEW_DB,
    create_review,
    get_review,
    list_reviews,
    review_history,
    update_review,
)

app = FastAPI(
    title="FlameGuard AI API",
    description="Evidence-grounded research intelligence for microgravity combustion and spacecraft fire safety.",
    version="0.1.0",
)


def _review_db_path():
    """Return the server-selected review database; never use client input."""
    return getattr(app.state, "review_db_path", DEFAULT_REVIEW_DB)


def _reject_client_database_path(payload: dict) -> None:
    if "db_path" in payload:
        raise ValueError("db_path is server-controlled and cannot be supplied.")


@app.get("/")
def root():
    return {
        "message": "FlameGuard AI backend is running",
        "project": "FlameGuard AI",
        "version": "0.1.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "flameguard-backend",
    }


@app.get("/research/search")
def research_search(
    q: str = Query(..., min_length=2),
    limit: int = Query(default=5, ge=1, le=20),
):
    try:
        return build_evidence_brief(
            DEFAULT_STORE_PATH,
            q,
            limit=limit,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.get("/research/online-search")
def online_research_search(
    q: str = Query(..., min_length=2),
    limit: int = Query(default=5, ge=1, le=20),
):
    try:
        return search_nasa_online(q, limit)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/research/combined-search")
def combined_research_search(
    q: str = Query(..., min_length=2),
    limit: int = Query(default=5, ge=1, le=20),
):
    try:
        return search_research_with_fallback(q, limit)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@app.post("/research/insights")
def research_insights(payload: dict):
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="JSON object is required.")
    query = payload.get("query")
    limit = payload.get("limit", 10)
    try:
        return build_research_insights(query, limit=limit)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.post("/research/insights/compare")
def research_insights_compare(payload: dict):
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="JSON object is required.")
    query = payload.get("query")
    limit = payload.get("limit", 10)
    try:
        return build_research_comparison(query, limit=limit)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.post("/research/mission-intelligence")
def research_mission_intelligence(payload: dict):
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="JSON object is required.")
    try:
        _reject_client_database_path(payload)
        return build_mission_intelligence_orchestration(
            payload.get("query"),
            mission_context=payload.get("mission_context"),
            limit=payload.get("limit", 10),
            review_status=payload.get("review_status"),
            review_db_path=_review_db_path(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.post("/research/reviews")
def research_review_create(payload: dict):
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="JSON object is required.")
    try:
        _reject_client_database_path(payload)
        return create_review(**payload, db_path=_review_db_path())
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/research/reviews")
def research_review_list(
    target_type: str | None = None,
    target_id: str | None = None,
    status: str | None = None,
    limit: int = 50,
):
    try:
        reviews = list_reviews(
            target_type=target_type,
            target_id=target_id,
            status=status,
            limit=limit,
            db_path=_review_db_path(),
        )
        return {
            "count": len(reviews),
            "reviews": reviews,
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/research/reviews/{review_id}")
def research_review_get(review_id: str):
    try:
        result = get_review(review_id, db_path=_review_db_path())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if result is None:
        raise HTTPException(status_code=404, detail="Review not found.")
    return result


@app.get("/research/reviews/{review_id}/history")
def research_review_history(review_id: str):
    try:
        result = review_history(review_id, db_path=_review_db_path())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not result:
        raise HTTPException(status_code=404, detail="Review not found.")
    return {"review_id": review_id, "history": result}


@app.patch("/research/reviews/{review_id}")
def research_review_update(review_id: str, payload: dict):
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="JSON object is required.")
    try:
        _reject_client_database_path(payload)
        return update_review(
            review_id,
            **payload,
            db_path=_review_db_path(),
        )
    except ValueError as exc:
        status = 404 if str(exc) == "Review not found." else 400
        raise HTTPException(status_code=status, detail=str(exc)) from exc


@app.post("/research/import/{nasa_id}")
def import_nasa_research_document(nasa_id: str):
    """
    Import one discovered NASA NTRS paper into the supplemental collection.
    Imported passages remain pending manual review.
    """
    result = import_nasa_document(nasa_id)

    if not result.get("success"):
        status = result.get("status", "")
        http_status = 400 if status == "invalid_nasa_id" else 502
        raise HTTPException(
            status_code=http_status,
            detail=result,
        )

    return result


@app.get("/research/evidence-search")
def nasa_evidence_search(
    q: str = Query(..., min_length=2),
    limit: int = Query(default=5, ge=1, le=20),
):
    results = search_nasa_evidence(q, limit)

    return {
        "query": q,
        "count": len(results),
        "results": results,
        "notice": (
            "These findings were manually reviewed against extracted "
            "NASA document text. They have not been independently "
            "scientifically verified. Consult the original cited paper."
        ),
    }


@app.get("/bass2/summary")
def bass2_summary():
    return get_bass2_summary()


@app.get("/bass2/search")
def bass2_search(
    q: str = Query(default="", max_length=200),
    limit: int = Query(default=10, ge=1, le=100),
    pi: str | None = Query(default=None, min_length=1, max_length=100),
    fuel: str | None = Query(default=None, min_length=1, max_length=100),
    initial_oxygen: float | None = Query(default=None, ge=0, le=100),
    final_oxygen: float | None = Query(default=None, ge=0, le=100),
    numeric_field: str | None = Query(default=None, max_length=80),
    numeric_value: float | None = Query(default=None),
    numeric_tolerance: float = Query(default=0, ge=0),
):
    try:
        results = search_bass2_records(
            query=q,
            limit=limit,
            pi=pi,
            fuel=fuel,
            initial_oxygen=initial_oxygen,
            final_oxygen=final_oxygen,
            numeric_field=numeric_field,
            numeric_value=numeric_value,
            numeric_tolerance=numeric_tolerance,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "query": q,
        "filters": {
            "pi": pi,
            "fuel": fuel,
            "initial_oxygen": initial_oxygen,
            "final_oxygen": final_oxygen,
            "numeric_field": numeric_field,
            "numeric_value": numeric_value,
            "numeric_tolerance": numeric_tolerance,
        },
        "count": len(results),
        "results": results,
        "notice": (
            "Search uses keyword matching, not semantic AI. "
            "Original experimental values are preserved as strings. "
            "Results are not independently scientifically verified."
        ),
    }


@app.get("/research/nasa-passage-search")
def nasa_passage_search(
    q: str = Query(default="", max_length=1000),
    limit: int = Query(default=10, ge=1, le=100),
    nasa_id: str | None = Query(
        default=None, min_length=1, max_length=30
    ),
    classification: str | None = Query(
        default=None, min_length=1, max_length=50
    ),
):
    try:
        results = search_nasa_passages(
            query=q,
            limit=limit,
            nasa_id=nasa_id,
            classification=classification,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "query": q,
        "filters": {
            "nasa_id": nasa_id,
            "classification": classification,
        },
        "count": len(results),
        "results": results,
        "notice": (
            "Results are extracted NASA document passages, not "
            "independently scientifically verified findings. "
            "Classification labels are candidates and may require "
            "manual review. Keyword matching is not semantic AI."
        ),
    }

from backend.services.mission_intelligence import build_mission_intelligence


@app.get("/dashboard/mission-brief")
def mission_dashboard_brief(
    mission: str = Query(..., pattern="^(moon|mars|spacecraft)$"),
    q: str = Query(..., min_length=2, max_length=200),
    fuel: str = Query(default="", max_length=120),
    oxygen_concentration: str = Query(default="", max_length=120),
    flow_condition: str = Query(default="", max_length=120),
    gravity_condition: str = Query(default="", max_length=120),
    environment: str = Query(default="", max_length=120),
    limit: int = Query(default=10, ge=1, le=50),
):
    try:
        return build_mission_intelligence(
            mission=mission,
            query=q,
            fuel=fuel,
            oxygen_concentration=oxygen_concentration,
            flow_condition=flow_condition,
            gravity_condition=gravity_condition,
            environment=environment,
            limit=limit,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.get("/research/mission-search")
def mission_research_search(
    q: str = Query(..., min_length=2, max_length=200),
    limit: int = Query(default=10, ge=1, le=50),
    fuel: str | None = Query(default=None, min_length=1, max_length=100),
    mission: str = Query(default="spacecraft", pattern="^(moon|mars|spacecraft)$"),
):
    """Search Subhan data first, then local NASA research and NASA NTRS."""
    try:
        return search_mission_research(q, limit, fuel=fuel, mission=mission)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
