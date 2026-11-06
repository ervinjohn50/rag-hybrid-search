"""Application settings, read from environment variables or a local .env file."""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Claude
    anthropic_api_key: str | None = None
    claude_model: str = "claude-sonnet-5-5"
    claude_effort: Literal["low", "medium", "high", "xhigh", "max"] = "medium"
    claude_max_tokens: int = Field(default=16000, ge=1)

    # Qdrant. Use ":memory:" for an in-process instance with no server.
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "documents"

    # Local models
    dense_model: str = "BAAI/bge-small-en-v1.5"
    dense_size: int = 384
    sparse_model: str = "Qdrant/bm25"
    rerank_model: str = "Xenova/ms-marco-MiniLM-L-6-v2"
    fastembed_cache_path: str | None = None

    # Retrieval funnel: candidates per search -> after merging -> after reranking
    prefetch_limit: int = Field(default=50, ge=1)
    fusion_limit: int = Field(default=30, ge=1)
    top_k: int = Field(default=6, ge=1)

    # Ingestion
    chunk_size: int = Field(default=1200, ge=100)
    chunk_overlap: int = Field(default=150, ge=0)
    max_upload_bytes: int = Field(default=25 * 1024 * 1024, ge=1)


@lru_cache
def get_settings() -> Settings:
    return Settings()
