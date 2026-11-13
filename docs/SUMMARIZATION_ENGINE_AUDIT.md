# FlameGuard AI Summarization Engine Audit

## Audit status

**Audit-only task completed. No code, dataset, benchmark fixture, NASA record,
or stash was modified during this audit.**

This report describes the implementation currently present on the
`feature/research-backend` branch. The repository already contained unrelated
working-tree changes from the preceding research-search work; those changes
were preserved.

The assessment uses these capability labels:

- **Fully implemented:** the capability exists with traceable behavior and
  adequate targeted tests for its current scope.
- **Partially implemented:** a working subset exists, but important cases or
  scientific guarantees are absent.
- **Missing:** no implementation was found.
- **Implemented but not adequately tested:** implementation exists, but the
  current tests do not establish the required behavior.

The labels describe software capability, not scientific validity.

## 1. Architecture overview

### Retrieval and federation

- [nasa_online.py](../backend/services/nasa_online.py) calls the NASA NTRS
  citation-search API. It normalizes title, abstract, NASA ID, citation URL,
  authors, publication metadata, availability status, and retrieval time.
  Returned records are explicitly marked
  `bibliographic_metadata_and_abstract`, `full_text_retrieved=false`, and
  `scientific_findings_verified=false`.
- [research_federation.py](../backend/services/research_federation.py)
  performs local-first retrieval through the summarizer, evaluates local
  sufficiency, and optionally merges NASA NTRS metadata. It deduplicates by
  NASA ID or canonical URL and retains local page provenance.
- [nasa_passage_search.py](../backend/services/nasa_passage_search.py) searches
  the prebuilt extracted NASA passage collection while preserving page,
  classification, evidence type, review status, and citation URL.
- [nasa_evidence_search.py](../backend/services/nasa_evidence_search.py)
  searches a smaller reviewed-evidence collection. It exposes the existing
  review and verification flags but uses simple token overlap.

### Full-text acquisition and document processing

- [nasa_documents.py](../backend/services/nasa_documents.py) queries NASA's
  download manifest, distinguishes converted text and PDF links, validates
  NASA-hosted download URLs, enforces size/content-type limits, and reports
  unavailable downloads explicitly.
- [nasa_ingestion.py](../backend/services/nasa_ingestion.py) is the explicit
  import path for one NASA PDF. It retrieves citation metadata, downloads the
  PDF, audits identity against the NASA title, extracts pages, extracts
  candidate passages, classifies them, and writes a supplemental collection
  pending manual review. It does not modify the primary audited dataset.
- [document_parser.py](../backend/services/document_parser.py) reads existing
  converted NASA text, heuristically splits presentation-like text into
  numeric blocks, extracts PDF text page by page with PyMuPDF, and performs a
  title/identity audit. It preserves PDF page numbers and reports pages with
  no extracted text.
- [evidence_extractor.py](../backend/services/evidence_extractor.py) emits
  title, abstract, supplied structured text, or PDF-page sentence passages
  with source-field, page, URL, and heuristic context metadata.
- [evidence_classifier_v3*.py](../backend/services/evidence_classifier_v3_4.py)
  assigns candidate evidence roles and modalities. These are classification
  labels, not independent scientific verification.

### Summarization and mission output

- [research_summarizer.py](../backend/services/research_summarizer.py) is an
  extractive evidence-brief service. It searches eligible passage records with
  deterministic scientific lexical/entity scoring, applies source
  diversification, preserves exact excerpts and provenance, and reports
  evidence modality, role, review, and verification flags. It does not
  generate a prose scientific summary or infer findings.
- [mission_intelligence.py](../backend/services/mission_intelligence.py)
  builds mission-scoped evidence buckets for experimental passages,
  simulations, reviewed context, and BASS-II metadata. It uses scenario term
  overlap and returns the fixed insufficient-evidence recommendation unless a
  record is explicitly marked scientifically verified.
- There is no `mission_research.py` file in the current repository. Mission
  brief behavior is implemented by `mission_intelligence.py` and exposed by
  `/dashboard/mission-brief`.
- [query_understanding.py](../backend/services/query_understanding.py)
  supplies scientific normalization, material/condition/phenomenon/environment
  intent, and explainable scoring to retrieval. It is not a document
  summarizer.

### API surfaces

[main.py](../backend/main.py) exposes:

