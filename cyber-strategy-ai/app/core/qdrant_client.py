from qdrant_client import QdrantClient as _QdrantClient
from qdrant_client.models import Distance, VectorParams
from app.core.config import get_settings

_client: _QdrantClient | None = None


def get_qdrant_client() -> _QdrantClient:
    global _client
    if _client is None:
        settings = get_settings()
        _client = _QdrantClient(host=settings.qdrant_host, port=settings.qdrant_port)
    return _client


def ensure_collection() -> None:
    settings = get_settings()
    client = get_qdrant_client()
    existing = [c.name for c in client.get_collections().collections]
    if settings.qdrant_collection not in existing:
        client.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=VectorParams(
                size=settings.embedding_dim,
                distance=Distance.COSINE,
            ),
        )
