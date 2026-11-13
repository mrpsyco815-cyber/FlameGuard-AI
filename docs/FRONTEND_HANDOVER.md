# FlameGuard AI Frontend Handover

## Audit scope and conclusion

This is the read-only backend handover audit completed on 2026-11-02. It
inspected `backend/main.py`, the services used by its routes, the BASS-II
dataset schema, the existing frontend contract, and the backend tests. No
backend logic, dataset, database, or existing frontend contract was changed.

**Conclusion: conditionally ready for controlled frontend integration, not
production-ready.** The HTTP routes and research workflows are implemented and
the existing test suite passes, but the frontend must surface scientific
verification state and limitations. Authentication, authorization, CORS,
stable generated schemas, and a production base URL are unavailable.

## Base behavior

- FastAPI application version: `0.1.0`.
- All successful route responses are JSON.
- No authentication or authorization is implemented.
- No CORS middleware is configured.
- The production base URL is not defined.
- NASA requests are synchronous and can take up to the upstream timeout.
- Review storage is server-selected. `db_path` is rejected from public review
  and mission-intelligence payloads and must never be exposed in the UI.
- Error responses normally use FastAPI's shape:

  ```json
  {"detail": "human-readable message"}
  ```

  FastAPI parameter validation can instead return HTTP 422 with a structured
  `detail` list. The NASA import route can return an object as `detail`.

## Endpoint inventory

### Service and health

#### `GET /`

Request: no parameters.

Response:

```json
{
  "message": "FlameGuard AI backend is running",
  "project": "FlameGuard AI",
  "version": "0.1.0"
}
```

Types: all strings.

Errors: no route-specific errors; unknown paths return HTTP 404.

#### `GET /health`

Request: no parameters.

Response:

```json
{
  "status": "healthy",
  "service": "flameguard-backend"
}
```

Types: both strings. This is a process health response, not a scientific data
or dependency health guarantee.

### Research search and NASA integration

#### `GET /research/search`

Example request:

```text
/research/search?q=oxygen%20concentration%20flame%20spread&limit=5
```

Parameters:

| Name | Location | Required | Type and validation |
|---|---|---:|---|
| `q` | query | yes | string, minimum 2 characters |
| `limit` | query | no | integer 1-20, default 5 |

Response: an evidence brief from the local research intelligence store. The
top-level implementation fields are `query`, `results`, `summary`,
`search_audit`, and evidence/ranking metadata produced by the store service.
Each result can include `record_id`, `record_origin`, `import_origin`,
`source_id`, `nasa_id`, `source_title`, `citation_url`, `source_url`,
`pdf_page_number`, `evidence_role`, `evidence_modality`,
`research_context`, `context_requirement`, `classification_version`,
`classification_review_status`, `source_review_status`, `evidence_type`,
`scientific_findings_verified`, `matched_query_terms`, `query_match_score`,
`relevance_components`, `matching_reasons`, `exact_source_excerpt`, and
`ranking_contract`. Result fields are source-record dependent.

Scientific status: local classifications are heuristic and
`scientific_findings_verified` is not a scientific certification.

Errors: HTTP 400 for invalid query/service validation; HTTP 422 for FastAPI
query validation; HTTP 503 if the local store is unavailable or a required
file is missing.

#### `GET /research/online-search`

Example request:

```text
/research/online-search?q=microgravity%20flame%20spread&limit=5
```

Parameters: `q` required string, minimum 2 characters; `limit` optional integer
1-20, default 5 at the HTTP route.

Response structure:

```json
{
  "source": "NASA NTRS",
  "query": "microgravity flame spread",
  "normalized_query": "microgravity flame spread",
  "count": 1,
  "results": [
    {
      "title": "string or null",
      "abstract": "string or null",
      "nasa_id": "string or number or null",
      "source_url": "string or null",
      "source": "NASA NTRS",
      "authors": [{"name": "string", "affiliation": "string or null"}],
      "publication_date": "string or null",
      "keywords": ["string"],
      "subject_categories": ["string"],
      "document_type": "value or null",
      "dissemination_status": "value or null",
      "document_available": false,
      "center": "string or null",
      "verification_status": "metadata_retrieved",
      "evidence_type": "bibliographic_metadata_and_abstract",
      "full_text_retrieved": false,
      "scientific_findings_verified": false,
      "review_status": "not_scientifically_reviewed",
      "relevance_score": 0.0,
      "matching_reasons": [],
      "retrieval_timestamp": "ISO-8601 string",
      "retrieved_at": "ISO-8601 string",
      "ranking_contract": {}
    }
  ],
  "retrieval_timestamp": "ISO-8601 string",
  "retrieved_at": "ISO-8601 string",
  "original_query": "string",
  "nasa_query": "string",
  "fallback_attempted": false,
  "fallback_reason": null,
  "original_result_count": 1,
  "fallback_result_count": 0
}
```

