# FlameGuard AI Research Insights Engine Audit

## 1. Executive summary

FlameGuard AI has a substantial **extractive, provenance-preserving research
backend**, but it is not yet a complete integrated Research Insights Engine.
The strongest implemented capabilities are local-first retrieval, NASA NTRS
metadata fallback, structured NASA passage extraction, source-linked claim
extraction, explicit condition comparison, duplicate-source annotation, and
conservative mission brief generation.

The principal architectural limitation is integration: the claim,
multi-document synthesis, human-review, and mission-brief services are mostly
standalone Python services. Only the lower-level search/federation services and
`mission_intelligence` are exposed through FastAPI. There is no public endpoint
that accepts retrieved documents and returns claim-level insights, cross-study
comparisons, research gaps, conflicts, or a review queue as one coherent
workflow.

**Overall readiness: PARTIALLY IMPLEMENTED / NOT SCIENTIFICALLY VALIDATED.**
The system is suitable as an evidence-retrieval and research-support
prototype. It is not ready to make autonomous scientific conclusions or
mission fire-safety recommendations.

## 2. Scope and preservation checks

Audit scope was read-only. The inspected working tree was already dirty on
`feature/research-backend`, with changes across backend services/tests and
untracked research modules, fixtures, and documentation. The existing stash
was preserved:

`stash@{0}: On feature/research-backend: backup local mission intelligence changes`

No source code, datasets, fixtures, databases, frontend files, or Git history
were modified by this audit except for creating this report.

## 3. Existing architecture and actual data flow

### Retrieval flow

1. `/research/search` calls
   `research_summarizer.build_evidence_brief()` and searches eligible local
   NASA passage records using parsed scientific terms and deterministic lexical
   scoring.
2. `/research/online-search` calls
   `nasa_online.search_nasa_online()`, which queries NASA NTRS, preserves
   metadata/abstract scope, and performs one bounded concise-query retry after
   a valid zero-result response.
3. `/research/combined-search` calls
   `research_federation.search_research_with_fallback()`. It assesses local
   passage/source/concept coverage, then adds NASA NTRS metadata when local
   evidence is insufficient. Stable NASA IDs/URLs are used for source merging.
4. `/research/nasa-passage-search` searches extracted NASA document passages.
5. `/research/evidence-search` searches reviewed NASA evidence records.
6. `/bass2/search` searches the raw 17-column BASS-II dataset using supported
   keyword and numeric filters.
7. `/dashboard/mission-brief` calls
   `mission_intelligence.build_mission_intelligence()` and returns
   scenario-term-ranked experimental, simulation, reviewed-context, and BASS-II
   context records.

The FastAPI route inventory is in
[main.py](../backend/main.py):38-238. No route calls
`extract_claims()`, `synthesize_documents()`, `build_mission_research_brief()`,
or `build_review_queue()` directly.

### Processing flow

Extracted NASA text is parsed into page-preserving sections by
[document_parser.py](../backend/services/document_parser.py):124-176 and
`parse_nasa_document()` at lines 392-424. Structured field extraction is
performed by
[evidence_extractor.py](../backend/services/evidence_extractor.py):113-238.
`document_parser` can attach a claim summary through
`claim_summarizer.build_paper_summary()` at lines 541-543.

The shared contract in
[ranking_contract.py](../backend/services/ranking_contract.py):200-456
normalizes provenance, condition matches, evidence scope, source identity,
duplicate grouping, and the explicit unknown independence status. It preserves
original source scores rather than claiming calibrated scientific quality.

## 4. Capability audit

### A. Evidence intelligence

**Status: IMPLEMENTED, with important limitations.**

Verified capabilities:

- `claim_summarizer.extract_claims()` identifies sentence-level claims from
  section-aware documents and retains source document ID, NASA ID, source URL,
  page numbers, section name, evidence type, exact excerpt, uncertainty, and
  verification status. See
  [claim_summarizer.py](../backend/services/claim_summarizer.py):121-221.
- Introduction, background, and references are rejected as eligible claim
  evidence roles rather than silently promoted to findings. See lines 145-160.
- Abstract statements, discussion/conclusion statements, experimental results,
  methods, and limitations receive different claim/evidence types. See lines
  13-38 and 53-119.
