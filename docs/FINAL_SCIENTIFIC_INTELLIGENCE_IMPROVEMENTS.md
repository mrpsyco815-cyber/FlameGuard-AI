# Final Scientific Intelligence Improvements

## Scope

This report documents the three targeted improvements requested after
[the final real-world acceptance test](./FINAL_REAL_WORLD_END_TO_END_TEST.md):

1. Long-query handling and bounded NASA NTRS fallback.
2. Conservative claim extraction and globally unique claim identifiers.
3. Separate BASS-II evidence in Mission Intelligence.

No frontend files, source datasets, NASA PDFs, or existing research records
were modified. No dependencies were installed.

## NASA search reliability

### Changes

- The NASA passage route now accepts bounded natural-language queries up to
  1,000 characters instead of rejecting the 200-character master question.
- The original query remains in the response.
- NASA fallback is bounded to at most three focused attempts.
- Focused strategies are only expanded for longer natural-language queries;
  concise queries retain the previous no-unnecessary-retry behavior.
- Each attempt records its query, status, result count, and reason.
- NASA records are deduplicated by stable NASA ID, with source URL fallback.
- Successful zero-result responses, network failures, invalid responses, and
  relevant returned records have distinct outcomes.
- NASA metadata remains explicitly metadata/abstract evidence and is not
  marked scientifically verified.

### Live NASA verification

The official NTRS endpoint was called with the existing HTTP integration. No
mock responses were used for these results.

| Query | Original results | Fallback attempts | Returned records |
|---|---:|---:|---:|
| `oxygen concentration microgravity combustion` | 5 | 0 | 5 |
| `microgravity flame spread` | 5 | 0 | 5 |
| `flame extinction oxygen` | 5 | 0 | 5 |
| `BASS-II combustion experiments` | 2 | 0 | 2 |
| `spacecraft material flammability` | 5 | 0 | 5 |

For the exact master query, the original focused NASA query returned zero
records, then the first bounded fallback succeeded:

```text
original query result count: 0
fallback query: oxygen concentration microgravity combustion
fallback result count: 5
fallback reason: original_query_returned_zero_results
attempts: 2 total (one original, one focused fallback)
```

Returned NASA IDs and titles included:

- `20130014061` — *Methanol Droplet Combustion in Oxygen-Inert Environments
  in Microgravity*
- `20120016855` — *Methanol Droplet Extinction in
  Oxygen/Carbon-dioxide/Nitrogen Mixtures in Microgravity: Results from the
  International Space Station Experiments*
- `20160000593` — *Combustion of Solids in Microgravity: Results from the
  BASS-II Experiment*
- `20140006750` — *Cool-flame Extinction During N-Alkane Droplet Combustion in
  Microgravity*
- `19970020606` — *Smoldering Combustion Experiments in Microgravity*

Each normalized record retained a NASA citation URL of the form
`https://ntrs.nasa.gov/citations/<NASA ID>`. No PDF was downloaded.

The exact master query also succeeded through
`GET /research/nasa-passage-search`:

```text
HTTP status: 200
local extracted passage count: 5
```

One returned source-linked excerpt was:

> However, one of the most important results is that, in microgravity, the
> extinction of the polyethylene occurs almost immediately when the flow of
> relatively low oxygen concentration (C = 21 percent) stops.

It remained classified as candidate background requiring manual review, not as
a verified scientific finding.

## Claim extraction and identifiers

### Changes

Claim extraction now rejects obvious:

- document titles and section headings;
- running-header/footer and page-number fragments;
- reference-list and common PDF extraction artifacts;
- incomplete fragments without a proposition-like scientific verb;
- claims without usable supporting excerpts.

Valid short scientific statements remain eligible. The exact source excerpt is
preserved alongside the normalized claim text, pages, sections, source URL,
NASA ID, evidence type, review status, and uncertainty.

Claim IDs are deterministic hashes prefixed with `claim-`. The hash includes
stable source identity, claim type, normalized claim text, and page numbers.
Therefore:

- repeated extraction of the same claim from the same source is stable;
- identical sequence positions in different documents do not collide;
- the identifier remains safe for review routes;
- NASA IDs and document IDs are unchanged.