The result item shape above is the normalized implementation shape; nullable
or upstream-dependent values remain nullable. If the original search returns
no records, bounded fallback queries may add `fallback_attempts`, each with
`query`, `status`, `result_count`, and `reason`. Network or malformed NASA
responses return HTTP 200 with `count: 0`, `results: []`, and an `error`
string rather than an HTTP error.

NASA integration is catalog search only here. It retrieves bibliographic
metadata and abstracts; it does not prove a scientific finding.

#### `GET /research/combined-search`

Example request:

```text
/research/combined-search?q=oxygen%20concentration%20combustion&limit=5
```

Parameters: `q` required string, minimum 2 characters; `limit` optional
integer 1-20, default 5.

Response: the local-first federation object:

```json
{
  "query": "string",
  "search_strategy": "local_first_with_nasa_ntrs_fallback",
  "fallback_triggered": false,
  "fallback_reason": [],
  "missing_query_concepts": [],
  "fallback_thresholds": {},
  "local_evidence_brief": {},
  "online_search": {},
  "combined_sources": [],
  "conflict_report": {},
  "counts": {},
  "notices": ["string"]
}
```

`online_search.results` contains NASA catalog records with
`record_type: "nasa_ntrs_catalog_metadata"` and
`evidence_scope: "bibliographic_metadata_and_abstract_only"` when fallback is
performed. `counts` includes local passages, local sources, online metadata,
new online sources, merged online sources, and unique combined sources.

Errors: HTTP 400 for query/limit validation; HTTP 422 for FastAPI validation;
HTTP 503 may occur when local research files are unavailable.

#### `GET /research/evidence-search`

Example request:

```text
/research/evidence-search?q=flame%20spread&limit=5
```

Parameters: `q` required string, minimum 2 characters; `limit` optional
integer 1-20, default 5.

Response:

```json
{
  "query": "flame spread",
  "count": 0,
  "results": [],
  "notice": "These findings were manually reviewed against extracted NASA document text. They have not been independently scientifically verified. Consult the original cited paper."
}
```

Each result, when present, contains `evidence_id`, `nasa_id`, `title`,
`finding`, `evidence_class`, `pdf_page_number`, `citation_url`,
`review_status`, `scientific_findings_verified`, `matched_terms`,
`relevance_score`, `source_type: "reviewed_evidence"`, and `ranking_contract`.
An empty result is valid. Search is lexical, not semantic.

#### `GET /research/nasa-passage-search`

Example request:

```text
/research/nasa-passage-search?q=oxygen%20concentration&limit=10&nasa_id=20000024924
```

Parameters:

| Name | Required | Type and validation |
|---|---:|---|
| `q` | no | string, default empty, maximum 1000 characters |
| `limit` | no | integer 1-100, default 10 |
| `nasa_id` | no | string, 1-30 characters |
| `classification` | no | string, 1-50 characters |

If no query, NASA ID, or classification is supplied, `results` is empty.
Response wrapper:

```json
{
  "query": "string",
  "filters": {"nasa_id": "string or null", "classification": "string or null"},
  "count": 0,
  "results": [],
  "notice": "Results are extracted NASA document passages, not independently scientifically verified findings. Classification labels are candidates and may require manual review. Keyword matching is not semantic AI."
}
```

Passage fields include `nasa_id`, `source_type`,
`title`, `pdf_page_number`, `citation_url`, `source_field`, `snippet`,
`matched_terms`, `relevance_score`, `exact_phrase_match`, `classification`,
`classification_status`, `classification_basis`, `evidence_type`,
`research_status`, `experimental_result_status`, `review_status`,
`scientific_findings_verified`, `relevance_components`,
`matching_reasons`, and `ranking_contract`.

#### `POST /research/import/{nasa_id}`

Example request:

```text
POST /research/import/20000024924
```

No request body. `nasa_id` is a path string and must contain digits only.

This route is **mutating**: it can download and extract a NASA PDF and append
candidate passages to the supplemental research collection. It is not a
read-only search operation and should not be exposed as an unrestricted
frontend action.

