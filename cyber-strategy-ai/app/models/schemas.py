from typing import Optional
from pydantic import BaseModel, Field

from app.core.config import get_settings


# ── Strategy ──────────────────────────────────────────────────────────────────

class StrategyRunRequest(BaseModel):
    analysis_name: str
    business_context: str
    focus_areas: list[str] = []
    top_k: int = Field(default_factory=lambda: get_settings().default_top_k)


class ClarificationAnswer(BaseModel):
    question: str
    answer: str


class ClarifyRequest(BaseModel):
    analysis_name: str
    answers: list[ClarificationAnswer]


# ── Review ────────────────────────────────────────────────────────────────────

class ReviewRequest(BaseModel):
    reviewer_name: str
    status: str          # approved | rejected | needs_review
    comments: Optional[str] = ""
