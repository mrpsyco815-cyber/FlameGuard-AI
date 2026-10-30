# FlameGuard AI

Evidence-grounded research intelligence for NASA microgravity combustion and spacecraft fire-safety research.

## Project objective

FlameGuard AI is being developed for the NASA Space Apps challenge. Its intended dashboard will help users discover, summarize, compare, rank, and interpret NASA fire/combustion research and turn appropriately qualified evidence into fire-safety insights for human space exploration.

## Current repository contents

This repository currently contains the **Python/FastAPI backend and research data**. A production dashboard frontend and the final AI synthesis / mission insight workflow are not yet implemented.

The backend currently provides:

- A local Research Intelligence Store containing NASA passages, reviewed evidence, and BASS-II experimental records.
- Local-first NASA passage retrieval with source IDs, citations, PDF page numbers, evidence roles, modality, and review status.
- Live NASA NTRS catalogue search when local evidence coverage is insufficient.
- NASA PDF download, identity checking, page-level text extraction, and supplemental ingestion.
- A separate BASS-II dataset summary and search service.
- Unit tests for store integrity, extraction search, NASA fallback, and supplemental document ingestion.

## Research data flow

1. Search the primary local Research Intelligence Store.
2. Search the supplemental collection of papers imported from NASA NTRS.
3. If local passage/source coverage is insufficient, query NASA NTRS for additional catalogue records.
4. Deduplicate discovered sources by NASA ID.
5. A selected NASA paper can be imported through the ingestion endpoint. Its PDF identity is checked, page text is extracted, and candidate passages are stored in the supplemental collection.
6. New imported passages remain pending manual review and are not marked as scientifically verified.

The primary dataset and its V3.4 audit are preserved as original inputs. The supplemental collection is additive and does not rewrite those source files.

## Important evidence safeguards

- V3.4 classifications are heuristic labels, not scientific validation.
- Query-match scores represent lexical overlap, not scientific quality, confidence, or mission relevance.
- Experimental results, simulations, interpretations, methods, and limitations must remain distinguishable.
- NASA NTRS abstracts are catalogue metadata; they are not substitutes for full-text, page-cited findings.
- Extracted PDF text can contain layout or OCR errors. Review the cited page before using a passage as a scientific conclusion.
- BASS-II source values are retained in their original form; do not silently normalize questionable or missing values.

## Setup

Python 3.10 or later is recommended.

### Windows PowerShell

```powershell
cd C:\Users\User\FlameGuard-AI

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Start the API

```powershell
python -m uvicorn backend.main:app --reload
```

API root: http://127.0.0.1:8000  
Interactive API documentation: http://127.0.0.1:8000/docs

## API endpoints

| Endpoint | Purpose |
|---|---|
| `GET /` | API identity and status |
| `GET /health` | Health check |
| `GET /research/search?q=...` | Search primary and supplemental local NASA passages |
| `GET /research/online-search?q=...` | Search NASA NTRS catalogue metadata |
| `GET /research/combined-search?q=...` | Local-first search with NASA NTRS fallback |
| `POST /research/import/{nasa_id}` | Import one NASA NTRS PDF into the supplemental collection |
| `GET /research/evidence-search?q=...` | Search manually reviewed NASA evidence records |
| `GET /research/nasa-passage-search?q=...` | Search extracted passages from the original combined NASA dataset |
| `GET /bass2/summary` | BASS-II dataset overview |
| `GET /bass2/search?q=...` | Search BASS-II experiment records |

Example:

```text
GET http://127.0.0.1:8000/research/combined-search?q=flame%20spread%20flow%20velocity&limit=5
```

Import a NASA paper:

```text
POST http://127.0.0.1:8000/research/import/20080034883
```

Imported papers are stored in `data/processed/supplemental_research_collection.json` after successful PDF identity checking and page extraction. Re-importing a paper already present in the primary or supplemental collection does not create another copy.

## Run tests

```powershell
python -m unittest discover -s backend/tests -v
```

GitHub Actions runs the same unit-test suite on pushes and pull requests.

## Main backend modules

- `backend/main.py` — FastAPI routes.
- `backend/services/research_intelligence_data.py` — primary unified-store builder and source validation.
- `backend/services/research_summarizer.py` — local extractive evidence retrieval across primary and supplemental collections.
- `backend/services/research_federation.py` — local-first retrieval and NASA NTRS fallback.
- `backend/services/nasa_online.py` — NASA NTRS catalogue search.
- `backend/services/nasa_documents.py` — NASA PDF/TXT download utilities.
- `backend/services/document_parser.py` — PDF page extraction and identity audit.
- `backend/services/evidence_extractor.py` — source passage extraction and page-context labels.
- `backend/services/nasa_ingestion.py` — duplicate-safe supplemental NASA paper ingestion.
- `backend/services/evidence_classifier_v3.py` through `evidence_classifier_v3_4.py` — chained heuristic evidence classification.
- `backend/services/bass2_dataset.py` — BASS-II dataset access.

## Remaining challenge-critical work

1. AI-assisted, citation-constrained research summarization.
2. Transparent evidence-strength and mission-relevance ranking.
3. Structured comparison of experiments and simulations, including conditions and limitations.
4. Evidence-backed fire-safety insights for selected Moon, Mars, and spacecraft scenarios.
5. Integrate future teammate-provided research data through validated, additive ingestion.
6. Build the interactive dashboard after the backend workflow is complete and tested.