Successful response varies by status:

```json
{
  "success": true,
  "status": "already_imported",
  "nasa_id": "20000024924",
  "title": "string or null",
  "passage_count": 0,
  "collection_path": "server filesystem path"
}
```

Other successful statuses include `already_in_primary_collection`. Failure
responses are HTTP 400 for an invalid NASA ID or HTTP 502 for citation,
download, identity, extraction, or passage failures. The HTTP `detail` may
contain `success: false`, `status`, `nasa_id`, `title`, `citation_url`,
`error`, `metadata_only`, `identity_audit`, `extraction_status`, or
`empty_pages`, depending on the failure.

### Research insights, summarization, comparison, and gaps

#### `POST /research/insights`

Example request:

```json
{
  "query": "oxygen concentration and flame spread in microgravity",
  "limit": 10
}
```

Body: required JSON object. `query` is required in practice, string with at
least 2 non-whitespace characters. `limit` is optional integer 1-100, default
10. Unknown body keys are accepted by the untyped route and ignored by the
service.

Actual top-level response:

```json
{
  "schema_version": "1.0",
  "query": "string",
  "retrieval": {
    "strategy": "string",
    "fallback_triggered": false,
    "fallback_reason": [],
    "missing_query_concepts": [],
    "online_search": {},
    "counts": {}
  },
  "evidence": {
    "paper_count": 0,
    "claim_count": 0,
    "papers": [],
    "claims": []
  },
  "conflict_report": {},
  "recommendation": "Insufficient verified evidence to support a mission-specific recommendation.",
  "scientific_findings_verified": false,
  "notices": ["string"],
  "limitations": ["string"]
}
```

Paper objects contain source identity (`document_id`, `nasa_id`, `source_url`,
`source_title`, `source_type`), `evidence_classification`,
`verification_status`, `review_status`, `scientific_findings_verified`,
`summary`, `claims`, `structured_findings`, and `provenance`. Claim objects
contain `claim_text`, `claim_type`, source identity, `exact_supporting_excerpt`,
`page_numbers`, `section_name`, `evidence_type`, `verification_status`,
`uncertain`, `supporting_evidence`, and
`scientific_findings_verified`. The implementation is extractive and
section/pattern based; it does not independently fact-check claims.

`structured_findings` is schema version `1.0` and includes source identity,
field status/value arrays, evidence, observations, findings, limitations, and
uncertainty notes. Extracted values preserve source text and units; no unit
conversion or causal inference is performed.

Errors: HTTP 400 for invalid body/query/limit; HTTP 422 if the body is not
accepted as a dictionary by FastAPI; HTTP 503 for missing local data files.

#### `POST /research/insights/compare`

Request: same object and validation as `/research/insights`.

Response contains the insights evidence and these additional top-level fields:

```json
{
  "schema_version": "1.0",
  "query": "string",
  "retrieval": {},
  "evidence": {},
  "comparison": {
    "sources": [],
    "comparable_sources": [],
    "non_comparable_sources": [],
    "condition_comparisons": [],
    "comparison_limitations": ["string"],
    "scientific_findings_verified": false
  },
  "conflicts": [],
  "research_gaps": [],
  "suggested_research_questions": [],
  "comparison_limitations": ["string"],
  "recommendation": "Insufficient verified evidence to support a mission-specific recommendation.",
  "scientific_findings_verified": false
}
```

Comparison dimensions are `material_fuel`, `gravity_condition`,
`oxygen_concentration`, `initial_oxygen_concentration`,
`final_oxygen_concentration`, `pressure`, `temperature`, `flow_condition`, and
`experimental_setup`. Dimension statuses are `unknown`, `partial_match`,
`exact_match`, or `mismatch`; overall statuses include `unknown`,
`partial_match`, `exact_match`, `compatible`, and `mismatch`.
`independence_status` is `unknown`. A mismatch is not a verified scientific
conflict. Values are compared by explicit text/unit signatures only; no unit
conversion or equivalence inference occurs.

Gaps contain `gap_id`, `gap_type`, `description`, related and missing
conditions, supporting source/claim IDs, `evidence_scope`,
`confidence_basis`, and `review_status`. Questions contain `question`,
`gap_ids`, and `supporting_source_ids`.

### Mission intelligence

#### `POST /research/mission-intelligence`

Example request:

