# FlameGuard AI — Real-World Search Test Report

## 1. Test information

* Test date: 2026-10-30
* Branch: `feature/research-backend`
* Test mode: local in-process services and FastAPI `TestClient`; live NASA
  NTRS requests where stated
* Datasets: read-only
* NASA PDFs: not downloaded

## 2. Repository status

The branch was `feature/research-backend`. The worktree had existing
uncommitted application/test/documentation changes and one existing stash.
The stash was not changed. No files under `data/` changed.

## 3. Bugs discovered and fixed during testing

Two real defects were found by the end-to-end run:

1. BASS-II numeric-only filters returned zero results because the empty-query
   guard ignored numeric filters. Fixed by including oxygen, numeric field,
   numeric value, and tolerance filters in the guard.
2. `/research/nasa-passage-search` raised `NameError: query_terms is not
   defined`; the refactor had removed the tokenizer variable but left two
   references. The undefined variable was replaced with the parsed scientific
   query and the missing `re` import was restored.

The affected searches were rerun successfully after both fixes.

## 4. Test A — Local database searches

Method: `build_evidence_brief(query, limit=3)`.
All results below came from
`primary_research_intelligence_store`; they were not live NASA results.

| Query | Count | Time | Representative records |
|---|---:|---:|---|
| `microgravity combustion` | 3 | 93.75 ms | `NASA-PASSAGE-19960008387-0000`, NASA `19960008387`, **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure**, score 0.75. Excerpt begins “Solid Surface Combustion Experiment — Flame Spread in a Quiescent, Microgravity Environment”. |
| `flame spread in spacecraft` | 3 | 82.57 ms | `NASA-PASSAGE-19960008387-0000`, NASA `19960008387`, same source title, score 0.55; also pages from NASA `19960008387` and `20000024924`. |
| `solid fuel combustion` | 3 | 83.25 ms | NASA `19960008387`, score 0.55; additional passages from the same source scored 0.40. |
| `oxygen concentration and flame behavior` | 3 | 102.73 ms | NASA `19960008387`, page passage score 0.525; excerpt begins “The experimental flame spread rates ... over the thin cellulosic fuel ... at three different ambient pressures”. |
| `BASS-II combustion experiments` | 3 | 85.06 ms | NASA `20000024924`, scores 0.5125; representative excerpt begins “Preliminary results of polyethylene-insulation flammability in microgravity were obtained in the NASA Wire Insulation Flammability experiment”. |

Representative local provenance:

* URL: `https://ntrs.nasa.gov/citations/19960008387`
* Evidence type: `extracted_source_text`
* Review status: `requires_manual_review`
* Scientific verification: `false`
* Origin: `primary_research_intelligence_store`

The local search returns passages, not BASS-II structured records. BASS-II was
tested separately below.

## 5. Test B — Live NASA NTRS searches

Endpoint used by the service:

```text
https://ntrs.nasa.gov/api/citations/search
```

All five live searches returned HTTP-successful service responses. Each record
had an official NASA URL, retrieval timestamp, `retrieved_at`, evidence type
`bibliographic_metadata_and_abstract`, `full_text_retrieved: false`, and
`scientific_findings_verified: false`.

### `microgravity flame spread`

Count: 3. Retrieval timestamp:
`2026-10-30T20:43:55.299853+00:00`.

1. NASA `20205004657` — **Effects of Confinement on Flame Spread in
   Microgravity**. Publication year was not supplied in the returned
   publication field. Abstract begins: “Solid fuel combustion experiments
   aboard the ISS examine the effects of confinement on a concurrent,
   purely-forced-flow flame spread in microgravity environment.”
   URL: <https://ntrs.nasa.gov/citations/20205004657>
2. NASA `20150008962` — **Concurrent Flame Growth, Spread and Extinction over
   Composite Fabric Samples in Low Speed Purely Forced Flow in Microgravity**.
   Publication year: 2015. Abstract begins: “As a part of the NASA BASS and
   BASS-II experimental projects aboard the International Space Station,
   flame growth, spread and extinction...”
   URL: <https://ntrs.nasa.gov/citations/20150008962>
3. NASA `19970020626` — **Microgravity Experiment on Flame Spread of a Fuel
   Droplet Array**. Publication year: 1997. Abstract begins: “Flame spread
   phenomena in a suspended fuel droplet array were experimentally
   investigated for n-decane and n-hexadecane...”
   URL: <https://ntrs.nasa.gov/citations/19970020626>

### `fire safety in spacecraft`

Count: 3. Retrieval timestamp:
`2026-10-30T20:43:57.260848+00:00`.

1. NASA `20150000894` — **Large-Scale Spacecraft Fire Safety Tests**. Year:
   2014. Abstract begins: “An international collaborative program is underway
   to address open issues in spacecraft fire safety.”
   URL: <https://ntrs.nasa.gov/citations/20150000894>
2. NASA `20130000677` — **Large Scale Experiments on Spacecraft Fire Safety**.
   Year: 2012. Abstract begins: “Full scale fire testing complemented by
   computer modelling has provided significant know how about the risk,
   prevention and suppression of fire...”
   URL: <https://ntrs.nasa.gov/citations/20130000677>
