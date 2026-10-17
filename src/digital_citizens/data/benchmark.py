"""The Benchmark container: questions + real human answer shares (+ optional respondent-level table)."""
from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from ..schema import Distribution, Question

Key = tuple[str, str]  # (question_id, group)


@dataclass
class Benchmark:
    name: str
    country: str
    questions: list[Question]
    real: dict[Key, Distribution]  # ground truth shares; group "ALL" plus segments like "sex=female"
    respondents: pd.DataFrame | None = None  # optional person-level table (one row per respondent)
    segment_keys: list[str] = field(default_factory=list)  # demographic columns used for segments
    notes: str = ""

    @property
    def qmap(self) -> dict[str, Question]:
        return {q.id: q for q in self.questions}

    def groups(self) -> list[str]:
        return sorted({g for _, g in self.real})

    def segments_for(self, qid: str) -> dict[str, Distribution]:
        return {g: d for (q, g), d in self.real.items() if q == qid and g != "ALL"}

    def subset(self, question_ids: list[str]) -> "Benchmark":
        keep = set(question_ids)
        return Benchmark(
            name=self.name,
            country=self.country,
            questions=[q for q in self.questions if q.id in keep],
            real={k: v for k, v in self.real.items() if k[0] in keep},
            respondents=self.respondents,
            segment_keys=list(self.segment_keys),
            notes=self.notes,
        )
