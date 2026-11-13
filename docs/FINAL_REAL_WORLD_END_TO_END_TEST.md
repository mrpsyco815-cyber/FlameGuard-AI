# FlameGuard AI Final Real-World End-to-End Acceptance Test

**Test date:** 2026-10-31  
**Test type:** Read-only real-world acceptance test  
**Branch:** `feature/research-backend`  
**Decision:** **PARTIAL PASS — INTEGRATION ISSUES**

## 1. Exact scientific query

The following query was used unchanged for the complete workflow:

> How does oxygen concentration affect flame spread and flame extinction in
> microgravity combustion experiments, and what evidence from NASA research and
> BASS-II experiments supports these observations? Compare available
> experimental conditions, identify consistent findings and disagreements,
> distinguish experimental evidence from simulations and theoretical models,
> identify missing evidence, and produce a source-linked mission research brief
> for spacecraft fire-safety researchers.

## 2. Environment and startup

Initial and final repository state:

```text
## feature/research-backend...origin/complete-project-upload [behind 33]
```

Existing worktree modifications and untracked files were preserved. Existing
stash was preserved:

```text
stash@{0}: On feature/research-backend: backup local mission intelligence changes
```

Runtime:

- Python: `3.10.9`
- FastAPI: `0.162.0`
- Uvicorn: `0.54.0`
- SQLite: `3.39.4`
- Existing `.venv` executable used.
- Temporary server: `127.0.0.1:8766`
- Startup: successful.
- Temporary review database: isolated path under `%TEMP%`.
- NASA requests: real requests to `https://ntrs.nasa.gov/api/citations/search`.
- NASA PDFs: not downloaded.

Basic endpoints:

| Endpoint | Status |
|---|---:|
| `/` | 200 |
| `/health` | 200 |
| `/openapi.json` | 200 |

No startup exception or warning affected the test.

Available local research data included:

- `research_intelligence_store.json`
- NASA extracted PDF-page records
- NASA reviewed evidence files
- BASS-II JSON dataset
- Existing NASA source PDFs/text already present before the test

## 3. Local-first retrieval

### Route

`GET /research/search?q=<master query>&limit=10`

### Result

- HTTP status: **200**
- Duration: **0.169 seconds**
- Retrieval method: `lexical_token_overlap`
- Local passages returned: **5**
- Local source documents represented: **1** in the displayed local brief
- Relevant source IDs observed:
  - `20000024924`
  - `19960008387`
  - `20210017787`
  - `20220012861`

### Representative returned evidence

#### NASA ID `20000024924`

Source URL:

`https://ntrs.nasa.gov/citations/20000024924`

Evidence role: `experimental_quantitative_result`  
Page: 7  
Evidence excerpt:

> However, one of the most important results is that, in microgravity, the
> extinction of the polyethylene occurs almost immediately when the flow of
> relatively low oxygen concentration (C = 21 percent) stops.

This is genuinely relevant to oxygen concentration, microgravity, and flame
extinction. It is not marked scientifically verified.

#### NASA ID `19960008387`

Source URL:

`https://ntrs.nasa.gov/citations/19960008387`

Page: 1  
Evidence excerpt:

> Solid Surface Combustion Experiment Flame Spread in a Quiescent,
> Microgravity Environment

This is relevant to flame spread and microgravity, although the returned
passage is a title/header passage rather than a complete experimental result.

#### NASA ID `20210017787`

Source URL:

`https://ntrs.nasa.gov/citations/20210017787`

Page: 8  
Evidence excerpt:

> These results indicate that concurrent flame spread in low pressure and
> normal gravity, may have similar characteristics as those in reduced gravity.

This is relevant to gravity and pressure comparison, but it does not establish
an oxygen-concentration effect by itself.

### Local retrieval observations

Positive:

- Stable NASA/source IDs were retained.
- Source URLs were retained.
- Exact excerpts and PDF pages were retained where available.
- Evidence roles and modalities were returned.
- Duplicate passages from the same NASA document were visible rather than
  silently treated as independent experiments.
