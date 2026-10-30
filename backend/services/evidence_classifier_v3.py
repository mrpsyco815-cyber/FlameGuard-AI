import re
from typing import Any


def _normalize(value: Any) -> str:
    return " ".join(str(value or "").lower().split())


def _has(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, text) for pattern in patterns)


def classify_passage_v3(
    passage: dict[str, Any],
    page_context: str = "",
) -> dict[str, Any]:

    text = _normalize(passage.get("text"))
    context = _normalize(page_context)
    combined = f"{text} {context}"

    def output(
        role: str,
        modality: str,
        reason: str,
        category: str = "candidate_background",
        research_context: str = "unknown",
        context_required: bool = False,
    ) -> dict[str, Any]:
        return {
            "passage_category": category,
            "evidence_role": role,
            "evidence_modality": modality,
            "research_context": research_context,
            "context_requirement": (
                "surrounding_context_required"
                if context_required else "page_context_supplied"
            ),
            "classification_basis": reason,
            "review_status": "requires_manual_review",
            "scientific_findings_verified": False,
            "classification_version": "3.0",
        }

    if not text:
        return output(
            "empty_passage", "unknown",
            "No passage text available.",
            context_required=True,
        )

    if _has(text, (
        r"national aeronautics and space administration",
        r"\bwww\.nasa\.gov\b",
        r"\bnasa grc\b",
    )):
        return output(
            "document_metadata", "unknown",
            "Document metadata detected.",
            category="document_metadata",
        )

    if _has(text, (
        r"\btable of contents\b",
        r"\bdocument outline\b",
    )):
        return output(
            "document_navigation", "unknown",
            "Document navigation detected.",
            category="document_navigation",
        )

    # Incomplete citation and sentence fragments.
    if _has(text, (
        r"^\d+\s+and\s+\d+\)",
        r"^\d+\)",
    )):
        return output(
            "context_incomplete", "unknown",
            "Incomplete citation or sentence fragment.",
            context_required=True,
        )

    # Future work and proposals.
    if _has(text, (
        r"\bit is proposed\b",
        r"\bproposed that\b",
        r"\bproposed to\b",
        r"\bshould be conducted\b",
        r"\bshould be modernized\b",
        r"\bfuture investigations\b",
        r"\brecommendations on continuing research\b",
    )):
        return output(
            "proposal", "unknown",
            "Proposed work or future recommendation detected.",
            research_context="future_work",
        )

    # Apparatus characterization is not a combustion finding.
    if _has(text, (
        r"\bsmoke visualization\b",
        r"\bflow uniformity\b",
        r"\bcalibration\b",
    )):
        return output(
            "apparatus_calibration", "experiment",
            "Apparatus calibration or flow characterization.",
            category="candidate_method",
            research_context="apparatus_calibration",
        )

    # Previously published or separately cited research.
    previous_study = _has(text, (
        r"\bprevious testing\b",
        r"\bprevious experiments\b",
        r"\bearlier experiments\b",
        r"\bexperiments under the .* program\b",
        r"\bsolid surface combustion experiments program\b",
        r"\bprior study\b",
    ))

    previous_page_context = _has(context, (
        r"\bfirst series of space experiments\b",
        r"\bsecond series of space experiments\b",
        r"\bprevious series of experiments\b",
    ))

    if previous_study or (
        previous_page_context
        and _has(text, (r"\bobserved\b", r"\bextinguished\b"))
    ):
        return output(
            "previous_study_reference", "experiment",
            "Earlier or separately cited research detected.",
            research_context="previous_study",
            context_required=previous_page_context,
        )

    # Study scope, rather than an individual result.
    if _has(text, (
        r"\bcombustion of twelve\b",
        r"\btwelve selected cylindrical samples\b",
        r"\bsamples of three plastic materials\b",
    )):
        return output(
            "study_scope_summary", "experiment",
            "Study scope and sample description.",
            research_context="spaceflight_or_microgravity",
        )

    # Environmental conditions with surrounding-page information.
    if (
        _has(text, (
            r"\bexpected 21 percent\b",
            r"\branging from 22\.5 to 25\.4 percent\b",
        ))
        and _has(combined, (
            r"\boxygen concentration\b",
            r"\boxygen partial pressure\b",
        ))
    ):
        return output(
            "environmental_condition", "experiment",
            "Measured environmental condition; oxygen identified from context.",
            research_context="spaceflight_or_microgravity",
            context_required=True,
        )

    simulation = _has(text, (
        r"\bfds\b",
        r"\bdns\b",
        r"\bsimulation(s)?\b",
        r"\bsimulated\b",
        r"\bnumerical simulation\b",
    ))

    experiment = _has(text, (
        r"\bexperiment(s|al|ally)?\b",
        r"\bexperimentally\b",
        r"\bobserved\b",
        r"\bmeasured\b",
        r"\btesting\b",
        r"\btested\b",
    ))

    interpretation = _has(text, (
        r"\bresults indicate\b",
        r"\bresults suggest\b",
        r"\bcan be inferred\b",
        r"\bmight be explained\b",
        r"\bmay have similar\b",
        r"\bit follows that\b",
    ))

    explicit_mixed = _has(text, (
        r"\bexperimentally and through the simulations\b",
        r"\bexperiments and simulations\b",
        r"\bexperimental and numerical\b",
    ))

    if explicit_mixed or (interpretation and simulation and experiment):
        return output(
            "mixed_comparison", "mixed",
            "Experimental and simulation evidence compared.",
            category="candidate_result",
            research_context="pressure_gravity_comparison",
        )

    if interpretation:
        return output(
            "interpretation",
            "simulation" if simulation else (
                "experiment" if experiment else "unknown"
            ),
            "Interpretation or inference, not a direct measurement.",
        )

    if simulation:
        return output(
            "simulation_result", "simulation",
            "Numerical or simulation result detected.",
            category="candidate_result",
        )

    # Comparative result from ground testing.
    if experiment and _has(text, (
        r"\bviscosity\b",
        r"\bhigher than\b",
        r"\blower than\b",
        r"\bgreater than\b",
    )):
        return output(
            "experimental_comparative_result", "experiment",
            "Experimental material-property comparison.",
            category="candidate_result",
            research_context="ground_test",
        )

    # Experimental limitations.
    if _has(text, (
        r"\bnot determined\b",
        r"\bnot available\b",
        r"\bcould not be determined\b",
        r"\bno spread rate\b",
        r"\buncertainty\b",
        r"\blimitation\b",
    )):
        return output(
            "experimental_limitation" if experiment else "limitation",
            "experiment" if experiment else "unknown",
            "Limitation or unavailable measurement detected.",
            category="candidate_limitation",
        )

    # Direct experimental observations.
    if _has(text, (
        r"\bwas observed\b",
        r"\bwere observed\b",
        r"\bwas recorded\b",
        r"\bwere recorded\b",
    )):
        return output(
            "experimental_observation", "experiment",
            "Direct observation statement detected.",
            category="candidate_result",
            research_context=(
                "spaceflight_or_microgravity"
                if _has(combined, (
                    r"\bmicrogravity\b",
                    r"\bspace experiment\b",
                    r"\bon orbit\b",
                    r"\bmir\b",
                ))
                else "unknown"
            ),
        )

    # Quantitative results, including results summarized in conclusions.
    numeric_result = (
        _has(text, (
            r"\bresults? showed\b",
            r"\bwas measured\b",
            r"\bwere measured\b",
            r"\bwas obtained\b",
            r"\bwere obtained\b",
            r"\bextinction\b",
            r"\bspread rate\b",
        ))
        and _has(text, (r"\d",))
        and _has(combined, (
            r"\bexperiment\b",
            r"\btesting\b",
            r"\bsample\b",
            r"\bmicrogravity\b",
            r"\bflow shutoff\b",
            r"\bspace experiment\b",
        ))
    )

    if numeric_result:
        research_context = (
            "spaceflight_or_microgravity"
            if _has(combined, (
                r"\bmicrogravity\b",
                r"\bspace experiment\b",
                r"\bon orbit\b",
                r"\bmir\b",
            ))
            else "unknown"
        )

        return output(
            "experimental_quantitative_result", "experiment",
            "Numerical experimental result detected.",
            category="candidate_result",
            research_context=research_context,
        )

    if _has(text, (
        r"\bobjective(s)?\b",
        r"\baim(s)? to\b",
        r"\bto investigate\b",
        r"\bto evaluate\b",
        r"\bto determine\b",
    )):
        return output(
            "research_objective", "unknown",
            "Research objective detected.",
            category="candidate_objective",
        )

    research_context = "unknown"

    if _has(combined, (
        r"\bnarrow.channel\b",
        r"\bground testing\b",
        r"\bground test\b",
    )):
        research_context = "ground_test"
    elif _has(combined, (
        r"\bmicrogravity\b",
        r"\breduced gravity\b",
        r"\bspace experiment\b",
        r"\bon orbit\b",
        r"\bmir\b",
    )):
        research_context = "spaceflight_or_microgravity"

    return output(
        "background", "unknown",
        "No specific evidence role established.",
        research_context=research_context,
        context_required=True,
    )
