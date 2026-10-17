"""Core data types shared across the package."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class Persona(BaseModel):
    """One digital citizen.

    A persona is grounded in three layers, each optional but increasingly valuable:

    1. ``attributes``: structured demographics (age, sex, education, region, ...). Cheap,
       available everywhere, but on their own they make the model answer like "the average
       45-year-old woman with a degree", which is the documented regression-to-the-mean failure.
    2. ``record``: the real survey answers of a real (anonymised) respondent this persona is
       anchored to (question text -> answer label). This is the layer that research shows
       carries most of the individual signal (interview/record-based agents beat demographic-only ones).
    3. ``narrative``: free text (e.g. an NVIDIA Nemotron persona paragraph or an interview summary).
       Useful for realism but LLM-written text can smuggle in stereotypes, so it must be ablated.
    """

    id: str
    country: str
    attributes: dict[str, Any] = Field(default_factory=dict)
    record: dict[str, str] = Field(default_factory=dict)
    narrative: str | None = None
    weight: float = 1.0
    source: str = ""

    def segment_value(self, key: str) -> str:
        v = self.attributes.get(key)
        return "NA" if v is None else str(v)


class Question(BaseModel):
    """A closed-ended survey question with a fixed option list."""

    id: str
    text: str
    options: list[str]
    ordinal: bool = False  # True if options form an ordered scale (lets us use a distance metric)
    source: str = ""
    topic: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @property
    def k(self) -> int:
        return len(self.options)


class Distribution(BaseModel):
    """Answer shares for one question in one group (population or segment)."""

    question_id: str
    group: str  # "ALL" or e.g. "sex=Female" or "country=Singapore"
    probs: list[float]
    n: int | None = None  # number of human respondents (None for simulated/predicted)

    def normalised(self) -> list[float]:
        s = sum(self.probs)
        return [p / s for p in self.probs] if s > 0 else [1.0 / len(self.probs)] * len(self.probs)


class Response(BaseModel):
    """One simulated (or real) answer by one persona to one question."""

    persona_id: str
    question_id: str
    option_index: int
    raw: str | None = None
    sample: int = 0
