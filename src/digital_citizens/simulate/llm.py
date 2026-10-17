"""LLM clients with on-disk caching, plus a deterministic mock for tests and dry runs."""
from __future__ import annotations

import hashlib
import json
import os
import random
import re
import time
from pathlib import Path
from typing import Protocol


class LLM(Protocol):
    name: str

    def complete(self, system: str, user: str, *, temperature: float = 1.0, max_tokens: int = 300, seed: int | None = None) -> str: ...


class DiskCache:
    def __init__(self, root: str | Path = "data/cache/llm") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def key(self, *parts: object) -> str:
        return hashlib.sha256(json.dumps(parts, sort_keys=True, default=str).encode()).hexdigest()

    def get(self, key: str) -> str | None:
        f = self.root / f"{key}.json"
        if f.exists():
            return json.loads(f.read_text())["text"]
        return None

    def put(self, key: str, text: str, meta: dict | None = None) -> None:
        (self.root / f"{key}.json").write_text(json.dumps({"text": text, "meta": meta or {}}))


class AnthropicLLM:
    """Thin wrapper over the Anthropic Messages API. Needs ANTHROPIC_API_KEY in the environment."""

    def __init__(self, model: str = "claude-sonnet-5-5", cache: DiskCache | None = None, max_retries: int = 5) -> None:
        import anthropic  # imported lazily so the rest of the package works without the SDK

        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise RuntimeError("ANTHROPIC_API_KEY is not set; set it or use MockLLM for a dry run")
        self._client = anthropic.Anthropic()
        self.model = model
        self.name = model
        self.cache = cache or DiskCache()
        self.max_retries = max_retries

    def complete(self, system: str, user: str, *, temperature: float = 1.0, max_tokens: int = 300, seed: int | None = None) -> str:
        key = self.cache.key("anthropic", self.model, system, user, temperature, max_tokens, seed)
        hit = self.cache.get(key)
        if hit is not None:
            return hit
        delay = 2.0
        for attempt in range(self.max_retries):
            try:
                msg = self._client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    system=system,
                    messages=[{"role": "user", "content": user}],
                )
                text = "".join(getattr(b, "text", "") for b in msg.content)
                self.cache.put(key, text, {"model": self.model, "temperature": temperature, "seed": seed})
                return text
            except Exception as e:  # noqa: BLE001 - retry on any transient API error
                if attempt == self.max_retries - 1:
                    raise
                time.sleep(delay)
                delay *= 2
                last = e
        raise RuntimeError(f"unreachable: {last}")


class MockLLM:
    """Deterministic stand-in for an LLM so the whole pipeline can be exercised offline.

    It understands the two prompt shapes in ``prompts.py``: for a role-play question it returns a
    single letter chosen pseudo-randomly from the listed options (seeded by the prompt text and the
    sample id so the same persona gives the same answer to the same question); for a distribution
    prompt it returns a random-but-fixed set of percentages. ``bias`` lets tests inject a behaviour,
    e.g. always pick the first option, to check that metrics detect it.
    """

    name = "mock"

    def __init__(self, bias: str | None = None) -> None:
        self.bias = bias
        self.calls = 0

    def complete(self, system: str, user: str, *, temperature: float = 1.0, max_tokens: int = 300, seed: int | None = None) -> str:
        self.calls += 1
        letters = re.findall(r"^\s*([A-Z])\.\s", user, flags=re.M)
        rng = random.Random(hashlib.md5(f"{system}|{user}|{seed}".encode()).hexdigest())
        if not letters:
            return "{}"
        if "percentage" in user.lower():
            raw = [rng.random() for _ in letters]
            if self.bias == "first":
                raw = [1.0] + [0.0] * (len(letters) - 1)
            total = sum(raw)
            return json.dumps({ch: round(100 * v / total, 1) for ch, v in zip(letters, raw)})
        choice = letters[0] if self.bias == "first" else rng.choice(letters)
        return json.dumps({"answer": choice})