- `/research/search` — local extractive evidence brief;
- `/research/online-search` — NASA NTRS metadata/abstract search;
- `/research/combined-search` — local-first search with NASA fallback;
- `/research/import/{nasa_id}` — explicit PDF import into supplemental data;
- `/research/evidence-search` — reviewed-evidence search;
- `/research/nasa-passage-search` — extracted page-passage search;
- `/dashboard/mission-brief` — mission-scoped evidence and guarded output; and
- BASS-II summary/search endpoints.

## 2. Capability audit

### A. NASA research document retrieval

**Assessment: Partially implemented.**

What works:

- Live NTRS search retrieves actual NASA catalogue records with titles,
  abstracts, NASA IDs, citation URLs, metadata, availability indicators, and
  retrieval timestamps.
- The download manifest path distinguishes converted-text and PDF entries.
- The explicit import path can retrieve a NASA PDF when an official valid
  download is listed.
- URL host/path validation, response limits, content-type checks, HTML
  rejection, and explicit error statuses are present.
- Missing PDFs produce `pdf_unavailable`/metadata-only behavior instead of
  pretending that full text was retrieved.

Limitations:

- `/research/online-search` and NASA fallback do not retrieve paper content;
  they return metadata and abstract text only.
- `document_available` indicates NASA dissemination metadata, not successful
  local full-text retrieval.
- The normalized online result does not expose the concrete PDF/text download
  URLs returned by the NASA download manifest.
- Restricted, unavailable, malformed, or failed downloads are reported, but
  there is no durable availability taxonomy or retry/provenance record for
  each attempted document.
- PDF import is an explicit side path and is not automatically connected to
  live fallback results.

**Sub-capability status:**

| Capability | Status |
|---|---|
| NASA metadata/abstract retrieval | Fully implemented for current scope |
| Actual PDF retrieval | Partially implemented |
| Converted full-text retrieval | Partially implemented |
| PDF/text availability distinction | Partially implemented |
| Restricted/unavailable document handling | Partially implemented |

### B. Document extraction

**Assessment: Partially implemented.**

What works:

- Converted NASA text can be loaded and searched.
- PDFs are extracted page by page with PyMuPDF.
- Page number, character count, word count, extraction status, source URL,
  page count, and empty-page counts are retained.
- PDF identity is checked against NASA metadata before ingestion.
- Empty PDF pages are explicitly represented as `no_text_extracted`.
- Text extraction failures, encrypted PDFs, empty PDFs, missing files, and
  malformed input return explicit errors.

Limitations:

- There is no OCR pipeline for scanned/image-only PDFs.
- A PDF with no extracted text is not classified specifically as scanned,
  image-only, or OCR-required; it is only represented as an empty page.
- There is no robust table, figure, footnote, multi-column, or reading-order
  reconstruction.
- Presentation block splitting uses a fragile heuristic and calls blocks
  “slides” based on standalone numeric lines.
- Extraction outputs are not automatically promoted into the primary research
  store; ingestion is required.

**Sub-capability status:**

| Capability | Status |
|---|---|
| Page-preserving text extraction | Fully implemented for text PDFs |
| Missing/malformed PDF errors | Partially implemented |
| Scanned PDF handling | Missing |
| Section reconstruction | Missing/heuristic only |
| Table/figure-aware extraction | Missing |
| Honest full-text vs abstract labeling | Fully implemented in current paths |

### C. Section-aware extraction

**Assessment: Missing for scientific sections; partially implemented for
heuristic topics.**

The parser recognizes candidate keywords for `methods`, `results`,
`limitations`, combustion, oxygen, microgravity, and fire safety. Page
context also recognizes a small set of phrases such as “completed content” and
“future investigations.” These labels are explicitly heuristic.

There is no structured section model for:

- Abstract;
- Introduction;
- Methodology;
- Experimental setup;
- Results;
- Discussion;
- Conclusion; or
- Limitations.

The current page extractor can attach a passage to a PDF page, but not
reliably to a document section. Heading detection is not normalized across
numbering, capitalization, headers/footers, or multi-page sections.

**Assessment:** Partially implemented as candidate topic/page context, missing
as section-aware scientific extraction.

### D. Scientific finding extraction

**Assessment: Partially implemented, with substantial missing structure.**

What works:

- Candidate passages can be extracted from titles, abstracts, supplied
  findings, or PDF page text.
- Existing classifications distinguish roles such as experimental result,
  observation, simulation, limitation, background, and reviewed context.
