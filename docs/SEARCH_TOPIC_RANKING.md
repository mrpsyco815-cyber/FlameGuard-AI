# Search Topic Ranking

## Status and scope

**Status: PARTIAL PASS.** This is a provisional software-QA assessment of the
21 individual searches in
[INDIVIDUAL_QUERY_BEFORE_AFTER_RESULTS.md](./INDIVIDUAL_QUERY_BEFORE_AFTER_RESULTS.md).
It is not a scientific validation, expert relevance judgment, or spacecraft
fire-safety certification. No independent reviewer has supplied relevance
labels or graded the retrieved papers.

The ranking considers:

- direct match to the requested phenomenon, material, gravity, environment, or
  measurement;
- number of independent sources, not just passage count;
- whether local evidence was sufficient without an unnecessary NASA request;
- whether NASA fallback returned topical records when local evidence was weak;
- evidence scope and review status; and
- observed mismatch, repetition, and missing-parameter limitations.

Raw result count is not used as a quality score. NASA catalog metadata and
abstracts remain unverified evidence.

## Provisional topic ranking

| Rank | Topic | Observed assessment | Final local / NASA / BASS-II records | Final fallback calls | Duplicate-source records |
|---:|---|---|---:|---:|---:|
| 1 | Microgravity flame spread | Strongest topical local coverage, with direct flame-spread and microgravity records; material-specific searches still expose mismatches and repeated sources. | 35 / 5 / 6 | 1/7 | 7 |
| 2 | Spacecraft fire safety | NASA fallback is highly topical, but local coverage is sparse and several local passages are generic material-flammability evidence. NASA results are metadata/abstract only. | 26 / 24 / 0 | 7/7 | 11 |
| 3 | Oxygen concentration and flame propagation | Weakest parameter-specific evidence. Numeric oxygen context is found in some passages, but quantitative measurement context, material compatibility, and extinction-threshold evidence are incomplete. | 35 / 10 / 5 | 3/7 | 8 |

The counts are accumulated across the seven queries in each topic and are
not independent-paper counts. Repeated passages and multiple records from one
NASA source are included in the duplicate column.

## Why microgravity flame spread ranks first

This topic has the clearest direct local matches. For example, T1-01
(`Microgravity flame spread`) returned:

- `19960008387`, *Solid surface combustion experiment flame spread in a
  quiescent, microgravity environment implications of spread rate and flame
  structure*;
- `20210017787`, *Determining the Cause of Reduced Concurrent Flame Spread over
  Thin Solid Fuels in Low Pressure and Low Gravity*; and
- `20000024924`, *Experimental Verification of Material Flammability in Space*.

The first two records directly combine flame spread with a reduced-gravity
condition. The parser also exposes the microgravity and flame-spread matches
in the explanations. T1-03 (`PMMA flame spread under microgravity conditions`)
returned a passage explicitly mentioning PMMA and microgravity, and NASA
fallback supplied topical catalog records such as `19990054038`, *Diffusive
and Radiative Transport in Fires (DARTFire): Opposed-Flow Flame Spread in
Low-Velocity Flows*.

This is not a claim that every returned passage is applicable. T1-03 also
returned thin-solid and cotton-related records with material-mismatch or
environment-mismatch penalties, and the same source can occur more than once.
The topic ranks first because it has the best observed combination of direct
phenomenon/condition matches and local evidence, not because it has been
scientifically validated.

## Why spacecraft fire safety ranks second

Spacecraft-specific NASA fallback performed well as a discovery mechanism.
T2-01 (`Spacecraft fire safety research`) returned topical NASA records
including:

- `20150000894`, *Large-Scale Spacecraft Fire Safety Tests*;
- `20130001713`, *Large Scale Experiments on Spacecraft Fire Safety*;
- `20130000677`, *Large Scale Experiments on Spacecraft Fire Safety*;
- `20140011433`, *Large-Scale Spacecraft Fire Safety Experiments in ISS
  Resupply Vehicles*; and
- `20170007283`, *Spacecraft Fire Safety Research at NASA Glenn Research
  Center*.

The environment-intent correction correctly caused fallback for queries with
insufficient local spacecraft coverage. However, the local side of T2-01
contained only two passages, both from `20000024924`, and the local result was
penalized for an environment mismatch. Across the topic, the seven queries
made seven fallback calls, returned 24 NASA records, and produced the highest
duplicate total (11). The NASA records are catalog metadata/abstracts with
`scientific_findings_verified=false` and
`review_status=not_scientifically_reviewed`; they are useful for discovery but
cannot support a verified engineering conclusion.

The topic therefore ranks above oxygen/flame propagation for environment
retrieval, but below microgravity flame spread for local evidence sufficiency
and source diversity.

## Why oxygen concentration and flame propagation ranks third

The correction improved this topic by distinguishing a quantitative oxygen
context from a simple oxygen keyword. T3-03 (`Limiting oxygen concentration for
flame extinction`) now identifies a passage containing `C = 21 percent` as
quantitative oxygen context. That passage is from
`20000024924`, *Experimental Verification of Material Flammability in Space*.

The same query also demonstrates the remaining defect: other returned
passages mention “extinction” or oxygen levels without providing the requested
limiting-oxygen measurement, and some refer to laser extinction rather than
flame extinction. The system marks missing quantitative context in the
explanation, but the result is still present as contextual evidence.

