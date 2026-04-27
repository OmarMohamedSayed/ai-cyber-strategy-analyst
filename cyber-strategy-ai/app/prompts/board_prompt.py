from langchain_core.prompts import PromptTemplate

BOARD_TEMPLATE = """You are a CISO preparing a board-level cybersecurity strategy presentation.

Create a BOARD-READY SUMMARY. Be concise, non-technical, and focused on business value.
Reference the confidence score and control frameworks where relevant.

Business Context: {business_context}
Recurring Themes: {themes}
Risk Scores: {risk_scores}
Prioritized Initiatives: {initiatives}
Control Mappings: {control_mappings}
Business Alignments: {business_alignments}
Confidence: {confidence}

Return ONLY valid JSON:
{{
  "executive_summary": "2-3 sentences for the board, referencing top risks and business impact",
  "roadmap": [
    "Q1 2026: action",
    "Q2 2026: action",
    "Q3 2026: action"
  ],
  "kpis_kris": [
    "KPI: measurable metric",
    "KRI: risk threshold indicator"
  ],
  "talking_points": [
    "Board talking point 1",
    "Board talking point 2"
  ]
}}
"""

board_prompt = PromptTemplate(
    input_variables=[
        "business_context", "themes", "risk_scores", "initiatives",
        "control_mappings", "business_alignments", "confidence"
    ],
    template=BOARD_TEMPLATE,
)
