from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
import uuid


# ── Chunk / Document ──────────────────────────────────────────────────────────

class ChunkMetadata(BaseModel):
    chunk_index: int
    document_type: str                  # pdf / docx / txt / json
    section: Optional[str] = None
    business_unit: Optional[str] = None
    framework: Optional[str] = None     # iso27001 | nist | cis | gdpr | internal
    control_id: Optional[str] = None    # e.g. "AC-1", "5.1", "CIS-3"


class DocumentChunk(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    document_id: str
    title: str
    description: str
    category: str   # audit | risk | incident | business | iso | nist | cis | gdpr
    source: str
    metadata: ChunkMetadata


class DocumentRecord(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    filename: str
    source_name: str
    category: str
    chunk_count: int
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)


# ── Gap 1: Evidence Traceability ──────────────────────────────────────────────

class EvidenceTrace(BaseModel):
    """Links an output finding back to its source evidence chunk."""
    chunk_title: str
    source: str                          # filename / source_name
    category: str                        # audit | risk | incident | ...
    framework: Optional[str] = None
    control_id: Optional[str] = None
    relevance_score: float = 0.0         # cosine similarity score from Qdrant


# ── Gap 2: Risk Scoring ───────────────────────────────────────────────────────

class RiskScore(BaseModel):
    """Structured risk score for a single risk mapping entry."""
    risk_statement: str
    likelihood: str                      # High | Medium | Low
    impact: str                          # High | Medium | Low
    risk_score: int                      # 1-9 (likelihood * impact 3x3)
    rationale: str


# ── Gap 3: Control Mapping ────────────────────────────────────────────────────

class ControlMapping(BaseModel):
    """Maps an initiative to one or more framework controls."""
    initiative: str
    iso27001: list[str] = []             # e.g. ["A.9.1.1", "A.9.2.3"]
    nist_csf: list[str] = []             # e.g. ["PR.AC-1", "ID.AM-5"]
    cis_controls: list[str] = []         # e.g. ["CIS-5", "CIS-6"]
    gdpr_articles: list[str] = []        # e.g. ["Article 32", "Article 25"]


# ── Gap 4: Business Plan Alignment ───────────────────────────────────────────

class BusinessAlignment(BaseModel):
    """Aligns a cyber initiative to a business objective."""
    initiative: str
    business_objective: str              # from business context / plan
    alignment_rationale: str
    dependency: Optional[str] = None     # e.g. "AWS migration Phase 2"


# ── Gap 5: Initiative with Effort / Cost ─────────────────────────────────────

class InitiativeDetail(BaseModel):
    """Full initiative with priority, effort, cost, and owner."""
    title: str
    priority: str                        # High | Medium | Low
    effort: str                          # Low | Medium | High
    cost_estimate: str                   # e.g. "$10k–$50k" or "Internal"
    timeframe: str                       # e.g. "Q1 2026", "30 days"
    owner: str                           # e.g. "CISO", "IT Security Team"
    rationale: str


# ── Gap 6: Confidence Score ───────────────────────────────────────────────────

class ConfidenceScore(BaseModel):
    """AI confidence in the overall analysis."""
    level: str                           # high | medium | low
    score: int                           # 0-100
    evidence_count: int
    conflicting_signals: bool
    rationale: str


# ── Strategy Inputs (what drove the analysis) ────────────────────────────────

class StrategyInput(BaseModel):
    """Grouped summary of one input source category."""
    category: str           # Business Inputs | Assessment Results | Threat Intelligence
    sources: list[str]      # source names used
    item_count: int         # number of evidence chunks from this category
    key_findings: list[str] # top findings extracted from this category


# ── Framework References (why each standard is used) ─────────────────────────

class FrameworkReference(BaseModel):
    """Explains the role of each applied framework in the strategy."""
    name: str               # ISO 27001 | NIST CSF | CIS Controls | GDPR
    version: str            # e.g. 2022, 2.0, v8.1
    url: str
    purpose: str            # why this framework is applied in this context
    applicable_controls: list[str]   # top controls referenced from evidence


# ── Board Summary ─────────────────────────────────────────────────────────────

class BoardSummary(BaseModel):
    executive_summary: str = ""
    roadmap: list[str] = []
    kpis_kris: list[str] = []
    talking_points: list[str] = []


# ── Review ────────────────────────────────────────────────────────────────────

class ReviewRecord(BaseModel):
    reviewer_name: str = ""
    status: str = ""
    comments: str = ""


# ── Full Strategy Result ──────────────────────────────────────────────────────

class StrategyResult(BaseModel):
    result_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    analysis_name: str
    status: str = "draft"               # draft | needs_review | approved | rejected

    # Core outputs
    recurring_themes: list[str] = []
    business_risk_mapping: list[str] = []
    prioritized_initiatives: list[str] = []
    strategy_options: list[str] = []
    clarification_questions: list[str] = []

    # Gap 1 — Evidence traceability
    evidence_traces: list[EvidenceTrace] = []

    # Gap 2 — Risk scoring
    risk_scores: list[RiskScore] = []

    # Gap 3 — Control mapping
    control_mappings: list[ControlMapping] = []

    # Gap 4 — Business alignment
    business_alignments: list[BusinessAlignment] = []

    # Gap 5 — Initiative details with effort/cost
    initiative_details: list[InitiativeDetail] = []

    # Gap 6 — Confidence score
    confidence: ConfidenceScore = Field(
        default_factory=lambda: ConfidenceScore(
            level="medium", score=50, evidence_count=0,
            conflicting_signals=False, rationale=""
        )
    )

    # Strategy inputs section
    strategy_inputs: list[StrategyInput] = []

    # Framework references section
    framework_references: list[FrameworkReference] = []

    board_summary: BoardSummary = Field(default_factory=BoardSummary)
    review: ReviewRecord = Field(default_factory=ReviewRecord)

    created_at: datetime = Field(default_factory=datetime.utcnow)
