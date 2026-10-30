import re
from typing import Any

from backend.services.evidence_classifier_v3 import classify_passage_v3


def classify_passage_v3_1(
    passage: dict[str, Any],
    page_context: str = "",
) -> dict[str, Any]:

    result = classify_passage_v3(
        passage,
        page_context=page_context,
    )

    text = " ".join(
        str(passage.get("text") or "").lower().split()
    )

    context = " ".join(
        str(page_context or "").lower().split()
    )

    combined = f"{text} {context}"

    # Correct previous-study context when adjacent pages contain
    # the current experiment's section heading.
    if (
        result["evidence_role"] == "experimental_observation"
        and result["research_context"] == "unknown"
        and re.search(
            r"\b(microgravity|space experiment|on orbit|mir)\b",
            combined,
        )
    ):
        result["research_context"] = "spaceflight_or_microgravity"
        result["classification_basis"] += (
            " Adjacent page context identifies the space experiment."
        )

    # Separate quantitative extinction time from qualitative comparison.
    extinction_time = (
        "flow shutoff" in text
        and "extinction" in text
        and re.search(r"\b\d+\s*to\s*\d+\s*s\b", text)
    )

    if extinction_time:
        result["evidence_role"] = "experimental_quantitative_result"
        result["evidence_modality"] = "experiment"
        result["passage_category"] = "candidate_result"

        if "microgravity" in combined:
            result["research_context"] = "spaceflight_or_microgravity"

        if "ground testing" in combined or "ground test" in combined:
            result["comparison_context"] = "ground_test"

        result["classification_basis"] = (
            "Numerical microgravity extinction-time result; "
            "ground testing is the comparison reference."
        )

    # Identify interpretations based on both experimental
    # and simulation context from the complete page.
    has_simulation = bool(
        re.search(r"\b(simulation|simulations|fds|dns)\b", combined)
    )

    has_experiment = bool(
        re.search(r"\b(experiment|experiments|experimentally)\b", combined)
    )

    if (
        result["evidence_role"] == "interpretation"
        and has_simulation
        and has_experiment
    ):
        result["evidence_modality"] = "mixed"
        result["comparison_context"] = "experimental_simulation_comparison"
        result["classification_basis"] += (
            " Complete page context includes both experiments and simulations."
        )

    result["classification_version"] = "3.1"

    # Scientific findings remain unverified.
    result["scientific_findings_verified"] = False
    result["review_status"] = "requires_manual_review"

    return result
