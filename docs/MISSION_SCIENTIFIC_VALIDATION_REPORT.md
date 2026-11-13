# Mission-Specific Scientific Validation Report

## Status

**PARTIAL PASS — evidence safeguards are implemented; qualified scientific
review remains required.**

The mission endpoint is `/dashboard/mission-brief` and is backed by
`build_mission_intelligence`. It accepts mission, query, fuel, oxygen
concentration, flow condition, gravity condition, environment, and result
limit. Missing values remain `None`/unspecified and are not silently filled.

## Evidence workflow

The current service:

1. Loads the persistent research intelligence store read-only.
2. Separates NASA experimental passages from simulation passages.
3. Preserves source ID, title, URL, page, exact excerpt, modality, role, and
   review status.
4. Includes reviewed-context and BASS-II metadata in separate evidence groups.
5. Keeps simulation evidence separate from experimental evidence.
6. Does not treat metadata or BASS-II context as a verified flame-spread
   finding.
7. Generates the required insufficiency response unless an experimental record
   is explicitly marked scientifically verified.

The default real store was exercised for spacecraft, lunar, Mars, missing
condition, and unrelated-query scenarios. It returned evidence candidates but
all generated recommendations were:

> Insufficient verified evidence to support a mission-specific recommendation.

This is the expected safeguard because the retrieved records are not marked
scientifically verified.

## Validation matrix

| Scenario | Executed | Result |
|---|---|---|
| Fully specified spacecraft scenario | PASS | Experimental/simulation evidence separated; no unverified recommendation |
| Partially specified lunar scenario | PASS | Missing values remain unspecified; evidence remains provisional |
| Missing experimental conditions | PASS | No assumptions added; compatibility requires review |
| No matching-evidence query | PASS | Recommendation remains insufficient-evidence response |
| Conflicting comparable evidence | PASS | Structured conflict reporter requires explicit comparable claims |
| Material mismatch | PASS | Search scorer exposes material mismatch; no recommendation generated |
| Environmental mismatch | PARTIAL PASS | Environment is carried through, but broad mission overlap still needs expert qrels |
| Metadata-only evidence | PASS | Metadata is not marked scientifically verified |
| Abstract-only evidence | PASS | Abstract scope is preserved as non-verified evidence |
| Source-link/provenance preservation | PASS | Source IDs, URLs, excerpts, roles, and review fields are retained |

## Recommendation contract

Recommendations include source ID, title, URL, passage, evidence type,
conditions, applicability limitations, evidence strength, and review status
when verified experimental evidence exists. Without such evidence, the service
returns the explicit insufficiency recommendation with no supporting source.

The safety boundary is always included:

> These outputs are research-support insights and must not be treated as
> certified safety decisions or substitutes for qualified engineering review.

## Remaining limitations

The mission scorer is deterministic term overlap. It does not establish
condition equivalence, infer experimental values, or independently validate a
NASA finding. Reviewed context and BASS-II metadata are currently included as
context groups rather than fully condition-matched recommendations.
