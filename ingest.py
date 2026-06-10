"""CLI para ingestao de documentos no vectorstore."""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from rag.loader import load_text, clean_text
from rag.chunker import chunk_text
from rag.embeddings import embed_batch
from rag.vectorstore import init_db, add_chunks, source_exists, delete_source


def ingest(path: str, force: bool = False) -> None:
    p = Path(path)
    if not p.exists():
        print(f"Arquivo nao encontrado: {path}")
        sys.exit(1)

    source = p.name
    init_db()

    if source_exists(source):
        if not force:
            print(f"'{source}' ja foi ingerido. Use --force para re-ingerir.")
            return
        delete_source(source)
        print(f"Re-ingerindo '{source}'...")

    print(f"Carregando {path}...")
    text = clean_text(load_text(p))
    chunks = chunk_text(text)
    print(f"  {len(chunks)} chunks gerados.")

    print("  Gerando embeddings...")
    embeddings = embed_batch(chunks)

    add_chunks(source, chunks, embeddings)
    print(f"  Pronto! '{source}' indexado com {len(chunks)} chunks.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingerir documentos no RAG")
    parser.add_argument("files", nargs="+", help="Arquivos PDF/TXT/MD para ingerir")
    parser.add_argument("--force", action="store_true", help="Re-ingerir se ja existir")
    args = parser.parse_args()

    for f in args.files:
        ingest(f, force=args.force)


if __name__ == "__main__":
    main()
