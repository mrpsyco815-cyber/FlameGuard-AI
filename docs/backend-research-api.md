# FlameGuard AI backend research API

## Main mission research endpoint

~~~http
GET /research/mission-search?q=flame%20spread%20microgravity&mission=spacecraft&fuel=PMMA&limit=10
~~~

Query parameters:

| Parameter | Required | Description |
|---|---:|---|
| q | Yes | Research question or topic, 2–200 characters |
| mission | No | moon, mars, or spacecraft; defaults to spacecraft |
| fuel | No | Optional material/fuel filter |
| limit | No | Number of passages, 1–50; defaults to 10 |

The endpoint searches in this order:

1. Subhan's PDF-page-checked verified-core passages.
2. FlameGuard's primary NASA research intelligence store, including already imported supplemental NASA passages.
3. Query-relevant BASS-II raw structured records (returned separately).
4. NASA NTRS catalogue search if local passage count, source diversity, or query-term coverage is insufficient.

The response includes:
- local_evidence: local page-cited passages with exact excerpts.
- subhan_data: Subhan core matches and separately labelled preliminary-index matches.
- bass2_structured_experimental_data: only query-relevant BASS-II rows.
- online_search: NASA NTRS catalogue results when fallback runs.
- evidence_intelligence: transparent mission relevance scores, modality counts, top cited excerpts, and evidence gaps.
- condition_comparison: recorded condition fields and whether metadata textually matches, differs, or is incomplete.

## NASA full-text import

NASA online search results initially contain catalogue metadata and abstracts. When NASA reports a document is available, the result includes full_text_import_endpoint.

Use the existing endpoint to retrieve and index a selected NASA PDF:

~~~http
POST /research/import/20240002981
~~~

The import workflow:
1. Retrieves official NASA citation metadata and download links.
2. Downloads the PDF only through the validated NASA NTRS download endpoint.
3. Checks the PDF's visible first-page title against NASA catalogue metadata.
4. Extracts page-level text and candidate passages.
5. Adds passages to data/processed/supplemental_research_collection.json.
6. Marks imported passages requires_manual_review; no scientific verification is claimed.

Imported passages are included in subsequent local-first research searches. A failed or unavailable PDF remains a metadata-only discovery.

## Existing research endpoints

| Endpoint | Purpose |
|---|---|
| GET /research/search | Search local extractive evidence |
| GET /research/online-search | Search NASA NTRS catalogue metadata |
| GET /research/combined-search | Existing local-first NASA NTRS source federation |
| GET /research/evidence-search | Search manually reviewed NASA evidence |
| GET /research/nasa-passage-search | Search extracted NASA passages with filters |
| POST /research/import/{nasa_id} | Import and page-index an official NASA PDF |
| GET /bass2/summary | BASS-II dataset quality/structure summary |
| GET /bass2/search | Keyword search raw BASS-II rows |

## Ranking and interpretation limits

Mission relevance is a transparent retrieval score based on:
- query-term overlap (maximum 50 points),
- mission-context match (maximum 25 points),
- optional fuel/material match (maximum 15 points),
- citation and PDF-page provenance (maximum 10 points).

It is not a scientific quality, certainty, risk, or safety score. Curated Moon/Mars priority metadata is shown as source-provided context, not an independently validated ranking.

Experimental and simulation passages remain separate. The condition comparison checks recorded text fields only; matching text does not prove experimental equivalence. Raw BASS-II values are not silently normalized.

The API does not issue operational safe/unsafe predictions. Consult original source documents and subject-matter experts before making spacecraft fire-safety decisions.

## Local run

From the repository root with the virtual environment activated:

~~~powershell
python -m uvicorn backend.main:app --reload
~~~

Open the interactive API documentation at http://127.0.0.1:8000/docs.