3. NASA `20130001713` — **Large Scale Experiments on Spacecraft Fire Safety**.
   Year: 2012. Abstract begins: “Full scale fire testing complemented by
   computer modelling has provided significant knowhow about the risk,
   prevention and suppression of fire...”
   URL: <https://ntrs.nasa.gov/citations/20130001713>

### `combustion in reduced gravity`

Count: 3. Retrieval timestamp:
`2026-10-30T20:43:59.161660+00:00`.

1. NASA `20010074057` — **Bi-Component Droplet Combustion in Reduced Gravity**.
   Year: 2001. Abstract begins: “This research deals with reduced-gravity
   combustion of bi-component droplets initially in the mm size range or
   larger.”
   URL: <https://ntrs.nasa.gov/citations/20010074057>
2. NASA `20040053548` — **Bi-Component Droplet Combustion in Reduced Gravity**.
   Year: 2003. Abstract begins with the same reduced-gravity
   bi-component-droplet research description.
   URL: <https://ntrs.nasa.gov/citations/20040053548>
3. NASA `19930004824` — **Combustion of Gaseous Fuels Under Reduced-Gravity
   Conditions**. Year: 1992. Abstract begins: “The need for an improved
   understanding of fires is becoming critically important with increased
   space travel...”
   URL: <https://ntrs.nasa.gov/citations/19930004824>

### `oxygen concentration and flame propagation`

Count: 3. Retrieval timestamp:
`2026-10-30T20:44:01.218253+00:00`.

1. NASA `19760046586` — **The effects of forced air flow and oxygen
   concentration on flammability, smoke density, and pyrolytic toxicity**.
   Year: 1976. Abstract begins: “The question is posed whether forced air flow
   should be incorporated into flammability tests...”
   URL: <https://ntrs.nasa.gov/citations/19760046586>
2. NASA `20170004702` — **NASA-STD-6001B Test 1 Upward Flame Propagation; Sample
   Length Impact on MOC Investigation**. Year: 2017. Abstract begins:
   “Understanding the combustion behavior of materials in the elevated oxygen
   environments of habitable spacecraft is of utmost importance...”
   URL: <https://ntrs.nasa.gov/citations/20170004702>
3. NASA `19990053980` — **A Study of Flame Propagation on Water-Mist Laden Gas
   Mixtures in Microgravity**. Year: 1999. Abstract begins: “The use of water
   mists ... for fire suppression is currently receiving increased attention...”
   URL: <https://ntrs.nasa.gov/citations/19990053980>

### `solid material combustion in microgravity`

Count: 3. Retrieval timestamp:
`2026-10-30T20:44:03.102109+00:00`.

1. NASA `19970020594` — **Quantitative Measurement of Oxygen in Microgravity
   Combustion**. Year: 1997. Abstract begins: “A low-gravity environment, in
   space or in ground-based facilities such as drop towers, provides a unique
   setting for studying combustion mechanisms.”
   URL: <https://ntrs.nasa.gov/citations/19970020594>
2. NASA `19970020547` — **Fourth International Microgravity Combustion
   Workshop**. Year: 1997. Abstract begins: “This proceedings document is a
   compilation about work performed by a community of researchers...”
   URL: <https://ntrs.nasa.gov/citations/19970020547>
3. NASA `19990053965` — **Fifth International Microgravity Combustion
   Workshop**. Year: 1999. Abstract begins: “On behalf of the NASA Headquarters
   Microgravity Research Division...”
   URL: <https://ntrs.nasa.gov/citations/19990053965>

These are NASA catalogue metadata and abstracts, not independently verified
scientific findings.

## 6. Test C — Local-first and NASA fallback

| Case | Local results | NASA results | Fallback | Reason |
|---|---:|---:|---|---|
| Strong local: `flame spread flow velocity` | 3 | 3 | Yes | `insufficient_local_source_coverage`; local passages were from one source |
| Weak local: `PMMA flame spread microgravity` | 3 | 3 | Yes | `too_few_local_passages`, `insufficient_local_source_coverage` |
| No likely local: `fire safety in spacecraft` | 2 | 3 | Yes | `too_few_local_passages`, `insufficient_local_source_coverage` |
| Nonsense: `zzzzzzzz marine biology 918273645` | 0 | 0 | Yes | No relevant local evidence; NASA returned zero |

The “strong local” case demonstrates an important behavior: three local
passages were not considered sufficient because they came from one source.
NASA fallback supplied additional metadata records.

Examples of merged provenance:

* Local `20000024924`: title **Experimental Verification of Material
  Flammability in Space**, local pages `[5, 13, 23]`, local record IDs
  `NASA-PASSAGE-20000024924-0089`,
  `NASA-PASSAGE-20000024924-0401`, and
  `NASA-PASSAGE-20000024924-0853`.
* Online fallback `19990054038`: title **Diffusive and Radiative Transport in
  Fires (DARTFire): Opposed-Flow Flame Spread in Low-Velocity Flows**, online
  metadata scope `bibliographic_metadata_and_abstract_only`.

No duplicate NASA ID was emitted as two combined source entries.

