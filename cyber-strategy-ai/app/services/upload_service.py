import uuid
from pathlib import Path
from datetime import datetime

from app.core.config import get_settings
from app.repositories.json_repository import JsonRepository


def _doc_repo() -> JsonRepository:
    settings = get_settings()
    return JsonRepository(f"{settings.data_dir}/documents.json")


def save_upload(file_bytes: bytes, filename: str) -> Path:
    """Persist raw file to uploads directory and return its path."""
    settings = get_settings()
    uploads = Path(settings.uploads_dir)
    uploads.mkdir(parents=True, exist_ok=True)
    dest = uploads / f"{uuid.uuid4()}_{filename}"
    dest.write_bytes(file_bytes)
    return dest


def register_document(
    filename: str,
    source_name: str,
    category: str,
    chunk_count: int,
) -> dict:
    record = {
        "id": str(uuid.uuid4()),
        "filename": filename,
        "source_name": source_name,
        "category": category,
        "chunk_count": chunk_count,
        "uploaded_at": datetime.utcnow().isoformat(),
    }
    return _doc_repo().insert(record)


def list_documents() -> list[dict]:
    return _doc_repo().all()
