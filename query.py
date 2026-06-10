"""CLI para consultar o RAG."""
from __future__ import annotations
import argparse
import sys

from dotenv import load_dotenv
load_dotenv()

from rag.retriever import retrieve, format_context
from rag.generator import generate
from rag.vectorstore import init_db


def main() -> None:
    parser = argparse.ArgumentParser(description="Consultar documentos via RAG")
    parser.add_argument("query", help="Pergunta sobre os documentos")
    parser.add_argument("--top-k", type=int, default=5, help="Qtd de chunks a recuperar (default: 5)")
    parser.add_argument("--no-generate", action="store_true", help="Mostrar apenas chunks, sem gerar resposta")
    args = parser.parse_args()

    init_db()
    chunks = retrieve(args.query, top_k=args.top_k)

    if not chunks:
        print("Nenhum documento indexado. Execute: python ingest.py <arquivo>")
        sys.exit(1)

    print(f"\n--- {len(chunks)} chunks recuperados ---")
    for i, c in enumerate(chunks, 1):
        print(f"[{i}] {c['source']} (score: {c['score']:.3f})")
        print(f"    {c['content'][:120]}...")

    if args.no_generate:
        return

    context = format_context(chunks)
    print("\n--- Resposta ---")
    print(generate(args.query, context))


if __name__ == "__main__":
    main()
