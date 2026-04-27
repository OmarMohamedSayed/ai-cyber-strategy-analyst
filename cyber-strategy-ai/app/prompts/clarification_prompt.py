from langchain_core.prompts import PromptTemplate

CLARIFICATION_TEMPLATE = """You are a cybersecurity strategy analyst.

Review the evidence and analysis. Identify gaps, missing business context, or conflicting
signals that require CLARIFICATION from the human expert before finalizing.

Consider specifically:
- Are business objectives explicitly stated or assumed?
- Are effort/cost estimates possible with current data?
- Are any control mappings ambiguous?
- Is evidence from all required categories (audit, risk, incident, business)?
- Are there conflicting signals between frameworks?

Business Context: {business_context}
Themes Found: {themes}
Risk Scores: {risk_scores}
Confidence: {confidence}
Evidence Count: {evidence_count}
Conflicting Signals: {conflicting_signals}

Return ONLY valid JSON:
{{
  "questions": [
    "Question 1?",
    "Question 2?"
  ]
}}
"""

clarification_prompt = PromptTemplate(
    input_variables=[
        "business_context", "themes", "risk_scores",
        "confidence", "evidence_count", "conflicting_signals"
    ],
    template=CLARIFICATION_TEMPLATE,
)
