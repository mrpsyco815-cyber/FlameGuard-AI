# FlameGuard AI Final Backend Integration Audit

**Audit date:** 2026-10-31  
**Audit type:** Read-only Phase 4 integration audit  
**Branch:** `feature/research-backend`  
**Decision after blocker remediation:** **READY WITH DOCUMENTED LIMITATIONS** for
limited frontend development; **not production-ready**.

## Remediation status

The two blockers identified by this audit were subsequently fixed:

1. Review routes now use one server-controlled database path. Public payloads
   reject `db_path`; temporary databases remain injectable through internal
   application state/test setup.
2. Mission review lookup normalizes numeric NASA identifiers to strings for
   validation and lookup without changing source records.

Regression coverage and live isolated HTTP verification now pass. The
remaining CORS, authentication, deployment, pagination, and typed-schema
limitations below are unchanged.

## 1. Executive summary

The backend starts successfully, exposes FastAPI/OpenAPI routes, and the
existing automated suite passes: **169 tests passed in 1.314 seconds**.
`compileall` and `git diff --check` also passed.

Live HTTP checks confirmed that the research, comparison, NASA fallback,
BASS-II, passage, evidence, dashboard, and review-create/update routes can
return usable JSON responses. Provenance fields were present in the tested
research results, and the system preserved conservative scientific labels and
the exact insufficiency recommendation.

Two integration blockers were found during the original audit and are now
resolved:

1. The review create/update routes accept a client-supplied `db_path`, while
   review retrieval/list/history routes always use the default database. A
   review created in an isolated database cannot be retrieved through the
   other HTTP routes.
2. The exact required scientific query causes
   `/research/mission-intelligence` to return HTTP 400 because some online NASA
   records expose numeric document IDs. The review lookup path passes those
   integers to review-store validation, which only accepts string identifiers.

The backend remains unsuitable for production deployment because of the
remaining security and deployment limitations documented below.

## 2. Repository and environment state

Initial and final repository state:

```text
## feature/research-backend...origin/complete-project-upload [behind 33]
```

The worktree was already dirty before the audit. Existing modified and
untracked backend, test, fixture, and documentation files were preserved.
The existing stash was preserved unchanged:

```text
stash@{0}: On feature/research-backend: backup local mission intelligence changes
```

Environment verified without installing dependencies:

- Python: `3.10.9`
- FastAPI: `0.162.0`
- Uvicorn: `0.54.0`
- SQLite: `3.39.4`
- Existing `.venv` executable used for all commands.

The temporary Uvicorn server ran on `127.0.0.1:8765` and was stopped after
testing. Audit-created temporary SQLite files were removed. No source code,
tests, datasets, research records, frontend files, or existing stash entries
were modified by the audit.

The review store creates its parent directory and table on first access. A
review list request with no records still initialized the default
`data/processed/research_reviews.sqlite3`; that audit-created file was removed.
This behavior must be considered before production deployment.

## 3. API inventory

The application is registered directly in `backend/main.py`; no separate
router modules are used. No authentication or authorization dependency is
registered. No CORS middleware is registered.

### Core and research routes

| Method | Path | Request | Response / behavior | Audit status |
|---|---|---|---|---|
| GET | `/` | None | Backend message, project, version | 200 live |
| GET | `/health` | None | `{status, service}` | 200 live |
| GET | `/research/search` | Required `q` (2+ chars); optional `limit` 1–20, default 5 | Evidence brief | 200 live; 400/422 validation possible |
| GET | `/research/online-search` | Required `q` (2+ chars); optional `limit` 1–20, default 5 | NASA online search and fallback metadata | 200 live |
| GET | `/research/combined-search` | Required `q` (2+ chars); optional `limit` 1–20, default 5 | Local-first plus NASA fallback | 200 live |
| POST | `/research/insights` | JSON object; required `query` string of 2+ chars; optional `limit` 1–100, default 10 | Evidence papers, claims, summaries, retrieval, provenance, notices, conservative recommendation | 200 live; empty query/invalid limit 400 |
| POST | `/research/insights/compare` | Same as insights | Evidence plus condition comparisons, conflicts, gaps, questions | 200 live; empty query 400 |
| POST | `/research/mission-intelligence` | JSON object; `query`, optional `mission_context` object, `limit`, `review_status`, `review_db_path` | Retrieval, evidence, comparisons, conflicts, gaps, reviews, mission brief, conservative conclusion | 200 for a short query; exact required query reproduced 400 blocker |
| GET | `/research/evidence-search` | Required `q` (2+ chars); optional `limit` 1–20, default 5 | Reviewed-extraction search with notice | 200 live |
| GET | `/research/nasa-passage-search` | Optional `q` max 200, `limit` 1–100, `nasa_id`, `classification` | Extracted passage records with notice | 200 live |
| POST | `/research/import/{nasa_id}` | NASA ID path parameter | Import result or 400/502 error | Not imported during audit to avoid data changes |