```json
{
  "query": "oxygen concentration and flame spread in microgravity",
  "mission_context": {
    "mission": "spacecraft",
    "fuel_material": "PMMA",
    "gravity_condition": "microgravity",
    "oxygen_concentration": "21 percent"
  },
  "limit": 10,
  "review_status": "accepted"
}
```

Body: JSON object. `query` is required in practice and must contain at least
2 characters. `mission_context` is optional object; supported condition keys
include `material_fuel` (also `fuel`/`material`/`fuel_material` aliases),
`gravity_condition`, `oxygen_concentration`, `pressure`, `temperature`,
`flow_condition`, `experimental_setup`, and research-objective/question
fields used by the mission brief. `limit` is optional and is validated by
the underlying insights service as integer 1-100. `review_status` is optional
and is passed to review filtering. `db_path` is rejected and is internal
only.

Top-level response:

```json
{
  "schema_version": "1.0",
  "query": "string",
  "mission_context": {},
  "retrieval": {},
  "evidence": {},
  "comparison": {},
  "conflicts": [],
  "research_gaps": [],
  "suggested_research_questions": [],
  "bass2_evidence": {},
  "reviews": {
    "records": [],
    "accepted_review_present": false,
    "authentication_status": "not_available"
  },
  "mission_research_brief": {},
  "conclusion": "Insufficient verified evidence to support a mission-specific recommendation.",
  "scientific_findings_verified": false,
  "limitations": ["string"]
}
```

`bass2_evidence` includes dataset availability/search status, applied filters,
matching records, dataset summary/name/source, exact field names, condition
summary, limitations, and `scientific_findings_verified: false`. The mission
brief classifies each source as `exact_match`, `partial_match`,
`different_conditions`, or `unknown_conditions`, and includes condition
matches, reported conditions, observations, interpretations, claims, source
URLs, and verification status. It does not generate operational fire-safety
instructions.

Errors: HTTP 400 for invalid query, limit, review status, body, or
`db_path`; HTTP 422 for FastAPI body parsing; HTTP 503 for missing local files.

#### `GET /dashboard/mission-brief`

This is a separate legacy scenario-term endpoint, not the same response
contract as `/research/mission-intelligence`.

Example request:

```text
/dashboard/mission-brief?mission=spacecraft&q=flame%20spread&fuel=PMMA&limit=10
```

Parameters:

| Name | Required | Type and validation |
|---|---:|---|
| `mission` | yes | one of `moon`, `mars`, `spacecraft` |
| `q` | yes | string, 2-200 characters |
| `fuel` | no | string, max 120, default empty |
| `oxygen_concentration` | no | string, max 120, default empty |
| `flow_condition` | no | string, max 120, default empty |
| `gravity_condition` | no | string, max 120, default empty |
| `environment` | no | string, max 120, default empty |
| `limit` | no | integer 1-50, default 10 |

Response top-level fields are `project`, `mission_scenario`, `retrieval`,
`evidence`, `comparison`, `insights`, `recommendations`, and summary/count
fields from the legacy mission service. Evidence is split into
`experimental`, `simulation`, `reviewed_context`, and `bass2_context`.
Recommendations are conservative and default to insufficient verified
evidence. This route uses scenario-term overlap, not semantic relevance or
scientific certainty.

### BASS-II dataset

#### `GET /bass2/summary`

Request: no parameters.

Observed response:

```json
{
  "dataset_name": "NASA PSI-25 BASS-II Experimental Table",
  "record_count": 129,
  "declared_record_count": 129,
  "column_count": 17,
  "pi_counts": {},
  "blank_cells": 0,
  "literal_none_cells": 0,
  "duplicate_identifiers": [],
  "quality_flags_count": 0,
  "source_values_modified": false,
  "scientific_findings_verified": false
}
```

Counts are data-dependent; the shown values are the audited dataset values.
`pi_counts` is an object of string PI names to integer counts. The source is a
user-provided transcription of a NASA PSI-25 table (uploaded CSV).

#### `GET /bass2/search`

Example request:

```text
/bass2/search?q=PMMA&limit=10&fuel=PMMA&initial_oxygen=21&numeric_tolerance=0.5
```

All parameters are optional:

| Name | Type and validation | Default |
|---|---|---|
| `q` | string, default empty, no HTTP max length | `""` |
| `limit` | integer 1-100 | `10` |
| `pi` | string, 1-100 characters | null |
| `fuel` | string, 1-100 characters | null |
| `initial_oxygen` | float 0-100 | null |
| `final_oxygen` | float 0-100 | null |
| `numeric_field` | exact supported column name | null |
| `numeric_value` | float; requires `numeric_field` | null |
| `numeric_tolerance` | float >= 0 | `0` |

