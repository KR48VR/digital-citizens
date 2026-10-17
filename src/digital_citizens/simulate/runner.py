"""Run simulations and aggregate answers into distributions."""
from __future__ import annotations

import random
from collections.abc import Callable, Mapping, Sequence
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field

import numpy as np
from tqdm import tqdm

from ..schema import Distribution, Persona, Question, Response
from .llm import LLM
from .prompts import (
    PersonaStyle,
    distribution_user_prompt,
    parse_answer_letter,
    parse_distribution,
    persona_system_prompt,
    roleplay_user_prompt,
)


@dataclass
class SimConfig:
    persona_style: PersonaStyle = "full"
    temperature: float = 1.0
    n_samples: int = 1  # answers per persona per question (role-play mode)
    shuffle_options: bool = True  # randomise option order per call to measure/undo order effects
    seed: int = 0
    workers: int = 8
    language: str = "en"
    n_hint: int | None = None  # tell the model the survey size in distribution mode


def _order(k: int, shuffle: bool, rng: random.Random) -> list[int]:
    order = list(range(k))
    if shuffle:
        rng.shuffle(order)
    return order


def simulate_roleplay(personas: Sequence[Persona], questions: Sequence[Question], llm: LLM, cfg: SimConfig = SimConfig(), progress: bool = True) -> list[Response]:
    """Every persona answers every question ``cfg.n_samples`` times. Unparsable answers get index -1."""
    jobs = [(p, q, s) for p in personas for q in questions for s in range(cfg.n_samples)]

    def run(job: tuple[Persona, Question, int]) -> Response:
        p, q, s = job
        rng = random.Random(f"{cfg.seed}|{p.id}|{q.id}|{s}")
        order = _order(q.k, cfg.shuffle_options, rng)
        system = persona_system_prompt(p, cfg.persona_style, cfg.language)
        user = roleplay_user_prompt(q, order)
        text = llm.complete(system, user, temperature=cfg.temperature, seed=rng.randint(0, 2**31))
        idx = parse_answer_letter(text, q.k, order)
        return Response(persona_id=p.id, question_id=q.id, option_index=-1 if idx is None else idx, raw=text, sample=s)

    with ThreadPoolExecutor(max_workers=cfg.workers) as ex:
        it = ex.map(run, jobs)
        return list(tqdm(it, total=len(jobs), disable=not progress, desc=f"role-play ({llm.name})"))


def aggregate(
    responses: Sequence[Response],
    personas: Sequence[Persona],
    questions: Sequence[Question],
    segment_keys: Sequence[str] = (),
    min_n: int = 1,
) -> list[Distribution]:
    """Tally role-play answers into weighted shares for the population and each segment value."""
    pmap = {p.id: p for p in personas}
    qmap = {q.id: q for q in questions}
    out: list[Distribution] = []
    by_q: dict[str, list[Response]] = {}
    for r in responses:
        if r.option_index >= 0:
            by_q.setdefault(r.question_id, []).append(r)
    for qid, rs in by_q.items():
        q = qmap[qid]
        groups: dict[str, list[Response]] = {"ALL": rs}
        for key in segment_keys:
            for r in rs:
                groups.setdefault(f"{key}={pmap[r.persona_id].segment_value(key)}", []).append(r)
        for g, members in groups.items():
            if len(members) < min_n:
                continue
            counts = np.zeros(q.k)
            for r in members:
                counts[r.option_index] += pmap[r.persona_id].weight
            out.append(Distribution(question_id=qid, group=g, probs=(counts / counts.sum()).tolist(), n=len(members)))
    return out


def simulate_distribution(
    questions: Sequence[Question],
    groups: Mapping[str, str],
    llm: LLM,
    cfg: SimConfig = SimConfig(),
    progress: bool = True,
    n_repeats: int = 1,
) -> list[Distribution]:
    """Ask the model directly for each group's answer shares. ``groups`` maps group key -> description."""
    jobs = [(g, desc, q, r) for g, desc in groups.items() for q in questions for r in range(n_repeats)]

    def run(job: tuple[str, str, Question, int]) -> tuple[str, str, list[float] | None]:
        g, desc, q, r = job
        rng = random.Random(f"{cfg.seed}|{g}|{q.id}|{r}")
        order = _order(q.k, cfg.shuffle_options, rng)
        system = "You are an expert survey methodologist with deep knowledge of public opinion, consumer behaviour and how they differ across countries and groups. Be precise and calibrated."
        user = distribution_user_prompt(desc, q, order, cfg.n_hint)
        text = llm.complete(system, user, temperature=cfg.temperature, seed=rng.randint(0, 2**31))
        return g, q.id, parse_distribution(text, q.k, order)

    with ThreadPoolExecutor(max_workers=cfg.workers) as ex:
        results = list(tqdm(ex.map(run, jobs), total=len(jobs), disable=not progress, desc=f"distribution ({llm.name})"))

    acc: dict[tuple[str, str], list[list[float]]] = {}
    for g, qid, probs in results:
        if probs is not None:
            acc.setdefault((g, qid), []).append(probs)
    return [
        Distribution(question_id=qid, group=g, probs=np.mean(ps, axis=0).tolist(), n=None)
        for (g, qid), ps in acc.items()
    ]
