import re
from typing import Any


def _normalize(text: Any) -> str:
    return " ".join(str(text or "").lower().split())


def _has(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, text) for pattern in patterns)


def _needs_context(text: str) -> bool:
    starts_with_reference = _has(
        text,
        (
            r"^(it|this|these|they|those|which|such)\b",
            r"^\d+\s+(and|or)\s+\d+\b",
        ),
    )

    ends_in_fragment = _has(
        text,
        (
            r"\b(and|or|of|with|at|from|to|that|such as)$",
            r"[\(\[]$",
        ),
    )

    return starts_with_reference or ends_in_fragment or len(text) < 45


def classify_passage_v2(
    passage: dict[str, Any],
) -> dict[str, Any]:
    text = _normalize(passage.get("text"))
    source_field = passage.get("source_field", "unknown")

    metadata_patterns = (
        r"national aeronautics and space administration",
        r"\bwww\.nasa\.gov\b",
        r"\bnasa grc\b",
        r"\b\d{1,2}\s+[a-z]+\s+20\d{2}\b",
    )

    if not text:
        return {
            "passage_category": "candidate_background",
            "evidence_role": "empty_passage",
            "evidence_modality": "unknown",
            "research_context": "unknown",
            "context_requirement": "surrounding_context_required",
            "classification_basis": "No passage text is available.",
            "review_status": "requires_manual_review",
            "scientific_findings_verified": False,
            "classification_version": "2.0",
        }

    if source_field in ("title", "bibliographic_metadata") or _has(
        text, metadata_patterns
    ):
        return {
            "passage_category": "document_metadata",
            "evidence_role": "document_metadata",
            "evidence_modality": "unknown",
            "research_context": "bibliographic",
            "context_requirement": "not_applicable",
            "classification_basis": "Bibliographic metadata detected.",
            "review_status": "metadata_only",
            "scientific_findings_verified": False,
            "classification_version": "2.0",
        }

    if re.search(r"\b(outline|table of contents)\b", text):
        return {
            "passage_category": "document_navigation",
            "evidence_role": "document_navigation",
            "evidence_modality": "unknown",
            "research_context": "document_structure",
            "context_requirement": "not_applicable",
            "classification_basis": "Document navigation text detected.",
            "review_status": "not_scientific_evidence",
            "scientific_findings_verified": False,
            "classification_version": "2.0",
        }

    simulation_signal = _has(
        text,
        (
            r"\bfds\b",
            r"\bdns\b",
            r"\bsimulation(s)?\b",
            r"\bsimulated\b",
            r"\bnumerical(ly)?\b",
        ),
    )

    experiment_signal = _has(
        text,
        (
            r"\bexperiment(s|al|ally)?\b",
            r"\btest(s|ed|ing)?\b",
            r"\bsample(s)?\b",
            r"\bobserved\b",
            r"\bmeasured\b",
            r"\bcombustion\b",
            r"\bflame spread\b",
            r"\bmicrogravity\b",
        ),
    )

    result_signal = _has(
        text,
        (
            r"\bresults? (show|showed|indicate|indicated|suggest|suggested)\b",
            r"\bfindings? (show|showed|indicate|indicated)\b",
            r"\bwas observed\b",
            r"\bwere observed\b",
            r"\bwas measured\b",
            r"\bwere measured\b",
            r"\bwas recorded\b",
            r"\bwere recorded\b",
            r"\bwas obtained\b",
            r"\bwere obtained\b",
            r"\bwas identified\b",
            r"\bwere identified\b",
            r"\bdemonstrated that\b",
            r"\bincreased by\b",
            r"\bdecreased by\b",
            r"\bspread rate\b",
            r"\bextinction\b",
            r"\boscillations?\b",
        ),
    )

    proposal_signal = _has(
        text,
        (
            r"\bit is proposed\b",
            r"\bproposed to\b",
            r"\bshould be conducted\b",
            r"\bshould be continued\b",
            r"\bshould be modernized\b",
            r"\bit is necessary to\b",
            r"\bfuture research\b",
            r"\bfuture investigation\b",
            r"\brecommendations? on\b",
            r"\bwe recommend\b",
        ),
    )

    calibration_signal = _has(
        text,
        (
            r"\bcalibration\b",
            r"\bsmoke visualization\b",
            r"\bflow uniformity\b",
            r"\bflow-core uniformity\b",
            r"\bcalibration purposes\b",
        ),
    )

    previous_study_signal = _has(
        text,
        (
            r"\bprevious (study|studies|testing|experiment|experiments|series)\b",
            r"\bearlier (study|testing|experiment|experiments)\b",
            r"\bfirst series of .* experiments\b",
            r"\bsecond series of .* experiments\b",
            r"\bprior (study|testing|experiment|experiments)\b",
        ),
    )

    citation_signal = _has(
        text,
        (
            r"\brefs?\.?\s*\d+",
            r"\breference\s+\d+\b",
        ),
    )

    if citation_signal and _has(
        text,
        (
            r"\bdrop tower\b",
            r"\bprevious testing\b",
            r"\bprevious experiments\b",
            r"\bsolid surface combustion experiments program\b",
        ),
    ):
        previous_study_signal = True

    environmental_signal = _has(
        text,
        (
            r"\boxygen concentration\b",
            r"\boxygen partial pressure\b",
            r"\bambient pressure\b",
            r"\btotal pressure\b",
            r"\bwater partial pressure\b",
            r"\bcarbon dioxide\b",
            r"\btemperature\b",
        ),
    ) and _has(
        text,
        (
            r"\bwas\b",
            r"\bwere\b",
            r"\branging from\b",
            r"\bmeasured\b",
            r"\brecorded\b",
        ),
    )

    limitation_signal = _has(
        text,
        (
            r"\blimitation(s)?\b",
            r"\buncertaint(y|ies)\b",
            r"\bdata gap(s)?\b",
            r"\bnot determined\b",
            r"\bnot available\b",
            r"\bcould not be determined\b",
            r"\bno spread rate\b",
        ),
    )

    objective_signal = _has(
        text,
        (
            r"\bobjective(s)?\b",
            r"\baim(s)? to\b",
            r"\bgoal(s)?\b",
            r"\bto investigate\b",
            r"\bto evaluate\b",
            r"\bto determine\b",
            r"\bto examine\b",
        ),
    )

    method_signal = _has(
        text,
        (
            r"\bexperimental setup\b",
            r"\bprocedure(s)?\b",
            r"\bmeasured using\b",
            r"\btested using\b",
            r"\bmethod(s)?\b",
        ),
    )

    comparison_signal = _has(
        text,
        (
            r"\bcompared with\b",
            r"\bin comparison\b",
            r"\bsimilar(ities)?\b",
            r"\bwhereas\b",
            r"\bwhile\b",
            r"\bboth\b",
            r"\bexperimentally and\b",
        ),
    )

    if proposal_signal:
        role = "proposal"
        modality = "unknown"
        basis = "Future work or proposed changes detected."

    elif calibration_signal:
        role = "apparatus_calibration"
        modality = "experiment"
        basis = "Apparatus calibration or flow-characterization context detected."

    elif simulation_signal and experiment_signal and comparison_signal:
        role = "mixed_comparison"
        modality = "mixed"
        basis = "Experimental and simulation evidence appear in a comparison."

    elif simulation_signal:
        role = (
            "simulation_result"
            if result_signal
            else "simulation_method"
        )
        modality = "simulation"
        basis = "Simulation or numerical-model context detected."

    elif previous_study_signal:
        role = "previous_study_reference"
        modality = "experiment" if experiment_signal else "unknown"
        basis = "Passage refers to earlier or cited research."

    elif environmental_signal:
        role = "environmental_condition"
        modality = "unknown"
        basis = "Experimental environment or test-condition information detected."

    elif limitation_signal:
        role = "limitation"
        modality = "unknown"
        basis = "Limitation or unavailable-result language detected."

    elif result_signal and experiment_signal:
        if _has(text, (r"\bobserved\b",)):
            role = "experimental_observation"
        else:
            role = "experimental_quantitative_result"

        modality = "experiment"
        basis = "Experimental context and result-related language detected."

    elif objective_signal:
        role = "research_objective"
        modality = "unknown"
        basis = "Research objective language detected."

    elif method_signal:
        role = "experimental_method"
        modality = "experiment"
        basis = "Experimental method or procedure language detected."

    elif _has(
        text,
        (
            r"\bresults? indicate(d)?\b",
            r"\bresults? suggest(ed)?\b",
            r"\bcan be inferred\b",
            r"\bmight be explained\b",
            r"\bmay have\b",
            r"\bit follows that\b",
        ),
    ):
        role = "interpretation"
        modality = "unknown"
        basis = "Interpretation or inference language detected."

    else:
        role = "background"
        modality = "unknown"
        basis = "No sufficiently specific evidence-role pattern detected."

    legacy_mapping = {
        "experimental_observation": "candidate_result",
        "experimental_quantitative_result": "candidate_result",
        "simulation_result": "candidate_result",
        "mixed_comparison": "candidate_result",
        "interpretation": "candidate_result",
        "apparatus_calibration": "candidate_method",
        "experimental_method": "candidate_method",
        "research_objective": "candidate_objective",
        "limitation": "candidate_limitation",
    }

    if role in legacy_mapping:
        legacy_category = legacy_mapping[role]
    else:
        legacy_category = "candidate_background"

    if role == "previous_study_reference":
        research_context = "previous_study"
    elif role == "apparatus_calibration":
        research_context = "apparatus_calibration"
    elif _has(text, (r"\bnarrow.channel\b", r"\bground testing\b", r"\bground test\b")):
        research_context = "ground_test"
    elif _has(text, (r"\bmicrogravity\b", r"\bspace experiment\b", r"\bmir\b")):
        research_context = "spaceflight_or_microgravity"
    else:
        research_context = "unknown"

    context_requirement = (
        "surrounding_context_required"
        if _needs_context(text)
        else "passage_context_available"
    )

    return {
        "passage_category": legacy_category,
        "evidence_role": role,
        "evidence_modality": modality,
        "research_context": research_context,
        "context_requirement": context_requirement,
        "classification_basis": basis,
        "review_status": "requires_manual_review",
        "scientific_findings_verified": False,
        "classification_version": "2.0",
    }