With no query or filters, `results` is empty. Response:

```json
{
  "query": "string",
  "filters": {
    "pi": "string or null",
    "fuel": "string or null",
    "initial_oxygen": "number or null",
    "final_oxygen": "number or null",
    "numeric_field": "string or null",
    "numeric_value": "number or null",
    "numeric_tolerance": 0
  },
  "count": 0,
  "results": [],
  "notice": "Search uses keyword matching, not semantic AI. Original experimental values are preserved as strings. Results are not independently scientifically verified."
}
```

Each result has `record` (the original object with all 17 fields), `source_type:
"bass_ii"`, `matched_terms`, numeric `relevance_score`,
`relevance_components`, `matching_reasons`, and `ranking_contract`.

Exact dataset fields and their observed type are:

| Field | Type |
|---|---|
| `PI` | string |
| `Test #` | string |
| `Date` | string |
| `GMT` | string |
| `Sample #` | string |
| `Fuel Sample Material` | string |
| `Flow restrictor` | string |
| `Fan display` | string |
| `Air display` | string |
| `Radiometer gain   (1000   250   50   10)` | string |
| `Total Frames Shot` | string |
| `Calibrated  initial O2 % by vol ` | string |
| `Calibrated final O2 % by vol` | string |
| `Initial CO2 % by vol` | string |
| `Final CO2 % by vol` | string |
| `Initial CO (ppm)` | string |
| `Final CO (ppm)` | string |

Supported `numeric_field` values are the exact names for calibrated initial
and final oxygen, initial/final CO2, initial/final CO, total frames, fan
display, air display, and flow restrictor. The double spaces and trailing
space in the initial oxygen field are significant.

The dataset does **not** contain gravity, pressure, temperature,
flame-spread-rate, or extinction-outcome fields. BASS-II results are metadata
and experimental conditions, not verified flame outcomes.

Errors: HTTP 400 for invalid numeric field, missing paired numeric parameter,
negative tolerance, or service limit validation; HTTP 422 for query parameter
type/range validation.

### Human review

#### `POST /research/reviews`

Example request:

```json
{
  "target_type": "claim",
  "target_id": "claim-001",
  "status": "pending",
  "source_document_id": "20000024924",
  "nasa_id": "20000024924",
  "source_url": "https://ntrs.nasa.gov/citations/20000024924",
  "reviewer_id": "optional-client-value",
  "reviewer_notes": "Review excerpt and evidence scope.",
  "correction_notes": null,
  "evidence_scope": "experimental_results"
}
```

Required: `target_type` and `target_id`. Optional: `status` (default
`pending`), source identity fields, reviewer identity/notes, correction notes,
and evidence scope. Supported target types are `paper`, `claim`,
`structured_finding`, `comparison`, `conflict`, `research_gap`, and
`mission_brief`. Supported statuses are `pending`, `accepted`, `rejected`,
`needs_correction`, and `insufficient_evidence`.

Response is one review row with `review_id` (UUID string), integer `revision`,
target/source fields, `reviewer_id`, `reviewer_identity_status`, `status`,
`reviewer_decision`, notes, `evidence_scope`, ISO-8601 timestamps, and
`scientific_findings_verified: false`. A client reviewer ID is explicitly
`unverified_client_supplied`; absent identity is `not_authenticated`.

#### `PATCH /research/reviews/{review_id}`

Example request:

```json
{
  "status": "accepted",
  "reviewer_notes": "Reviewed source-linked excerpt."
}
```

`status` is required; notes, correction notes, and reviewer ID are optional.
The update appends a revision and returns the current review row. `review_id`
must match a safe identifier of 1-200 characters:
`[A-Za-z0-9][A-Za-z0-9._:-]{0,199}`.

#### `GET /research/reviews`

Example request:

```text
/research/reviews?target_type=claim&target_id=claim-001&status=pending&limit=50
```

All query parameters are optional: `target_type`, `target_id`, `status`, and
`limit` (default 50, service range 1-100). Response:

```json
{"count": 0, "reviews": []}
```

`reviews` contains the current revision for each review ID.

#### `GET /research/reviews/{review_id}`

Returns one current review row. Unknown IDs return HTTP 404:

```json
{"detail": "Review not found."}
```

#### `GET /research/reviews/{review_id}/history`

