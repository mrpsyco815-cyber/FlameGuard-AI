import re
from typing import Any

from backend.services.evidence_classifier_v3_1 import (
    classify_passage_v3_1,
)


def _normalize(value: Any) -> str:
    return " ".join(str(value or "").lower().split())


def _has(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(p, text) for p in patterns)


def classify_passage_v3_2(
    passage: dict[str, Any],
    page_context: str = "",
) -> dict[str, Any]:

    text = _normalize(passage.get("text"))
    context = _normalize(page_context)
    combined = f"{text} {context}"

    result = classify_passage_v3_1(
        passage,
        page_context=page_context,
    ).copy()

    def update(
        role: str,
        modality: str,
        category: str,
        reason: str,
        research_context: str | None = None,
    ) -> dict[str, Any]:
        result.update({
            "evidence_role": role,
            "evidence_modality": modality,
            "passage_category": category,
            "classification_basis": reason,
            "classification_version": "3.2",
            "review_status": "requires_manual_review",
            "scientific_findings_verified": False,
        })

        if research_context:
            result["research_context"] = research_context

        return result

    if not text:
        return update(
            "empty_passage",
            "unknown",
            "candidate_background",
            "No passage text available.",
        )

    # Administrative form language is not scientific limitation.
    if _has(text, (
        r"\blimitation of abstract\b",
        r"\blimitation of report\b",
        r"\blimitation of this page\b",
        r"\bstandard form 298\b",
        r"\bnsn\s+7540\b",
    )):
        return update(
            "administrative_metadata",
            "unknown",
            "document_metadata",
            "Administrative report-form classification detected.",
        )

    # Author affiliations and institutional information.
    if (
        passage.get("pdf_page_number") == 1
        and _has(text, (
            r"\bdepartment of\b",
            r"\buniversity\b",
            r"\bresearch center\b",
            r"\bmississippi state\b",
        ))
        and not _has(text, (
            r"\bresults showed\b",
            r"\bwas observed\b",
            r"\bwas measured\b",
        ))
    ):
        return update(
            "institutional_metadata",
            "unknown",
            "document_metadata",
            "Author affiliation or institutional information detected.",
        )

    # Bibliography and cited paper titles.
    reference_signal = (
        _has(text, (
            r"\bet\s+a/?l\.?",
            r"\bproceedings\b",
            r"\bnasa cp\b",
            r"\bcombustion and flame\b",
            r"\bphysical modeling method\b",
        ))
        and _has(text, (
            r"\bjournal\b",
            r"\bvolume\b",
            r"\bvol\.\b",
            r"\bpp\.\b",
            r"\bthe study of\b",
            r"\btheory\b",
            r"\ba numerical simulation\b",
            r"\bresearch\b",
        ))
    )

    if reference_signal:
        return update(
            "bibliographic_reference",
            "unknown",
            "candidate_background",
            "Cited publication or bibliography entry detected.",
            "previous_study",
        )

    # Simulation-related objectives are not simulation results.
    if _has(text, (
        r"\bobjective\b",
        r"\boverall objective\b",
        r"\bspecific objective\b",
        r"\bthe aim of\b",
        r"\bthe goal of\b",
    )):
        if _has(combined, (
            r"\bsimulation(s)?\b",
            r"\bnumerical model\b",
            r"\bfds\b",
            r"\bdns\b",
        )):
            return update(
                "simulation_objective",
                "simulation",
                "candidate_objective",
                "Objective of numerical or simulation research detected.",
            )

    # Figure captions describe figures; they are not raw results.
    if re.match(r"^(figure|fig\.)\s*\d+", text):
        modality = (
            "mixed"
            if _has(text, (
                r"\bexperiment(s|al)?\b",
            )) and _has(text, (
                r"\bsimulation(s)?\b",
                r"\bfds\b",
                r"\bdns\b",
            ))
            else "simulation"
            if _has(text, (r"\bsimulation(s)?\b", r"\bfds\b", r"\bdns\b"))
            else "unknown"
        )

        return update(
            "figure_caption",
            modality,
            "candidate_background",
            "Figure caption or visual description; inspect its underlying data separately.",
        )

    simulation_signal = _has(text, (
        r"\bsimulation(s)?\b",
        r"\bsimulated\b",
        r"\bsimulator\b",
        r"\bnumerical model\b",
        r"\bfds\b",
        r"\bdns\b",
    ))

    experimental_signal = _has(text, (
        r"\bexperiment(s|al|ally)?\b",
        r"\bexperimental data\b",
        r"\bexperimental measurements\b",
    ))

    # Simulation setup, parameters and procedures.
    setup_signal = _has(text, (
        r"\bmodel description\b",
        r"\bnumerical model\b",
        r"\bcell size\b",
        r"\bgrid\b",
        r"\bcomputational field\b",
        r"\bcomputational domain\b",
        r"\bboundary condition\b",
        r"\bradiation solver\b",
        r"\bradiation transport equation\b",
        r"\bdns mode\b",
        r"\bfds version\b",
        r"\bsimulations are initiated\b",
        r"\bsimulations run\b",
        r"\bmodel is set to\b",
        r"\bmesh\b",
        r"\bsolver\b",
    ))

    if simulation_signal and setup_signal:
        return update(
            "simulation_method",
            "simulation",
            "candidate_method",
            "Numerical model, simulation configuration or method detected.",
        )

    # A result needs an outcome, not merely a simulation mention.
    simulation_outcome = _has(text, (
        r"\bsimulations? show(s|ed)?\b",
        r"\bsimulation results?\b",
        r"\bfds confirms?\b",
        r"\bsimulations? (reproduce|predicted|predict|underpredict|overpredict)\b",
        r"\bunderpredict(s|ed)?\b",
        r"\boverpredict(s|ed)?\b",
        r"\bqualitatively reproduce\b",
        r"\bresults obtained from the simulations\b",
        r"\bin the simulations\b.*\b(decreases?|increases?|lower|higher)\b",
        r"\bfrom the figure it is seen\b",
    ))

    comparison_signal = _has(text, (
        r"\bcompared with\b",
        r"\bcomparison\b",
        r"\bboth the experiments and\b",
        r"\bexperiments and the fds simulations\b",
        r"\bexperimental and numerical\b",
        r"\bexperimentally and through the simulations\b",
        r"\bagree with the experimental\b",
    ))

    if simulation_signal and simulation_outcome:
        if experimental_signal and comparison_signal:
            return update(
                "mixed_comparison",
                "mixed",
                "candidate_result",
                "Simulation outcome explicitly compared with experimental evidence.",
                "experimental_simulation_comparison",
            )

        return update(
            "simulation_result",
            "simulation",
            "candidate_result",
            "Simulation outcome or numerical result detected.",
        )

    # A passage may express an experimental/simulation interpretation
    # without repeating both modalities in the sentence itself.
    if (
        result.get("evidence_role") == "interpretation"
        and _has(text, (
            r"\bresults indicate\b",
            r"\bresults suggest\b",
            r"\bsimilar characteristics\b",
        ))
        and _has(combined, (
            r"\bfds\b",
            r"\bsimulations?\b",
        ))
        and _has(combined, (
            r"\bexperiments?\b",
            r"\bexperimental data\b",
        ))
    ):
        return update(
            "mixed_comparison",
            "mixed",
            "candidate_result",
            "Interpretation supported by experimental and simulation context.",
            "experimental_simulation_comparison",
        )

    if simulation_signal:
        return update(
            "simulation_mention",
            "simulation",
            "candidate_method",
            "Simulation is mentioned, but a result or outcome is not established.",
        )

    # Preserve genuine scientific uncertainty and unavailable measurements.
    if _has(text, (
        r"\buncertaint(y|ies)\b",
        r"\bmeasurement error\b",
        r"\berror analysis\b",
        r"\bno spread rate was determined\b",
        r"\bcould not be determined\b",
        r"\bnot determined due to\b",
    )):
        return update(
            "scientific_limitation",
            "experiment" if experimental_signal else "unknown",
            "candidate_limitation",
            "Scientific uncertainty or unavailable measurement detected.",
        )

    return result