- Ranking metadata and search-audit fields were returned.

Limitations:

- The local display limit returned multiple passages from one source, so the
  displayed source count was lower than the passage count.
- Some extracted passages were title/header material or text with extraction
  artifacts.
- Section names were absent in the raw local search response for these
  passages, although later insight claims mapped sections conservatively.
- The local result set alone did not establish a controlled oxygen comparison.

## 4. Live NASA NTRS fallback

### Route

`GET /research/online-search?q=<master query>&limit=5`

### Actual result

- HTTP status: **200**
- Duration: **6.194 seconds**
- Network: reachable; no request exception.
- Original natural-language query: recorded exactly.
- Original result count: **0**
- Focused NASA query:

  `oxygen concentration flame spread extinction microgravity combustion fire hazard`

- Fallback attempted: `true`
- Fallback reason: `original_query_returned_zero_results`
- Fallback result count: **0**
- Final NASA records: **0**

This is a real zero-result response, not a mocked success. The endpoint
distinguished a successful zero-result response from a network exception, but
there were no live NASA records to inspect in this run.

### Combined search

`GET /research/combined-search` returned HTTP 200 in **2.982 seconds**:

- Local passages returned: 5
- Local sources returned: 1
- Online metadata records: 0
- New online sources: 0
- Unique combined sources: 4
- Fallback triggered: `true`
- Reasons:
  - `too_few_local_passages`
  - `insufficient_local_source_coverage`
  - `required_scientific_concepts_not_covered`

The fallback metadata was preserved even though NASA returned zero records.

## 5. BASS-II dataset search

The actual dataset was inspected before filtering:

- Dataset: `NASA PSI-25 BASS-II Experimental Table`
- Records: **129**
- Columns: **17**
- Duplicate identifiers: **none**
- Source: user-provided transcription of NASA PSI-25 table.

Actual columns include:

- Fuel Sample Material
- Calibrated initial O2 % by volume
- Calibrated final O2 % by volume
- Flow restrictor
- Fan display
- Air display
- Radiometer gain
- Total Frames Shot
- Initial/final CO2
- Initial/final CO

The schema does **not** contain explicit columns for gravity condition, flame
spread rate, flame extinction outcome, pressure, or temperature.

### Fuel search

`GET /bass2/search?fuel=PMMA&limit=5`

- HTTP status: **200**
- Duration: **0.016 seconds**
- Results: **5**

Representative records:

| PI | Test | Material | Initial O2 | Final O2 | Flow restrictor | Frames |
|---|---|---|---:|---:|---|---:|
| Bhattacharjee | B1 | 100 micron PMMA film | 22.2 | 22.2 | 2 | 57 |
| Bhattacharjee | B2 | 200 micron PMMA film | 22.2 | 1.6 | 2 | none |
| Bhattacharjee | B4 | 300 micron PMMA film | 22.2 | 22.2 | 2 | 137 |
| Bhattacharjee | B6 | 0.1 mm PMMA film | 21 | 20.9 | 2 | 80 |
| Bhattacharjee | B8 | 0.2 mm PMMA film | 21 | 20.5 | 0 | 226 |

### Oxygen filter search

`GET /bass2/search?initial_oxygen=22.2&final_oxygen=22.2&limit=5`

- HTTP status: **200**
- Duration: **0.013 seconds**
- Results: **3**

The returned records included PMMA and Nomex records. This confirms that
initial/final oxygen filtering works against actual schema fields.

### BASS-II conclusion

BASS-II provides useful experimental metadata and oxygen-condition context, but
this dataset alone cannot establish measured flame-spread or flame-extinction
outcomes because those outcome fields are not present. The backend did not
invent those fields or infer outcomes from frame counts, fan displays, or
oxygen values.

## 6. Research Insights pipeline

### Route

`POST /research/insights`

Request used:

```json
{
  "query": "<exact master query>",
  "limit": 5
}
```

### Result

- HTTP status: **200**
- Duration: **2.868 seconds**
- Grouped papers: **4**
- Extracted claims: **5**
- Recommendation:

  `Insufficient verified evidence to support a mission-specific recommendation.`

