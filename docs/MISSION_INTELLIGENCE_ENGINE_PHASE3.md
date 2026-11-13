# Mission Intelligence Engine Phase 3

## Architecture

Phase 3 adds two integration layers:

1. `review_store.py` provides append-only SQLite review records with revision
   history.
2. `mission_intelligence_orchestrator.py` composes Phase 1 retrieval and
   Phase 2 comparison/gap services with mission research brief generation.

The workflow is:

`retrieval -> claims -> paper summaries -> structured findings -> comparison ->
conflicts -> gaps -> review lookup -> mission brief`

Existing retrieval, extraction, comparison, and gap algorithms are reused.

## API routes

### `POST /research/mission-intelligence`

Example:

```json
{
  "query": "oxygen concentration and flame spread in microgravity",
  "mission_context": {
    "mission": "spacecraft",
    "fuel_material": "PMMA",
    "gravity_condition": "microgravity",
    "oxygen_concentration": "21 percent"
  },
  "limit": 10
}
```

The response contains retrieval metadata, evidence papers and claims,
comparisons, conflicts, research gaps, review records, a mission research
brief, limitations, and the conservative conclusion:

`Insufficient verified evidence to support a mission-specific recommendation.`

### Review routes

- `POST /research/reviews`
- `GET /research/reviews`
- `GET /research/reviews/{review_id}`
- `GET /research/reviews/{review_id}/history`
- `PATCH /research/reviews/{review_id}`

Example create request:

```json
{
  "target_type": "claim",
  "target_id": "NASA-123-claim-001",
  "status": "pending",
  "source_document_id": "NASA-123",
  "nasa_id": "NASA-123",
  "evidence_scope": "experimental_results"
}
```

## Persistence model

SQLite is used through Python's standard-library `sqlite3` module. The default
database is `data/processed/research_reviews.sqlite3`. Tests inject isolated
temporary database paths. The `research_reviews` table stores:

- Review ID and revision.
- Target type and target ID.
- Source/document identity.
- Reviewer identity and identity status.
- Review status and decision.
- Reviewer/correction notes.
- Evidence scope.
- Created/updated timestamps.
- An explicit `scientific_findings_verified` value that remains false.

Updates append a new revision; prior decisions are retained in review history.
Source datasets and research records are not modified.

## Review statuses

Supported statuses are:

- `pending`
- `accepted`
- `rejected`
- `needs_correction`
- `insufficient_evidence`

Accepted review is evidence workflow state, not scientific certification.

## Authentication limitation

The repository has no authentication or authorization subsystem. Reviewer IDs
supplied by clients are therefore labeled
`unverified_client_supplied`, and the API does not claim authenticated identity.
This must be addressed before using the workflow in a multi-user deployment.

## Provenance and safeguards

Claims, comparisons, conflicts, and gaps retain source IDs, NASA IDs, URLs,
excerpts, pages, sections, evidence types, and review/verification labels when
available. Missing values remain missing. Abstracts and metadata remain
abstract-only, simulations remain distinct from experiments, and different
papers are not assumed to be independent experiments.

No route generates operational spacecraft fire-safety instructions. The
orchestrator always returns the conservative insufficiency conclusion for this
phase.

## Known limitations

- Review persistence is implemented, but authentication is not.
- The default SQLite file is created on first review-store access.
- Review records are not yet linked to an immutable source-content hash.
- Mission brief generation reuses the existing research brief and does not
  certify applicability.
- This implementation provides software safeguards and traceability, not
  scientific validation.

## Tests

Phase 3 tests cover review persistence, revisions, invalid statuses and IDs,
identity limitations, conservative orchestration, simulation distinction,
empty evidence, API validation, and review API operations. Full test results
are recorded in the implementation report accompanying this phase.