Review association continues to resolve against the complete claim ID.
Accepted review remains a review status only and does not set
`scientific_findings_verified` to `true`.

## BASS-II Mission Intelligence integration

Mission Intelligence now has an additive `bass2_evidence` section. It uses the
existing schema-aware BASS-II loader and search implementation and exposes:

- dataset availability and search status;
- applied supported filters;
- matching and returned record counts;
- raw dataset records;
- original dataset column names;
- separate initial and final oxygen field names;
- supported condition fields such as fuel material, flow restrictor, fan,
  air display, and total frames;
- dataset provenance and limitations;
- `scientific_findings_verified: false`.

The integration does **not** invent gravity, pressure, temperature,
flame-spread-rate, or extinction-outcome fields. It does not infer a flame
outcome from oxygen values alone. BASS-II condition records remain distinct
from NASA bibliographic or extracted-passage evidence.

For the exact master query, BASS-II was available and searched, but no
material-specific filter was safely extractable from the question. The
returned mission section reported zero matching records while still exposing
the authoritative dataset schema and limitations. This is a conservative
result rather than a fabricated BASS-II finding.

The response shape is additive:

```json
{
  "bass2_evidence": {
    "dataset_available": true,
    "search_status": "completed",
    "applied_filters": {},
    "total_matching_records": 0,
    "returned_records": [],
    "field_names": ["Fuel Sample Material", "Calibrated  initial O2 % by vol "],
    "scientific_findings_verified": false,
    "limitations": [
      "BASS-II records provide condition and instrument metadata, not a verified flame-spread or extinction outcome."
    ]
  }
}
```

## Tests and validation

Added deterministic regression coverage for:

- bounded three-attempt NASA fallback;
- early stopping after relevant NASA results;
- zero-result attempt metadata;
- stable NASA-ID deduplication;
- long natural-language route queries;
- title/header/PDF-artifact filtering;
- exact excerpt preservation;
- stable same-source claim IDs;
- different-document claim identity;
- additive BASS-II Mission Intelligence evidence;
- initial/final oxygen separation;
- unsupported BASS-II fields not being invented.

Validation results:

```text
Targeted improvement and regression tests: 41 passed
Complete backend test suite:              178 passed
compileall -q backend:                    passed
git diff --check:                         passed
```

The temporary FastAPI server used for HTTP verification was stopped after the
checks. The isolated review database used by the tests was temporary and was
removed by test cleanup.

## Updated end-to-end result

The exact master query completed the following real workflow:

- local-first passage retrieval;
- long-query NASA passage HTTP retrieval;
- live NASA NTRS fallback;
- Research Insights;
- comparison and conservative conflict handling;
- gap analysis;
- human-review lookup;
- Mission Intelligence;
- separate BASS-II dataset context.

Mission Intelligence returned HTTP 200 and included the expected
`bass2_evidence`, `comparison`, `research_gaps`, `reviews`, and
`mission_research_brief` sections. The exact conservative conclusion remained:

> Insufficient verified evidence to support a mission-specific recommendation.

This conclusion is appropriate because NASA results in this integration are
metadata/abstract records or extracted passages requiring review, while
BASS-II does not provide the requested flame-spread and extinction outcomes in
its available schema.

## Remaining scientific limitations

1. NASA NTRS result relevance is ranked and explained, but live NTRS metadata
   and abstracts are not equivalent to full-text experimental verification.
2. The fallback strategies are deliberately bounded; a zero-result or
   irrelevant result remains possible for other queries.
3. BASS-II provides useful experimental-condition and instrument metadata but
   not a complete outcome dataset for the master question.
4. Human review identity is not authenticated by the backend.
5. Experimental independence cannot be established solely from bibliographic
   records and remains explicitly unknown where unsupported.
6. Comparison reports unknown or not-comparable dimensions rather than
   inferring missing pressure, temperature, gravity, or outcome values.

## Decision

**READY WITH DOCUMENTED LIMITATIONS**

The three identified integration limitations are addressed and the complete
backend workflow is testable with source-linked, conservative outputs.
Frontend integration may proceed against the additive response contract, but
the scientific limitations above must remain visible in the frontend and must
not be presented as verified mission recommendations.
