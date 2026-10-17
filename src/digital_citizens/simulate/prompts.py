"""Prompt builders and answer parsers.

Two ways to get a population's answer out of an LLM are implemented, because the research is split
on which works better and the answer may differ by country and topic:

- role-play: one call per persona per question; the model answers *as that person*; we tally the
  answers into shares. Captures individual-level texture; risks caricature.
- distribution: one call per segment per question; the model is asked directly what share of that
  group would pick each option. Cheaper; often better calibrated; cannot give individual answers.
"""
from __future__ import annotations

import json
import re
from collections.abc import Mapping, Sequence
from typing import Literal

from ..schema import Persona, Question

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
PersonaStyle = Literal["demographic", "narrative", "record", "full"]

ATTRIBUTE_LABELS = {
    "age": "Age",
    "sex": "Sex",
    "gender": "Gender",
    "race": "Race",
    "ethnicity": "Ethnicity",
    "hispanic": "Hispanic origin",
    "education": "Highest education",
    "degree": "Highest degree",
    "region": "Region",
    "planning_area": "Neighbourhood (planning area)",
    "marital": "Marital status",
    "marital_status": "Marital status",
    "income": "Household income",
    "party": "Party identification",
    "partyid": "Party identification",
    "polviews": "Political views",
    "religion": "Religion",
    "relig": "Religion",
    "occupation": "Occupation",
    "industry": "Industry",
    "urbanicity": "Type of place",
    "work_status": "Work status",
}


def _attribute_lines(attrs: Mapping[str, object]) -> str:
    lines = []
    for k, v in attrs.items():
        if v is None or str(v).strip() in {"", "NA", "nan"}:
            continue
        lines.append(f"- {ATTRIBUTE_LABELS.get(k, k.replace('_', ' ').capitalize())}: {v}")
    return "\n".join(lines)


def persona_system_prompt(persona: Persona, style: PersonaStyle = "full", language: str = "en") -> str:
    parts = [
        "You are taking part in a survey. Answer every question honestly as the specific person described below, "
        "in the way that this particular person would actually answer, not the way an average person or an assistant would. "
        "Do not add caveats. People differ, and so should your answers.",
        f"Country of residence: {persona.country}",
    ]
    if style in {"demographic", "record", "full"} and persona.attributes:
        parts.append("About you:\n" + _attribute_lines(persona.attributes))
    if style in {"narrative", "full"} and persona.narrative:
        parts.append("Background:\n" + persona.narrative.strip())
    if style in {"record", "full"} and persona.record:
        rec = "\n".join(f"- Q: {q}\n  A: {a}" for q, a in persona.record.items())
        parts.append("Answers you gave earlier in this survey (stay consistent with who you are):\n" + rec)
    if language != "en":
        parts.append(f"Answer in {language}.")
    return "\n\n".join(parts)


def format_options(options: Sequence[str], order: Sequence[int] | None = None) -> str:
    order = list(range(len(options))) if order is None else list(order)
    return "\n".join(f"{LETTERS[i]}. {options[j]}" for i, j in enumerate(order))


def roleplay_user_prompt(question: Question, order: Sequence[int] | None = None) -> str:
    return (
        f"Question: {question.text}\n\nOptions:\n{format_options(question.options, order)}\n\n"
        'Reply with JSON only, in the form {"answer": "<letter>"}.'
    )


def segment_description(segment: Mapping[str, object], country: str) -> str:
    if not segment:
        return f"adults living in {country}"
    desc = ", ".join(f"{ATTRIBUTE_LABELS.get(k, k).lower()}: {v}" for k, v in segment.items())
    return f"adults living in {country} with {desc}"


def distribution_user_prompt(group: str, question: Question, order: Sequence[int] | None = None, n_hint: int | None = None) -> str:
    size = f" (a representative survey of about {n_hint} such people)" if n_hint else ""
    return (
        f"Consider {group}{size}. If they were asked the survey question below, what percentage of them would choose each option? "
        "Base this on what you know about this specific group, and make the groups differ when they really do differ.\n\n"
        f"Question: {question.text}\n\nOptions:\n{format_options(question.options, order)}\n\n"
        'Reply with JSON only, mapping each option letter to a percentage, e.g. {"A": 40, "B": 60}. Percentages must sum to 100.'
    )


def _json_block(text: str) -> dict | None:
    m = re.search(r"\{.*\}", text, flags=re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


def parse_answer_letter(text: str, k: int, order: Sequence[int] | None = None) -> int | None:
    """Return the ORIGINAL option index chosen (undoing any option shuffle), or None if unparsable."""
    letter = None
    obj = _json_block(text)
    if obj and isinstance(obj.get("answer"), str):
        letter = obj["answer"].strip().upper()[:1]
    else:
        # take the LAST standalone capital letter that is a valid option (models often end with the answer)
        cands = [c for c in re.findall(r"\b([A-Z])\b", text.strip().upper()) if c in LETTERS[:k]]
        letter = cands[-1] if cands else None
    if letter is None or letter not in LETTERS[:k]:
        return None
    pos = LETTERS.index(letter)
    order = list(range(k)) if order is None else list(order)
    return order[pos]


def parse_distribution(text: str, k: int, order: Sequence[int] | None = None) -> list[float] | None:
    obj = _json_block(text)
    if not obj:
        return None
    order = list(range(k)) if order is None else list(order)
    probs = [0.0] * k
    found = False
    for key, val in obj.items():
        key = str(key).strip().upper()[:1]
        if key in LETTERS[:k]:
            try:
                probs[order[LETTERS.index(key)]] = max(0.0, float(val))
                found = True
            except (TypeError, ValueError):
                continue
    if not found or sum(probs) <= 0:
        return None
    s = sum(probs)
    return [p / s for p in probs]