- `scientific_findings_verified`: `false`

### Returned grouped sources

| NASA ID | Title | Classification | Review status |
|---|---|---|---|
| `20000024924` | Experimental Verification of Material Flammability in Space | experimental quantitative result | requires manual review |
| `19960008387` | Solid surface combustion experiment flame spread in a quiescent, microgravity environment | experimental quantitative result | requires manual review |
| `20210017787` | Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity | mixed comparison | requires manual review |
| `20220012861` | Determining Flame Temperature By Broadband Two Color Pyrometry in A Flame Spreading Over A Thin Solid in Microgravity | experimental quantitative result | requires manual review |

### Claim provenance

The important extinction claim from `20000024924` retained:

- `claim_id`: `claim-001`
- NASA ID and source document ID
- Source URL
- Exact supporting excerpt
- Page `[7]`
- Section `results`
- Evidence type `experimental_results`
- Verification status `not_scientifically_verified`
- `uncertain: false`

The pipeline also preserved the distinction that these are extracted,
source-linked claims rather than independently verified scientific findings.

### Claim-quality limitation

Some extractive claims were weakly formed from title/header text or contained
PDF text extraction artifacts. For example, the `19960008387` claim is
primarily a title/header passage. This is exposed as extractive evidence and
should not be presented by a frontend as a validated finding.

No abstract-only NASA records were returned in this particular run because the
live NASA fallback returned zero records. Existing response logic still labels
NASA metadata/abstract records as abstract-only when such records are returned.

## 7. Scientific comparison and conflict analysis

### Route

`POST /research/insights/compare`

### Result

- HTTP status: **200**
- Duration: **3.788 seconds**
- Sources compared: **4**
- Pairwise comparisons: **6**
- Comparable pairs: **0**
- Non-comparable pairs: **6**
- Pair statuses:
  - `partial_match`: 4
  - `mismatch`: 2

The comparison inspected these dimensions:

- Material/fuel
- Gravity condition
- Oxygen concentration
- Initial oxygen concentration
- Final oxygen concentration
- Pressure
- Temperature
- Flow condition
- Experimental setup

### Representative pair

For `20000024924` versus `19960008387`:

- Material: `partial_match`
- Gravity: `exact_match` (`microgravity`)
- Oxygen concentration: `partial_match`
- Initial oxygen: `unknown`
- Final oxygen: `unknown`
- Pressure: `unknown`
- Temperature: `unknown`
- Flow: `partial_match`
- Overall: `partial_match`

The returned rationale stated that values are compared only by explicit
value/unit signatures, missing values remain unknown, and no unit conversion
is performed.

### Conflict classifications

Six conservative conflict records were returned:

- `insufficient_information`: 4
- `not_comparable`: 2
- `potential_difference`: 0
- `supported_difference`: 0

No verified scientific contradiction was reported. This is appropriate because
the retrieved records did not provide sufficiently comparable conditions.

## 8. Research gap intelligence

The comparison response returned **5 gaps** and **37 follow-up questions**.

Observed gaps:

- `gap-001` through `gap-004`: condition information absent from the retrieved
  source representation.
- `gap-005`: insufficient comparable experiments.

The condition gaps identified missing combinations of:

- Material/fuel
- Gravity
- Oxygen concentration
- Initial oxygen
- Final oxygen
- Pressure
- Temperature
- Flow
- Experimental setup

Each gap included:

- Unique gap ID
- Description
- Related conditions
- Supporting source IDs
- Supporting claim IDs where available
- Missing information
- Evidence scope
- Confidence basis
- Review status

The generated questions were explicitly framed around retrieved studies and
did not claim that the entire scientific literature lacks the information.

## 9. Human review workflow

All review operations used an isolated temporary SQLite database selected by
server-side application state. The repository review database was not used.

### Verified operations

- Paper review creation: HTTP 200.
- Claim review creation: HTTP 200.
- All supported statuses:
  - `pending`
  - `accepted`
  - `rejected`
  - `needs_correction`
  - `insufficient_evidence`