- Exact source text, NASA ID/source ID, citation URL, and PDF page are retained
  where available.
- The store contains condition fields for reviewed evidence and BASS-II raw
  oxygen/material/flow fields.
- The system consistently keeps `scientific_findings_verified=false` unless
  source and review flags explicitly support verification.

What is missing or unsafe for a summarization engine:

- No general structured extractor maps passages into material/fuel, gravity,
  oxygen concentration, pressure, flow, environment, measurement, units,
  observation, finding, and limitation fields.
- Existing `conditions` are often `None` for NASA passage records.
- Numeric text is not systematically normalized with measurement type,
  initial/final status, uncertainty, or unit provenance.
- A classifier role is not equivalent to a verified finding.
- Extracted sentences may split tables, bullets, headings, or context and are
  not claim-complete.
- Missing parameters are preserved as missing, but there is no uniform
  “unknown/not reported/not applicable” schema across all sources.

**Assessment:** Candidate evidence extraction is implemented; scientific
finding extraction is only partial and not sufficient for autonomous
scientific summarization.

### E. Evidence-linked summarization

**Assessment: Partially implemented.**

Strong existing behavior:

- `build_evidence_brief()` returns exact source excerpts, source title,
  source ID, citation URL, PDF page, record ID, evidence role/modality,
  review status, classification version, and verification state.
- NASA metadata/abstract results are explicitly separated from extracted
  passages.
- The output includes ranking explanations and limitations.
- Mission output preserves source excerpts and URLs and refuses a
  mission-specific recommendation without explicit verified evidence.

Missing behavior:

- The engine produces a ranked evidence list and overview, not a generated
  claim-by-claim summary.
- There is no stable claim ID linked to one or more exact passages.
- There is no citation object that records source field plus section plus page
  for every generated claim because generated claims do not yet exist.
- Abstract sentences and full-text passages are distinguished at the record
  level, but there is no unified evidence-scope contract across every API
  response.
- There is no automated completeness check that every summary statement has
  at least one supporting passage and no unsupported quantitative assertion.

**Assessment:** Traceable extractive retrieval is implemented; evidence-linked
  summarization is not complete.

### F. Multi-paper summarization

**Assessment: Partially implemented, not adequately tested for summaries.**

Existing support:

- Local and NASA records can be merged by source identity.
- Source-level diversification reduces repeated passages in display results.
- [conflict_reporting.py](../backend/services/conflict_reporting.py) can
  identify comparable structured disagreements and avoids inventing conflicts
  from unstructured passages.
- Mission intelligence keeps experimental and simulation evidence separate.

Limitations:

- There is no multi-paper synthesis that produces a comparison of findings.
- Conflict detection is a separate structured utility, not integrated into a
  summarization result.
- Comparability requires structured fields, but most NASA passage records do
  not carry structured conditions.
- There is no cross-paper normalization of material, oxygen, gravity, flow,
  measurement, uncertainty, or experimental protocol.
- Existing tests cover conflict utility behavior, but not end-to-end
  multi-paper summary generation because that feature is absent.

**Assessment:** Source federation and limited conflict reporting are present;
multi-paper scientific summarization is missing.

### G. Mission research brief

**Assessment: Partially implemented.**

What works:

- `/dashboard/mission-brief` accepts mission, query, fuel, oxygen,
  flow, gravity, and environment inputs.
- Experimental passages, simulations, reviewed context, and BASS-II metadata
  are separated.
- Supplied conditions are preserved and missing values are not defaulted.
- Source IDs, titles, URLs, excerpts, review states, and evidence modalities
  are retained.
- The fixed insufficient-evidence recommendation is returned when no
  explicitly verified experimental record is available.
- Output includes safety-boundary language and requires qualified review.

Limitations:

- Ranking is scenario term overlap, not condition compatibility or scientific
  applicability matching.
- Supplied mission conditions are preserved but not systematically compared
  with record conditions before inclusion.
- The brief does not synthesize findings, identify comparable conflicts, or
  produce a sectioned mission research summary.
- Generic mission terms can retrieve contextual evidence that is not actually
  mission-specific; the output labels this as requiring review but does not
  fully filter it.
- BASS-II records are included as context without a shared claim/finding
  schema.

**Assessment:** Safe evidence-oriented mission briefing exists; a
condition-aware mission summarization engine does not.

