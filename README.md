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
