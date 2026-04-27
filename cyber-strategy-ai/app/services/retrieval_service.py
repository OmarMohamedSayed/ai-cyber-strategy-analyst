from openai import OpenAI
from app.core.config import get_settings
from app.core.qdrant_client import get_qdrant_client


def _embed_query(query: str) -> list[float]:
    settings = get_settings()
    client = OpenAI(api_key=settings.openai_api_key)
    response = client.embeddings.create(model=settings.embedding_model, input=[query])
    return response.data[0].embedding


def retrieve_chunks(query: str, top_k: int = 8) -> list[dict]:
    """Return top_k relevant chunks from Qdrant as plain dicts."""
    settings = get_settings()
    qdrant = get_qdrant_client()

    vector = _embed_query(query)
    response = qdrant.query_points(
        collection_name=settings.qdrant_collection,
        query=vector,
        limit=top_k,
        with_payload=True,
    )

    return [
        {
            "score": hit.score,
            "title": hit.payload.get("title", ""),
            "description": hit.payload.get("description", ""),
            "category": hit.payload.get("category", ""),
            "source": hit.payload.get("source", ""),
            "section": hit.payload.get("section", ""),
            "framework": hit.payload.get("framework", ""),
            "control_id": hit.payload.get("control_id", ""),
        }
        for hit in response.points
    ]
