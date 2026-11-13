# Research Phase Tracker

| Phase | Status | Evidence |
|---|---|---|
| 1. Architecture audit | Completed | `ARCHITECTURE_AUDIT.md`; existing modules and tests inspected |
| 2. Query understanding | Completed | Shared parser/scorer; unit tests |
| 3. Local coverage/fallback | Completed for tested cases | Empty, weak, wrong-material, insufficient-source, and NASA-failure regressions pass |
| 4. NASA NTRS integration | Completed for connector scope | Mocked errors/duplicates plus live success and empty-result smoke tests pass; no PDF download |
| 5. Provenance/deduplication | Completed for available structures | Source/page provenance, duplicate handling, retrieval timestamps, and explicit conflict reporting are tested; free-text conflict extraction is intentionally not performed |
| 6. BASS-II search | Completed for available schema | Fuel, initial/final O2, supported numeric columns, tolerance, and missing-value handling pass |
| 7. Quality benchmark | Partially completed | 30 synthetic labelled cases pass; labels are not domain-reviewed scientific ground truth |
| 8. API reliability/docs | Completed for tested endpoints | FastAPI valid, invalid, empty, limit, schema, and NASA-unavailable cases pass |
| 9. Regression/acceptance | Completed for executed scope | 60/60 `unittest` tests passed; compileall passed |

## Test-count discrepancy

Current discovery reports 60 tests after this validation work. The previous
report's 43 consisted of the four committed baseline modules plus seven new
tests. Historical commits `991de61` and `0b81f68` contain intermediate
`test_empty_research_stores.py` and `test_mission_research.py` files, but those
files are absent from `HEAD` and current discovery. They were not skipped or
renamed in the current tree. The earlier claim of a 44-test baseline cannot
be reproduced from the current checkout.