- Review retrieval: HTTP 200.
- Review listing: HTTP 200.
- Review update: HTTP 200.
- Review history: HTTP 200 with revisions 1 and 2.
- Numeric NASA target ID `19960008415`: accepted and preserved as a string.
- Invalid status: HTTP 400.
- Invalid/path-traversal identifier: HTTP 400.
- Client-supplied arbitrary `db_path`: HTTP 400.
- Arbitrary path database created: `false`.

Accepted reviews returned:

```json
{
  "status": "accepted",
  "scientific_findings_verified": false
}
```

Reviewer identity was represented as:

`unverified_client_supplied`

The mission response included review records, but claim IDs such as
`claim-001` recur across multiple documents. This can cause review lookup to
associate same-named claim IDs across sources; frontend review displays should
use source document ID plus claim ID until claim identifiers are globally
unique.

## 10. Complete Mission Intelligence

### Route

`POST /research/mission-intelligence`

Request used:

```json
{
  "query": "<exact master query>",
  "mission_context": {
    "gravity_condition": "microgravity",
    "oxygen_concentration": "unknown",
    "fuel_material": "unknown",
    "pressure": "unknown",
    "temperature": "unknown",
    "flow_condition": "unknown"
  },
  "limit": 5
}
```

### Actual response summary

- HTTP status: **200**
- Duration: **2.877 seconds**
- Evidence papers: **4**
- Claims: **5**
- Comparison sources: **4**
- Pairwise comparisons: **6**
- Conflicts: **6**
- Research gaps: **5**
- Follow-up questions: **37**
- Human-review records: present
- Mission research brief: present
- `scientific_findings_verified`: `false`
- Conclusion:

  `Insufficient verified evidence to support a mission-specific recommendation.`

The mission response retained the same source IDs, evidence, comparisons, gaps,
and conservative conclusion observed in the preceding comparison response.
No operational spacecraft fire-safety instruction was generated.

### BASS-II orchestration observation

The mission response did not contain a separate BASS-II evidence section.
BASS-II was tested independently through its supported API and was not
silently treated as NASA flame-outcome evidence. The mission endpoint’s
returned evidence consisted of the research-insights corpus; BASS-II metadata
must therefore be presented separately unless an explicit integration field is
added in a future change.

## 11. Scientific response quality matrix

| Criterion | Rating | Evidence |
|---|---|---|
| Addresses oxygen concentration and flame extinction | PARTIAL | One local claim links 21% oxygen, microgravity, and extinction after flow stops |
| Addresses flame spread in microgravity | PASS | Local NASA passages and claims identify microgravity flame-spread studies |
| Distinguishes experiment, simulation, and theory | PARTIAL | Evidence classifications exist; this run contained mostly experimental/local passages and no live simulation comparison |
| Distinguishes initial from final oxygen | PASS | BASS-II schema and filters expose separate fields; research comparison leaves missing values unknown |
| Compares only compatible conditions | PASS | No comparable pairs were asserted; mismatches became non-comparable or insufficient-information |
| Identifies insufficient evidence | PASS | Five gaps and the exact conservative conclusion were returned |
| Avoids unsupported causal claims | PASS | No causal recommendation or universal conclusion was generated |
| Preserves source-linked claims | PASS | IDs, URLs, excerpts, pages, sections, and evidence types were present where available |
| Distinguishes metadata, abstracts, and full text | NOT TESTABLE in this run | Live NASA returned zero records; code path and response contract preserve this distinction |
| Avoids assuming paper independence | PASS | Comparison independence status remains unknown |
| Avoids treating BASS-II metadata as flame outcomes | PASS | Dataset lacks those outcome columns and response retained metadata-only limitations |
| Produces a mission research brief | PASS | Mission response contained `mission_research_brief` |

### Scientific-response assessment

