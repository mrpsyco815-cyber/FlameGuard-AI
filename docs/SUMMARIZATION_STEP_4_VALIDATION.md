# Summarization Engine Step 4 Validation

## Status

**PASS for the scoped structured scientific finding extraction layer.**

This step adds conservative, source-linked candidate extraction on top of the
page-preserving and section-aware outputs from Steps 2 and 3. It does not
perform scientific verification, unit conversion, causal inference, claim
generation, or multi-paper synthesis.

No live NASA downloads were performed.

## Exact files changed

### Implementation

- [evidence_extractor.py](../backend/services/evidence_extractor.py)
  - Added `extract_structured_findings()`.
  - Added conservative patterns for material/fuel, gravity, oxygen,
    pressure, temperature, flow, and explicitly labeled measurements.
  - Added section-aware evidence typing.
  - Added exact excerpt, page, source, section, method, verification, and
    uncertainty provenance.
  - Added explicit missing-field states.
- [document_parser.py](../backend/services/document_parser.py)
  - Adds `structured_findings` to the existing PDF extraction result.
  - Does not change the existing `pages` or extraction diagnostics.
- [nasa_ingestion.py](../backend/services/nasa_ingestion.py)
  - Preserves structured findings in the imported document entry.
  - Does not overwrite primary or existing records.

### Tests

- [test_structured_findings_step4.py](../backend/tests/test_structured_findings_step4.py)
  - Added focused synthetic-document tests for fields, provenance,
    classification, uncertainty, missing values, and rejection behavior.

### Documentation

- [SUMMARIZATION_STEP_4_VALIDATION.md](./SUMMARIZATION_STEP_4_VALIDATION.md)

No NASA/BASS-II dataset, benchmark fixture, or existing research record was
modified.

## Structured finding schema

`extract_structured_findings()` returns:

```text
schema_version
source
fields
measurements
scientific_observations
scientific_findings
limitations
uncertainty
evidence
scientific_findings_verified
extraction_note
```

### Source object

```text
source.document_id
source.nasa_id
source.source_url
```

Missing source identifiers remain `null`; they are not fabricated.

### Structured fields

The following fields use the same shape:

```text
{
  "status": "reported" | "not_reported",
  "values": [...]
}
```

Supported field names:

- `material_fuel`
- `gravity_condition`
- `oxygen_concentration`
- `pressure`
- `temperature`
- `flow_condition`
- `measurement`

Each reported value contains:

```text
field
value
raw_value
unit
exact_supporting_text
source_document_id
nasa_id
source_url
page_numbers
section_name
evidence_type
extraction_method
verification_status
uncertain
```

Values retain the source wording and units. No unit conversion is performed.
For example, `21 percent`, `100 kPa`, `300 K`, and `10 cm/s` remain in their
reported forms.

### Measurements

`measurements` contains only evidence items with an explicitly detected
measurement value and unit. A numeric value without an explicit supported
measurement context is not promoted into this list.

The extractor requires explicit labels for pressure and temperature. For
example:

```text
ambient pressure 100 kPa
temperature 300 K
```

An unlabeled `100 kPa` or `300 K` is not treated as pressure or temperature.
This prevents unsupported field assignment.

### Observations and findings

- `scientific_observations` is populated only from `results` or
  `results_and_discussion` section text.
- `scientific_findings` is populated only from `discussion` or `conclusion`
  section text.
- Discussion/conclusion items are source statements and are not treated as
  direct measurements.
- Conclusion-derived items are marked uncertain.
- Abstract statements remain typed as `abstract_statement` and do not become
  experimental observations.
- Introduction or unclassified text does not generate observations/findings
  merely because it contains scientific keywords.

### Limitations and uncertainty

- `limitations` is populated from the `limitations` section.
- `uncertainty.status` is `present` when section detection or unclassified
  text creates an explicit uncertainty note.
- Ambiguous sections retain their uncertainty reason.
- Missing values use `not_reported` with an empty list.

## Evidence classification

The extractor preserves these evidence types:

| Source section | Evidence type |
|---|---|
| Abstract | `abstract_statement` |
| Methods/Methodology | `experimental_methods` |
| Experimental Setup | `experimental_setup` |
| Results | `experimental_results` |
| Results and Discussion | `results_and_discussion_statement` |
| Discussion | `discussion_interpretation` |
| Conclusion | `conclusion_statement` |
| Limitations | `limitation_statement` |
| Unclassified text | `unclassified_source_text` |