- `scientific_findings_verified` remains false throughout extraction and
  review-queue construction.
- `evidence_extractor.extract_structured_findings()` retains original values
  and units, page provenance, section provenance, and explicit
  `not_scientifically_verified` status. It does not convert units or infer
  causality.
- NASA online results explicitly use
  `bibliographic_metadata_and_abstract`, `metadata_retrieved`,
  `not_scientifically_reviewed`, and `scientific_findings_verified=False`.
- BASS-II results are explicitly labeled experimental metadata and warn that
  records alone are not flame-spread results. See
  [bass2_dataset.py](../backend/services/bass2_dataset.py):63-113 and 187-224.

Limitations:

- Unsupported-claim rejection is structural and section-based, not a general
  scientific fact-checker. A sentence in an eligible results section can be
  extracted even when its interpretation is scientifically questionable.
- `MEASUREMENT_TERMS` in `claim_summarizer.py`:39-43 includes broad verbs such
  as `was` and `were`; this can classify ordinary results prose as a result
  without independently proving that a measurement occurred.
- Human review is an in-memory copied queue. It records decisions but does not
  persist them, authenticate reviewers, or change the source record. See
  [human_review.py](../backend/services/human_review.py):16-117.
- There is no API path that exposes the claim schema, evidence-linked paper
  summary, or review queue.

### B. Cross-study scientific analysis

**Status: PARTIALLY IMPLEMENTED / NOT EXPOSED THROUGH API.**

`scientific_synthesis.synthesize_documents()` compares documents only when all
supported condition fields are explicitly populated and their signatures are
equal. Supported fields include material/fuel, gravity, oxygen concentration,
pressure, temperature, flow, and experimental setup. See
[scientific_synthesis.py](../backend/services/scientific_synthesis.py):17-29,
101-132, and 222-368.

Verified behavior:

- Exact comparable groups are separated from non-comparable studies.
- Different conditions are reported as `different_experimental_conditions`.
- Shared observations retain claim-level provenance.
- Different reported measurement values under a comparable signature are
  labeled `potential_disagreement`, not verified contradiction.
- Missing conditions prevent a study from entering a comparable group.
- Synthesis always reports `scientific_findings_verified=False`.
- Duplicate passage independence is not inferred. The ranking contract emits
  `independence_status: "unknown"` and `independent_evidence: None` in
  [ranking_contract.py](../backend/services/ranking_contract.py):375-406.

Gaps:

- The synthesis grouping is based on complete equal extracted condition
  signatures; it does not produce a complete partial-match matrix for every
  pair or quantify which fields prevent comparison.
- It does not establish independent experiments, even when documents differ.
- It does not consume the full federated search response directly; callers
  must construct document objects with compatible sections/findings.
- It is not reachable through a FastAPI route.

### C. Research gap intelligence

**Status: PARTIALLY IMPLEMENTED.**

The synthesis and mission-brief layers emit limited evidence gaps:

- no comparable study group;
- no exact mission-condition match;
- mission conditions not supplied;
- unknown condition fields;
- need for source evidence or qualified review.

The required safety response is implemented exactly in
[mission_research_brief.py](../backend/services/mission_research_brief.py):20-22:

`Insufficient verified evidence to support a mission-specific recommendation.`

However, there is no dedicated research-gap engine. The implementation does
not reliably distinguish an understudied condition from an absent search
result, does not aggregate gaps across the entire NASA/BASS-II corpus, and
does not rank unanswered questions by evidence coverage. It correctly avoids
inventing gaps from retrieval absence alone, but it does not yet provide
systematic gap intelligence.

### D. Scientific insight generation

**Status: PARTIALLY IMPLEMENTED / NOT EXPOSED THROUGH API.**

Evidence-linked observations are generated in mission intelligence and
condition-aware synthesis. Mission intelligence separates experimental
passages from simulation passages and refuses to generate a positive
recommendation unless both classification and review records explicitly mark
the evidence scientifically verified. See
[mission_intelligence.py](../backend/services/mission_intelligence.py):258-303.

