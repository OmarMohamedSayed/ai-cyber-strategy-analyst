# Demo Guide

This page explains a full demo flow for the AI Cyber Strategy Analyst Assistant.

## Goal

Demonstrate how raw cybersecurity inputs are converted into:
- structured strategy JSON
- board-ready HTML report
- initiative PowerPoint slides

## Prerequisites

- Docker running
- Python environment prepared
- `.env` configured in `cyber-strategy-ai/.env`

## 1) Start dependencies

```bash
docker compose up -d qdrant
```

## 2) Start API

```bash
cd cyber-strategy-ai
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 3) Ingest sample data

```bash
cd ..
./ingest_all.sh
```

## 4) Run strategy analysis

Use Swagger (`/docs`) or curl:

```bash
curl -X POST http://localhost:8000/strategy/run \
  -H "Content-Type: application/json" \
  -d '{
    "analysis_name": "demo_strategy",
    "business_context": "Regional enterprise in cloud migration with regulatory pressure.",
    "focus_areas": ["IAM", "third-party risk", "resilience"],
    "top_k": 8
  }'
```

## 5) View outputs

- JSON result: `GET /strategy/results/{result_id}`
- HTML report: `GET /strategy/results/{result_id}/report`
- PPTX export: `GET /strategy/results/{result_id}/powerpoint/initiative-slide`
