# Search Quality Report

The original four-record fixture remains a small, manually labelled regression
fixture, not a claim of scientific ground truth. An expanded fixture now
contains 30 clearly labelled **synthetic** cases because available repository
records do not provide 30 domain-reviewed query judgments.

Metrics use conventional fixed-K precision: relevant results divided by K;
when fewer than K candidates are available, missing slots count as
non-relevant. Recall@10 is relevant results in the top 10 divided by the
total labelled relevant candidates. The 30-case fixture has one labelled
relevant candidate per case and is synthetic, not expert-reviewed.

### Original fixture

* Precision@1: 1.00
* Precision@2: 0.50
* Recall@10: 1.00
* Duplicate rate: 0.00
* Material mismatch rate in top-1: 0.00

### Expanded synthetic fixture

* Cases: 30
* Precision@1: 1.00 (30/30)
* Precision@5: 0.20 (30 relevant results / 150 fixed slots)
* Recall@10: 1.00 (30/30 labelled relevant candidates)
* Material mismatch rate: 0.00 at top-1
* Environment mismatch rate: 0.00 at top-1
* Duplicate rate: 0.00 in the fixture
* False-positive rate at top-1: 0.00
* Fallback accuracy: NOT MEASURED as a benchmark metric; targeted fallback tests pass

The suite also tests stopword-only rejection, synonym handling, numeric values,
material mismatch penalties, empty stores, weak evidence, and NASA fallback
failure. A larger domain-expert reviewed benchmark is still needed before
interpreting these metrics beyond regression protection.
