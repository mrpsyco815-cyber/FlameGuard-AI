import re
from typing import Any

from backend.services.evidence_classifier_v3_2 import (
    classify_passage_v3_2,
)


def classify_passage_v3_3(
    passage: dict[str, Any],
    page_context: str = "",
) -> dict[str, Any]:

    result = classify_passage_v3_2(
        passage,
        page_context=page_context,
    ).copy()

    text = " ".join(
        str(passage.get("text") or "").lower().split()
    )

    def set_role(role, modality, category, reason):
        result.update({
            "evidence_role": role,
            "evidence_modality": modality,
            "passage_category": category,
            "classification_basis": reason,
            "classification_version": "3.3",
            "review_status": "requires_manual_review",
            "scientific_findings_verified": False,
        })

    # Simulation blow-off with unavailable spread-rate measurement.
    if (
        re.search(r"\bblow[\s-]?off\b", text)
        and re.search(
            r"\b(partial burning|no spread rate|spread rate was determined)\b",
            text,
        )
        and re.search(r"\b(fds|simulation|simulations)\b", text)
    ):
        set_role(
            "simulation_limitation",
            "simulation",
            "candidate_limitation",
            "Simulation flame blow-off and unavailable spread-rate result.",
        )
        return result

    if result.get("evidence_role") == "simulation_result":

        # A figure introduction is not a scientific outcome.
        if (
            re.search(r"^effect of\b", text)
            and re.search(r"\bfigure\s*\d+", text)
            and re.search(r"\bsnapshots?\b", text)
            and not re.search(
                r"\b(underpredict|overpredict|decreases|increases|"
                r"reproduce|hr r|heat release)\b",
                text,
            )
        ):
            set_role(
                "simulation_figure_caption",
                "simulation",
                "candidate_background",
                "Section heading and figure introduction, not a result.",
            )
            return result

        # Definition of a measurement is methodology.
        if (
            re.search(r"\bpyrolysis length\b", text)
            and re.search(
                r"\b(determined|calculated|defined)\b",
                text,
            )
            and re.search(
                r"\b(burnout front|subtracting|position)\b",
                text,
            )
        ):
            set_role(
                "simulation_method",
                "simulation",
                "candidate_method",
                "Definition or calculation method for a simulation variable.",
            )
            return result

    # Supporting simulation data used by another measurement technique.
    if (
        result.get("evidence_role") == "simulation_mention"
        and re.search(r"\bcoflame\b", text)
        and re.search(r"\bsimulated values\b", text)
    ):
        set_role(
            "supporting_simulation_input",
            "simulation",
            "candidate_method",
            "Supporting simulated input used in a measurement or diagnostic process.",
        )
        return result

    # Figure references are not independent simulation findings.
    if (
        result.get("evidence_role") == "simulation_mention"
        and re.search(r"^(figure|fig\.)\s*\d+", text)
    ):
        set_role(
            "simulation_figure_caption",
            "simulation",
            "candidate_background",
            "Figure caption or visual-reference passage.",
        )
        return result

    # Bibliographic references to simulation papers or software.
    if (
        result.get("evidence_role") == "simulation_mention"
        and re.search(
            r"\b(user.s guide|evaluation of fds|a numerical simulation|"
            r"combustion and flame)\b",
            text,
        )
    ):
        set_role(
            "bibliographic_reference",
            "unknown",
            "candidate_background",
            "Cited research publication or simulation software reference.",
        )
        return result

    return result
