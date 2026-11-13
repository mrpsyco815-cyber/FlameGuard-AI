"""Deterministic scientific query normalization and explainable scoring."""

import re
from dataclasses import dataclass


SCIENTIFIC_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
    "in", "is", "it", "of", "on", "or", "that", "the", "their", "this",
    "to", "was", "were", "what", "when", "with",
}

SYNONYMS = {
    "microgravity": {"microgravity", "reduced gravity", "reduced-gravity"},
    "flame spread": {"flame", "spread", "propagation", "propagate"},
    "oxygen concentration": {"oxygen", "o2", "concentration", "level"},
    "polyethylene": {"polyethylene", "pe"},
    "polymethyl methacrylate": {"polymethyl", "methacrylate", "pmma"},
    "solid fuel combustion": {"solid", "fuel", "combustion"},
    "flame extinction": {"extinction", "extinguish"},
    "fire detection": {"detection", "detector", "detect"},
    "fire suppression": {"suppression", "suppress"},
    "fire hazard": {"hazard", "hazards", "safety"},
}

PHENOMENA = {
    "flame spread": {"flame spread", "flame propagation", "spread", "propagation"},
    "flame extinction": {"flame extinction", "extinction", "extinguish"},
    "combustion": {"combustion", "burning"},
    "fire detection": {"fire detection", "detector", "detection"},
    "fire suppression": {"fire suppression", "suppress", "suppression"},
}

ENVIRONMENTS = {
    "spacecraft": {"spacecraft", "spaceflight", "space station", "iss"},
    "spacecraft cabin": {"cabin", "compartment", "enclosed"},
    "microgravity": {"microgravity", "reduced gravity", "low gravity"},
}

OXYGEN_QUANTITATIVE_PATTERN = re.compile(
    r"(?:oxygen|o2)[^.\n]{0,40}?\d+(?:\.\d+)?\s*(?:%|percent|ppm)"
    r"|\d+(?:\.\d+)?\s*(?:%|percent|ppm)[^.\n]{0,40}?(?:oxygen|o2)",
    re.IGNORECASE,
)

MATERIALS = {
    "pmma": "polymethyl methacrylate",
    "polymethyl methacrylate": "polymethyl methacrylate",
    "pe": "polyethylene",
    "polyethylene": "polyethylene",
}

UNIT_PATTERN = re.compile(
    r"\b\d+(?:\.\d+)?\s*(?:%|percent|ppm|kpa|pa|bar|atm|cm/s|m/s|mm/s|g)\b",
    re.IGNORECASE,
)


def _stem(token: str) -> str:
    if len(token) > 4 and token.endswith("ies"):
        return token[:-3] + "y"
    if len(token) > 4 and token.endswith("es"):
        return token[:-2]
    if len(token) > 3 and token.endswith("s") and not token.endswith("ss"):
        return token[:-1]
    return token


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^\w.%/+ -]", " ", value.lower())).strip()


def scientific_tokens(value: str) -> list[str]:
    tokens = re.findall(r"[a-z0-9]+(?:\.[0-9]+)?|%", normalize_text(value))
    return [_stem(token) for token in tokens if token not in SCIENTIFIC_STOPWORDS]


@dataclass(frozen=True)
class ScientificQuery:
    original: str
    normalized: str
    tokens: tuple[str, ...]
    concepts: tuple[str, ...] = ()
    materials: tuple[str, ...] = ()
    units: tuple[str, ...] = ()
    numbers: tuple[str, ...] = ()
    conditions: tuple[str, ...] = ()
    contradictions: tuple[str, ...] = ()
    phenomena: tuple[str, ...] = ()
    environments: tuple[str, ...] = ()
    measurement_required: bool = False


def parse_query(query: str) -> ScientificQuery:
    if not isinstance(query, str) or not query.strip():
        raise ValueError("A non-empty research query is required.")
    normalized = normalize_text(query)
    tokens = tuple(dict.fromkeys(scientific_tokens(normalized)))
    if not tokens:
        raise ValueError("Query must contain at least one meaningful search term.")
    lower = normalized
    concepts = tuple(
        concept for concept, alternatives in SYNONYMS.items()
        if any(term in lower for term in alternatives)
    )
    materials = tuple(
        canonical for term, canonical in MATERIALS.items() if term in lower
    )
    units = tuple(UNIT_PATTERN.findall(normalized))
    numbers = tuple(re.findall(r"\b\d+(?:\.\d+)?\b", normalized))
    conditions = tuple(
        condition for condition in ("microgravity", "reduced gravity", "low pressure",
                                    "oxygen", "ambient pressure", "spaceflight")
        if condition in lower
    )
    phenomena = tuple(
        phenomenon for phenomenon, alternatives in PHENOMENA.items()
        if any(term in lower for term in alternatives)
    )
    environments = tuple(
        environment for environment, alternatives in ENVIRONMENTS.items()
        if any(term in lower for term in alternatives)
    )
    measurement_required = (
        "oxygen" in lower
        and any(term in lower for term in (
            "concentration", "percentage", "percent", "limiting", "extinction",
        ))
    )
    contradictions = []
    if "polymethyl methacrylate" in materials and "liquid" in tokens:
        contradictions.append("PMMA is specified together with liquid fuel.")
    if "microgravity" in lower and "normal gravity" in lower:
        contradictions.append("microgravity is specified together with normal gravity.")
    return ScientificQuery(
        query, normalized, tokens, concepts, tuple(dict.fromkeys(materials)),
        units, numbers, conditions, tuple(contradictions), phenomena,
        environments, measurement_required,
    )