### BASS-II and dashboard routes

| Method | Path | Request | Response / behavior | Audit status |
|---|---|---|---|---|
| GET | `/bass2/summary` | None | Dataset structure and quality counts | 200 live |
| GET | `/bass2/search` | Optional `q` max 200, `limit` 1–100, `pi`, `fuel`, initial/final oxygen, supported `numeric_field`, `numeric_value`, nonnegative tolerance | Raw-field-preserving BASS-II records, ranking metadata, scientific notice | 200 live; unsupported numeric field returns 400 |
| GET | `/dashboard/mission-brief` | Required `mission` in `moon\|mars\|spacecraft`, required `q` 2–200; optional supported context strings and `limit` 1–50 | Legacy scenario-term mission brief | 200 live |

### Review routes

| Method | Path | Request | Response / behavior | Audit status |
|---|---|---|---|---|
| POST | `/research/reviews` | JSON passed to `create_review`; target type/id, status, provenance fields, notes, optional `db_path` | Review revision 1 | 200 isolated live |
| GET | `/research/reviews` | Optional target type/id, status, limit | Current review rows from default DB | 200 live, but no database selector |
| GET | `/research/reviews/{review_id}` | Review ID path | Current revision or 404 | 404 for review created in isolated DB |
| GET | `/research/reviews/{review_id}/history` | Review ID path | Revision history or 404 | 404 for review created in isolated DB |
| PATCH | `/research/reviews/{review_id}` | JSON status plus notes and optional `db_path` | Appended revision | 200 isolated live |

Review statuses are `pending`, `accepted`, `rejected`,
`needs_correction`, and `insufficient_evidence`. Accepted reviews retain
`scientific_findings_verified: false`.

The review API has no authentication requirement because no authentication
system exists. Client-supplied reviewer IDs are returned as
`unverified_client_supplied`.

## 4. Live HTTP results

### Basic API

- `/`: HTTP 200.
- `/health`: HTTP 200 with healthy service response.
- `/openapi.json`: HTTP 200.
- Unknown route: HTTP 404.

### Research and comparison

- Valid `/research/insights`: HTTP 200; returned papers, claims, exact
  excerpts, page numbers, sections, evidence types, source URLs, NASA IDs, and
  conservative recommendation.
- Empty insights query: HTTP 400.
- Invalid insights limit: HTTP 400.
- Valid comparison: HTTP 200 with comparison structure and evidence.
- Empty comparison query: HTTP 400.
- Local search, online search, combined search, evidence search, and passage
  search: HTTP 200 in the live run.
- BASS-II summary and search: HTTP 200.
- Unsupported BASS-II numeric field: HTTP 400.
- Dashboard mission brief: HTTP 200.

### Review persistence

Using a temporary SQLite database:

1. POST create returned HTTP 200, revision 1, status `pending`.
2. PATCH update returned HTTP 200, revision 2, status `accepted`.
3. Both responses returned `scientific_findings_verified: false`.
4. Reviewer identity was `unverified_client_supplied`.
5. GET and history without a database selector returned 404.
6. List without a database selector returned an empty default-database list.
7. Invalid status returned HTTP 400 with the allowed-status message.

The temporary database was deleted after testing.

## 5. Exact end-to-end scientific workflow

The required query was tested exactly:

> How does oxygen concentration affect flame spread and flame extinction in
> microgravity combustion experiments, and what evidence from NASA research and
> BASS-II experiments supports these observations?

