# RAG Python — Consulta Inteligente em Documentos

![CI](https://github.com/Dimitrearaujo/rag-python-documentos/actions/workflows/ci.yml/badge.svg)

Sistema RAG (Retrieval-Augmented Generation) em Python puro — ingere PDFs e textos, gera embeddings, armazena em SQLite e responde perguntas via Claude.

Sem dependencias pesadas: sem LangChain, sem Chroma, sem FAISS. SQLite + OpenAI Embeddings + Claude.

## Fluxo

```
PDF / TXT / MD
      |
   loader.py (pypdf)
      |
   chunker.py (500 palavras, 50 overlap)
      |
   embeddings.py (text-embedding-3-small)
      |
   vectorstore.db (SQLite)
      |
   query.py → retriever.py (cosine similarity)
      |
   generator.py (Claude Haiku)
      |
   Resposta fundamentada nos documentos
```

## Instalacao

```bash
git clone https://github.com/Dimitrearaujo/rag-python-documentos
cd rag-python-documentos
pip install -r requirements.txt

cp .env.example .env
# Edite .env com suas chaves
```

## Uso

```bash
# Ingerir documentos
python ingest.py contrato.pdf manual.pdf relatorio.txt

# Re-ingerir (se o arquivo foi atualizado)
python ingest.py contrato.pdf --force

# Consultar
python query.py "Qual e o prazo de entrega previsto no contrato?"

# Ver apenas chunks recuperados, sem gerar resposta
python query.py "Clausulas de rescisao" --no-generate

# Recuperar mais chunks (padrao: 5)
python query.py "Penalidades" --top-k 8
```

## Modulos

| Arquivo | Funcao |
|---|---|
| `rag/loader.py` | Carrega PDF, TXT, MD |
| `rag/chunker.py` | Divide texto em chunks com overlap |
| `rag/embeddings.py` | OpenAI text-embedding-3-small, cache local |
| `rag/vectorstore.py` | SQLite — armazena chunks e embeddings |
| `rag/retriever.py` | Cosine similarity, retorna top-K chunks |
| `rag/generator.py` | Claude Haiku — responde com base no contexto |
| `ingest.py` | CLI de ingestao |
| `query.py` | CLI de consulta |

## Cache de embeddings

Embeddings sao salvos em `~/.rag-cache/embeddings/` (hash MD5 do texto). Re-ingestao do mesmo arquivo nao re-embeda chunks identicos — economiza tokens.

## Casos de uso

- Contratos e documentos juridicos
- Manuais tecnicos e procedimentos
- Bases de conhecimento internas
- Relatorios e planilhas exportadas como texto

## Licenca

MIT

---

<details>
<summary>🇺🇸 English</summary>

# RAG Python — Intelligent Document Q&A

![CI](https://github.com/Dimitrearaujo/rag-python-documentos/actions/workflows/ci.yml/badge.svg)

RAG (Retrieval-Augmented Generation) system in pure Python — ingests PDFs and text files, generates embeddings, stores in SQLite and answers questions via Claude.

No heavy dependencies: no LangChain, no Chroma, no FAISS. SQLite + OpenAI Embeddings + Claude.

## Flow

```
PDF / TXT / MD
      |
   loader.py (pypdf)
      |
   chunker.py (500 words, 50 overlap)
      |
   embeddings.py (text-embedding-3-small)
      |
   vectorstore.db (SQLite)
      |
   query.py → retriever.py (cosine similarity)
      |
   generator.py (Claude Haiku)
      |
   Answer grounded in your documents
```

## Installation

```bash
git clone https://github.com/Dimitrearaujo/rag-python-documentos
cd rag-python-documentos
pip install -r requirements.txt

cp .env.example .env
# Edit .env with your keys
```

## Usage

```bash
# Ingest documents
python ingest.py contract.pdf manual.pdf report.txt

# Re-ingest (if file was updated)
python ingest.py contract.pdf --force

# Query
python query.py "What is the delivery deadline in the contract?"

# See only retrieved chunks, without generating answer
python query.py "Termination clauses" --no-generate

# Retrieve more chunks (default: 5)
python query.py "Penalties" --top-k 8
```

## Modules

| File | Function |
|---|---|
| `rag/loader.py` | Loads PDF, TXT, MD |
| `rag/chunker.py` | Splits text into chunks with overlap |
| `rag/embeddings.py` | OpenAI text-embedding-3-small, local cache |
| `rag/vectorstore.py` | SQLite — stores chunks and embeddings |
| `rag/retriever.py` | Cosine similarity, returns top-K chunks |
| `rag/generator.py` | Claude Haiku — answers based on context |
| `ingest.py` | Ingestion CLI |
| `query.py` | Query CLI |

## Embeddings cache

Embeddings are saved to `~/.rag-cache/embeddings/` (MD5 hash of the text). Re-ingesting the same file doesn't re-embed identical chunks — saves tokens.

## Use cases

- Contracts and legal documents
- Technical manuals and procedures
- Internal knowledge bases
- Reports and spreadsheets exported as text

## License

MIT

</details>

---

[← Back to profile](https://github.com/Dimitrearaujo)
