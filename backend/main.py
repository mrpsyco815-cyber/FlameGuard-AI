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

app = FastAPI(
    title="FlameGuard AI API",
    description="Evidence-grounded research intelligence for microgravity combustion and spacecraft fire safety.",
    version="0.1.0",
)


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
    return search_nasa_online(q, limit)


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
):
    results = search_bass2_records(
        query=q,
        limit=limit,
        pi=pi,
        fuel=fuel,
    )

    return {
        "query": q,
        "filters": {
            "pi": pi,
            "fuel": fuel,
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
    q: str = Query(default="", max_length=200),
    limit: int = Query(default=10, ge=1, le=100),
    nasa_id: str | None = Query(
        default=None, min_length=1, max_length=30
    ),
    classification: str | None = Query(
        default=None, min_length=1, max_length=50
    ),
):
    results = search_nasa_passages(
        query=q,
        limit=limit,
        nasa_id=nasa_id,
        classification=classification,
    )

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