The system provides a useful evidence-traceability and limitation report for
the query, but it does not answer the full scientific question conclusively.
It supports a narrow source-linked observation about polyethylene extinction
under a reported 21% oxygen condition in microgravity and identifies
microgravity flame-spread studies. It does not establish a controlled,
general oxygen-concentration relationship for flame spread and extinction.

## 12. Performance and regression

### HTTP timings

| Operation | Time |
|---|---:|
| Root | 0.023 s |
| Health | 0.014 s |
| OpenAPI | 0.042 s |
| Local search | 0.169 s |
| NASA online search | 6.194 s |
| Combined search | 2.982 s |
| Evidence search | 0.035 s |
| BASS-II summary | 0.005 s |
| BASS-II fuel search | 0.016 s |
| BASS-II oxygen search | 0.013 s |
| Research insights | 2.868 s |
| Scientific comparison | 3.788 s |
| Mission intelligence | 2.877 s |

Review CRUD/history operations were approximately 0.009–0.033 seconds each.

### Counts

- Unique grouped research sources: 4
- Local passages displayed: 5
- Comparison pairs: 6
- Extracted claims: 5
- Identified gaps: 5
- Follow-up questions: 37
- NASA records returned: 0
- NASA network errors: 0
- Comparable source pairs: 0

### Full regression suite

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s backend\tests -p "test*.py"
```

Result:

```text
173 tests passed
0 failed
0 skipped
Runtime: 1.473 seconds
```

Additional checks:

- `compileall -q backend`: passed.
- `git diff --check`: passed.

## 13. Failed or limited stages

### A. Exact query rejected by passage-search route length validation

Request:

```text
GET /research/nasa-passage-search?q=<exact master query>&limit=5
```

Actual response:

- HTTP **422**
- `q` has a maximum length of 200 characters.

The master query is longer than 200 characters. This is a route-level
integration limitation; other endpoints accepted the exact query.

### B. NASA fallback returned zero records

NASA was reachable and returned HTTP 200. The original query returned zero,
and the focused fallback also returned zero. This is a real live result, not a
mocked response. Consequently, no live NASA metadata/abstract record IDs were
available to verify in this run.

### C. Claim identifier collision

Multiple source documents produced `claim-001`. Mission review lookup returned
records for that shared claim ID rather than a globally source-qualified claim
identifier. This is a traceability limitation for review UI and should be
resolved before treating claim review records as uniquely source-bound.

## 14. Evidence provenance audit

Provenance survived local retrieval, insights, comparison, and mission
orchestration for the returned local records:

- NASA ID/source document ID
- Source URL
- Exact excerpt
- PDF page number
- Mapped section in extracted claims
- Evidence role/type
- Verification status
- Review status

Missing fields were not fabricated. BASS-II records retained original
experimental values and dataset field names. The system did not claim NASA
full-text evidence for the zero-result live fallback.

## 15. Final acceptance decision

**PARTIAL PASS — INTEGRATION ISSUES**

The complete local-to-mission workflow executes and returns a conservative,
source-linked response. Review persistence, comparison, gap analysis, and
mission orchestration work together in the tested environment. Unit tests,
compileall, and diff checks pass.

However, this is not a full workflow pass because:

1. The exact master query cannot be sent to the passage-search route because
   of its 200-character limit.
2. The real NASA fallback was reachable but produced zero records, so live NASA
   evidence could not be incorporated in this run.
3. Extracted claim IDs are not globally unique across source documents.
4. BASS-II context is available through its own API but is not included as a
   distinct section in the mission-intelligence response.

The backend is suitable for controlled frontend prototyping with these
limitations explicitly displayed. It should not be represented as a
scientifically validated or production-ready spacecraft fire-safety authority.

## 16. Preservation confirmation

- No source code modified during this acceptance test.
- No existing tests modified.
- No datasets modified.
- No research records modified.
- No existing database contents modified.
- No frontend files modified.
- Temporary review database removed with its temporary directory.
- Temporary server stopped.
- Existing worktree changes preserved.
- Existing stash preserved.
- No dependencies installed.
- No commits, pushes, merges, rebases, resets, cleans, or stash operations
  performed.