## 3. Existing tests and test-quality audit

### Test inventory

The current backend suite contains **77 passing tests**:

- `test_research_summarizer.py` — 11 tests for candidate retrieval,
  background exclusion, experiment/simulation separation, provenance,
  verification flags, source diversification, validation, and supplemental
  passages.
- `test_nasa_ingestion.py` — 5 tests for mocked PDF import, provenance,
  identity failure, duplicate prevention, primary-dataset collision, and
  invalid IDs.
- `test_nasa_online.py` — 3 tests for metadata normalization, duplicate
  removal, and explicit HTTP failure.
- `test_research_federation.py` — 8 tests for local sufficiency, fallback,
  source merging, metadata-only status, online failure, limits, and oxygen
  measurement fallback.
- `test_research_remaining_work.py` — 13 tests for fallback edge cases,
  provenance retention, BASS-II filters, and validation.
- `test_mission_intelligence.py` — 6 tests for evidence separation,
  background exclusion, verification safeguards, invalid mission, and query
  validation.
- `test_scientific_validation.py` — 10 tests for conditions, insufficient
  evidence, conflicts, mismatch safeguards, metadata-only evidence, and
  provenance.
- `test_research_intelligence_store.py` — 9 tests for store counts,
  record identity, source/audit preservation, BASS-II preservation, and
  verification invariants.
- Query understanding, conflict reporting, and benchmark tests cover the
  search/ranking layer rather than document summarization.

### Test strengths

- Most tests use synthetic records and temporary stores, making them
  deterministic and safe.
- NASA HTTP calls, PDF downloads, extraction, classification, and citation
  metadata are mocked in ingestion tests.
- Tests explicitly assert that metadata/abstract records do not become
  verified findings.
- Page numbers, URLs, exact excerpts, source IDs, review flags, and duplicate
  handling are tested.
- Dataset integrity and record-count invariants are tested against the
  checked-in processed data.

### Test gaps and edge cases

The suite does not adequately establish:

- real malformed, encrypted, image-only, OCR, multi-column, table-heavy, or
  corrupted PDFs;
- section-heading extraction across realistic paper layouts;
- page-to-section provenance;
- abstract-only versus full-text behavior through every API endpoint;
- download-manifest variants, redirects, restricted files, invalid MIME
  responses, truncated streams, and content-length mismatches;
- claim-level summary citation completeness;
- extraction of material, gravity, oxygen, pressure, flow, measurements,
  units, uncertainty, initial/final values, findings, and limitations;
- multi-paper synthesis or condition-comparable conflict presentation;
- mission-condition compatibility filtering;
- property-based or fixture-based tests for scientific number/unit parsing;
- regression tests for the five existing real PDFs beyond mocked extraction
  paths.

The tests are therefore strong for the current provenance and safety
invariants, but they do not prove that a scientific summarization engine can
produce accurate structured findings.

### Test evidence result

Command executed with the existing virtual environment:

```text
.\.venv\Scripts\python.exe -m unittest discover -s backend\tests -p "test_*.py"
Ran 77 tests in 1.359s
OK
```

No dependencies were installed. No live NASA retrieval or PDF download was
performed as part of this audit.

## 4. Scientific integrity risk assessment

### Controlled risks

- NASA online metadata and abstracts are labeled as unverified.
- PDF extraction and imported passages remain pending manual review.
- Verification requires explicit record and review flags.
- Exact excerpts and source links are preserved.
- Mission recommendations default to insufficient verified evidence.
- The system does not automatically download full-text PDFs during ordinary
  search fallback.

### Remaining risks

1. **Section/context loss:** sentence splitting can detach a result from its
   heading, table, caption, method, or limitation.
2. **Claim overreach:** a candidate passage or classifier role can be mistaken
   by a downstream consumer for a complete scientific finding.
3. **Parameter ambiguity:** numeric oxygen, flow, pressure, or spread values
   are not consistently typed or associated with initial/final state and
   uncertainty.
4. **Applicability leakage:** mission term overlap can surface records with
   incompatible materials or conditions.
5. **Comparability failure:** multi-paper differences cannot be safely
   synthesized without normalized conditions and measurement definitions.
6. **Extraction failure:** scanned PDFs and complex layouts may yield partial
   or empty text without an OCR-specific status.
7. **Evidence-scope inconsistency:** different endpoints expose related but
   not identical names for full-text, abstract, review, and verification
   state.

