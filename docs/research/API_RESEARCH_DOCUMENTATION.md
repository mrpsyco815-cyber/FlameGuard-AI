# Research API Documentation

## `GET /research/search`

Searches reviewed/annotated local evidence passages. `q` is required and
`limit` is 1–20. Results include exact excerpts, source IDs, citation URLs,
PDF pages, evidence roles/modalities, review status, verification status,
relevance components, and matching reasons.

## `GET /research/combined-search`

Runs local-first evidence retrieval and conditionally searches official NASA
NTRS metadata. `q` is required and `limit` is 1–20. `fallback_triggered` and
`fallback_reason` explain whether local evidence lacked relevant passage/source,
material, experimental-condition, or scientific-concept coverage. Online
records are catalogue metadata/abstracts only and are never marked
scientifically verified. Combined responses include a `conflict_report`; it
compares only explicitly structured parameter/value/unit/condition/source
fields and leaves disagreements unresolved for scientific review. Free-text
passages are not converted into claims.

## `GET /research/online-search`

Queries `https://ntrs.nasa.gov/api/citations/search`. Results include NASA ID,
title, abstract, authors, publication date, keywords, subjects, document type,
official URL, retrieval scope, `retrieved_at`, and relevance reasons. Timeouts
and malformed responses return an explicit error object with zero results.

## `GET /research/nasa-passage-search`

Searches extracted local NASA passages. This is distinct from NTRS catalogue
metadata and preserves PDF page and classification provenance.

## `GET /bass2/search`

Searches structured BASS-II records without converting them into passages.
Original column names and raw values are returned. `pi`, `fuel`,
`initial_oxygen`, `final_oxygen`, `numeric_field`, `numeric_value`, and
`numeric_tolerance` are optional filters; `limit` is 1–100. Supported numeric
fields are the O2, CO2, CO, frames, fan display, air display, and flow
restrictor columns present in the original dataset. Pressure, temperature, and
gravity filters are not exposed because those columns do not exist in the
source schema. Results are not independent scientific
verification.

## Error behavior

Invalid query/limits are HTTP 400 where validated by the route. Missing local
stores are HTTP 503 for local evidence routes. NASA availability failures are
represented explicitly in the online-search/federation payload while local
results are retained.
