# FlameGuard Research Architecture Audit

## Current flow

* `research_summarizer.py` loads the persistent primary store and the additive
  supplemental collection, filters eligible evidence roles, and preserves
  record IDs, source IDs, page numbers, excerpts, review status, and
  verification flags.
* `query_understanding.py` normalizes scientific queries, removes generic
  stopwords, recognizes defensible material/concept aliases, and produces
  explainable relevance components.
* `research_federation.py` performs local-first retrieval and invokes NASA NTRS
  only when relevant passage, source, material, or condition coverage is weak.
* `nasa_online.py` retrieves NTRS catalogue metadata and abstracts only. It
  does not download PDFs and explicitly marks metadata as unverified.
* `nasa_ingestion.py` is the separately controlled path for an explicitly
  requested document import; imported passages remain pending review.
* `bass2_dataset.py` reads the original JSON without rewriting it and returns
  structured records separately from PDF passages.

## Findings and mitigations

| Area | Finding | Current treatment |
|---|---|---|
| Retrieval | Earlier ranking was generic token overlap | Shared normalized scientific scoring with visible reasons |
| Scientific entities | Material and condition requirements were not coverage gates | Federation checks material and condition coverage |
| Online evidence | Metadata could be mistaken for findings | Explicit evidence type, retrieval, review, and verification fields |
| Provenance | Local source/page identity was already present but needed merge safety | Source-key deduplication retains local pages and online metadata |
| Data integrity | BASS-II is a raw structured dataset | No source rewriting; search returns original record values |
| Validation | Tests were `unittest` based and pytest was unavailable | Offline `unittest` suite remains dependency-free |

## Remaining limitations

The scorer is deterministic lexical/entity matching, not semantic inference.
Scientific verification still requires domain review. Live NTRS availability
and network-dependent smoke testing were not made part of ordinary tests.