The default recommendation is the required insufficiency response when no
verified evidence qualifies. The mission research brief also returns
source-linked observations, interpretations, evidence gaps, uncertainty, and
limitations. See
[mission_research_brief.py](../backend/services/mission_research_brief.py):224-298.

Remaining limitations:

- There is no single insight object that combines claim IDs, agreement/
  disagreement, gap status, limitations, and mission applicability across all
  source types.
- Mission intelligence uses deterministic scenario term overlap; its score is
  explicitly not scientific quality or certainty.
- The positive recommendation branch is guarded by stored verification flags,
  but there is no independent validation that those flags were earned through a
  completed scientific review workflow.
- Abstracts, models, and metadata are not automatically promoted, which is
  safe, but this also means the system cannot produce verified conclusions from
  those sources.

### E. Mission context intelligence

**Status: PARTIALLY IMPLEMENTED / IMPLEMENTED FOR RETRIEVAL SUPPORT.**

The `/dashboard/mission-brief` route accepts mission (`moon`, `mars`, or
`spacecraft`), query, fuel, oxygen concentration, flow, gravity, environment,
and limit. `mission_intelligence.build_mission_intelligence()` separates
experimental and simulation records, includes reviewed and BASS-II context,
preserves excerpts and source links, and returns exact/partial/different/
unknown condition information in the ranking contract where applicable.

`build_mission_research_brief()` provides a richer document-level comparison
with `exact_match`, `partial_match`, `different_conditions`, and
`unknown_conditions`, plus source references and limitations.

The service does not provide operational recommendations, certified limits, or
causal conclusions. This is appropriate for the current evidence state.
The richer mission research brief is not exposed through FastAPI, and
mission intelligence currently uses term-overlap matching rather than the
full condition-aware document synthesis path.

### F. API and architecture integration

**Status: PARTIALLY IMPLEMENTED.**

Publicly integrated:

- local evidence search;
- NASA NTRS search and bounded fallback;
- combined local-first search;
- extracted NASA passage search;
- reviewed evidence search;
- BASS-II summary/search;
- NASA import;
- mission intelligence dashboard.

Partially integrated:

- `research_federation` calls `build_conflict_report()` at
  [research_federation.py](../backend/services/research_federation.py):382-384,
  but the conflict report is assembled from local passages plus online
  metadata, not from claim-level comparable study findings.
- `ranking_contract` is integrated into local passages, NASA online records,
  BASS-II records, and mission intelligence, but it is an additive metadata
  contract rather than a calibrated unified scientific score.
- The online fallback metadata is forwarded into the combined response, but
  claim/synthesis services are not wired into that response.

Disconnected or prototype-like modules:

- `claim_summarizer.py`, `scientific_synthesis.py`,
  `mission_research_brief.py`, and `human_review.py` are imported by tests and
  by document-processing code, but have no dedicated API routes.
- `conflict_reporting.py` is used by federation but has no standalone
  conflict/insight endpoint.
- There are multiple classifier generations (`evidence_classifier_v3.py`,
  `v3_1.py`, `v3_2.py`, `v3_3.py`, `v3_4.py`), while runtime behavior mainly
  consumes classifications already stored in records. This creates a
  maintenance and provenance risk unless the active classifier contract is
  documented and enforced.
- API responses are plain dictionaries without shared Pydantic response
  models. This preserves current flexibility but makes additive schema
  compatibility and validation dependent on tests and convention.

### G. Testing and reliability

**Status: IMPLEMENTED TEST COVERAGE, WITH INTEGRATION GAPS.**

The current suite contains 145 passing tests and covers:

- query parsing and condition mismatch behavior;
- NASA parsing, deduplication, technical errors, and smart fallback;
- local-first federation and source merging;
- ranking provenance, condition statuses, duplicate groups, and unknown
  independence;
- structured findings, section provenance, abstract/result distinction,
  limitations, and unsupported introduction claims;
- claim extraction, provenance, claim-linked summaries, and review queues;
- comparable synthesis, non-comparable conditions, potential disagreements,
  and insufficient evidence;
- mission intelligence separation of experimental/simulation evidence and
  refusal to recommend from unverified evidence;
- conflict reporting for structured comparable records;
- BASS-II schema and numeric filtering.

