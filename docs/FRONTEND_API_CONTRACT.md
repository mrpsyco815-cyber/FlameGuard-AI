# FlameGuard AI Frontend API Contract

This document records the contracts observed during the read-only backend
integration audit on 2026-10-31 and the subsequent blocker remediation. It is
an integration reference, not a
promise that the backend is production-ready. Fields not listed as guaranteed
should be treated as optional or unverified by the frontend.

## Base behavior

- Local development server used during audit: `http://127.0.0.1:8765`.
- Production base URL: **unverified**.
- JSON responses are used for successful POST and GET requests.
- No authentication mechanism is currently implemented.
- No CORS middleware is currently configured.
- The frontend must not expose or allow users to select `db_path`; the server
  now rejects client-supplied database paths.
- NASA-backed requests are synchronous and may take up to the backend request
  timeout; show a loading state and support request cancellation/retry.

## Endpoint inventory

### Health and root

#### `GET /health`

Response:

```json
{
  "status": "healthy",
  "service": "flameguard-backend"
}
```

#### `GET /`

Response:

```json
{
  "message": "FlameGuard AI backend is running",
  "project": "FlameGuard AI",
  "version": "0.1.0"
}
```

### Unified research insights

#### `POST /research/insights`

Request:

```json
{
  "query": "oxygen concentration and flame spread in microgravity",
  "limit": 10
}
```

- `query`: required string; at least two characters.
- `limit`: optional integer from 1 through 100; default 10.

Representative response shape:

```json
{
  "schema_version": "1.0",
  "query": "oxygen concentration and flame spread in microgravity",
  "retrieval": {
    "strategy": "local_first_with_nasa_ntrs_fallback",
    "fallback_triggered": true,
    "fallback_reason": [],
    "online_search": {
      "performed": true,
      "status": "completed",
      "original_query": "...",
      "nasa_query": "...",
      "fallback_attempted": true,
      "original_result_count": 0,
      "fallback_result_count": 3,
      "content_scope": "bibliographic_metadata_and_abstract_only"
    },
    "counts": {}
  },
  "evidence": {
    "paper_count": 1,
    "claim_count": 1,
    "papers": [],
    "claims": []
  },
  "recommendation": "Insufficient verified evidence to support a mission-specific recommendation.",
  "scientific_findings_verified": false,
  "notices": [],
  "limitations": []
}
```

Paper and claim provenance may include:

- `document_id`
- `nasa_id`
- `source_url`
- `source_title`
- `source_type`
- `evidence_classification`
- `verification_status`
- `review_status`
- `summary`
- `claims`
- `structured_findings`
- `provenance`

Claims may include `exact_supporting_excerpt`, `page_numbers`,
`section_name`, and `evidence_type`. Missing values must render as unknown or
not available; the frontend must not infer them.

### Scientific comparison

#### `POST /research/insights/compare`

Request is the same as `/research/insights`.

Additional response fields:

```json
{
  "comparison": {
    "sources": [],
    "condition_comparisons": [],
    "comparable_sources": [],
    "non_comparable_sources": [],
    "scientific_findings_verified": false
  },
  "conflicts": {},
  "research_gaps": [],
  "suggested_research_questions": [],
  "comparison_limitations": []
}
```

Comparison statuses include `exact_match`, `compatible`, `partial_match`,
`mismatch`, and `unknown`. A `mismatch` is not a verified scientific
contradiction. `independence_status` is explicitly unknown where applicable.

### Mission intelligence

#### `POST /research/mission-intelligence`

Request:

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

- `query`: required in practice; same minimum length as research insights.
- `mission_context`: optional object. Only supported dimensions should be
  supplied; unknown conditions must remain unknown.
- `limit`: bounded by the underlying research-insights service.
- `review_status`: optional review status filter.
- `review_db_path`: internal/test-only parameter accepted by the current
  implementation but **must not be exposed by a frontend**.

Response shape:

```json
{
  "schema_version": "1.0",
  "query": "...",
  "mission_context": {},
  "retrieval": {},
  "evidence": {},
  "comparison": {},
  "conflicts": [],
  "research_gaps": [],
  "suggested_research_questions": [],
  "reviews": {
    "records": [],
    "accepted_review_present": false,
    "authentication_status": "not_available"
  },
  "mission_research_brief": {},
  "conclusion": "Insufficient verified evidence to support a mission-specific recommendation.",
  "scientific_findings_verified": false,
  "limitations": []
}
```

Numeric NASA document identifiers are normalized to strings for review lookup
without changing the original source record. The exact numeric-ID mission
workflow was verified successfully after remediation.

### Review workflow

#### `POST /research/reviews`

Request:

```json
{
  "target_type": "claim",
  "target_id": "claim-001",
  "status": "pending",
  "source_document_id": "20000024924",
  "nasa_id": "20000024924",
  "source_url": "https://ntrs.nasa.gov/citations/20000024924",
  "reviewer_notes": "Review excerpt and evidence scope.",
  "correction_notes": null,
  "evidence_scope": "experimental_results"
}
```

