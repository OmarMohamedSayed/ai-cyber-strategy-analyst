import uuid
from pathlib import Path

from openai import OpenAI
from qdrant_client.models import PointStruct

from app.core.config import get_settings
from app.core.qdrant_client import get_qdrant_client
from app.models.domain import DocumentChunk
from app.utils.document_loader import extract_text
from app.utils.text_chunker import chunk_document
from app.services.upload_service import save_upload, register_document


def _embed_texts(texts: list[str]) -> list[list[float]]:
    settings = get_settings()
    client = OpenAI(api_key=settings.openai_api_key)
    response = client.embeddings.create(model=settings.embedding_model, input=texts)
    return [item.embedding for item in response.data]


def ingest_document(
    file_bytes: bytes,
    filename: str,
    category: str,
    source_name: str,
    chunk_size: int,
    chunk_overlap: int,
) -> dict:
    ext = Path(filename).suffix.lower().lstrip(".")

    # 1. Persist raw file
    save_upload(file_bytes, filename)

    # 2. Extract text
    text = extract_text(file_bytes, filename)

    # 3. Chunk
    document_id = str(uuid.uuid4())
    chunks: list[DocumentChunk] = chunk_document(
        text=text,
        document_id=document_id,
        source=source_name,
        category=category,
        document_type=ext,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    if not chunks:
        raise ValueError("No text content extracted from document.")

    settings = get_settings()
    BATCH = settings.embedding_batch_size
    all_embeddings: list[list[float]] = []
    for i in range(0, len(chunks), BATCH):
        batch_texts = [c.description for c in chunks[i : i + BATCH]]
        all_embeddings.extend(_embed_texts(batch_texts))

    qdrant = get_qdrant_client()
    points = [
        PointStruct(
            id=c.id,
            vector=emb,
            payload={
                "document_id": c.document_id,
                "title": c.title,
                "description": c.description,
                "category": c.category,
                "source": c.source,
                "chunk_index": c.metadata.chunk_index,
                "document_type": c.metadata.document_type,
                "section": c.metadata.section,
                "business_unit": c.metadata.business_unit,
                "framework": c.metadata.framework,
                "control_id": c.metadata.control_id,
            },
        )
        for c, emb in zip(chunks, all_embeddings)
    ]
    qdrant.upsert(collection_name=settings.qdrant_collection, points=points)

    # 6. Save metadata
    doc_record = register_document(
        filename=filename,
        source_name=source_name,
        category=category,
        chunk_count=len(chunks),
    )

    return {**doc_record, "document_id": document_id}
