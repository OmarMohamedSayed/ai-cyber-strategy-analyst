# AI Cyber Strategy Analyst Assistant

AI Cyber Strategy Analyst Assistant is an open-source, AI-powered cybersecurity strategy platform that combines Retrieval-Augmented Generation (RAG), Large Language Models (LLMs), and multi-agent orchestration to support CISO teams in making evidence-based strategic decisions.

## What It Does

The platform ingests security and business inputs (framework documents, audit findings, risk registers, incidents, and plans), retrieves relevant context through vector search, and generates actionable cybersecurity strategy outputs for leadership and board communication.

## Core Features

- **Framework-aligned risk scoring** across NIST CSF, ISO/IEC 27001, CIS Controls, and GDPR
- **AI-powered strategy generation** with prioritized initiatives and business alignment
- **Board-ready outputs** including executive summaries, roadmaps, KPIs/KRIs, HTML reports, and PowerPoint slides
- **FastAPI backend** with OpenAPI/Swagger endpoints for integration and automation
- **Qdrant vector search** for semantic retrieval and evidence traceability
- **Human-in-the-loop workflow** to review, clarify, approve, or reject AI-generated results

## Architecture Highlights

- **RAG pipeline** for grounded responses from your ingested documents
- **LLM synthesis layer** for theme extraction, risk mapping, and initiative generation
- **Multi-agent orchestration** to structure analysis steps and maintain output consistency
- **Traceable evidence model** linking recommendations back to source chunks and controls

## GitHub Repository

[https://github.com/OmarMohamedSayed/ai_cyber_strategy_analyst_assistant](https://github.com/OmarMohamedSayed/ai_cyber_strategy_analyst_assistant)