### Insights and comparison

Both endpoints returned HTTP 200 and retained the workflow output. The live
retrieval result included:

- Local passages: 3.
- Local sources: 1.
- NASA metadata records: 3.
- Unique combined sources: 6.
- Extracted claims: 22.
- NASA original query: the full natural-language query.
- Focused fallback query:
  `oxygen concentration flame spread extinction microgravity combustion`.
- Original NASA result count: 0.
- Fallback result count: 3.
- NASA content scope: `bibliographic_metadata_and_abstract_only`.

### Mission intelligence

The exact mission-intelligence request returned HTTP 400:

```text
target_id must be a non-empty safe identifier.
```

Direct inspection of the comparison output showed that some online document
IDs were integers, for example `19960008415`, while
`review_store._validate_target()` requires `target_id` to be a string matching
its safe-identifier regex. The orchestrator attempts review lookup for those
IDs and fails before returning the mission brief.

This prevents the required exact query from completing the full orchestration
through human-review lookup and mission-brief response.

## 6. Provenance audit

The tested local evidence and claim responses preserved, where available:

- Stable document ID.
- NASA ID.
- NASA citation URL.
- Exact supporting excerpt.
- Page number.
- Section name.
- Evidence type.
- Review status.
- Verification status.
- Source type.

The tested local claim included a page and results section. NASA fallback
records were clearly marked metadata/abstract-only and did not claim full-text
retrieval. Missing provenance fields were not fabricated.

Comparison sources retain source identity and condition-match rationale.
Comparison output explicitly reports `independence_status: "unknown"` and does
not infer experiment independence from paper IDs.

The exact workflow could not complete its mission-intelligence response because
of the numeric-ID review lookup defect, so provenance of the final mission
brief could not be verified for that query.

## 7. NASA fallback behavior

NASA fallback is bounded and explainable. For the exact query, the original
long query returned zero records, then the focused query returned three
application-limited records. The response exposed:

- `original_query`
- `nasa_query`
- `fallback_attempted`
- `fallback_reason`
- `original_result_count`
- `fallback_result_count`
- `content_scope`

The live behavior did not download NASA PDFs. NASA records were represented as
metadata/abstract evidence.

NASA requests use a 20-second request timeout in `nasa_online.py`. The
orchestration is synchronous, so a frontend must show loading state and handle
slow or failed requests.

## 8. Scientific safety and data integrity

Verified safeguards:

- NASA metadata and abstracts remain metadata/abstract evidence.
- Simulation/model evidence remains distinct from experimental observations.
- Missing conditions remain unknown.
- Units are compared by explicit value/unit signatures; no silent conversion.
- Mismatched conditions are not labeled verified contradictions.
- Different papers are not assumed independent experiments.
- Scientific verification remains false in tested outputs.
- Accepted review does not set scientific verification true.
- The exact insufficiency recommendation is returned:

  `Insufficient verified evidence to support a mission-specific recommendation.`

- BASS-II search exposes the dataset's supported fields and preserves original
  values as strings.
- No operational spacecraft fire-safety instruction was generated.

No datasets, research records, or source database contents were changed.

## 9. Test suite and code quality

