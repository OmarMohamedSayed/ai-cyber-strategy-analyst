import json
import uuid

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from qdrant_client.models import PointStruct

from app.services.ingestion_service import ingest_document, _embed_texts
from app.services.upload_service import list_documents, register_document
from app.core.config import get_settings
from app.core.qdrant_client import get_qdrant_client
from app.models.domain import DocumentChunk, ChunkMetadata
from app.utils.json_normalizer import normalize_dataset

router = APIRouter(prefix="/documents", tags=["Documents"])

settings = get_settings()
ALLOWED_EXTENSIONS = set(settings.allowed_extensions.split(","))
ALLOWED_CATEGORIES = set(settings.allowed_categories.split(","))
_CATEGORY_DESCRIPTION = " | ".join(sorted(ALLOWED_CATEGORIES))


@router.post("/upload", summary="Upload and ingest a PDF/DOCX/TXT document")
async def upload_document(
    file: UploadFile = File(...),
    category: str = Form(..., description=_CATEGORY_DESCRIPTION),
    source_name: str = Form(..., description="Human-readable source name"),
    chunk_size: int = Form(0, description="0 = use framework auto-preset"),
    chunk_overlap: int = Form(0, description="0 = use framework auto-preset"),
):
    suffix = "." + file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{suffix}'. Allowed: {ALLOWED_EXTENSIONS}",
        )
    if category not in ALLOWED_CATEGORIES:
        raise HTTPException(status_code=400, detail=f"Invalid category. Allowed: {ALLOWED_CATEGORIES}")

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    result = ingest_document(
        file_bytes=file_bytes,
        filename=file.filename,
        category=category,
        source_name=source_name,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return {"message": "Document ingested successfully.", "document": result}


@router.post(
    "/ingest-json",
    summary="Ingest any JSON dataset (audit, risk, cloud, incident, third-party, controls)",
)
async def ingest_json_dataset(
    file: UploadFile = File(..., description="JSON file — bare list [] or {items:[...]} wrapper"),
    category: str = Form(..., description=_CATEGORY_DESCRIPTION),
    source_name: str = Form(..., description="Human-readable source name"),
):
    """
    Accepts any of the supported dataset shapes:

    | Dataset file                  | Auto-detected schema  |
    |-------------------------------|-----------------------|
    | audit_finding_dataset.json    | audit_finding         |
    | risk_register_dataset.json    | risk_register         |
    | cloud_migration_dataset.json  | cloud_migration       |
    | third_party_risk_dataset.json | third_party_risk      |
    | incident_reports_dataset.json | incident_report       |
    | business_plan.json            | generic               |

    Each item is normalized into a rich description string before embedding,
    so context like likelihood, impact, mitigation, vendor, gap, etc. is
    all searchable via semantic retrieval.
    """
    if category not in ALLOWED_CATEGORIES:
        raise HTTPException(status_code=400, detail=f"Invalid category. Allowed: {ALLOWED_CATEGORIES}")

    raw = await file.read()
    if not raw:
        raise HTTPException(status_code=400, detail="File is empty.")

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}")

    # Accept bare list or {items:[...]} / {findings:[...]} / {risks:[...]} etc.
    if isinstance(payload, list):
        raw_items = payload
    elif isinstance(payload, dict):
        # Try common wrapper keys
        for key in ("items", "findings", "risks", "reports", "plans", "vendors", "workloads"):
            if key in payload:
                raw_items = payload[key]
                break
        else:
            # Fall back to first list-valued key
            raw_items = next(
                (v for v in payload.values() if isinstance(v, list)), []
            )
    else:
        raw_items = []

    if not raw_items:
        raise HTTPException(status_code=400, detail="No items found in JSON file.")

    # Normalize heterogeneous schemas into a common format
    normalized = normalize_dataset(raw_items)
    if not normalized:
        raise HTTPException(status_code=400, detail="No valid items with descriptions after normalization.")

    settings = get_settings()
    qdrant = get_qdrant_client()
    document_id = str(uuid.uuid4())

    chunks: list[DocumentChunk] = [
        DocumentChunk(
            id=str(uuid.uuid4()),
            document_id=document_id,
            title=item.title,
            description=item.description,
            category=category,
            source=source_name,
            metadata=ChunkMetadata(
                chunk_index=idx,
                document_type="json",
                section=item.section,
                framework=item.framework or category,
                control_id=item.control_id,
            ),
        )
        for idx, item in enumerate(normalized)
    ]

    BATCH = settings.embedding_batch_size
    all_embeddings: list[list[float]] = []
    for i in range(0, len(chunks), BATCH):
        batch_texts = [c.description for c in chunks[i : i + BATCH]]
        all_embeddings.extend(_embed_texts(batch_texts))

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
                "framework": c.metadata.framework,
                "control_id": c.metadata.control_id,
            },
        )
        for c, emb in zip(chunks, all_embeddings)
    ]
    qdrant.upsert(collection_name=settings.qdrant_collection, points=points)

    doc_record = register_document(
        filename=file.filename,
        source_name=source_name,
        category=category,
        chunk_count=len(chunks),
    )
    return {
        "message": f"Ingested {len(chunks)} items from '{file.filename}'.",
        "document": {**doc_record, "document_id": document_id},
    }


@router.get("/items", summary="List all ingested documents")
def get_documents():
    return list_documents()
