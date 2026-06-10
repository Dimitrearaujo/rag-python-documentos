"""Ingestao de documentos — PDF, TXT e Markdown."""
from __future__ import annotations
import re
from pathlib import Path


def load_text(path: str | Path) -> str:
    """Carrega texto bruto de PDF, TXT ou MD."""
    p = Path(path)
    if p.suffix.lower() == ".pdf":
        return _load_pdf(p)
    return p.read_text(encoding="utf-8", errors="replace")


def _load_pdf(path: Path) -> str:
    try:
        import pypdf
        reader = pypdf.PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except ImportError:
        raise ImportError("Instale pypdf: pip install pypdf")


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\x00-\x7FÀ-ɏḀ-ỿ]", "", text)
    return text.strip()