Every extracted item has:

```text
verification_status=not_scientifically_verified
scientific_findings_verified=false
```

The extractor does not convert an abstract, discussion, or conclusion into a
verified experimental result.

## Provenance behavior

Every extracted evidence item retains:

- Exact supporting sentence.
- Source document identifier.
- NASA ID when available.
- Source URL when available.
- Section name.
- Section page numbers.
- Evidence type.
- Extraction method.
- Verification status.
- Uncertainty status.

For multi-page sections, the evidence item retains the section's complete
page span. It does not invent a more precise page number for a sentence when
the current section representation cannot establish one.

## Actual sample extraction behavior

Controlled synthetic source text included:

```text
PMMA samples were tested in reduced gravity at 21 percent oxygen,
ambient pressure 100 kPa, and temperature 300 K.
Forced flow velocity was 10 cm/s.
```

Actual extracted field examples:

```text
material_fuel: reported
gravity_condition: reported
oxygen_concentration: value=21, unit=percent
pressure: value=100, unit=kPa
temperature: value=300, unit=K
flow_condition: value=10, unit=cm/s
```

The supporting excerpts, NASA ID, citation URL, and page numbers were retained
in each evidence item.

Results text:

```text
The flame spread rate was 0.3 mm/s.
The observed flame became shorter.
```

was categorized as `experimental_results` observations rather than as
verified findings.

Discussion text:

```text
These results may indicate a flow effect.
```

was categorized as `discussion_interpretation`, preserving the source
wording rather than asserting the causal relationship.

Introduction text containing “may increase” and “combustion” generated no
scientific observation or finding.

## Focused tests

Command:

```text
.\.venv\Scripts\python.exe -m unittest `
  backend.tests.test_structured_findings_step4 `
  backend.tests.test_document_processing_step2 `
  backend.tests.test_section_extraction_step3 `
  backend.tests.test_nasa_ingestion
```

Actual result:

```text
Ran 30 tests in 0.356s
OK
```

The focused Step 4 tests cover:

1. Material/fuel extraction.
2. Gravity-condition extraction.
3. Oxygen concentration with units.
4. Pressure and temperature only when explicitly labeled.
5. Flow-condition extraction.
6. Measurements and original units.
7. Results versus discussion classification.
8. Limitations extraction.
9. Missing-field handling.
10. Exact excerpt and page provenance.
11. Ambiguous section statements.
12. Abstract versus experimental-result distinction.
13. Unsupported finding rejection from introduction text.
14. Multi-page section provenance.
15. Step 2 and Step 3 regression behavior.

## Full validation

### Full backend test suite

Command:

```text
.\.venv\Scripts\python.exe -m unittest discover -s backend\tests -p "test_*.py"
```

Final result:

```text
Ran 102 tests
OK
```

### Compile check

```text
.\.venv\Scripts\python.exe -m compileall -q backend
PASS
```

### Diff check

```text
git diff --check
PASS
```

## Preservation checks

- No live NASA downloads were performed.
- No NASA or BASS-II dataset changed.
- No benchmark fixture changed.
- No existing research record was overwritten.
- No search or ranking behavior was changed.
- No automatic PDF download was enabled.
- No dependency was installed.
- No reset, clean, rebase, merge, commit, push, or stash operation occurred.
- Existing user changes and stash were preserved.
- Step 5 claim-level evidence-linked summarization was not started.

## Scientific-integrity limitations

- Pattern extraction identifies candidate source-supported values; it does not
  establish that the source value is correct or experimentally valid.
- A section label does not prove that every sentence belongs scientifically to
  that section.
- Numeric extraction does not establish a threshold, causal relationship,
  initial/final measurement state, uncertainty, or applicability.
- Materials and conditions are not normalized into interchangeable scientific
  entities.
- Observation/finding entries preserve source statements but do not produce
  synthesized conclusions.
- Abstract, discussion, and conclusion statements remain distinct from direct
  experimental results.
- OCR is not performed.
- Human scientific review remains required before any finding can support a
  mission-specific or engineering conclusion.
