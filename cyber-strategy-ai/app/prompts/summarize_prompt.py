from langchain_core.prompts import PromptTemplate

SUMMARIZE_TEMPLATE = """You are a senior cybersecurity strategist assisting a CISO.

Analyze the following evidence chunks and identify RECURRING CYBER THEMES.
Use ONLY the provided evidence. Do not hallucinate. Be conservative.

Each chunk is labeled with its SOURCE, CATEGORY, FRAMEWORK, and CONTROL_ID.
You MUST cite which chunks support each theme.

Business Context: {business_context}
Focus Areas: {focus_areas}

Evidence Chunks:
{chunks}

Return ONLY valid JSON:
{{
  "recurring_themes": [
    {{
      "theme": "Short theme title",
      "description": "1-2 sentence description",
      "evidence_refs": ["chunk title or source that supports this theme"]
    }}
  ],
  "confidence": {{
    "level": "high | medium | low",
    "score": 0-100,
    "conflicting_signals": true | false,
    "rationale": "Why this confidence level"
  }}
}}
"""

summarize_prompt = PromptTemplate(
    input_variables=["business_context", "focus_areas", "chunks"],
    template=SUMMARIZE_TEMPLATE,
)
