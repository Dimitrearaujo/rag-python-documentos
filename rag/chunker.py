"""Divisao de texto em chunks com overlap."""
from __future__ import annotations


def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[str]:
    """
    Divide texto em chunks de N palavras com overlap.
    Prefere quebrar em fim de frase quando possivel.
    """
    words = text.split()
    chunks: list[str] = []
    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])

        # Tenta encerrar no fim de frase mais proximo
        if end < len(words):
            for i in range(end - 1, max(start + chunk_size // 2, start) - 1, -1):
                if words[i].endswith((".", "!", "?")):
                    chunk = " ".join(words[start : i + 1])
                    end = i + 1
                    break

        if chunk.strip():
            chunks.append(chunk.strip())

        if end >= len(words):
            break

        new_start = end - overlap
        start = new_start if new_start > start else start + 1

    return chunks
