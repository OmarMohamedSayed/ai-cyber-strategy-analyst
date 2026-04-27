from langchain_core.prompts import PromptTemplate

RISK_MAPPING_TEMPLATE = """You are a cybersecurity risk advisor aligned with ISO 27001.

Map each cyber theme to a STRUCTURED BUSINESS RISK with a numeric risk score.
Use only the evidence provided. Cite the source evidence for each risk.

Risk Score = Likelihood × Impact using this 3×3 matrix:
  High×High=9, High×Med=6, High×Low=3
  Med×High=6,  Med×Med=4,  Med×Low=2
  Low×High=3,  Low×Med=2,  Low×Low=1

Business Context: {business_context}
Recurring Themes: {themes}

Evidence Chunks:
{chunks}

Return ONLY valid JSON:
{{
  "risk_scores": [
    {{
      "risk_statement": "Clear business risk statement",
      "likelihood": "High | Medium | Low",
      "impact": "High | Medium | Low",
      "risk_score": 1-9,
      "rationale": "Why this score, citing specific evidence source"
    }}
  ]
}}
"""

risk_mapping_prompt = PromptTemplate(
    input_variables=["business_context", "themes", "chunks"],
    template=RISK_MAPPING_TEMPLATE,
)