Supported `target_type` values:

`paper`, `claim`, `structured_finding`, `comparison`, `conflict`,
`research_gap`, `mission_brief`.

Supported statuses:

`pending`, `accepted`, `rejected`, `needs_correction`,
`insufficient_evidence`.

Response fields include:

- `review_id`
- `revision`
- `target_type`
- `target_id`
- source identity fields
- `reviewer_id`
- `reviewer_identity_status`
- `status`
- `reviewer_decision`
- notes
- `evidence_scope`
- timestamps
- `scientific_findings_verified`

The frontend must display accepted review as workflow state only. It must not
display it as scientific certification.

#### `PATCH /research/reviews/{review_id}`

Request:

```json
{
  "status": "accepted",
  "reviewer_notes": "Reviewed source-linked excerpt."
}
```

Updates append a revision. Client-supplied `db_path` is rejected; database
selection is server-controlled.

#### `GET /research/reviews`

Optional query parameters:

- `target_type`
- `target_id`
- `status`
- `limit`

Response:

```json
{
  "count": 0,
  "reviews": []
}
```

#### `GET /research/reviews/{review_id}`

Returns the current revision or:

```json
{
  "detail": "Review not found."
}
```

#### `GET /research/reviews/{review_id}/history`

Response:

```json
{
  "review_id": "uuid",
  "history": []
}
```

Review create, get, list, patch, and history now use the same server-selected
database. Tests may inject an isolated database through internal application
configuration; that mechanism is not a public API contract.

### Existing search APIs

#### `GET /research/search`

Required query parameter `q` (minimum two characters). Optional `limit` 1–20,
default 5. Returns the existing evidence brief.

#### `GET /research/online-search`

Required `q`, optional `limit` 1–20, default 5. Returns NASA online records and
fallback metadata.

#### `GET /research/combined-search`

Required `q`, optional `limit` 1–20, default 5. Returns local-first combined
results and fallback metadata.

#### `GET /research/evidence-search`

Required `q`, optional `limit` 1–20, default 5. Returns reviewed-extraction
results and a notice that results are not independently scientifically verified.

#### `GET /research/nasa-passage-search`

Optional `q` max 200, `limit` 1–100, `nasa_id`, and `classification`.

#### `GET /bass2/search`

Optional `q`, `limit` 1–100, `pi`, `fuel`, `initial_oxygen`,
`final_oxygen`, supported `numeric_field`, `numeric_value`, and
`numeric_tolerance`. Unsupported numeric fields return HTTP 400. Original
BASS-II values are preserved as strings.

#### `GET /bass2/summary`

Returns dataset counts, columns/quality counts, duplicate identifiers, and
`scientific_findings_verified: false`.

#### `GET /dashboard/mission-brief`

Requires `mission=moon|mars|spacecraft` and `q`; optional legacy scenario
context fields and `limit`.

## Error handling

Observed responses:

- HTTP 400: application validation errors, such as short queries, invalid
  limits, unsupported statuses, or unsupported BASS-II numeric fields.
- HTTP 404: unknown routes and missing reviews.
- HTTP 422: FastAPI query-parameter validation may occur before route logic.
- HTTP 503: some local data/file failures from research routes.
- HTTP 502: NASA import failures represented by the import route.

The frontend should render `detail` when present, but should not assume every
error has an identical nested schema.

## Loading and NASA behavior

NASA calls are synchronous and can be slow. The frontend should:

1. Show an explicit loading state.
2. Disable duplicate submissions while a request is active.
3. Allow retry after timeout or 5xx errors.
4. Display fallback metadata when `fallback_attempted` is true.
5. Display `content_scope` and evidence classification prominently.
6. Never label NASA metadata or abstracts as full-text verified findings.

## Provenance rendering requirements

For every claim or result, render available:

- Source/document ID.
- NASA ID.
- Source URL.
- Source title.
- Exact excerpt.
- Page number(s).
- Section.
- Evidence type/classification.
- Verification status.
- Review status.
- Condition-match rationale where applicable.

Do not fabricate missing page, section, URL, or document values. Display
`Unknown` or `Not reported` instead.

## Limits and pagination

All current routes use bounded result limits, but no route provides page,
cursor, or continuation-token pagination. The frontend must not assume that a
returned result set is exhaustive.

## Authentication and CORS

Authentication and authorization are not implemented. Reviewer identity is not
verified. CORS is not configured. Frontend integration requires a deployment
policy and backend configuration before browser requests from a separate
origin can be considered supported.

## Scientific safety

The backend returns the exact conservative conclusion:

`Insufficient verified evidence to support a mission-specific recommendation.`

The frontend must preserve this language, distinguish abstract/model evidence
from experiments, and avoid presenting research-support output as a certified
fire-safety recommendation.