No current output should be treated as a certified spacecraft safety decision.
Qualified engineering and scientific review remain necessary.

## 5. Prioritized Step 2 implementation roadmap

The roadmap deliberately starts with schemas and provenance before generating
any prose summary. Each step is independently testable and should be accepted
before the next step begins.

### Step 1 — Establish a unified document/evidence scope contract

**Priority:** Critical; prerequisite for every later step.

1. **Exact files involved**
   - New shared schema/helper module under `backend/services/`.
   - [nasa_online.py](../backend/services/nasa_online.py)
   - [nasa_documents.py](../backend/services/nasa_documents.py)
   - [document_parser.py](../backend/services/document_parser.py)
   - [evidence_extractor.py](../backend/services/evidence_extractor.py)
   - [research_summarizer.py](../backend/services/research_summarizer.py)
   - Related API tests.
2. **Existing functionality**  
   Each path independently reports metadata, abstract, extracted text, review,
   and verification fields.
3. **Defect/missing capability**  
   Scope fields are not a single versioned contract and concrete document
   availability/download provenance is not consistently carried through all
   outputs.
4. **Minimal correction**  
   Define a versioned evidence-scope object with source identity, citation URL,
   content scope (`metadata`, `abstract`, `converted_full_text`,
   `extracted_pdf_text`), availability status, retrieval timestamp, page,
   section, review status, and scientific verification status. Map existing
   outputs into it without changing search ranking.
5. **Unit tests required**  
   Scope mapping for metadata-only, abstract-only, converted text, extracted
   PDF, failed download, and missing page/section.
6. **Integration tests required**  
   NASA online search, PDF import, passage search, federation, and API
   responses preserve the same scope values.
7. **Expected output**  
   Every evidence item states exactly what source content was available and
   what was not verified.
8. **Acceptance criteria**  
   No endpoint can label an abstract-only record as full text; no page or
   section is invented; all existing 77 tests remain green.

### Step 2 — Harden document acquisition and extraction diagnostics

**Priority:** Critical.

1. **Exact files involved**
   - [nasa_documents.py](../backend/services/nasa_documents.py)
   - [document_parser.py](../backend/services/document_parser.py)
   - [nasa_ingestion.py](../backend/services/nasa_ingestion.py)
   - New/updated extraction fixtures and tests.
2. **Existing functionality**  
   Official NASA PDF/text downloads, size/content checks, page extraction,
   identity audit, and explicit failure statuses exist.
3. **Defect/missing capability**  
   Scanned/image-only pages, malformed layout, OCR need, and partial extraction
   are not classified with enough precision.
4. **Minimal correction**  
   Add extraction diagnostics and explicit statuses such as
   `text_extracted`, `empty_page`, `ocr_required`, `partial_extraction`,
   `encrypted`, and `malformed`. Do not add OCR until an approved dependency
   and policy exist.
5. **Unit tests required**  
   Empty, encrypted, malformed, zero-page, text, mixed text/image, oversized,
   wrong-content-type, HTML, and truncated-download cases.
6. **Integration tests required**  
   Mocked NASA manifest/download through PDF import, identity audit, and page
   extraction.
7. **Expected output**  
   Honest extraction diagnostics with no false claim of complete full-text
   access.
8. **Acceptance criteria**  
   Every page/document has an explicit extraction status; partial or scanned
   documents cannot be promoted as complete text.

### Step 3 — Add section-aware, page-linked document structure

**Priority:** High.

1. **Exact files involved**
   - [document_parser.py](../backend/services/document_parser.py)
   - [evidence_extractor.py](../backend/services/evidence_extractor.py)
   - [nasa_ingestion.py](../backend/services/nasa_ingestion.py)
   - New section parser module if separation is cleaner.
2. **Existing functionality**  
   Page text and heuristic topic/page context are available.
3. **Defect/missing capability**  
   No reliable abstract/introduction/methods/setup/results/discussion/
   conclusion/limitations model exists.
4. **Minimal correction**  
   Add conservative heading detection with `section_name`,
   `section_detection_method`, confidence/status, and page span. Preserve
   `unknown` when headings cannot be established.
5. **Unit tests required**  
   Numbered headings, capitalization variants, multi-page sections, repeated
   headers/footers, missing headings, and presentation text.
6. **Integration tests required**  
   Parse the five existing extracted PDFs without modifying them and verify
   page/section provenance.
