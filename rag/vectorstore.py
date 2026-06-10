"""VectorStore em SQLite — armazena chunks e seus embeddings."""
from __future__ import annotations
import json
import sqlite3
from pathlib import Path

from rag.embeddings import cosine_similarity

DB_PATH = Path.home() / ".rag-cache" / "vectorstore.db"


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _connect() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            source      TEXT NOT NULL,
            content     TEXT NOT NULL,
            embedding   TEXT NOT NULL,
            created_at  TEXT DEFAULT (datetime('now'))
        )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_source ON chunks(source)")


def add_chunks(source: str, chunks: list[str], embeddings: list[list[float]]) -> None:
    with _connect() as conn:
        conn.executemany(
            "INSERT INTO chunks (source, content, embedding) VALUES (?, ?, ?)",
            [(source, c, json.dumps(e)) for c, e in zip(chunks, embeddings)],
        )


def source_exists(source: str) -> bool:
    with _connect() as conn:
        row = conn.execute(
            "SELECT 1 FROM chunks WHERE source=? LIMIT 1", (source,)
        ).fetchone()
    return row is not None


def delete_source(source: str) -> None:
    with _connect() as conn:
        conn.execute("DELETE FROM chunks WHERE source=?", (source,))


def search(query_embedding: list[float], top_k: int = 5) -> list[dict]:
    """Retorna os top_k chunks mais similares."""
    with _connect() as conn:
        rows = conn.execute(
            "SELECT source, content, embedding FROM chunks"
        ).fetchall()

    scored = []
    for row in rows:
        vec = json.loads(row["embedding"])
        score = cosine_similarity(query_embedding, vec)
        scored.append({"source": row["source"], "content": row["content"], "score": score})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]