T3-05 (`Oxygen concentration effects on PMMA flame spread`) returned five
BASS-II records and local/NASA records, but the available evidence does not
establish a PMMA-specific oxygen threshold. T3-07 returned NASA records about
oxygen, suppression, silicone, and other materials; those records are
discovery evidence and not interchangeable material-specific findings.
BASS-II remains limited to its actual fields, including initial/final O2 and
the recorded material; it does not supply authoritative pressure, temperature,
or gravity fields.

The topic ranks third because the requested numerical parameter and
material/phenomenon combination are the least consistently represented.
No limiting oxygen concentration, extinction threshold, or causal engineering
rule is inferred.

## Best and weakest individual queries

### Best observed queries

1. **T1-01 — Microgravity flame spread.** Direct local records matched both
   the phenomenon and gravity condition, including `19960008387` and
   `20210017787`. The result set still contained one repeated source.
2. **T2-01 — Spacecraft fire safety research.** Local coverage was
   insufficient, but fallback correctly produced several directly titled
   spacecraft fire-safety records. They remain unverified metadata/abstract
   evidence.
3. **T3-05 — Oxygen concentration effects on PMMA flame spread.** This query
   produced the strongest oxygen-topic source volume, including five BASS-II
   records and NASA discovery results. It remains limited by incomplete
   quantitative and material-specific verification, so volume is not treated
   as proof of quality.

### Weakest observed queries

1. **T3-03 — Limiting oxygen concentration for flame extinction.** A numeric
   oxygen value was found, but the final set did not establish a limiting
   threshold. Some passages conflate flame extinction with optical/laser
   extinction or lack quantitative context.
2. **T2-07 — Spacecraft cabin atmosphere and combustion hazards.** Final local
   results remained concentrated in two source identities with three repeated
   source records; the correction appropriately triggered NASA fallback, but
   NASA returned no records in that run.
3. **T1-03 — PMMA flame spread under microgravity conditions.** One local
   passage directly mentioned PMMA and microgravity, but other top-five
   passages were different materials or lacked the requested environment.
   NASA returned useful discovery records, but all were metadata/abstract
   scope.

## Before/after interpretation

Across all 21 queries, the correction pass changed:

| Metric | Baseline | Final | Interpretation |
|---|---:|---:|---|
| Local records | 96 | 96 | Retrieval volume was unchanged. |
| NASA records | 44 | 39 | Five fewer NASA records, primarily because T1-07 no longer fell back. |
| BASS-II records | 11 | 11 | Schema-preserving behavior was unchanged. |
| Combined local/NASA records | 140 | 135 | Lower volume was not treated as a quality regression by itself. |
| Accumulated unique-source positions | 114 | 109 | Source diversity did not improve. |
| Duplicate-source records | 26 | 26 | Repeated-source limitation remains unresolved when source supply is small. |
| Mean local latency | 41.09 ms | 35.17 ms | Improved in this run; timing is workload and filesystem dependent. |
| Mean combined latency | 1624.37 ms | 1558.03 ms | Still dominated by variable live NASA latency. |

Fallback behavior changed at the query level even though the net total stayed
at 11 calls: T1-07 changed from fallback to no fallback, while T2-07 changed
from no fallback to fallback. This is consistent with the new
environment/coverage checks and should not be summarized as a blanket increase
or decrease in fallback quality.

## Final readiness score

**6.5/10 — operational research prototype, not scientifically validated.**

Rationale:

- **Strengths:** local-first execution, explainable query intent, material and
  condition penalties, source provenance, NASA fallback, evidence-scope
  separation, BASS-II schema preservation, and individual validation of all
  21 queries.
- **Deductions:** repeated source passages remain, lexical/entity ranking is
  not semantic relevance validation, some material and condition matches are
  incomplete, NASA latency is variable, and no independent expert labels or
  verified mission-specific findings are available.

## Remaining defects and limitations

- Source-level diversification cannot create independent studies when the
  local corpus contains too few source identities; repeated passages remain
  visible and are reported as duplicates.
- Generic lexical matches can still appear as contextual records despite
  mismatch penalties.
- Quantitative oxygen detection recognizes numeric context but does not prove
  that a value is a limiting threshold, initial measurement, final
  measurement, or causally related to flame behavior.
- NASA fallback is an official-source discovery path, not full-text evidence
  retrieval. NASA PDFs were not downloaded automatically.
- No precision, recall, MRR, or NDCG claim is defensible without expert
  relevance labels.
- Mission-specific recommendations remain guarded and must return insufficient
  verified evidence when the evidence requirements are not met.

## Verification references

- [FINAL_21_QUERY_SEARCH_VALIDATION.md](./FINAL_21_QUERY_SEARCH_VALIDATION.md)
- [SEARCH_CORRECTIONS_ROOT_CAUSE_REPORT.md](./SEARCH_CORRECTIONS_ROOT_CAUSE_REPORT.md)
- [SEARCH_CORRECTIONS_IMPLEMENTATION_REPORT.md](./SEARCH_CORRECTIONS_IMPLEMENTATION_REPORT.md)
- [FINAL_SEARCH_QUALITY_AUDIT.md](./FINAL_SEARCH_QUALITY_AUDIT.md)
- [SCIENTIFIC_VALIDATION_LIMITATIONS.md](./SCIENTIFIC_VALIDATION_LIMITATIONS.md)
