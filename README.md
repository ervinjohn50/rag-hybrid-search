# RAG Pipeline with Hybrid Search

An API that answers questions about your documents and cites the passages behind each answer. Retrieval combines dense vector search with BM25 keyword search, then reranks the results before Claude Sonnet writes the answer.

> **Status: work in progress.** Document parsing and chunking are finished and tested. Retrieval, answer generation, the API and the Docker setup are still being built, so the project can't answer questions yet.

## Planned pipeline

```
ADD A DOCUMENT   file → extract text → split into chunks → dense + BM25 vectors → Qdrant

ASK A QUESTION   question ─┬─ dense search (top 50) ─┐
                           └─ BM25 search  (top 50) ─┴→ merge (top 30) → rerank (top 6) → Claude → answer + citations
```

Dense search matches on meaning, and BM25 matches exact terms such as error codes and part numbers. Combining them covers each one's blind spots, and a cross-encoder then reranks the merged candidates so that only the most relevant passages reach the model.

## Stack

| Part | Technology |
| --- | --- |
| Backend | Python, FastAPI |
| Dense vectors | FastEmbed with `BAAI/bge-small-en-v1.5` |
| Keyword search | BM25 with FastEmbed's `Qdrant/bm25` |
| Reranking | FastEmbed with `Xenova/ms-marco-MiniLM-L-6-v2` |
| Vector store | Qdrant |
| LLM | Claude Sonnet |
| Deployment | Docker Compose |

## Progress

- [x] Text extraction from PDF, Markdown and TXT files
- [x] Chunking with overlap, keeping page numbers and headings
- [x] Sample documents and tests
- [ ] Local models and Qdrant store
- [ ] Hybrid retrieval and reranking
- [ ] Cited answers from Claude Sonnet
- [ ] REST API
- [ ] Docker setup

## Running the tests

This project uses [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run pytest
```

The files in `sample_docs/` describe a fictional product and exist only for testing.
