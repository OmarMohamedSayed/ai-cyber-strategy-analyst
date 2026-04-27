from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.config import get_settings
from app.core.qdrant_client import ensure_collection
from app.routers import documents, strategy, review

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_collection()
    yield


app = FastAPI(
    title=settings.app_title,
    description=(
        "RAG-powered API for CISO teams to analyze cybersecurity inputs "
        "and generate board-ready strategy insights with human-in-the-loop validation."
    ),
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(documents.router)
app.include_router(strategy.router)
app.include_router(review.router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "service": settings.app_title}
