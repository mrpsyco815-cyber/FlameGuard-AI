# Scientific Expert Review Guide

## Purpose

This guide supports an independent reviewer evaluating the 30-query FlameGuard
AI search benchmark. The review queue is
[SCIENTIFIC_SEARCH_HUMAN_REVIEW.csv](./SCIENTIFIC_SEARCH_HUMAN_REVIEW.csv).
The queue contains actual retrieved passages and machine suggestions only.
Human labels and comments must be supplied by a qualified reviewer.

## Reviewer qualifications

Record the reviewer's name or identifier, affiliation, relevant combustion or
spacecraft fire-safety experience, information-retrieval experience, and review
date outside the result rows or in the project's approved review record. Do
not claim expert validation until those details and judgments exist.

## Review procedure

1. Review one query and all returned ranks together.
2. Open the NASA citation URL when available.
3. Determine whether the available excerpt is enough to judge relevance.
4. Compare material, phenomenon, environment, gravity, oxygen, pressure, flow,
   and numerical conditions explicitly; do not infer missing values.
5. Record a label in `human_reviewer_relevance_label` and explain difficult
   decisions in `reviewer_comments`.
6. Use `U` when the excerpt or metadata does not support a defensible decision.
7. Record disagreements separately rather than silently averaging them.

## Labels

* `3` — Highly relevant: directly addresses the query's material/phenomenon
  and relevant environment or conditions.
* `2` — Relevant: substantially useful, but one condition, material detail, or
  evidence limitation is incomplete.
* `1` — Partially relevant: shares a scientific topic but does not answer the
  requested scenario directly.
* `0` — Irrelevant: does not support the requested scientific topic or is
  materially/environmentally incompatible.
* `U` — Cannot determine from available evidence.

The machine-generated `proposed_relevance_category` is not an expert
judgment and must not be copied without review.

## Evidence scope

Distinguish these scopes in comments:

* **Metadata**: title, identifier, authors, dates, and catalogue fields.
* **Abstract**: author-provided summary; not a full-text verification.
* **Full text/passage**: an extracted passage whose surrounding context should
  be checked in the source document.
* **Verified finding**: only when the record explicitly carries an approved
  scientific-verification status. NASA origin alone is not verification.

## Condition mismatch checklist

Flag mismatches for:

* Fuel/material (for example PMMA versus polyethylene).
* Combustion phenomenon (spread, extinction, ignition, suppression, droplet
  combustion).
* Gravity or environment (microgravity, reduced gravity, normal gravity,
  spacecraft, lunar, Mars).
* Oxygen concentration, pressure, and flow.
* Numerical values and units.

Missing fields are unknown, not equivalent to a matching condition.

## Disagreements and adjudication

For disagreements, preserve both reviewer labels, the rationale, and the
adjudicator identity/date. Do not convert an unresolved disagreement into
ground truth. Metrics should identify whether they use first-review labels,
adjudicated labels, or remain unavailable.

## Safety boundary

Review outcomes assess retrieval relevance only. They do not certify a
spacecraft design, establish a fire-safety limit, or replace qualified
engineering review.
