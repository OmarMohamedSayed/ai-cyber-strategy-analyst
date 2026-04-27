from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    app_title: str = "AI Cyber Strategy Analyst Assistant"
    app_version: str = "1.0.0"
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    # LLM
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    llm_temperature: float = 0.0

    # Qdrant
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection: str = "cyber_docs"

    # Embedding
    embedding_model: str = "text-embedding-3-small"
    embedding_dim: int = 1536
    embedding_batch_size: int = 50

    # Storage
    data_dir: str = "data"
    uploads_dir: str = "data/uploads"

    # Chunking defaults
    default_chunk_size: int = 700
    default_chunk_overlap: int = 100

    # Retrieval
    default_top_k: int = 8

    # Document processing
    min_page_chars: int = 200

    # PowerPoint branding
    pptx_copyright: str = "Copyright © 2026 Accenture. All rights reserved."
    pptx_font: str = "Arial"

    # Allowed file types and categories
    allowed_extensions: str = ".pdf,.docx,.txt"
    allowed_categories: str = "audit,risk,incident,business,iso,nist,cis,gdpr"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