Representative tests include
[test_claim_summarizer_step5.py](../backend/tests/test_claim_summarizer_step5.py),
[test_scientific_synthesis_step6.py](../backend/tests/test_scientific_synthesis_step6.py),
[test_scientific_validation.py](../backend/tests/test_scientific_validation.py),
[test_ranking_contract.py](../backend/tests/test_ranking_contract.py), and
[test_summarization_end_to_end_step8.py](../backend/tests/test_summarization_end_to_end_step8.py).

Untested or insufficiently tested paths:

- End-to-end FastAPI workflow from search response through claim extraction,
  synthesis, review, and mission brief.
- Public API schemas for claims, synthesis, research gaps, and review queues;
  these routes do not exist.
- Persistence and authorization of review decisions.
- Real NASA online responses through the full combined-to-insight path.
- Cross-source synthesis involving actual NASA metadata, extracted passages,
  reviewed evidence, and BASS-II records together.
- Corpus-level research-gap precision and recall; no expert relevance or gap
  labels are present.
- Scientific validity, causal inference, experimental independence, and
  engineering applicability. The tests verify safeguards and data handling,
  not scientific truth.

## 5. Scientific reliability and safety limitations

The implementation has appropriate conservative safeguards:

- metadata and abstracts remain unverified;
- simulation/model roles are separated from experiments;
- missing and unknown conditions are retained;
- source excerpts and identifiers are preserved;
- stable source IDs, not title similarity, drive duplicate grouping;
- differing conditions are not treated as contradictions;
- no automatic unit conversion, causality, or certified safety limit is
  generated;
- mission recommendations default to the exact insufficiency statement when
  evidence is not explicitly verified.

The principal risks are not unsafe automatic claims but incomplete
integration and heuristic inputs:

1. Lexical overlap remains the primary retrieval/ranking mechanism in local,
   BASS-II, and mission intelligence paths.
2. Stored classification and verification flags are trusted as inputs; the
   platform does not provide a complete authenticated review lifecycle.
3. Claim extraction is conservative but still pattern-based and cannot assess
   whether a claim is scientifically sound.
4. Complete-condition equality is strict, so useful partial comparisons may be
   omitted from synthesis rather than surfaced with a structured explanation.
5. No corpus-level evidence graph links the same claim, passage, experiment,
   document, and dataset record across all source types.

## 6. Overall readiness assessment

| Area | Status |
|---|---|
| Local/NASA/BASS-II retrieval | IMPLEMENTED |
| NASA zero-result fallback | IMPLEMENTED |
| Provenance and duplicate safeguards | IMPLEMENTED |
| Claim-level extraction | IMPLEMENTED |
| Unsupported-claim structural filtering | PARTIALLY IMPLEMENTED |
| Condition-aware cross-study comparison | PARTIALLY IMPLEMENTED |
| Conflict reporting | PARTIALLY IMPLEMENTED |
| Research-gap intelligence | MISSING as a dedicated engine |
| Evidence-linked insight object | PARTIALLY IMPLEMENTED |
| Mission context retrieval | IMPLEMENTED |
| Mission research brief | NOT EXPOSED THROUGH API |
| Claim/synthesis/review API workflow | MISSING |
| Scientific validation and engineering applicability | NOT SCIENTIFICALLY VALIDATED |

**Final status: PARTIALLY READY for research-support retrieval and
provenance-aware extraction; BLOCKED for a complete public Research Insights
Engine and autonomous mission recommendations.**

## 7. Exactly three implementation phases

### Phase 1 — Integrate an evidence-insight API

**Objective:** Expose the existing extractive capabilities through one
backward-compatible, read-only Research Insights endpoint without changing
retrieval semantics.

**Reuse:**

- `research_federation.search_research_with_fallback()`
- `research_summarizer.build_evidence_brief()`
- `nasa_passage_search.search_nasa_passages()`
- `nasa_evidence_search.search_nasa_evidence()`
- `bass2_dataset.search_bass2_records()`
- `claim_summarizer.extract_claims()` and `build_paper_summary()`
- `ranking_contract.py`
- existing `conflict_reporting.py`

**Modify/create:**

- Add a dedicated service facade, for example
  `backend/services/research_insights.py`.
- Add a versioned request/response schema module using the repository’s chosen
  validation convention.