Commands executed:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s backend\tests -p "test*.py"
.\.venv\Scripts\python.exe -m compileall -q backend
git diff --check
```

Results:

- **169 tests passed**
- **0 failed**
- **0 skipped**
- Runtime: **1.314 seconds**
- Compileall: **passed**
- Diff check: **passed** (existing CRLF conversion warnings were emitted by
  Git for pre-existing modified files; no whitespace error was reported)

Passing tests do not cover the live review database-path inconsistency or the
exact-query numeric-ID orchestration failure.

## 10. Frontend readiness matrix

| Category | Status | Finding |
|---|---|---|
| API contract stability | PARTIALLY READY | Routes respond consistently for common paths, but review database selection and exact mission orchestration are inconsistent |
| Request/response consistency | PARTIALLY READY | Research schemas are usable; review routes do not share database selection behavior |
| Error response consistency | PARTIALLY READY | FastAPI validation and explicit 400/404/503 paths exist, but some validation failures are discovered late |
| CORS | NOT READY | No CORS middleware is configured |
| Authentication/authorization | NOT READY | No authentication or authorization subsystem exists |
| Database configuration | NOT READY | Default review DB is implicit, initialized on reads, and not consistently selectable |
| Review persistence | PARTIALLY READY | SQLite revisions work directly and through create/update, but HTTP retrieval cannot target the same isolated DB |
| NASA request behavior | PARTIALLY READY | Bounded timeout and fallback metadata exist; requests are synchronous and can be slow |
| Timeout/failure handling | PARTIALLY READY | NASA service catches request errors, but frontend-facing long-running behavior is not asynchronous |
| Provenance consistency | PARTIALLY READY | Strong source-linked fields are present; exact mission workflow is blocked for numeric NASA IDs |
| Pagination/result limits | PARTIALLY READY | Bounded limits exist; there is no page/cursor pagination |
| OpenAPI documentation | PARTIALLY READY | OpenAPI is available, but dict payloads and untyped response contracts are weakly documented |
| Frontend-compatible response schemas | PARTIALLY READY | JSON is usable, but heterogeneous nested structures and legacy/new mission routes differ |
| Review API security | NOT READY | Client can supply reviewer identity and database path; no authorization controls |

## 11. Exact blockers and reproduction

### Blocker A — Review database path is not a coherent HTTP contract

**Severity:** High integration/security concern  
**Files:** `backend/main.py`, `backend/services/review_store.py`

Reproduction:

1. POST `/research/reviews` with `"db_path": "<temporary SQLite path>"`.
2. Observe HTTP 200 and a review ID.
3. GET `/research/reviews/{review_id}`.
4. Observe HTTP 404 because GET uses the default database.
5. GET `/research/reviews/{review_id}/history`.
6. Observe HTTP 404 for the same reason.

The API also accepts a filesystem path from an unauthenticated client. This
creates path-disclosure/configuration and multi-tenant isolation risks.

### Blocker B — Numeric NASA IDs break mission orchestration

**Severity:** High functional integration concern  
**Files:** `backend/services/research_insights.py`,
`backend/services/mission_intelligence_orchestrator.py`,
`backend/services/review_store.py`

Reproduction:

1. POST `/research/mission-intelligence` using the exact scientific query
   above, a bounded limit, and an isolated `review_db_path`.
2. Observe HTTP 400:
   `target_id must be a non-empty safe identifier.`
3. Inspect the preceding comparison evidence: online NASA documents include
   numeric IDs such as `19960008415`.
4. The orchestrator passes those IDs to review lookup, while review-store
   validation requires `str`.

The endpoint therefore cannot complete the required exact workflow whenever
numeric NASA IDs are present.

### Additional deployment limitations

- No CORS configuration.
- No authentication or authorization.
- No page/cursor pagination.
- Synchronous NASA calls.
- Dict-based request bodies without typed Pydantic contracts.
- Default review database path is implicit and initialized by read operations.
- The legacy dashboard brief and the new mission-intelligence brief expose
  different response contracts.

## 12. Required fixes before frontend integration

At minimum:

1. Remove client control of database paths; configure one server-side review
   database or use an explicitly authenticated tenant/database policy.
2. Make all review routes use the same configured database and test create,
   get, list, patch, and history over HTTP.
3. Normalize document and claim identifiers to safe strings before review
   lookup, or update the identifier contract consistently.
4. Add regression tests for the exact required query and numeric NASA IDs.
5. Add CORS policy for the selected frontend origin.
6. Define authentication/authorization before exposing review mutation routes.
7. Publish typed, stable request/response schemas and frontend error/loading
   behavior.

## 13. Production deployment limitations

The backend is not production-ready. Scientific research outputs remain
unverified research support, not certification or operational fire-safety
authority. Authentication, authorization, CORS, review tenancy, database
configuration, observability, rate limiting, and asynchronous external-request
handling require additional work.

## 14. Final decision

**READY WITH DOCUMENTED LIMITATIONS** for constrained frontend development,
API exploration, and presentation-layer prototyping that does not depend on
the broken review retrieval workflow or exact-query mission orchestration.

**NOT READY for production deployment or unqualified frontend integration**
until Blockers A and B and the security/deployment limitations above are
resolved.
