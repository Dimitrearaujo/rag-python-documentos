"""Recupera chunks relevantes para uma query."""
from __future__ import annotations
from rag.embeddings import embed
from rag.vectorstore import search


def retrieve(query: str, top_k: int = 5) -> list[dict]:
    """Retorna chunks relevantes para a query com score de similaridade."""
    query_emb = embed(query)
    return search(query_emb, top_k=top_k)


def format_context(chunks: list[dict]) -> str:
    """Formata chunks em contexto para o prompt."""
    parts = []
    for i, c in enumerate(chunks, 1):
        parts.append(f"[{i}] (fonte: {c['source']})\n{c['content']}")
    return "\n\n".join(parts)
