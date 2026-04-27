# AI Cyber Strategy Analyst Assistant

A production-ready **RAG-powered API** that helps CISO teams analyze cybersecurity inputs and generate **board-ready strategy insights** with human-in-the-loop (HITL) validation.

Built with **FastAPI**, **OpenAI**, **Qdrant**, and **LangChain**.

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Environment Variables](#environment-variables)
- [API Documentation (Swagger)](#api-documentation-swagger)
- [API Reference](#api-reference)
- [Data Sources](#data-sources)
- [Human-in-the-Loop Lifecycle](#human-in-the-loop-lifecycle)
- [Output Schema](#output-schema)
- [Project Structure](#project-structure)
- [LLM Guardrails](#llm-guardrails)

---

## Features

- **Multi-framework compliance mapping** — ISO 27001, NIST CSF 2.0, CIS Controls v8.1, GDPR
- **Structure-aware document chunking** — Framework-specific heading patterns and chunk sizes
- **5-step LLM analysis pipeline** — Themes, risk scoring, initiatives, board output, clarification
- **Evidence traceability** — Every recommendation links back to source documents and controls
- **AI confidence scoring** — Transparent confidence levels with conflict detection
- **Human-in-the-loop review** — Draft → Needs Review → Approved/Rejected workflow
- **Board-ready HTML reports** — Consulting-style interactive reports with charts
- **PowerPoint generation** — Initiative slides with timeline, priorities, and branding
- **JSON + PDF + DOCX ingestion** — Supports structured datasets and unstructured documents

---

## Architecture

```
Documents (PDF/DOCX/TXT/JSON)
        │
        ▼
  Text Extraction (pypdf, docx2txt)
        │
        ▼
  Structure-Aware Chunking (LangChain)
  ┌─────────────────────────────────────────────┐
  │ ISO 27001  → 800/100  (clause-level chunks) │
  │ NIST CSF   → 1200/150 (section-level)       │
  │ CIS v8.1   → 1200/200 (control blocks)      │
  │ GDPR       → 1000/150 (topic headings)      │
  │ Default    → 700/100  (generic)              │
  └─────────────────────────────────────────────┘
        │
        ▼
  Embeddings (OpenAI text-embedding-3-small)
        │
        ▼
  Qdrant (Vector Database — Cosine Similarity)
        │
        ▼
  Semantic Retrieval (top-K chunks)
        │
        ▼
  LangChain LLM Pipeline (5 steps)
  ┌─────────────────────────────────────────────┐
  │ 1. Summarize → Recurring cyber themes       │
  │ 2. Risk Map  → Scored business risks        │
  │ 3. Initiatives → Prioritized actions        │
  │ 4. Board Output → Executive summary + KPIs  │
  │ 5. Clarification → Questions for humans     │
  └─────────────────────────────────────────────┘
        │
        ▼
  Human Review (HITL)
  draft → needs_review → approved / rejected
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| API Framework | FastAPI |
| LLM | OpenAI GPT-4o / GPT-4o-mini |
| Embeddings | OpenAI text-embedding-3-small |
| Vector Database | Qdrant |
| Prompt Orchestration | LangChain |
| Text Splitting | LangChain RecursiveCharacterTextSplitter |
| PDF Extraction | pypdf |
| DOCX Extraction | docx2txt |
| PowerPoint Generation | python-pptx |
| Configuration | pydantic-settings + dotenv |

---

## Quick Start

### 1. Clone and create environment

```bash
git clone <repo-url>
cd AI_Cyber_Strategy_Analyst_Assistant/cyber-strategy-ai
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env and set your OPENAI_API_KEY
```

### 4. Run Qdrant (Docker)

```bash
docker run -d \
  --name qdrant \
  -p 6333:6333 \
  -v $(pwd)/qdrant_storage:/qdrant/storage \
  qdrant/qdrant
```

### 5. Run the API

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Ingest all data

```bash
cd ..
chmod +x ingest_all.sh
./ingest_all.sh
```

### 7. Open Swagger UI

Navigate to **[http://localhost:8000/docs](http://localhost:8000/docs)** in your browser.

---

## API Documentation (Swagger)

FastAPI auto-generates interactive API documentation:

| Interface | URL | Description |
|-----------|-----|-------------|
| **Swagger UI** | [http://localhost:8000/docs](http://localhost:8000/docs) | Interactive API explorer — test endpoints directly from the browser |
| **ReDoc** | [http://localhost:8000/redoc](http://localhost:8000/redoc) | Alternative read-friendly API documentation |
| **OpenAPI JSON** | [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json) | Raw OpenAPI 3.1 schema (for code generators, Postman import, etc.) |

---

## Environment Variables

All configuration is managed through environment variables loaded from `.env`. See `.env.example` for a complete reference.

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_TITLE` | `AI Cyber Strategy Analyst Assistant` | Application title shown in Swagger UI |
| `APP_VERSION` | `1.0.0` | API version |
| `APP_HOST` | `0.0.0.0` | Server bind host |
| `APP_PORT` | `8000` | Server bind port |
| `OPENAI_API_KEY` | *(required)* | Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-4o-mini` | GPT model for analysis |
| `LLM_TEMPERATURE` | `0.0` | LLM temperature (0 = deterministic) |
| `QDRANT_HOST` | `localhost` | Qdrant server host |
| `QDRANT_PORT` | `6333` | Qdrant server port |
| `QDRANT_COLLECTION` | `cyber_docs` | Qdrant collection name |
| `EMBEDDING_MODEL` | `text-embedding-3-small` | OpenAI embedding model |
| `EMBEDDING_DIM` | `1536` | Embedding vector dimensions |
| `EMBEDDING_BATCH_SIZE` | `50` | Texts per embedding API call |
| `DATA_DIR` | `data` | JSON persistence directory |
| `UPLOADS_DIR` | `data/uploads` | Uploaded file storage |
| `DEFAULT_CHUNK_SIZE` | `700` | Default chunk size (chars) |
| `DEFAULT_CHUNK_OVERLAP` | `100` | Default chunk overlap (chars) |
| `DEFAULT_TOP_K` | `8` | Chunks retrieved per query |
| `MIN_PAGE_CHARS` | `200` | Min chars to include a PDF page |
| `PPTX_COPYRIGHT` | `Copyright © 2026 Accenture...` | Slide footer copyright |
| `PPTX_FONT` | `Arial` | Slide font family |
| `ALLOWED_EXTENSIONS` | `.pdf,.docx,.txt` | Accepted upload file types |
| `ALLOWED_CATEGORIES` | `audit,risk,incident,...` | Valid document categories |

---

## API Reference

### Health Check

```
GET /
```

Returns `{"status": "ok", "service": "AI Cyber Strategy Analyst Assistant"}`

---

### Document Endpoints

#### Upload a document

```
POST /documents/upload
```

```bash
curl -X POST http://localhost:8000/documents/upload \
  -F "file=@audit_findings.pdf" \
  -F "category=audit" \
  -F "source_name=2025 IT Audit Report" \
  -F "chunk_size=700" \
  -F "chunk_overlap=100"
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `file` | File | PDF, DOCX, or TXT file |
| `category` | string | `audit` \| `risk` \| `incident` \| `business` \| `iso` \| `nist` \| `cis` \| `gdpr` |
| `source_name` | string | Human-readable source name |
| `chunk_size` | int | Custom chunk size (0 = auto-detect per framework) |
| `chunk_overlap` | int | Custom overlap (0 = auto-detect per framework) |

#### Ingest a JSON dataset

```
POST /documents/ingest-json
```

```bash
curl -X POST http://localhost:8000/documents/ingest-json \
  -F "file=@risk_register_dataset.json" \
  -F "category=risk" \
  -F "source_name=Enterprise Risk Register 2025"
```

Accepts bare list `[]` or wrapper objects `{items: [...]}`, `{findings: [...]}`, etc.

#### List ingested documents

```
GET /documents/items
```

---

### Strategy Endpoints

#### Run AI strategy analysis

```
POST /strategy/run
```

```bash
curl -X POST http://localhost:8000/strategy/run \
  -H "Content-Type: application/json" \
  -d '{
    "analysis_name": "2026_strategy",
    "business_context": "Enterprise undergoing cloud migration with 3rd-party dependencies",
    "focus_areas": ["IAM", "cloud security", "third-party risk"],
    "top_k": 8
  }'
```

#### List all strategy results

```
GET /strategy/results
```

#### Get a specific result

```
GET /strategy/results/{result_id}
```

#### Generate HTML report

```
GET /strategy/results/{result_id}/report
```

Returns a board-ready interactive HTML report with charts, risk heatmaps, and framework mappings.

#### Generate PowerPoint slides

```
GET /strategy/results/{result_id}/powerpoint/initiative-slide
```

Downloads a `.pptx` file with strategy overview and initiative detail slides.

#### Submit clarification answers

```
POST /strategy/clarify
```

```bash
curl -X POST http://localhost:8000/strategy/clarify \
  -H "Content-Type: application/json" \
  -d '{
    "analysis_name": "2026_strategy",
    "answers": [
      {
        "question": "Should regulatory urgency be prioritized over cost?",
        "answer": "Yes, regulatory compliance is the top priority."
      }
    ]
  }'
```

---

### Review Endpoints

#### Submit human review

```
POST /strategy/results/{result_id}/review
```

```bash
curl -X POST http://localhost:8000/strategy/results/{result_id}/review \
  -H "Content-Type: application/json" \
  -d '{
    "reviewer_name": "Omar",
    "status": "approved",
    "comments": "Increase resilience priority in Q2."
  }'
```

**Valid statuses:** `approved` | `rejected` | `needs_review`

---

## Data Sources

All source documents are stored in the `data/` directory at the project root. See [`data/README.md`](../data/README.md) for detailed descriptions of each document and why it's used.

### Framework Documents (PDF)

| File | Framework |
|------|-----------|
| `ISO_IEC-270012022-ed.3.pdf` | ISO/IEC 27001:2022 — ISMS requirements + Annex A controls |
| `NIST.CSWP.29.pdf` | NIST CSF 2.0 — Six-function cybersecurity framework |
| `CIS_Controls_Guide_v8.1.2_0325_v2.pdf` | CIS Controls v8.1 — Implementation safeguards (IG1-IG3) |
| `GDPR_FINAL_EPSU.pdf` | GDPR — EU data protection regulation briefing |
| `2026_Cyber_Strategy — Cyber Strategy Report.pdf` | Internal cyber strategy report |

### Operational Datasets (JSON)

| File | Type |
|------|------|
| `audit_finding_dataset.json` | Internal audit findings and control gaps |
| `risk_register_dataset.json` | Enterprise risk register with scores |
| `cloud_migration_dataset.json` | Cloud workload security gaps |
| `third_party_risk_dataset.json` | Vendor/third-party risk assessments |
| `incident_reports_dataset.json` | Historical security incidents |
| `business_plan.json` | Business objectives and strategic priorities |

---

## Human-in-the-Loop Lifecycle

```
[Upload Documents]
        │
[POST /strategy/run]
        │
   status = "draft"
        │
   ┌── (if low confidence / conflicts / clarification needed) ──┐
   │                                                             │
   │    status = "needs_review"                                  │
   │         │                                                   │
   │    [POST /strategy/clarify]  ← human answers questions      │
   │         │                                                   │
   └─────────┘                                                   │
        │                                                        │
[POST /strategy/results/{id}/review]  ← reviewer decision        │
        │                                                        │
   status = "approved"  or  "rejected"                           │
```

**Auto-escalation triggers:**
- AI confidence level = `low`
- Conflicting evidence signals detected
- Fewer than 2 evidence chunks retrieved
- Clarification questions generated

---

## Output Schema

```json
{
  "result_id": "uuid",
  "analysis_name": "2026_strategy",
  "status": "draft | needs_review | approved | rejected",
  "created_at": "2026-04-10T10:00:00",

  "recurring_themes": ["Theme description 1", "Theme description 2"],
  "business_risk_mapping": ["[6/9 | Medium×High] Risk statement"],
  "prioritized_initiatives": ["[High] Initiative | Effort: Medium | ..."],
  "strategy_options": ["Option A: Zero-Trust architecture"],

  "evidence_traces": [
    {
      "chunk_title": "A.8 Technological controls",
      "source": "ISO/IEC 27001:2022",
      "category": "iso",
      "framework": "iso27001",
      "control_id": "A.8",
      "relevance_score": 0.8742
    }
  ],

  "risk_scores": [
    {
      "risk_statement": "Insufficient IAM controls",
      "likelihood": "High",
      "impact": "High",
      "risk_score": 9,
      "rationale": "Multiple audit findings..."
    }
  ],

  "control_mappings": [
    {
      "initiative": "MFA Rollout",
      "iso27001": ["A.8.5"],
      "nist_csf": ["PR.AA-01"],
      "cis_controls": ["CIS-6"],
      "gdpr_articles": ["Art. 32"]
    }
  ],

  "business_alignments": [
    {
      "initiative": "MFA Rollout",
      "business_objective": "Secure digital transformation",
      "alignment_rationale": "Directly supports...",
      "dependency": "Cloud migration completion"
    }
  ],

  "initiative_details": [
    {
      "title": "MFA Rollout",
      "priority": "High",
      "effort": "Medium",
      "cost_estimate": "$150K-250K",
      "timeframe": "Q1 2026 / 6 months",
      "owner": "CISO",
      "rationale": "Addresses credential theft..."
    }
  ],

  "confidence": {
    "level": "high",
    "score": 82,
    "evidence_count": 8,
    "conflicting_signals": false,
    "rationale": "Strong evidence from multiple sources"
  },

  "strategy_inputs": [
    {
      "category": "Business Context",
      "sources": ["Analyst-provided context"],
      "item_count": 1,
      "key_findings": ["Cloud migration..."]
    }
  ],

  "framework_references": [
    {
      "name": "ISO/IEC 27001",
      "version": "2022",
      "url": "https://www.iso.org/isoiec-27001-information-security.html",
      "purpose": "Provides ISMS requirements...",
      "applicable_controls": ["A.5.1", "A.8.5"]
    }
  ],

  "board_summary": {
    "executive_summary": "...",
    "roadmap": ["Q1 2026: Foundation phase...", "Q2 2026: ..."],
    "kpis_kris": ["KPI: MFA coverage > 95%", "KRI: Unpatched critical vulns < 5"],
    "talking_points": ["Our top risk is...", "We recommend..."]
  },

  "clarification_questions": ["Should regulatory urgency be prioritized over cost?"],

  "review": {
    "reviewer_name": "Omar",
    "status": "approved",
    "comments": "Increase resilience priority."
  }
}
```

---

## Project Structure

```
AI_Cyber_Strategy_Analyst_Assistant/
├── data/                              # Source documents and datasets
│   ├── README.md                      # Documentation for each data file
│   ├── ISO_IEC-270012022-ed.3.pdf     # ISO 27001 standard
│   ├── NIST.CSWP.29.pdf              # NIST CSF 2.0
│   ├── CIS_Controls_Guide_v8.1.2_0325_v2.pdf  # CIS Controls v8.1
│   ├── GDPR_FINAL_EPSU.pdf           # GDPR briefing
│   ├── audit_finding_dataset.json     # Audit findings
│   ├── risk_register_dataset.json     # Risk register
│   ├── cloud_migration_dataset.json   # Cloud migration risks
│   ├── third_party_risk_dataset.json  # Third-party risks
│   ├── incident_reports_dataset.json  # Incident reports
│   └── business_plan.json            # Business plan
├── cyber-strategy-ai/                 # Application root
│   ├── app/
│   │   ├── main.py                    # FastAPI entry point
│   │   ├── core/
│   │   │   ├── config.py              # Settings (pydantic-settings + .env)
│   │   │   └── qdrant_client.py       # Qdrant client singleton
│   │   ├── routers/
│   │   │   ├── documents.py           # /documents/* endpoints
│   │   │   ├── strategy.py            # /strategy/* endpoints
│   │   │   └── review.py              # Review endpoint
│   │   ├── models/
│   │   │   ├── schemas.py             # Pydantic request schemas
│   │   │   └── domain.py              # Domain models
│   │   ├── services/
│   │   │   ├── ingestion_service.py   # Extract → Chunk → Embed → Store
│   │   │   ├── upload_service.py      # File storage + registry
│   │   │   ├── retrieval_service.py   # Qdrant semantic search
│   │   │   ├── strategy_analysis_service.py  # 5-step LLM pipeline
│   │   │   ├── review_service.py      # Human review logic
│   │   │   ├── result_store.py        # JSON persistence
│   │   │   ├── report_service.py      # HTML report generator
│   │   │   └── powerpoint_service.py  # PPTX slide generator
│   │   ├── prompts/
│   │   │   ├── summarize_prompt.py    # Recurring themes prompt
│   │   │   ├── risk_mapping_prompt.py # Risk scoring prompt
│   │   │   ├── initiative_prompt.py   # Initiative generation prompt
│   │   │   ├── board_prompt.py        # Board output prompt
│   │   │   └── clarification_prompt.py # Clarification prompt
│   │   ├── repositories/
│   │   │   └── json_repository.py     # Generic JSON file store
│   │   └── utils/
│   │       ├── document_loader.py     # PDF/DOCX/TXT text extraction
│   │       ├── text_chunker.py        # Framework-aware chunking
│   │       └── json_normalizer.py     # JSON dataset normalization
│   ├── data/                          # Runtime data (generated)
│   │   ├── documents.json             # Ingested document registry
│   │   ├── strategy_results.json      # Strategy analysis results
│   │   └── uploads/                   # Uploaded file copies
│   ├── .env.example                   # Environment template
│   ├── .env                           # Local config (git-ignored)
│   └── requirements.txt              # Python dependencies
├── ingest_all.sh                      # Batch ingestion script
├── .gitignore                         # Git ignore rules
└── README.md                          # This file (project root)
```

---

## LLM Guardrails

- Uses **only retrieved evidence** — no hallucination from pre-training
- Conservative and **ISO 27001 aligned** by default
- Returns **structured JSON only** — all outputs are machine-parseable
- AI is **not a decision maker** — all outputs require human review
- **Confidence scoring** with automatic escalation on low confidence or conflicts
- **Evidence traceability** — every recommendation links back to source chunks
