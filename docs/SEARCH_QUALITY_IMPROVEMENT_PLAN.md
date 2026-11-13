# Scientific Search Quality Improvement Plan

## Critical issues

1. **Independent relevance labels are absent.** The current benchmark stores
   queries only. No domain expert has reviewed query/result pairs, so
   scientific precision, recall, MRR, and NDCG must not be presented as
   validated ground truth.
2. **Lexical matching can reward arbitrary exact tokens.** A nonsense token can
   score against identical text even though it has no scientific meaning.
3. **Passage diversity is not source diversity.** Several top passages can come
   from one NASA document and should not be counted as independent evidence.
4. **Fallback quality is operationally tested but not benchmark-labelled.**
   Trigger correctness needs expert-reviewed expected coverage decisions.

Implemented in the current validation pass:

* Source-aware display diversification.
* Explicit rejection of two observed incompatible query combinations.
* Mission recommendation safeguard requiring explicitly verified experimental
  evidence.

## High-priority issues

1. Build a domain-expert qrels file with query-result labels 0–3, reviewer
   identity/status, and review date. Keep it separate from source data.
2. Add source-aware evaluation that reports passage count and unique NASA source
   count for every query.
3. Add explicit negative-query rejection for arbitrary tokens and unrelated
   domains before retrieval.
4. Add benchmark cases with known structured BASS-II filters separately from
   passage retrieval.

## Medium-priority issues

1. Improve phrase and unit matching so numeric values are associated with their
   scientific parameter rather than matched anywhere in an excerpt.
2. Add condition contradiction detection for gravity, material, oxygen, and
   pressure terms.
3. Add a calibrated threshold policy for weak results and fallback.
4. Add live NASA response fixtures captured from approved test runs, without
   treating them as permanent scientific ground truth.

## Optional improvements

1. Add semantic retrieval only after lexical/entity errors are measured and
   domain labels exist.
2. Add reviewer tooling for qrels creation and disagreement adjudication.
3. Add temporal/source-quality analysis for publication and review status.

## Recommended implementation order

1. Obtain expert-reviewed qrels for the 30-query benchmark.
2. Recompute graded metrics with fixed-K conventions.
3. Fix negative-query rejection and condition contradiction handling.
4. Tune source-diversity and fallback thresholds against reviewed labels.
5. Re-run the complete regression and live smoke suites.

No paid API, embedding model, or external LLM is required for these steps.