7. **Expected output**  
   Candidate passages carry page and section only when supported by extracted
   text.
8. **Acceptance criteria**  
   No passage receives a fabricated section; unknown sections remain explicit.

### Step 4 — Build structured scientific finding extraction

**Priority:** High.

1. **Exact files involved**
   - [evidence_extractor.py](../backend/services/evidence_extractor.py)
   - [research_intelligence_data.py](../backend/services/research_intelligence_data.py)
   - [evidence_classifier_v3_4.py](../backend/services/evidence_classifier_v3_4.py)
   - New finding-extraction module and focused tests.
2. **Existing functionality**  
   Candidate sentences and evidence roles are extracted, while BASS-II and
   reviewed evidence already contain some structured conditions.
3. **Defect/missing capability**  
   NASA passages lack a uniform structured finding/condition schema.
4. **Minimal correction**  
   Extract only explicitly supported fields: material, gravity, oxygen,
   pressure, flow, environment, measurement, value, unit, observation,
   finding, and limitation. Store raw text spans and an
   `unknown/not_reported` state; never infer absent conditions.
5. **Unit tests required**  
   Numeric units, ranges, percentages, initial/final oxygen, material aliases,
   gravity terms, uncertainty, negation, and ambiguous values.
6. **Integration tests required**  
   Existing NASA PDF passages, reviewed evidence, and BASS-II records must
   retain raw values and provenance.
7. **Expected output**  
   Structured candidate findings with exact supporting spans and explicit
   uncertainty/absence.
8. **Acceptance criteria**  
   Every extracted value links to source text and page; no threshold or causal
   statement is created from keyword overlap alone.

### Step 5 — Implement claim-level evidence-linked summaries

**Priority:** High; depends on Steps 1–4.

1. **Exact files involved**
   - [research_summarizer.py](../backend/services/research_summarizer.py)
   - New summary/claim model module.
   - [main.py](../backend/main.py)
   - Summarizer/API tests.
2. **Existing functionality**  
   Extractive evidence briefs provide ranked passages and exact excerpts.
3. **Defect/missing capability**  
   There is no generated claim object or completeness check.
4. **Minimal correction**  
   Add an extractive, template-based summary format first. Each claim must
   include claim ID, wording limited to source-supported text, source IDs,
   citation URL, page, section when known, evidence scope, and review status.
5. **Unit tests required**  
   Claim citation completeness, abstract-only wording restrictions, missing
   parameter statements, duplicate-source handling, and no-evidence output.
6. **Integration tests required**  
   Local-only, NASA fallback, imported PDF, and mixed evidence searches.
7. **Expected output**  
   A concise summary that distinguishes “reported by source” from
   “verified/reviewed” and exposes unsupported/missing fields.
8. **Acceptance criteria**  
   Every claim has at least one exact source span; unsupported numerical
   conclusions are rejected; output retains existing provenance.

### Step 6 — Add condition-aware multi-paper comparison

**Priority:** High.

1. **Exact files involved**
   - [conflict_reporting.py](../backend/services/conflict_reporting.py)
   - [research_summarizer.py](../backend/services/research_summarizer.py)
   - [mission_intelligence.py](../backend/services/mission_intelligence.py)
   - New comparison module/tests.
2. **Existing functionality**  
   Structured conflict reporting and source federation exist independently.
3. **Defect/missing capability**  
   They are not integrated into a multi-paper summary, and most passages lack
   normalized comparable conditions.
4. **Minimal correction**  
   Compare only records with compatible structured material, gravity,
   environment, measurement, and units. Otherwise report “not comparable”
   with the missing dimensions and preserve each source separately.
5. **Unit tests required**  
   Comparable agreement, comparable disagreement, incompatible material,
   incompatible gravity, missing conditions, and mixed evidence modalities.
6. **Integration tests required**  
   Multi-source local/NASA search and mission brief comparison.
7. **Expected output**  
   Source-attributed comparison with explicit agreement, disagreement, or
   non-comparability.
8. **Acceptance criteria**  
   No cross-paper conflict or consensus is reported without comparable
   conditions and measurements.

### Step 7 — Upgrade the mission research brief

**Priority:** High after structured findings exist.

1. **Exact files involved**
   - [mission_intelligence.py](../backend/services/mission_intelligence.py)
   - [main.py](../backend/main.py)
   - New mission-brief tests and API tests.
