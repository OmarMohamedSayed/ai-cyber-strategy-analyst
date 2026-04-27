# Architecture

## High-Level Flow

1. Document ingestion (`/documents/upload`, `/documents/ingest-json`)
2. Text extraction and normalization
3. Structure-aware chunking
4. OpenAI embeddings generation
5. Qdrant vector storage and retrieval
6. Multi-step LLM strategy synthesis
7. Output generation (JSON, HTML report, PPTX)
8. Human-in-the-loop review lifecycle

## Core Components

- `app/main.py`: FastAPI app initialization and router registration
- `app/core/config.py`: environment-driven runtime settings
- `app/core/qdrant_client.py`: vector collection bootstrap and client singleton
- `app/services/ingestion_service.py`: file processing + embedding + upsert
- `app/services/retrieval_service.py`: semantic retrieval over Qdrant
- `app/services/strategy_analysis_service.py`: orchestrates multi-step LLM pipeline
- `app/services/report_service.py`: renders board-ready HTML report
- `app/services/powerpoint_service.py`: renders initiative presentation slides

## Data Stores

- Qdrant collection (vectors + payload metadata)
- `cyber-strategy-ai/data/documents.json` (ingested document registry)
- `cyber-strategy-ai/data/strategy_results.json` (analysis outputs)
- `cyber-strategy-ai/data/uploads/` (uploaded document copies)

## Deployment Notes

- API and Qdrant can run via `docker-compose.yml`.
- Runtime behavior is controlled through `.env` variables.
- Swagger/OpenAPI is available by default at `/docs` and `/openapi.json`.
