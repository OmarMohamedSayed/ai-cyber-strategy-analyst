import json
from langchain_openai import ChatOpenAI

from app.core.config import get_settings
from app.models.domain import (
    StrategyResult, BoardSummary,
    EvidenceTrace, RiskScore, ControlMapping, BusinessAlignment,
    InitiativeDetail, ConfidenceScore,
    StrategyInput, FrameworkReference,
)
from app.prompts.summarize_prompt import summarize_prompt
from app.prompts.risk_mapping_prompt import risk_mapping_prompt
from app.prompts.initiative_prompt import initiative_prompt
from app.prompts.board_prompt import board_prompt
from app.prompts.clarification_prompt import clarification_prompt
from app.services.retrieval_service import retrieve_chunks
from app.services.result_store import save_result


def _llm() -> ChatOpenAI:
    settings = get_settings()
    return ChatOpenAI(
        model=settings.openai_model,
        openai_api_key=settings.openai_api_key,
        temperature=settings.llm_temperature,
    )


def _call_llm(prompt_template, **kwargs) -> dict:
    llm = _llm()
    prompt_text = prompt_template.format(**kwargs)
    response = llm.invoke(prompt_text)
    content = response.content.strip()
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
    return json.loads(content)


def _format_chunks(chunks: list[dict]) -> str:
    """Format chunks with full provenance metadata for LLM context."""
    lines = []
    for i, c in enumerate(chunks, 1):
        fw = c.get("framework") or ""
        ctrl = c.get("control_id") or ""
        meta = f" | Framework: {fw}" if fw else ""
        meta += f" | Control: {ctrl}" if ctrl else ""
        lines.append(
            f"[{i}] SOURCE: {c['source']} | CATEGORY: {c['category'].upper()}{meta}\n"
            f"TITLE: {c['title']}\n"
            f"{c['description'][:500]}"
        )
    return "\n\n".join(lines)


def _build_evidence_traces(chunks: list[dict]) -> list[EvidenceTrace]:
    return [
        EvidenceTrace(
            chunk_title=c["title"],
            source=c["source"],
            category=c["category"],
            framework=c.get("framework") or None,
            control_id=c.get("control_id") or None,
            relevance_score=round(c.get("score", 0.0), 4),
        )
        for c in chunks
    ]


def _parse_confidence(raw: dict, evidence_count: int) -> ConfidenceScore:
    level = raw.get("level", "medium")
    score = raw.get("score", 50)
    conflicting = raw.get("conflicting_signals", False)
    rationale = raw.get("rationale", "")
    # Penalise score if evidence is sparse
    if evidence_count < 3:
        score = min(score, 40)
        level = "low"
    return ConfidenceScore(
        level=level,
        score=score,
        evidence_count=evidence_count,
        conflicting_signals=conflicting,
        rationale=rationale,
    )


def _parse_risk_scores(raw: list[dict]) -> list[RiskScore]:
    out = []
    for r in raw:
        try:
            out.append(RiskScore(
                risk_statement=r.get("risk_statement", ""),
                likelihood=r.get("likelihood", "Medium"),
                impact=r.get("impact", "Medium"),
                risk_score=int(r.get("risk_score", 4)),
                rationale=r.get("rationale", ""),
            ))
        except Exception:
            continue
    return out


def _parse_initiative_details(raw: list[dict]) -> list[InitiativeDetail]:
    out = []
    for r in raw:
        try:
            out.append(InitiativeDetail(
                title=r.get("title", ""),
                priority=r.get("priority", "Medium"),
                effort=r.get("effort", "Medium"),
                cost_estimate=r.get("cost_estimate", "TBD"),
                timeframe=r.get("timeframe", "TBD"),
                owner=r.get("owner", "CISO"),
                rationale=r.get("rationale", ""),
            ))
        except Exception:
            continue
    return out


def _parse_control_mappings(raw: list[dict]) -> list[ControlMapping]:
    out = []
    for r in raw:
        try:
            out.append(ControlMapping(
                initiative=r.get("initiative", ""),
                iso27001=r.get("iso27001", []),
                nist_csf=r.get("nist_csf", []),
                cis_controls=r.get("cis_controls", []),
                gdpr_articles=r.get("gdpr_articles", []),
            ))
        except Exception:
            continue
    return out


def _parse_business_alignments(raw: list[dict]) -> list[BusinessAlignment]:
    out = []
    for r in raw:
        try:
            out.append(BusinessAlignment(
                initiative=r.get("initiative", ""),
                business_objective=r.get("business_objective", ""),
                alignment_rationale=r.get("alignment_rationale", ""),
                dependency=r.get("dependency") or None,
            ))
        except Exception:
            continue
    return out