2. **Existing functionality**  
   Mission parameters are accepted and preserved; evidence types are
   separated; unsafe recommendations are guarded.
3. **Defect/missing capability**  
   Scenario term overlap is not condition-aware and does not produce a
   sectioned evidence summary.
4. **Minimal correction**  
   Match supplied mission conditions against structured findings, expose
   compatibility per field, preserve unknowns, integrate the claim-level
   summary, and keep the insufficient-evidence fallback unchanged.
5. **Unit tests required**  
   Compatible/incompatible material, gravity, oxygen, flow, and environment;
   absent conditions; verified versus unverified evidence.
6. **Integration tests required**  
   `/dashboard/mission-brief` with local, NASA metadata-only, imported PDF,
   reviewed evidence, and BASS-II context.
7. **Expected output**  
   A mission research brief with evidence-linked observations, compatibility
   gaps, limitations, and no unsupported recommendation.
8. **Acceptance criteria**  
   The endpoint never upgrades metadata/abstract or unverified passages into a
   mission-specific safety recommendation.

### Step 8 — Add document-level regression and human-review fixtures

**Priority:** Medium; required before declaring the engine ready.

1. **Exact files involved**
   - `backend/tests/fixtures/` new document fixtures only; existing fixtures
     remain unchanged.
   - New tests under `backend/tests/`.
   - Documentation under `docs/`.
2. **Existing functionality**  
   Current tests are predominantly synthetic and mocked.
3. **Defect/missing capability**  
   There is no repeatable document-level regression suite for section,
   extraction, finding, and claim provenance.
4. **Minimal correction**  
   Add small redacted/text fixtures and expected structured outputs; add a
   human-review queue for provisional findings without fabricating labels.
5. **Unit tests required**  
   Fixture-level golden tests and invariant checks.
6. **Integration tests required**  
   End-to-end document-to-summary tests with no live NASA dependency.
7. **Expected output**  
   Reproducible regression evidence for every supported document state.
8. **Acceptance criteria**  
   Full suite passes; all summary claims are traceable; no scientific quality
   metric is reported without expert labels.

## 6. Proposed future file changes

No future implementation files were changed in this audit. The likely future
change surface is:

- [research_summarizer.py](../backend/services/research_summarizer.py)
- [document_parser.py](../backend/services/document_parser.py)
- [evidence_extractor.py](../backend/services/evidence_extractor.py)
- [nasa_documents.py](../backend/services/nasa_documents.py)
- [nasa_ingestion.py](../backend/services/nasa_ingestion.py)
- [mission_intelligence.py](../backend/services/mission_intelligence.py)
- [conflict_reporting.py](../backend/services/conflict_reporting.py)
- [research_intelligence_data.py](../backend/services/research_intelligence_data.py)
- [main.py](../backend/main.py)
- New shared evidence-scope, section, finding, and claim modules as needed.
- New focused tests and non-destructive document fixtures.

The following must remain unchanged unless a later approved step demonstrates
a direct dependency defect:

- NASA and BASS-II source datasets;
- existing benchmark fixtures;
- primary research records;
- the existing stash; and
- search ranking behavior unrelated to summarization.

## 7. Final audit conclusion

The current system is a reliable **evidence retrieval and provenance
prototype**, not yet a complete scientific summarization engine.

### Fully implemented or adequately covered

- NASA metadata/abstract discovery with explicit unverified scope.
- Local-first federation and source identity merging.
- Page-preserving extraction for available text PDFs.
- PDF identity checks and explicit basic download failures.
- Extractive evidence briefs with exact excerpts and provenance.
- Experimental/simulation/background separation.
- Guarded mission recommendations.
- Existing provenance and scientific-integrity invariants, as shown by
  77 passing tests.

### Partially implemented

- Actual NASA full-text acquisition and import.
- PDF failure/scanned-document handling.
- Structured evidence roles and page context.
- Mission-specific evidence selection.
- Multi-source conflict support.

### Missing

- Reliable section-aware extraction.
- Structured scientific finding extraction across the requested fields.
- Claim-level generated summaries with citation completeness enforcement.
- Condition-aware multi-paper synthesis.
- End-to-end section/finding/summary regression fixtures.

### Audit recommendation

Proceed to Step 2 only after approval, beginning with the unified
evidence-scope contract. That dependency prevents later summarization work
from conflating metadata, abstracts, extracted text, and reviewed findings.