def score_text(query: ScientificQuery, text: str) -> dict:
    """Score text with visible components; no score is a scientific conclusion."""
    candidate = normalize_text(text)
    candidate_tokens = set(scientific_tokens(candidate))

    if query.contradictions:
        return {
            "score": 0.0,
            "matched_terms": [],
            "concept_matches": [],
            "material_matches": [],
            "numeric_matches": [],
            "condition_matches": [],
            "phenomenon_matches": [],
            "environment_matches": [],
            "quantitative_measurement_matches": [],
            "measurement_required": query.measurement_required,
            "matching_reasons": [
                f"query contradiction: {reason}"
                for reason in query.contradictions
            ],
        }

    def contains_term(term: str) -> bool:
        return term in candidate if " " in term else _stem(term) in candidate_tokens

    matched = sorted(set(query.tokens).intersection(candidate_tokens))
    token_score = len(matched) / len(query.tokens)
    concept_matches = [
        concept for concept in query.concepts
        if any(contains_term(term) for term in SYNONYMS[concept])
    ]
    material_matches = [
        material for material in query.materials
        if contains_term(material) or any(
            contains_term(alias) for alias, canonical in MATERIALS.items()
            if canonical == material
        )
    ]
    numeric_matches = [
        value for value in query.numbers if value in candidate
    ]
    condition_matches = [
        condition for condition in query.conditions if condition in candidate
    ]
    phenomenon_matches = [
        phenomenon for phenomenon in query.phenomena
        if any(term in candidate for term in PHENOMENA[phenomenon])
    ]
    environment_matches = [
        environment for environment in query.environments
        if any(term in candidate for term in ENVIRONMENTS[environment])
    ]
    quantitative_measurement_matches = (
        OXYGEN_QUANTITATIVE_PATTERN.findall(candidate)
        if query.measurement_required else []
    )
    score = (
        token_score * 0.45
        + (0.25 if query.concepts and concept_matches else 0)
        + (0.15 if query.materials and material_matches else 0)
        + (0.10 if query.numbers and numeric_matches else 0)
        + (0.05 if query.conditions and condition_matches else 0)
        + (0.10 if query.environments and environment_matches else 0)
        + (0.10 if query.phenomena and phenomenon_matches else 0)
        + (0.10 if quantitative_measurement_matches else 0)
    )
    reasons = []
    if matched:
        reasons.append(f"matched terms: {', '.join(matched)}")
    if concept_matches:
        reasons.append(f"scientific concepts: {', '.join(concept_matches)}")
    if material_matches:
        reasons.append(f"material: {', '.join(material_matches)}")
    if numeric_matches:
        reasons.append(f"numeric values: {', '.join(numeric_matches)}")
    if condition_matches:
        reasons.append(f"conditions: {', '.join(condition_matches)}")
    if phenomenon_matches:
        reasons.append(f"phenomena: {', '.join(phenomenon_matches)}")
    if environment_matches:
        reasons.append(f"environments: {', '.join(environment_matches)}")
    if quantitative_measurement_matches:
        reasons.append("quantitative oxygen measurement context")
    if query.materials and not material_matches:
        score *= 0.25
        reasons.append("material mismatch penalty")
    if query.environments and not environment_matches:
        score *= 0.45
        reasons.append("environment mismatch penalty")
    if query.measurement_required and not quantitative_measurement_matches:
        score *= 0.45
        reasons.append("quantitative measurement context missing")
    if not candidate.strip():
        score = 0.0
        reasons.append("empty excerpt")
    return {
        "score": round(min(score, 1.0), 4),
        "matched_terms": matched,
        "concept_matches": concept_matches,
        "material_matches": material_matches,
        "numeric_matches": numeric_matches,
        "condition_matches": condition_matches,
        "phenomenon_matches": phenomenon_matches,
        "environment_matches": environment_matches,
        "quantitative_measurement_matches": quantitative_measurement_matches,
        "measurement_required": query.measurement_required,
        "matching_reasons": reasons,
    }
