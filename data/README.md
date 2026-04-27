# Data Directory

This folder contains all source documents and datasets that feed the AI Cyber Strategy Analyst Assistant's RAG (Retrieval-Augmented Generation) pipeline. Each file is ingested, chunked, embedded, and stored in Qdrant for semantic retrieval during strategy analysis.

---

## Cybersecurity Framework Documents (PDF)

These are the foundational compliance and security frameworks. They provide the standards, controls, and regulatory requirements that anchor every strategy recommendation.

| File | Framework | Why It's Used |
|------|-----------|---------------|
| `ISO_IEC-270012022-ed.3.pdf` | **ISO/IEC 27001:2022** | The international standard for Information Security Management Systems (ISMS). Provides Annex A controls (93 controls across 4 themes) that form the governance backbone of the cybersecurity strategy. Used to map initiatives to specific control clauses and validate that recommendations meet certification requirements. |
| `NIST.CSWP.29.pdf` | **NIST Cybersecurity Framework 2.0** | The US national framework organizing cybersecurity around six functions: Govern, Identify, Protect, Detect, Respond, and Recover. Enables risk-based prioritization of initiatives and provides a common language for board-level communication. |
| `CIS_Controls_Guide_v8.1.2_0325_v2.pdf` | **CIS Controls v8.1** | Implementation-level safeguards organized into 18 control families and three Implementation Groups (IG1-IG3). Translates high-level strategy into actionable technical controls with clear prioritization for organizations of different maturity levels. |
| `GDPR_FINAL_EPSU.pdf` | **GDPR (General Data Protection Regulation)** | EU data protection regulation briefing. Defines obligations for personal data handling relevant to cloud migration, third-party data processing, and cross-border data transfers. Essential for any strategy involving customer or employee data. |
| `2026_Cyber_Strategy — Cyber Strategy Report.pdf` | **Internal Cyber Strategy Report** | Organization-specific cybersecurity strategy document. Provides internal context about current security posture, strategic objectives, and planned initiatives that the AI uses to align recommendations with existing organizational direction. |

---

## Operational Datasets (JSON)

These are structured datasets representing the organization's current security posture. Each item becomes an individually searchable evidence chunk in the vector database.

| File | Dataset Type | Records | Why It's Used |
|------|-------------|---------|---------------|
| `audit_finding_dataset.json` | **Internal Audit Findings** | ~15 items | Contains policy compliance gaps, control deficiencies, and audit observations. The AI uses these to identify recurring weaknesses, map them to framework controls, and prioritize remediation initiatives. |
| `risk_register_dataset.json` | **Enterprise Risk Register** | ~25 items | Enterprise-wide risks with likelihood, impact, and risk scores. Drives the risk-scoring step of the analysis pipeline — the AI correlates these risks with audit findings and framework gaps to produce weighted recommendations. |
| `cloud_migration_dataset.json` | **Cloud Migration Risk Assessment** | ~25 items | Workload-level security gaps identified during cloud migration planning. Includes configuration risks, shared responsibility gaps, and compliance concerns. Ensures cloud-specific risks are reflected in the strategy. |
| `third_party_risk_dataset.json` | **Third-Party Risk Register** | ~25 items | Vendor and third-party compliance assessments covering SLA adherence, data handling, and security posture. Critical for strategies involving supply chain risk and vendor governance. |
| `incident_reports_dataset.json` | **Incident Reports** | ~15 items | Historical security incidents with severity, response actions, and lessons learned. The AI uses these as evidence for threat patterns and to validate that proposed initiatives address real-world attack vectors. |
| `business_plan.json` | **Business Plan** | ~5 items | Business objectives, growth plans, and strategic priorities. Provides the business context that ensures cybersecurity initiatives are aligned with organizational goals rather than being purely technical. |

---

## How These Documents Are Used in the Pipeline

```
1. INGESTION     → Each document is uploaded via /documents/upload or /documents/ingest-json
2. EXTRACTION    → PDFs: text extracted via pypdf | JSON: items normalized to common schema
3. CHUNKING      → Structure-aware splitting with framework-specific chunk sizes and heading detection
4. EMBEDDING     → OpenAI text-embedding-3-small converts each chunk to a 1536-dim vector
5. STORAGE       → Vectors stored in Qdrant with full metadata (source, category, framework, control_id)
6. RETRIEVAL     → During /strategy/run, the top-K most relevant chunks are retrieved via semantic search
7. ANALYSIS      → Retrieved evidence feeds a multi-step LLM pipeline that produces strategy outputs
```

---

## Adding New Documents

To add new evidence sources:

1. **PDF/DOCX/TXT files** — Place them in this folder and use the `/documents/upload` endpoint or add an entry to `ingest_all.sh`
2. **JSON datasets** — Follow the existing schema patterns (flat list or `{items: [...]}` wrapper) and use `/documents/ingest-json`
3. **New categories** — Update the `ALLOWED_CATEGORIES` environment variable in `.env`

The system auto-detects framework type from the category and source name, applying optimized chunk sizes and heading patterns automatically.
