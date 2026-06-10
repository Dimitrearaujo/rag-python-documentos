"""Gera resposta com Claude usando contexto recuperado."""
from __future__ import annotations
import os
from anthropic import Anthropic

_client = None

SYSTEM = """Voce e um assistente especialista em documentos. Responda APENAS com base
no contexto fornecido. Se a resposta nao estiver no contexto, diga claramente que
nao encontrou essa informacao nos documentos. Cite a fonte quando relevante."""


def _get_client() -> Anthropic:
    global _client
    if _client is None:
        _client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    return _client


def generate(query: str, context: str, model: str | None = None) -> str:
    model = model or os.getenv("MODEL", "claude-haiku-4-5-20251001")
    prompt = f"Contexto dos documentos:\n\n{context}\n\nPergunta: {query}"
    resp = _get_client().messages.create(
        model=model,
        max_tokens=1024,
        system=SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text.strip()