## 7. Test D — Relevance and false positives

The deterministic scorer produced these representative scores against
challenge texts:

| Query | Matching text | Score | Observation |
|---|---|---:|---|
| `microgravity flame spread in solid materials` | PMMA flame spread in microgravity solid fuel | 0.66 | Correct phenomenon/environment match |
| `liquid fuel combustion in reduced gravity` | Liquid fuel combustion in reduced gravity | 0.75 | Correct environment/fuel-language match |
| `fire suppression in spacecraft` | Fire suppression spacecraft | 0.45 | Correct intent match |
| `oxygen concentration effects on flame propagation` | Oxygen concentration flame propagation | 0.66 | Correct concept match |
| `marine biology` | Marine biology | 0.45 | Correctly unrelated to combustion; no domain concept match |
| `qwertyzz 918273645` | Random nonsense text | 0.55 | Lexical scorer can score exact nonsense tokens; local/NASA retrieval returned no records |

The final row is a limitation: generic arbitrary tokens can produce lexical
scores in direct text comparisons, although the actual research stores did not
return corresponding evidence for the nonsense search.

NASA results remained explicitly metadata-only and unverified.

## 8. Test E — BASS-II searches

Dataset summary from the actual source:

* Dataset: `NASA PSI-25 BASS-II Experimental Table`
* Records: 129
* Columns: 17
* Blank cells: 19
* Literal `none` cells: 16
* Duplicate identifiers: none
* Original values modified: false

Actual searches after the numeric-filter fix:

| Filter | Results | Representative records |
|---|---:|---|
| Fuel `PMMA` | 3 | Bhattacharjee/B1, B2, B4 |
| Initial O₂ `22.2` | 3 | Bhattacharjee/B1, B2, B3 |
| Initial CO `0` | 3 | Bhattacharjee/B1, Bhattacharjee/B5, Bhattacharjee/B6 |
| Total frames `57` | 2 | Bhattacharjee/B1 and Fernandez-Pello/P21a |
| Flow restrictor `2` | 3 | Bhattacharjee/B1, B2, B3 |

Raw values remain strings from the original dataset. Missing values such as
`none` and empty cells do not match numeric filters.

Pressure, temperature, and gravity were not queried because those fields are
absent from the source schema.

## 9. HTTP endpoint results

Requests were executed through FastAPI `TestClient`, without changing
persistent data.

| Endpoint | Status | Time | Result/schema |
|---|---:|---:|---|
| `/research/search?q=microgravity+combustion&limit=3` | 200 | 152.57 ms | Evidence brief schema; results under `results`, count represented in `summary` |
| `/research/online-search?q=microgravity+flame+spread&limit=2` | 200 | 1887.75 ms | NASA schema with `count`, `results`, `retrieved_at` |
| `/research/combined-search?q=fire+safety+in+spacecraft&limit=2` | 200 | 2456.42 ms | Local/online counts, fallback reasons, combined sources, conflict report |
| `/research/evidence-search?q=flame+spread&limit=2` | 200 | 16.28 ms | `query`, `count`, `results`, `notice` |
| `/bass2/search?fuel=PMMA&limit=2` | 200 | 16.17 ms | `query`, `filters`, `count`, `results`, `notice` |
| `/bass2/summary` | 200 | 12.63 ms | Dataset summary and integrity fields |
| `/research/nasa-passage-search?q=microgravity&limit=2` | 200 after fix | 161.69 ms | `query`, `filters`, `count`, `results`, `notice` |
| `/research/mission-search?q=flame+spread` | 404 | 5.93 ms | Endpoint does not exist |

The initial passage-search request failed with `NameError`; it was fixed and
the same endpoint then returned two real passages successfully.

## 10. Performance and reliability

Observed timings are environment/network dependent:

* Local evidence search: approximately 82–106 ms
* BASS-II search: approximately 1–3 ms at service level
* NASA live search: approximately 1.9–2.4 seconds
* Combined local-plus-NASA search: approximately 1.2–2.2 seconds
* HTTP in-process local endpoints: approximately 12–162 ms

Final regression after the two fixes:

```text
Ran 60 tests in 0.501s
OK
compileall: PASS
git diff --check: PASS
```

Live NASA timeout/error behavior was not induced against the real service.
Those cases remain covered by mocked tests.

## 11. Overall assessment

Status: **PARTIAL PASS — Working with limitations**

The real search system successfully retrieved local NASA passages, live NASA
NTRS catalogue records, combined fallback results, and BASS-II records. It
preserved source IDs, URLs, page references, retrieval timestamps, and
metadata-only verification status.

The test run also found and corrected two real defects, demonstrating that the
system required end-to-end validation beyond unit-test results.

Limitations:

1. NASA live error and timeout cases were not fault-injected.
2. The local scorer remains deterministic lexical/entity matching.
3. Random exact tokens can receive lexical scores even when no research result
   is returned.
4. BASS-II has no pressure, temperature, or gravity columns.
5. NASA catalogue metadata and abstracts are not scientific verification.
6. `/research/mission-search` does not exist in the current API.

## Final decision

**SEARCH SYSTEM PASSED WITH LIMITATIONS**