- Add one API route in `backend/main.py`; do not change existing response
  contracts.

**Capabilities:**

- Accept a query and optional source/limit controls.
- Return local and online evidence with claim IDs, exact excerpts, stable source
  identity, evidence scope, condition status, and verification labels.
- Preserve fallback metadata and explicit insufficient-evidence notices.
- Keep metadata, abstracts, simulations, and experimental passages distinct.

**Dependency:** None beyond the existing services.

**Test plan:** API contract tests, empty/error cases, real-shaped NASA metadata
fixtures, provenance round trips, duplicate grouping, and regression tests for
all existing routes.

**Risks and limitations:** This phase still cannot prove scientific truth.
The new facade must avoid presenting lexical relevance as evidence strength.

**Expected deliverable:** A public, deterministic, source-linked Research
Insights response assembled from existing capabilities.

### Phase 2 — Build condition-aware comparison and gap intelligence

**Objective:** Turn extracted claims and structured fields into an explicit
cross-study comparison and evidence-gap report.

**Reuse:**

- `scientific_synthesis.synthesize_documents()`
- `evidence_extractor.extract_structured_findings()`
- `claim_summarizer.extract_claims()`
- `mission_research_brief.py`
- `conflict_reporting.py`
- `ranking_contract.condition_match()`

**Modify/create:**

- Extend `scientific_synthesis.py` to emit a complete pairwise condition
  matrix with exact, partial, mismatch, and unknown statuses without relaxing
  safety rules.
- Add a dedicated `research_gap_analysis.py` service.
- Add schemas and an API route for comparison/gap output.

**Capabilities:**

- Compare material, gravity, oxygen, pressure, temperature, flow, and setup.
- Distinguish shared observations, potential disagreements, and
  non-comparable records.
- Track missing quantitative measurements and unresolved conditions only when
  source coverage supports the statement.
- Preserve unknown rather than infer independence or causality.
- Link every gap and comparison statement to source claims or explicitly state
  that no supporting claim exists.

**Dependency:** Phase 1’s normalized insight document/claim contract.

**Test plan:** Pairwise exact/partial/mismatch/unknown fixtures, same-document
  passage cases, distinct-document cases with unknown independence, metadata
  versus experimental records, BASS-II contextual records, and no-result
  behavior.

**Risks and limitations:** A gap report is a coverage analysis, not proof that
  a scientific question has never been studied. Expert labels remain required
  for validity evaluation.

**Expected deliverable:** A public, provenance-linked comparison and gap report
  that is explicit about evidence limitations.

### Phase 3 — Add review-backed mission insight orchestration

**Objective:** Integrate human review, mission matching, and safety-gated
  insight generation into a persistent, auditable workflow.

**Reuse:**

- `human_review.py`
- `mission_research_brief.py`
- `mission_intelligence.py`
- Phase 1 insight facade
- Phase 2 comparison/gap service

**Modify/create:**

- Add a persistence layer for review queues and decisions without modifying
  source datasets.
- Add authenticated review/update API routes and explicit reviewer audit
  fields.
- Add a mission-insight orchestration service that consumes only reviewed,
  provenance-complete claims for any qualified recommendation branch.

**Capabilities:**

- Persist pending, accepted, rejected, corrected, and insufficient-evidence
  decisions.
- Require reviewer identity and preserve immutable source excerpts/version
  references.
- Produce mission-specific exact/partial/different/unknown matches.
- Return the exact insufficiency response whenever no reviewed evidence
  supports a recommendation.
- Keep recommendations qualified and separate from scientific findings,
  interpretations, and engineering decisions.

**Dependency:** Phases 1 and 2 normalized schemas and claim/gap references.

**Test plan:** End-to-end API tests, persistence/reload tests, reviewer
  authorization tests, rejected-claim exclusion, stale-source/version tests,
  mission-condition mismatch tests, and regression tests for all existing
  search endpoints.

**Risks and limitations:** Human review does not itself establish universal
  scientific validity. Engineering recommendations still require domain
  experts, mission certification processes, and independent validation.

**Expected deliverable:** An auditable, review-gated Research Insights Engine
  with mission-context support and safe insufficient-evidence behavior.