Returns:

```json
{"review_id": "uuid", "history": []}
```

`history` contains every append-only revision in ascending revision order.
Unknown IDs return HTTP 404.

Review errors: HTTP 400 for unsupported target/status, unsafe identifiers,
invalid limits, or rejected `db_path`; HTTP 404 for missing reviews; HTTP 422
may occur for body parsing. Review persistence is not authenticated and an
accepted review is workflow state, not scientific certification.

## Scientific verification and provenance contract

The frontend must preserve, display, and never silently coerce these
distinctions:

- `scientific_findings_verified` is currently false throughout the audited
  public workflows.
- `verification_status`, `review_status`, `classification_status`, and
  `reviewer_identity_status` are different fields with different meanings.
- Source identity may be represented by `document_id`, `nasa_id`, `source_id`,
  `record_id`, `source_url`, `citation_url`, and `source_title`.
- Claim provenance includes `exact_supporting_excerpt`,
  `supporting_evidence`, `page_numbers`, `section_name`, `evidence_type`,
  `source_document_id`, `nasa_id`, and `source_url`.
- Structured field evidence includes `value`, `raw_value`, `unit`,
  `exact_supporting_text`, page/section provenance, extraction method,
  verification status, and uncertainty.
- Missing source fields are returned as null, empty, or absent depending on
  the source. The frontend must render “unknown/not available” and must not
  infer values.
- `relevance_score` and ranking metadata measure lexical retrieval behavior;
  they are not confidence, certainty, or safety scores.
- Abstracts and NASA catalog metadata are not full-text findings.
- Simulations, interpretations, limitations, and experimental observations
  must remain distinct.

## Frontend integration recommendations

1. Generate a typed client around the exact route behavior above, but retain
   nullable/unknown fields and tolerate additive response fields.
2. Show loading, timeout, cancellation, retry, and partial-result states for
   synchronous NASA-backed calls.
3. Use `/research/insights` as the primary research screen, `/compare` for
   explicit condition comparison, and `/research/mission-intelligence` for
   the review-aware mission workflow. Treat `/dashboard/mission-brief` as a
   legacy compatibility surface.
4. Render the exact source excerpt, citation URL, NASA ID, page, section,
   evidence type, review status, and verification status beside every claim or
   structured finding.
5. Clearly label lexical ranking, metadata-only evidence, heuristic
   classifications, unknown conditions, and non-comparable sources.
6. Do not present recommendations as certified fire-safety limits. The
   current recommendation is intentionally conservative.
7. Keep `/research/import/{nasa_id}` behind an explicit privileged workflow;
   it changes server data and may download external documents.
8. Do not expose `db_path`, server filesystem paths, or unauthenticated
   reviewer identity as trusted identity.
9. Treat HTTP 400, 404, 422, 502, and 503 separately and display the
   structured `detail` value where available.
10. Plan for a deployment decision on CORS, authentication/authorization,
    review tenancy, rate limiting, and a production base URL before release.

## Existing test status

The available command `python -m unittest discover -s backend\tests -p
"test_*.py" -q` completed successfully:

```text
Ran 178 tests in 2.102s
OK
```

`pytest -q backend/tests` could not be run because `pytest` is not installed.
No dependency was installed during this audit. The passing suite is not a
replacement for contract tests against deployed infrastructure, NASA network
failure tests, browser/CORS tests, authentication tests, or production
performance tests.

## Known frontend integration limitations

- No authentication, authorization, or authenticated reviewer identity.
- No CORS middleware.
- No production base URL or generated stable OpenAPI request/response models.
- Untyped dictionary bodies accept unknown keys and have limited client
  discoverability.
- NASA calls depend on an external synchronous service and can return a
  successful HTTP response containing an `error` and no results.
- Search is lexical/heuristic in several routes; scores are not scientific
  confidence.
- NASA online results are metadata/abstract scope unless separately imported
  and reviewed.
- The import endpoint mutates the supplemental collection and was not invoked
  by this audit.
- BASS-II preserves all values as strings and lacks gravity, pressure,
  temperature, spread-rate, and extinction-outcome fields.
- Review records are persisted, but accepted status is not scientific
  verification.
- The existing `docs/FRONTEND_API_CONTRACT.md` remains unchanged; this final
  handover records implementation details that contract did not fully specify,
  including the actual `nasa-passage-search` limit, BASS-II query validation,
  the `bass2_evidence` mission response, and the mutating import route.
