# Scientific Validation Limitations

## Human review

No qualified domain expert has supplied relevance labels for the 30-query
benchmark. The human-review CSV is a pending queue, not a completed qrels
dataset. Precision, recall, MRR, and NDCG therefore remain unavailable as
validated scientific metrics.

## Retrieval limitations

* The deterministic scorer is lexical/entity based.
* A passage is not an independent source; source IDs must be counted
  separately.
* Source diversification can reduce repeated passages but cannot prove
  relevance.
* Contradiction detection currently covers only explicit PMMA/liquid-fuel and
  microgravity/normal-gravity combinations.
* Broad mission terms can retrieve candidates that still require condition
  compatibility review.
* Metadata and abstracts are not full-text findings and are not scientifically
  verified by retrieval.

## Dataset limitations

BASS-II records remain read-only contextual data. Existing fields are used as
provided; pressure, temperature, and gravity filters are not invented.

## Mission-safety limitations

The system is a research-support tool, not a certified spacecraft fire-safety
authority. It must not be used as a substitute for qualified engineering
review or as the source of an operational safety threshold. Unverified or
incompatible evidence must not produce a mission-specific recommendation.

## Required next step

Have a qualified reviewer complete the human-review queue, document
qualifications and disagreements, adjudicate labels, and recompute the
relevance metrics using the documented fixed-K methodology.
