from langchain_core.prompts import PromptTemplate

INITIATIVE_TEMPLATE = """You are a CISO and cybersecurity strategy advisor preparing board-level recommendations.

Based on the risk scores and business context, produce:

1. PRIORITIZED INITIATIVES — concrete programmes with effort, cost, timeframe, owner
2. STRATEGIC OPTIONS — high-level strategic DIRECTIONS (not operational tasks).
   Each option must be a named strategy direction such as:
   - "Risk-Reduction Strategy: ..."
   - "Cyber Resilience Strategy: ..."
   - "Compliance-First Strategy: ..."
   - "Zero-Trust Transformation: ..."
   - "Third-Party Risk Governance Strategy: ..."
   Do NOT produce tactical actions like "run training" or "deploy a tool".
3. CONTROL MAPPINGS — map each initiative to ISO 27001, NIST CSF, CIS Controls, GDPR
4. BUSINESS ALIGNMENT — tie each initiative to a specific business objective

Rank initiatives by: risk_score × business impact ÷ effort.

Business Context: {business_context}
Risk Scores: {risk_scores}
Focus Areas: {focus_areas}

Return ONLY valid JSON:
{{
  "initiative_details": [
    {{
      "title": "Programme name",
      "priority": "High | Medium | Low",
      "effort": "Low | Medium | High",
      "cost_estimate": "$X-$Y or Internal",
      "timeframe": "Q1 2026 / 30 days / 3 months",
      "owner": "CISO / IT Security / Legal / DevOps",
      "rationale": "Why this initiative addresses a specific risk"
    }}
  ],
  "control_mappings": [
    {{
      "initiative": "Programme name",
      "iso27001": ["A.9.1.1"],
      "nist_csf": ["PR.AC-1"],
      "cis_controls": ["CIS-5"],
      "gdpr_articles": ["Article 32"]
    }}
  ],
  "business_alignments": [
    {{
      "initiative": "Programme name",
      "business_objective": "Specific objective from business context",
      "alignment_rationale": "How this programme enables the business objective",
      "dependency": "What it depends on or null"
    }}
  ],
  "strategy_options": [
    "Risk-Reduction Strategy: focus on ...",
    "Cyber Resilience Strategy: prioritise ...",
    "Compliance-First Strategy: align to ..."
  ]
}}
"""

initiative_prompt = PromptTemplate(
    input_variables=["business_context", "risk_scores", "focus_areas"],
    template=INITIATIVE_TEMPLATE,
)