_CATEGORY_GROUPS = {
    "Business Inputs":        {"business"},
    "Assessment Results":     {"audit", "risk", "incident"},
    "Threat Intelligence":    {"incident"},
    "Compliance & Standards": {"iso", "nist", "cis", "gdpr"},
}

_FRAMEWORK_META = {
    "iso27001": FrameworkReference(
        name="ISO/IEC 27001",
        version="2022",
        url="https://www.iso.org/isoiec-27001-information-security.html",
        purpose="Provides the information security management system (ISMS) requirements and Annex A controls that anchor the overall governance structure.",
        applicable_controls=[],
    ),
    "nist": FrameworkReference(
        name="NIST Cybersecurity Framework",
        version="2.0",
        url="https://www.nist.gov/cyberframework",
        purpose="Structures the strategy around six functions — Govern, Identify, Protect, Detect, Respond, Recover — enabling risk-based prioritisation.",
        applicable_controls=[],
    ),
    "cis": FrameworkReference(
        name="CIS Controls",
        version="v8.1",
        url="https://www.cisecurity.org/controls",
        purpose="Provides implementation-level safeguards mapped to implementation groups (IG1–IG3), used to translate strategy into actionable technical controls.",
        applicable_controls=[],
    ),
    "gdpr": FrameworkReference(
        name="General Data Protection Regulation",
        version="2018",
        url="https://gdpr.eu/",
        purpose="Defines data protection obligations relevant to personal data processed during cloud migration and third-party engagements.",
        applicable_controls=[],
    ),
}


def _build_strategy_inputs(
    chunks: list[dict], business_context: str, focus_areas: list[str]
) -> list[StrategyInput]:
    """Group evidence chunks by input category and extract key findings."""
    group_map: dict[str, list[dict]] = {g: [] for g in _CATEGORY_GROUPS}

    for chunk in chunks:
        cat = chunk.get("category", "").lower()
        for group, cats in _CATEGORY_GROUPS.items():
            if cat in cats:
                group_map[group].append(chunk)
                break

    inputs: list[StrategyInput] = []
    for group, items in group_map.items():
        if not items:
            continue
        sources = list(dict.fromkeys(c["source"] for c in items))
        key_findings = [c["title"] for c in sorted(items, key=lambda x: -x.get("score", 0))[:3]]
        inputs.append(StrategyInput(
            category=group,
            sources=sources,
            item_count=len(items),
            key_findings=key_findings,
        ))

    # Always include the business context as an input
    if business_context:
        inputs.insert(0, StrategyInput(
            category="Business Context",
            sources=["Analyst-provided context"],
            item_count=1,
            key_findings=[business_context[:120] + ("…" if len(business_context) > 120 else "")],
        ))

    return inputs


def _build_framework_references(
    chunks: list[dict], control_mappings: list[ControlMapping]
) -> list[FrameworkReference]:
    """Collect which frameworks appeared in evidence and populate their controls."""
    # Gather frameworks from evidence
    active_fws: set[str] = set()
    fw_controls: dict[str, list[str]] = {k: [] for k in _FRAMEWORK_META}

    for chunk in chunks:
        fw = (chunk.get("framework") or "").lower()
        ctrl = chunk.get("control_id") or ""
        if fw in _FRAMEWORK_META:
            active_fws.add(fw)
            if ctrl and ctrl not in fw_controls[fw]:
                fw_controls[fw].append(ctrl)

    # Enrich with controls from mappings
    for mapping in control_mappings:
        for ctrl in mapping.iso27001:
            if ctrl not in fw_controls["iso27001"]:
                fw_controls["iso27001"].append(ctrl)
                active_fws.add("iso27001")
        for ctrl in mapping.nist_csf:
            if ctrl not in fw_controls["nist"]:
                fw_controls["nist"].append(ctrl)
                active_fws.add("nist")
        for ctrl in mapping.cis_controls:
            if ctrl not in fw_controls["cis"]:
                fw_controls["cis"].append(ctrl)
                active_fws.add("cis")
        for ctrl in mapping.gdpr_articles:
            if ctrl not in fw_controls["gdpr"]:
                fw_controls["gdpr"].append(ctrl)
                active_fws.add("gdpr")

    result = []
    for fw_key in ["iso27001", "nist", "cis", "gdpr"]:
        if fw_key in active_fws:
            ref = _FRAMEWORK_META[fw_key].model_copy(
                update={"applicable_controls": fw_controls[fw_key][:8]}
            )
            result.append(ref)
    return result


