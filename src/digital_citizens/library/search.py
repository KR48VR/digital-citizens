"""Find the closest previously asked question in a library of surveys, by wording.

Two matchers: ``tfidf`` (word overlap; cheap, misses synonyms such as 'churches' vs 'organized religion') and
``semantic`` (a small sentence-embedding model run locally; handles synonyms). Both are scored against the
hand-checked crosswalk in the library test.
"""
from __future__ import annotations

import re
from collections import Counter

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def strip_shared_stems(texts: dict[str, str], max_share: float = 0.25) -> dict[str, str]:
    """Drop words that appear in more than ``max_share`` of a survey's questions (battery stems such as
    'how much confidence do you have in...'), so matching runs on what is specific to each item."""
    toks = {k: re.findall(r"[a-z0-9']+", v.lower()) for k, v in texts.items()}
    df = Counter(w for ws in toks.values() for w in set(ws))
    limit = max_share * len(texts)
    return {k: " ".join(w for w in ws if df[w] <= limit) or texts[k] for k, ws in toks.items()}


def _rank(S: np.ndarray, q_ids: list[str], l_ids: list[str], top: int) -> dict[str, list[tuple[str, float]]]:
    out = {}
    for i, qid in enumerate(q_ids):
        order = np.argsort(-S[i])[:top]
        out[qid] = [(l_ids[j], float(S[i, j])) for j in order]
    return out


def match_questions(queries: dict[str, str], library: dict[str, str], top: int = 3, method: str = "tfidf", strip_stems: bool = False) -> dict[str, list[tuple[str, float]]]:
    """For each query question, the ``top`` library questions by similarity of wording."""
    if strip_stems:
        queries, library = strip_shared_stems(queries), strip_shared_stems(library)
    q_ids, l_ids = list(queries), list(library)
    if method == "tfidf":
        vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), sublinear_tf=True).fit([*queries.values(), *library.values()])
        S = cosine_similarity(vec.transform([queries[i] for i in q_ids]), vec.transform([library[i] for i in l_ids]))
    elif method == "semantic":
        from sentence_transformers import SentenceTransformer  # local model, no API

        model = SentenceTransformer(EMBED_MODEL)
        Q = model.encode([queries[i] for i in q_ids], normalize_embeddings=True)
        L = model.encode([library[i] for i in l_ids], normalize_embeddings=True)
        S = Q @ L.T
    else:
        raise ValueError(method)
    return _rank(np.asarray(S), q_ids, l_ids, top)
