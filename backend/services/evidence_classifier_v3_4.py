from typing import Any

from backend.services.evidence_classifier_v3_3 import (
    classify_passage_v3_3,
)


def classify_passage_v3_4(
    passage: dict[str, Any],
    page_context: str = "",
) -> dict[str, Any]:

    text = " ".join(
        str(passage.get("text") or "").lower().split()
    )

    result = classify_passage_v3_3(
        passage,
        page_context=page_context,
    ).copy()

    if (
        "pyrolysis length" in text
        and any(term in text for term in (
            "obtained by subtracting",
            "determined by subtracting",
            "determined similarly",
        ))
        and "burnout front" in text
        and "pyrolysis front" in text
    ):
        simulation = any(term in text for term in (
            "simulation results",
            "fds simulations",
            "simulation",
        ))

        result.update({
            "evidence_role": "measurement_definition",
            "evidence_modality": (
                "simulation" if simulation else "experiment"
            ),
            "passage_category": "candidate_method",
            "classification_basis": (
                "Definition of pyrolysis length using burnout "
                "front and pyrolysis front positions."
            ),
            "classification_version": "3.4",
            "review_status": "requires_manual_review",
            "scientific_findings_verified": False,
        })

    result["classification_version"] = "3.4"
    return result
