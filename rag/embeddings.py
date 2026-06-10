"""Embeddings via OpenAI text-embedding-3-small (1536 dims)."""
from __future__ import annotations
import os
import json
import hashlib
import math
from pathlib import Path

_client = None
_CACHE_DIR = Path.home() / ".rag-cache" / "embeddings"


def _get_client():
    global _client
    if _client is None:
        from openai import OpenAI
        _client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    return _client


def _cache_path(text: str) -> Path:
    key = hashlib.md5(text.encode()).hexdigest()
    return _CACHE_DIR / f"{key}.json"


def embed(text: str, use_cache: bool = True) -> list[float]:
    """Retorna vetor de embedding para o texto."""
    if use_cache:
        cp = _cache_path(text)
        if cp.exists():
            return json.loads(cp.read_text())

    resp = _get_client().embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    vec = resp.data[0].embedding

    if use_cache:
        _CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cp.write_text(json.dumps(vec))

    return vec


def embed_batch(texts: list[str], use_cache: bool = True) -> list[list[float]]:
    """Embeds lista de textos, com cache por item."""
    results = []
    to_embed: list[tuple[int, str]] = []

    for i, t in enumerate(texts):
        if use_cache:
            cp = _cache_path(t)
            if cp.exists():
                results.append((i, json.loads(cp.read_text())))
                continue
        to_embed.append((i, t))

    if to_embed:
        resp = _get_client().embeddings.create(
            model="text-embedding-3-small",
            input=[t for _, t in to_embed],
        )
        _CACHE_DIR.mkdir(parents=True, exist_ok=True)
        for (i, t), emb_obj in zip(to_embed, resp.data):
            vec = emb_obj.embedding
            results.append((i, vec))
            if use_cache:
                _cache_path(t).write_text(json.dumps(vec))

    results.sort(key=lambda x: x[0])
    return [vec for _, vec in results]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)