def run_strategy_analysis(
    analysis_name: str,
    business_context: str,
    focus_areas: list[str],
    top_k: int = 8,
) -> dict:

    # ── 1. Retrieve relevant chunks ───────────────────────────────────────────
    query = f"{business_context} {' '.join(focus_areas)}"
    chunks = retrieve_chunks(query, top_k=top_k)
    chunks_text = _format_chunks(chunks)
    evidence_count = len(chunks)

    # Gap 1 — Evidence traces (built directly from retrieved chunks)
    evidence_traces = _build_evidence_traces(chunks)

    # ── 2. Summarize themes + confidence ─────────────────────────────────────
    step1 = _call_llm(
        summarize_prompt,
        business_context=business_context,
        focus_areas=", ".join(focus_areas),
        chunks=chunks_text,
    )
    raw_themes = step1.get("recurring_themes", [])
    # Flatten to strings for backward compat display
    themes: list[str] = [
        f"{t['theme']}: {t['description']}" if isinstance(t, dict) else str(t)
        for t in raw_themes
    ]
    raw_conf = step1.get("confidence", {})
    if isinstance(raw_conf, str):
        raw_conf = {"level": raw_conf, "score": 50, "conflicting_signals": False, "rationale": ""}

    # Gap 6 — Confidence score
    confidence = _parse_confidence(raw_conf, evidence_count)

    # ── 3. Risk scoring ───────────────────────────────────────────────────────
    step2 = _call_llm(
        risk_mapping_prompt,
        business_context=business_context,
        themes="\n".join(themes),
        chunks=chunks_text,
    )
    # Gap 2 — Risk scores
    risk_scores = _parse_risk_scores(step2.get("risk_scores", []))
    # Flat strings for display / backward compat
    risk_mapping: list[str] = [
        f"[{r.risk_score}/9 | {r.likelihood}×{r.impact}] {r.risk_statement}"
        for r in risk_scores
    ]
    risk_scores_text = json.dumps([r.model_dump() for r in risk_scores])

    # ── 4. Initiatives + control mapping + business alignment ─────────────────
    step3 = _call_llm(
        initiative_prompt,
        business_context=business_context,
        risk_scores=risk_scores_text,
        focus_areas=", ".join(focus_areas),
    )
    # Gap 3 — Control mappings
    control_mappings = _parse_control_mappings(step3.get("control_mappings", []))
    # Gap 4 — Business alignments
    business_alignments = _parse_business_alignments(step3.get("business_alignments", []))
    # Gap 5 — Initiative details
    initiative_details = _parse_initiative_details(step3.get("initiative_details", []))
    strategy_options: list[str] = step3.get("strategy_options", [])

    # Flat initiative strings for display
    initiatives: list[str] = [
        f"[{d.priority}] {d.title} | Effort: {d.effort} | Cost: {d.cost_estimate} | {d.timeframe} | Owner: {d.owner}"
        for d in initiative_details
    ]

    # ── 5. Board-ready output ─────────────────────────────────────────────────
    step4 = _call_llm(
        board_prompt,
        business_context=business_context,
        themes="\n".join(themes),
        risk_scores=risk_scores_text,
        initiatives="\n".join(initiatives),
        control_mappings=json.dumps([c.model_dump() for c in control_mappings]),
        business_alignments=json.dumps([b.model_dump() for b in business_alignments]),
        confidence=json.dumps(confidence.model_dump()),
    )
    board = BoardSummary(
        executive_summary=step4.get("executive_summary", ""),
        roadmap=step4.get("roadmap", []),
        kpis_kris=step4.get("kpis_kris", []),
        talking_points=step4.get("talking_points", []),
    )

    # ── 6. Clarification questions ────────────────────────────────────────────
    step5 = _call_llm(
        clarification_prompt,
        business_context=business_context,
        themes="\n".join(themes),
        risk_scores=risk_scores_text,
        confidence=json.dumps(confidence.model_dump()),
        evidence_count=str(evidence_count),
        conflicting_signals=str(confidence.conflicting_signals),
    )
    clarification_questions: list[str] = step5.get("questions", [])

    # ── 7. Determine status ───────────────────────────────────────────────────
    needs_review = (
        confidence.level == "low"
        or confidence.conflicting_signals
        or evidence_count < 2
        or bool(clarification_questions)
    )
    status = "needs_review" if needs_review else "draft"

    # ── 8. Build inputs + framework references ───────────────────────────────
    strategy_inputs = _build_strategy_inputs(chunks, business_context, focus_areas)
    framework_references = _build_framework_references(chunks, control_mappings)

    # ── 9. Build and persist result ───────────────────────────────────────────
    result = StrategyResult(
        analysis_name=analysis_name,
        status=status,
        recurring_themes=themes,
        business_risk_mapping=risk_mapping,
        prioritized_initiatives=initiatives,
        strategy_options=strategy_options,
        clarification_questions=clarification_questions,
        evidence_traces=evidence_traces,
        risk_scores=risk_scores,
        control_mappings=control_mappings,
        business_alignments=business_alignments,
        initiative_details=initiative_details,
        confidence=confidence,
        strategy_inputs=strategy_inputs,
        framework_references=framework_references,
        board_summary=board,
    )
    record = result.model_dump()
    save_result(record)
    return record
