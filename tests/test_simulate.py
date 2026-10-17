from digital_citizens.evaluate import metrics as M
from digital_citizens.schema import Persona, Question
from digital_citizens.simulate.llm import MockLLM
from digital_citizens.simulate.prompts import (
    distribution_user_prompt,
    parse_answer_letter,
    parse_distribution,
    persona_system_prompt,
    roleplay_user_prompt,
)
from digital_citizens.simulate.runner import SimConfig, aggregate, simulate_distribution, simulate_roleplay

Q = Question(id="q1", text="How happy are you?", options=["Very happy", "Pretty happy", "Not too happy"], ordinal=True)
P = [Persona(id=f"p{i}", country="Singapore", attributes={"age": 30 + i, "sex": "Female" if i % 2 else "Male"}, record={"Do you trust most people?": "Yes"}) for i in range(10)]


def test_prompts_contain_layers_by_style():
    s = persona_system_prompt(P[0], "demographic")
    assert "Sex: Male" in s and "trust" not in s
    s = persona_system_prompt(P[0], "full")
    assert "Sex: Male" in s and "Do you trust most people?" in s
    u = roleplay_user_prompt(Q, [2, 0, 1])
    assert "A. Not too happy" in u and "C. Pretty happy" in u


def test_parsers_undo_shuffle():
    assert parse_answer_letter('{"answer": "A"}', 3, [2, 0, 1]) == 2
    assert parse_answer_letter("I would say B.", 3) == 1
    assert parse_answer_letter('{"answer": "Z"}', 3) is None
    d = parse_distribution('{"A": 50, "B": 25, "C": 25}', 3, [2, 0, 1])
    assert d == [0.25, 0.25, 0.5]
    assert parse_distribution("no json here", 3) is None


def test_roleplay_pipeline_with_mock_and_segments():
    llm = MockLLM()
    cfg = SimConfig(n_samples=2, workers=2)
    resp = simulate_roleplay(P, [Q], llm, cfg, progress=False)
    assert len(resp) == 20 and all(r.option_index >= 0 for r in resp)
    dists = aggregate(resp, P, [Q], segment_keys=["sex"])
    groups = {d.group for d in dists}
    assert groups == {"ALL", "sex=Female", "sex=Male"}
    for d in dists:
        assert abs(sum(d.probs) - 1) < 1e-9


def test_biased_mock_is_detected_by_metrics():
    llm = MockLLM(bias="first")
    dists = aggregate(simulate_roleplay(P, [Q], llm, SimConfig(workers=1, shuffle_options=False), progress=False), P, [Q])
    sim = dists[0].probs
    assert sim[0] == 1.0
    assert M.entropy_ratio(sim, [0.3, 0.5, 0.2]) == 0.0


def test_distribution_mode():
    llm = MockLLM()
    out = simulate_distribution([Q], {"sex=Female": "women in Singapore", "sex=Male": "men in Singapore"}, llm, SimConfig(workers=1), progress=False, n_repeats=2)
    assert len(out) == 2 and all(abs(sum(d.probs) - 1) < 1e-9 for d in out)
    assert "percentage" in distribution_user_prompt("women in Singapore", Q)
