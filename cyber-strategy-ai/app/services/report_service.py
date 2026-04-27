"""
Board-ready HTML report — consulting style.

Flow:  Cover → Inputs → Analysis → Strategy → Execution → Appendix
"""

from datetime import datetime


_STATUS_STYLE = {
    "approved":     ("bg-emerald-100 text-emerald-800 border-emerald-300", "fa-circle-check"),
    "needs_review": ("bg-amber-100 text-amber-800 border-amber-300",       "fa-triangle-exclamation"),
    "draft":        ("bg-slate-100 text-slate-700 border-slate-300",        "fa-file-pen"),
    "rejected":     ("bg-red-100 text-red-800 border-red-300",              "fa-circle-xmark"),
}
_PRIORITY_COLOR = {"High": "red", "Medium": "amber", "Low": "green"}
_EFFORT_COLOR   = {"High": "rose", "Medium": "orange", "Low": "teal"}
_LH_COLOR       = {"High": "red", "Medium": "amber", "Low": "green"}
_FW_STYLE = {
    "ISO/IEC 27001":                 ("bg-blue-700",   "ISO 27001"),
    "NIST Cybersecurity Framework":  ("bg-indigo-700", "NIST CSF"),
    "CIS Controls":                  ("bg-cyan-700",   "CIS v8.1"),
    "General Data Protection Regulation": ("bg-violet-700", "GDPR"),
}
_INPUT_ICON = {
    "Business Context":      ("fa-building",        "bg-teal-600"),
    "Business Inputs":       ("fa-briefcase",        "bg-teal-600"),
    "Assessment Results":    ("fa-magnifying-glass", "bg-orange-600"),
    "Threat Intelligence":   ("fa-biohazard",        "bg-red-600"),
    "Compliance & Standards":("fa-scale-balanced",   "bg-blue-600"),
}


def _status_badge(status: str) -> str:
    style, icon = _STATUS_STYLE.get(status, _STATUS_STYLE["draft"])
    return (f'<span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full '
            f'border text-sm font-semibold {style}">'
            f'<i class="fa-solid {icon}"></i>{status.replace("_"," ").title()}</span>')


def _section_header(title: str, subtitle: str = "", step: int = 0) -> str:
    step_html = (f'<span class="w-7 h-7 rounded-full bg-slate-700 text-white text-xs '
                 f'font-bold flex items-center justify-center flex-shrink-0">{step}</span>'
                 if step else "")
    sub_html = f'<p class="text-slate-500 text-sm mt-0.5">{subtitle}</p>' if subtitle else ""
    return f"""
    <div class="flex items-center gap-3 mb-4">
      {step_html}
      <div>
        <h2 class="text-lg font-bold text-slate-800">{title}</h2>
        {sub_html}
      </div>
    </div>"""


def _card(title: str, icon: str, color: str, content: str, count: str = "") -> str:
    count_html = (f'<span class="ml-auto text-xs px-2 py-0.5 rounded-full bg-slate-100 '
                  f'text-slate-600 border font-medium">{count}</span>') if count else ""
    return f"""<div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
      <div class="px-5 py-4 border-b border-slate-100 flex items-center gap-2">
        <div class="w-8 h-8 rounded-lg {color} flex items-center justify-center">
          <i class="fa-solid {icon} text-white text-sm"></i>
        </div>
        <h3 class="font-semibold text-slate-800">{title}</h3>
        {count_html}
      </div>
      <div class="px-5 py-4">{content}</div>
    </div>"""


# ── Section 1: Strategy Inputs ────────────────────────────────────────────────

def _inputs_section(inputs: list[dict]) -> str:
    if not inputs:
        return '<p class="text-slate-400 italic text-sm">No input sources recorded.</p>'
    cards = ""
    for inp in inputs:
        cat = inp.get("category", "")
        icon, color = _INPUT_ICON.get(cat, ("fa-database", "bg-slate-600"))
        sources = inp.get("sources", [])
        findings = inp.get("key_findings", [])
        count = inp.get("item_count", 0)
        src_html = ", ".join(f'<span class="text-xs bg-slate-100 border border-slate-200 px-1.5 py-0.5 rounded text-slate-600">{s}</span>' for s in sources)
        findings_html = "".join(f'<li class="text-xs text-slate-600 py-0.5">• {f}</li>' for f in findings)
        cards += f"""<div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
          <div class="px-4 py-3 border-b border-slate-100 flex items-center gap-2">
            <div class="w-7 h-7 rounded-lg {color} flex items-center justify-center flex-shrink-0">
              <i class="fa-solid {icon} text-white text-xs"></i>
            </div>
            <p class="font-semibold text-slate-800 text-sm">{cat}</p>
            <span class="ml-auto text-xs bg-slate-100 text-slate-500 px-2 py-0.5 rounded-full border">{count} items</span>
          </div>
          <div class="px-4 py-3">
            <div class="flex flex-wrap gap-1 mb-2">{src_html}</div>
            <ul class="mt-1">{findings_html}</ul>
          </div>
        </div>"""
    return f'<div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">{cards}</div>'


# ── Section 2: Frameworks & Standards ────────────────────────────────────────

def _frameworks_section(frameworks: list[dict]) -> str:
    if not frameworks:
        return '<p class="text-slate-400 italic text-sm">No frameworks detected in evidence.</p>'
    cards = ""
    for fw in frameworks:
        name = fw.get("name", "")
        version = fw.get("version", "")
        url = fw.get("url", "#")
        purpose = fw.get("purpose", "")
        controls = fw.get("applicable_controls", [])
        badge_color, badge_label = _FW_STYLE.get(name, ("bg-slate-600", name))
        ctrl_tags = " ".join(
            f'<span class="text-xs font-mono px-1.5 py-0.5 rounded bg-slate-100 border border-slate-200 text-slate-700">{c}</span>'
            for c in controls[:6]
        )
        cards += f"""<div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
          <div class="px-4 py-3 border-b border-slate-100 flex items-center gap-2">
            <span class="text-xs font-bold text-white px-2 py-1 rounded {badge_color}">{badge_label}</span>
            <span class="text-slate-500 text-xs">v{version}</span>
            <a href="{url}" target="_blank" class="ml-auto text-xs text-blue-500 hover:underline">
              <i class="fa-solid fa-arrow-up-right-from-square mr-1"></i>Reference
            </a>
          </div>
          <div class="px-4 py-3">
            <p class="text-sm text-slate-700 leading-relaxed mb-3">{purpose}</p>
            {"<div class='flex flex-wrap gap-1'>" + ctrl_tags + "</div>" if controls else ""}
          </div>
        </div>"""
    return f'<div class="grid grid-cols-1 md:grid-cols-2 gap-4">{cards}</div>'


# ── Section 3: Analysis — Themes + Risk Scores ───────────────────────────────

def _themes_list(themes: list[str]) -> str:
    if not themes:
        return '<p class="text-slate-400 italic text-sm">No themes identified.</p>'
    return "".join(
        f'<div class="flex gap-2 items-start py-2 border-b border-slate-100 last:border-0">'
        f'<i class="fa-solid fa-circle-dot text-rose-400 mt-1 text-xs flex-shrink-0"></i>'
        f'<span class="text-sm text-slate-700">{t}</span></div>'
        for t in themes
    )


def _risk_score_cards(risk_scores: list[dict]) -> str:
    if not risk_scores:
        return '<p class="text-slate-400 italic text-sm">No risk scores calculated.</p>'
    sorted_risks = sorted(risk_scores, key=lambda r: r.get("risk_score", 0), reverse=True)

    def _color(s: int) -> str:
        return "red" if s >= 7 else "amber" if s >= 4 else "green"

    cards = ""
    for r in sorted_risks:
        score = r.get("risk_score", 0)
        c = _color(score)
        lh = r.get("likelihood", "")
        imp = r.get("impact", "")
        lhc = _LH_COLOR.get(lh, "slate")
        impc = _LH_COLOR.get(imp, "slate")
        cards += f"""<div class="p-4 rounded-xl border-l-4 border-{c}-500 bg-{c}-50 border border-{c}-200">
          <div class="flex items-start justify-between gap-2 mb-2">
            <p class="text-sm font-semibold text-slate-800">{r.get("risk_statement","")}</p>
            <span class="w-9 h-9 rounded-full bg-{c}-500 text-white font-bold text-sm flex items-center justify-center shadow flex-shrink-0">{score}</span>
          </div>
          <div class="flex gap-2 flex-wrap mb-2">
            <span class="text-xs px-2 py-0.5 rounded-full bg-{lhc}-100 text-{lhc}-800 border border-{lhc}-200">Likelihood: {lh}</span>
            <span class="text-xs px-2 py-0.5 rounded-full bg-{impc}-100 text-{impc}-800 border border-{impc}-200">Impact: {imp}</span>
          </div>
          <p class="text-xs text-slate-600">{r.get("rationale","")}</p>
        </div>"""
    return f'<div class="flex flex-col gap-3">{cards}</div>'


def _risk_chart_js(risk_scores: list[dict]) -> str:
    if not risk_scores:
        return ""
    items = sorted(risk_scores, key=lambda r: r.get("risk_score", 0), reverse=True)[:8]
    labels = [r.get("risk_statement", "")[:32] for r in items]
    scores = [r.get("risk_score", 0) for r in items]
    colors = [
        '"rgba(239,68,68,0.85)"' if s >= 7 else
        '"rgba(245,158,11,0.85)"' if s >= 4 else
        '"rgba(34,197,94,0.85)"'
        for s in scores
    ]
    return f"""<canvas id="riskChart" class="max-h-56"></canvas>
    <script>new Chart(document.getElementById('riskChart'),{{
      type:'bar',
      data:{{labels:{str(labels).replace("'",'"')},datasets:[{{label:'Risk Score',data:{scores},backgroundColor:[{",".join(colors)}],borderRadius:5,borderSkipped:false}}]}},
      options:{{indexAxis:'y',responsive:true,scales:{{x:{{min:0,max:9,ticks:{{stepSize:1}}}},y:{{ticks:{{font:{{size:10}}}}}}}},plugins:{{legend:{{display:false}}}}}}
    }});</script>"""


# ── Section 4: Strategy — Initiatives + Options + Alignment ──────────────────

def _initiative_cards(details: list[dict]) -> str:
    if not details:
        return '<p class="text-slate-400 italic text-sm">No initiatives generated.</p>'
    cards = ""
    for d in details:
        priority = d.get("priority", "Medium")
        effort = d.get("effort", "Medium")
        pc = _PRIORITY_COLOR.get(priority, "slate")
        ec = _EFFORT_COLOR.get(effort, "slate")
        cards += f"""<div class="bg-white rounded-xl border border-slate-200 shadow-sm p-4">
          <div class="flex items-start justify-between gap-2 mb-3">
            <p class="font-semibold text-slate-800 text-sm leading-snug">{d.get("title","")}</p>
            <span class="px-2 py-0.5 rounded-full text-xs font-bold bg-{pc}-100 text-{pc}-800 border border-{pc}-200 flex-shrink-0">{priority}</span>
          </div>
          <div class="grid grid-cols-2 gap-y-1.5 gap-x-3 text-xs text-slate-600 mb-3">
            <span><i class="fa-solid fa-bolt text-{ec}-500 mr-1"></i>Effort: <strong>{effort}</strong></span>
            <span><i class="fa-solid fa-dollar-sign text-emerald-500 mr-1"></i>{d.get("cost_estimate","TBD")}</span>
            <span><i class="fa-solid fa-calendar text-blue-500 mr-1"></i>{d.get("timeframe","TBD")}</span>
            <span><i class="fa-solid fa-user text-violet-500 mr-1"></i>{d.get("owner","CISO")}</span>
          </div>
          <p class="text-xs text-slate-500 bg-slate-50 p-2 rounded border border-slate-100 leading-relaxed">{d.get("rationale","")}</p>
        </div>"""
    return f'<div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">{cards}</div>'


def _strategy_options(options: list[str]) -> str:
    if not options:
        return '<p class="text-slate-400 italic text-sm">No strategic options.</p>'
    direction_icons = {
        "risk": "fa-shield-halved",
        "resilien": "fa-rotate",
        "compliance": "fa-scale-balanced",
        "zero": "fa-lock",
        "third": "fa-handshake",
        "growth": "fa-chart-line",
    }
    cards = ""
    for i, opt in enumerate(options):
        key = next((k for k in direction_icons if k in opt.lower()), None)
        icon = direction_icons.get(key, "fa-compass")
        colors = ["bg-blue-600","bg-indigo-600","bg-violet-600","bg-teal-600","bg-cyan-600"]
        color = colors[i % len(colors)]
        label, desc = (opt.split(":", 1) if ":" in opt else (f"Option {i+1}", opt))
        cards += f"""<div class="bg-white rounded-xl border border-slate-200 shadow-sm p-4 flex gap-3">
          <div class="w-9 h-9 rounded-xl {color} flex items-center justify-center flex-shrink-0 mt-0.5">
            <i class="fa-solid {icon} text-white text-sm"></i>
          </div>
          <div>
            <p class="font-semibold text-slate-800 text-sm">{label.strip()}</p>
            <p class="text-xs text-slate-600 mt-1 leading-relaxed">{desc.strip()}</p>
          </div>
        </div>"""
    return f'<div class="grid grid-cols-1 md:grid-cols-2 gap-3">{cards}</div>'


def _alignment_table(alignments: list[dict]) -> str:
    if not alignments:
        return '<p class="text-slate-400 italic text-sm">No business alignments generated.</p>'
    rows = ""
    for a in alignments:
        dep = a.get("dependency") or ""
        dep_html = f'<span class="text-xs text-slate-400"><i class="fa-solid fa-link mr-1"></i>{dep}</span>' if dep and dep != "null" else ""
        rows += f"""<tr class="border-b border-slate-100 hover:bg-slate-50 align-top">
          <td class="py-3 px-3 text-sm font-medium text-slate-800">{a.get("initiative","")}</td>
          <td class="py-3 px-3 text-sm text-blue-700">{a.get("business_objective","")}</td>
          <td class="py-3 px-3 text-sm text-slate-600">{a.get("alignment_rationale","")}</td>
          <td class="py-3 px-3">{dep_html}</td>
        </tr>"""
    return f"""<div class="overflow-x-auto"><table class="w-full text-left text-sm">
      <thead><tr class="bg-slate-50 text-xs text-slate-500 uppercase tracking-wider">
        <th class="py-2 px-3">Initiative</th>
        <th class="py-2 px-3">Business Objective</th>
        <th class="py-2 px-3">Rationale</th>
        <th class="py-2 px-3">Dependency</th>
      </tr></thead><tbody>{rows}</tbody>
    </table></div>"""


# ── Section 5: Execution — Roadmap + KPIs + Controls ─────────────────────────

def _roadmap_timeline(roadmap: list[str]) -> str:
    if not roadmap:
        return '<p class="text-slate-400 italic text-sm">No roadmap defined.</p>'
    colors = ["bg-blue-500","bg-indigo-500","bg-violet-500","bg-purple-500","bg-cyan-500","bg-teal-500"]
    items = ""
    for i, item in enumerate(roadmap):
        color = colors[i % len(colors)]
        label, text = (item.split(":", 1) if ":" in item else (f"Step {i+1}", item))
        connector = "<div class='w-0.5 h-full bg-slate-200 mt-1'></div>" if i < len(roadmap)-1 else ""
        items += f"""<div class="flex gap-4 items-start">
          <div class="flex flex-col items-center flex-shrink-0">
            <div class="w-8 h-8 rounded-full {color} flex items-center justify-center text-white font-bold text-xs shadow">{i+1}</div>
            {connector}
          </div>
          <div class="pb-4">
            <p class="font-semibold text-slate-800 text-sm">{label.strip()}</p>
            <p class="text-slate-600 text-sm mt-0.5">{text.strip()}</p>
          </div>
        </div>"""
    return f'<div class="flex flex-col">{items}</div>'


def _control_mapping_table(mappings: list[dict]) -> str:
    if not mappings:
        return '<p class="text-slate-400 italic text-sm">No control mappings generated.</p>'

    def _tags(items: list, color: str) -> str:
        return " ".join(
            f'<span class="text-xs font-mono px-1.5 py-0.5 rounded bg-{color}-100 text-{color}-800 border border-{color}-200">{i}</span>'
            for i in items
        ) or '<span class="text-slate-300 text-xs">—</span>'

    rows = ""
    for m in mappings:
        rows += f"""<tr class="border-b border-slate-100 hover:bg-slate-50 align-top">
          <td class="py-3 px-3 text-sm font-medium text-slate-800">{m.get("initiative","")}</td>
          <td class="py-3 px-3">{_tags(m.get("iso27001",[]),"blue")}</td>
          <td class="py-3 px-3">{_tags(m.get("nist_csf",[]),"indigo")}</td>
          <td class="py-3 px-3">{_tags(m.get("cis_controls",[]),"cyan")}</td>
          <td class="py-3 px-3">{_tags(m.get("gdpr_articles",[]),"violet")}</td>
        </tr>"""
    return f"""<div class="overflow-x-auto"><table class="w-full text-left text-sm">
      <thead><tr class="bg-slate-50 text-xs text-slate-500 uppercase tracking-wider">
        <th class="py-2 px-3">Initiative</th>
        <th class="py-2 px-3 text-blue-700">ISO 27001</th>
        <th class="py-2 px-3 text-indigo-700">NIST CSF</th>
        <th class="py-2 px-3 text-cyan-700">CIS Controls</th>
        <th class="py-2 px-3 text-violet-700">GDPR</th>
      </tr></thead><tbody>{rows}</tbody>
    </table></div>"""


# ── Appendix helpers ──────────────────────────────────────────────────────────

def _evidence_table(traces: list[dict]) -> str:
    if not traces:
        return '<p class="text-slate-400 italic text-sm">No evidence traces available.</p>'
    cat_colors = {"audit":"blue","risk":"orange","incident":"red","iso":"indigo",
                  "nist":"violet","cis":"cyan","gdpr":"purple","business":"teal"}
    rows = ""
    for t in traces:
        fw = t.get("framework") or ""
        ctrl = t.get("control_id") or ""
        cat = t.get("category","")
        cc = cat_colors.get(cat, "slate")
        score = t.get("relevance_score", 0)
        fw_tag = f'<span class="text-xs px-1 rounded bg-slate-700 text-white font-mono">{fw}</span>' if fw else ""
        ctrl_tag = f'<span class="text-xs px-1 rounded bg-slate-100 text-slate-700 font-mono border">{ctrl}</span>' if ctrl else ""
        rows += f"""<tr class="border-b border-slate-100 hover:bg-slate-50">
          <td class="py-2 px-3 text-xs text-slate-700 max-w-xs truncate">{t.get("chunk_title","")}</td>
          <td class="py-2 px-3 text-xs text-slate-500">{t.get("source","")}</td>
          <td class="py-2 px-3"><span class="px-1.5 py-0.5 rounded text-xs bg-{cc}-100 text-{cc}-800">{cat}</span></td>
          <td class="py-2 px-3 flex gap-1 flex-wrap">{fw_tag}{ctrl_tag}</td>
          <td class="py-2 px-3">
            <div class="flex items-center gap-1.5">
              <div class="w-12 bg-slate-100 rounded-full h-1.5">
                <div class="h-1.5 rounded-full bg-blue-500" style="width:{int(score*100)}%"></div>
              </div>
              <span class="text-xs text-slate-400">{score:.2f}</span>
            </div>
          </td>
        </tr>"""
    return f"""<div class="overflow-x-auto"><table class="w-full text-left">
      <thead><tr class="bg-slate-50 text-xs text-slate-500 uppercase tracking-wider">
        <th class="py-2 px-3">Evidence Title</th>
        <th class="py-2 px-3">Source</th>
        <th class="py-2 px-3">Category</th>
        <th class="py-2 px-3">Framework / Control</th>
        <th class="py-2 px-3">Relevance</th>
      </tr></thead><tbody>{rows}</tbody>
    </table></div>"""


def _confidence_widget(conf: dict) -> str:
    level = conf.get("level","medium")
    score = conf.get("score", 50)
    evidence_count = conf.get("evidence_count", 0)
    conflicting = conf.get("conflicting_signals", False)
    rationale = conf.get("rationale","")
    color = {"high":"emerald","medium":"amber","low":"red"}.get(level,"slate")
    return f"""<div class="bg-white rounded-xl border border-slate-200 shadow-sm p-4">
      <div class="flex items-center justify-between mb-2">
        <div class="flex items-center gap-2">
          <i class="fa-solid fa-brain text-slate-500"></i>
          <span class="font-semibold text-slate-700 text-sm">AI Confidence</span>
        </div>
        <span class="px-2 py-0.5 rounded-full text-xs font-bold bg-{color}-100 text-{color}-800 border border-{color}-200">{level.title()} · {score}/100</span>
      </div>
      <div class="w-full bg-slate-100 rounded-full h-2 mb-3">
        <div class="h-2 rounded-full bg-{color}-500" style="width:{score}%"></div>
      </div>
      <div class="flex gap-3 text-xs text-slate-600">
        <span><i class="fa-solid fa-database mr-1 text-slate-400"></i>{evidence_count} evidence chunks</span>
        <span class="{'text-red-600' if conflicting else 'text-emerald-600'}">
          <i class="fa-solid {'fa-triangle-exclamation' if conflicting else 'fa-check'} mr-1"></i>{'Conflicts detected' if conflicting else 'No conflicts'}
        </span>
      </div>
      {"<p class='mt-2 text-xs text-slate-500'>" + rationale + "</p>" if rationale else ""}
    </div>"""


def _clarification_section(questions: list[str]) -> str:
    if not questions:
        return ""
    items = "".join(
        f'<div class="flex gap-3 items-start p-3 bg-amber-50 rounded-lg border border-amber-200">'
        f'<i class="fa-solid fa-circle-question text-amber-500 mt-0.5"></i>'
        f'<p class="text-sm text-amber-800">{q}</p></div>'
        for q in questions
    )
    return f"""<div class="bg-white rounded-xl shadow-sm border border-amber-300 overflow-hidden">
      <div class="px-5 py-4 border-b border-amber-200 bg-amber-50 flex items-center gap-2">
        <i class="fa-solid fa-triangle-exclamation text-amber-500"></i>
        <h3 class="font-semibold text-amber-800">Human Clarification Required Before Finalising</h3>
        <span class="ml-auto text-xs bg-amber-200 text-amber-800 px-2 py-0.5 rounded-full font-medium">{len(questions)} question{"s" if len(questions)>1 else ""}</span>
      </div>
      <div class="px-5 py-4 flex flex-col gap-2">{items}</div>
    </div>"""


def _review_section(review: dict) -> str:
    if not review.get("reviewer_name"):
        return ""
    status = review.get("status","")
    style, icon = _STATUS_STYLE.get(status, _STATUS_STYLE["draft"])
    return f"""<div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
      <div class="px-5 py-4 border-b border-slate-100 flex items-center gap-2">
        <div class="w-8 h-8 rounded-lg bg-slate-700 flex items-center justify-center">
          <i class="fa-solid fa-user-shield text-white text-sm"></i>
        </div>
        <h3 class="font-semibold text-slate-800">Human Review Decision</h3>
      </div>
      <div class="px-5 py-4 flex flex-col gap-3">
        <div class="flex items-center gap-3">
          <span class="text-sm text-slate-500">Reviewer:</span>
          <span class="text-sm font-semibold text-slate-800">{review.get("reviewer_name","")}</span>
          <span class="ml-auto"><span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full border text-sm font-semibold {style}"><i class="fa-solid {icon}"></i>{status.replace("_"," ").title()}</span></span>
        </div>
        {"<div class='p-3 bg-slate-50 rounded-lg text-sm text-slate-700 border'>" + review.get("comments","") + "</div>" if review.get("comments") else ""}
      </div>
    </div>"""


# ── Main ──────────────────────────────────────────────────────────────────────

def generate_html_report(result: dict) -> str:
    analysis_name       = result.get("analysis_name", "Cyber Strategy Report")
    status              = result.get("status", "draft")
    result_id           = result.get("result_id", "")
    created_at          = result.get("created_at", "")
    themes              = result.get("recurring_themes", [])
    strategy_options    = result.get("strategy_options", [])
    clarifications      = result.get("clarification_questions", [])
    board               = result.get("board_summary", {})
    review              = result.get("review", {})
    evidence_traces     = result.get("evidence_traces", [])
    risk_scores         = result.get("risk_scores", [])
    control_mappings    = result.get("control_mappings", [])
    business_alignments = result.get("business_alignments", [])
    initiative_details  = result.get("initiative_details", [])
    confidence          = result.get("confidence", {})
    strategy_inputs     = result.get("strategy_inputs", [])
    framework_refs      = result.get("framework_references", [])

    try:
        dt = datetime.fromisoformat(str(created_at)).strftime("%d %B %Y, %H:%M UTC")
    except Exception:
        dt = str(created_at)

    conf_level  = confidence.get("level", "medium")
    conf_score  = confidence.get("score", 50)
    conf_color  = {"high":"emerald","medium":"amber","low":"red"}.get(conf_level,"slate")
    exec_summary = board.get("executive_summary","") or "<em>No executive summary generated.</em>"

    kpi_html = "".join(
        f'<div class="flex gap-2 items-start p-3 rounded-lg bg-slate-50 border border-slate-200">'
        f'<i class="fa-solid fa-gauge-high text-indigo-500 mt-0.5 text-sm"></i>'
        f'<span class="text-sm text-slate-700">{k}</span></div>'
        for k in board.get("kpis_kris", [])
    ) or '<p class="text-slate-400 italic text-sm">No KPIs defined.</p>'

    tp_html = "".join(
        f'<div class="flex gap-3 items-start p-3 rounded-lg bg-blue-50 border border-blue-100">'
        f'<i class="fa-solid fa-microphone text-blue-400 mt-0.5 text-sm"></i>'
        f'<span class="text-sm text-slate-700">{t}</span></div>'
        for t in board.get("talking_points", [])
    ) or '<p class="text-slate-400 italic text-sm">No talking points.</p>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{analysis_name} — Cyber Strategy Report</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet"/>
  <style>
    body {{ font-family:'Inter',sans-serif; }}
    @media print {{ .no-print {{ display:none!important; }} body {{ background:white!important; }} }}
    .gradient-header {{ background:linear-gradient(135deg,#0f172a 0%,#1e3a5f 60%,#0f172a 100%); }}
    .step-divider {{ border-left:3px solid #e2e8f0; padding-left:1.25rem; margin-left:0.75rem; }}
  </style>
</head>
<body class="bg-slate-100 min-h-screen">

<!-- ═══════════════ COVER ═══════════════ -->
<div class="gradient-header text-white shadow-xl">
  <div class="max-w-7xl mx-auto px-6 py-10">
    <div class="flex items-start justify-between flex-wrap gap-4">
      <div>
        <div class="flex items-center gap-3 mb-3">
          <div class="w-12 h-12 bg-blue-500 rounded-2xl flex items-center justify-center shadow-lg">
            <i class="fa-solid fa-shield-halved text-white text-xl"></i>
          </div>
          <div>
            <p class="text-blue-300 text-xs font-semibold uppercase tracking-widest">AI Cyber Strategy Analyst Assistant</p>
            <h1 class="text-3xl font-bold text-white">{analysis_name}</h1>
          </div>
        </div>
        <div class="flex flex-wrap items-center gap-3 mt-2">
          {_status_badge(status)}
          <span class="text-slate-400 text-xs"><i class="fa-regular fa-clock mr-1"></i>{dt}</span>
          <span class="text-slate-500 text-xs font-mono">Ref: {result_id[:8]}…</span>
          <span class="px-2 py-0.5 rounded text-xs font-semibold bg-{conf_color}-900 text-{conf_color}-200 border border-{conf_color}-700">
            <i class="fa-solid fa-brain mr-1"></i>AI Confidence: {conf_score}/100
          </span>
        </div>
        <p class="mt-4 text-slate-300 text-sm max-w-2xl leading-relaxed">{exec_summary}</p>
      </div>
      <div class="flex flex-col items-end gap-3 no-print">
        <button onclick="window.print()" class="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white text-sm px-4 py-2 rounded-lg transition">
          <i class="fa-solid fa-print"></i> Export PDF
        </button>
        <div class="flex flex-wrap gap-1 justify-end mt-1">
          <a href="https://www.iso.org/isoiec-27001-information-security.html" target="_blank" class="text-xs px-2 py-0.5 rounded bg-blue-800 text-blue-200 hover:bg-blue-700 transition">ISO 27001</a>
          <a href="https://www.nist.gov/cyberframework" target="_blank" class="text-xs px-2 py-0.5 rounded bg-indigo-800 text-indigo-200 hover:bg-indigo-700 transition">NIST CSF</a>
          <a href="https://www.cisecurity.org/controls" target="_blank" class="text-xs px-2 py-0.5 rounded bg-cyan-800 text-cyan-200 hover:bg-cyan-700 transition">CIS v8.1</a>
          <a href="https://gdpr.eu/" target="_blank" class="text-xs px-2 py-0.5 rounded bg-violet-800 text-violet-200 hover:bg-violet-700 transition">GDPR</a>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- CLARIFICATION ALERT -->
<div class="max-w-7xl mx-auto px-6 pt-6">
  {_clarification_section(clarifications)}
</div>

<div class="max-w-7xl mx-auto px-6 py-6 flex flex-col gap-10">

  <!-- ═══════════════ STEP 1: INPUTS ═══════════════ -->
  <div>
    {_section_header("Strategy Inputs", "What data drove this analysis", 1)}
    <div class="step-divider">
      {_inputs_section(strategy_inputs)}
    </div>
  </div>

  <!-- ═══════════════ STEP 2: FRAMEWORKS ═══════════════ -->
  <div>
    {_section_header("Frameworks & Standards Applied", "Why each framework was selected and what it contributes", 2)}
    <div class="step-divider">
      {_frameworks_section(framework_refs)}
    </div>
  </div>

  <!-- ═══════════════ STEP 3: ANALYSIS ═══════════════ -->
  <div>
    {_section_header("Threat & Risk Analysis", "Recurring themes identified and their scored business risk", 3)}
    <div class="step-divider flex flex-col gap-5">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {_card("Recurring Cyber Themes", "fa-rotate", "bg-rose-500", _themes_list(themes), f"{len(themes)} themes")}
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div class="px-5 py-4 border-b border-slate-100 flex items-center gap-2">
            <div class="w-8 h-8 rounded-lg bg-red-600 flex items-center justify-center"><i class="fa-solid fa-chart-bar text-white text-sm"></i></div>
            <h3 class="font-semibold text-slate-800">Risk Heat Map</h3>
            <span class="ml-auto flex gap-1 text-xs">
              <span class="bg-red-100 text-red-700 px-1.5 rounded border border-red-200">High ≥7</span>
              <span class="bg-amber-100 text-amber-700 px-1.5 rounded border border-amber-200">Med ≥4</span>
              <span class="bg-green-100 text-green-700 px-1.5 rounded border border-green-200">Low &lt;4</span>
            </span>
          </div>
          <div class="px-5 py-4">{_risk_chart_js(risk_scores)}</div>
        </div>
      </div>
      {_card("Risk Score Details", "fa-triangle-exclamation", "bg-orange-600", _risk_score_cards(risk_scores), f"{len(risk_scores)} risks")}
    </div>
  </div>

  <!-- ═══════════════ STEP 4: STRATEGY ═══════════════ -->
  <div>
    {_section_header("Cybersecurity Strategy", "Strategic options, prioritised initiatives, and business alignment", 4)}
    <div class="step-divider flex flex-col gap-5">
      {_card("Strategic Directions", "fa-compass", "bg-blue-700", _strategy_options(strategy_options))}
      <div>
        <div class="flex items-center gap-2 mb-3">
          <div class="w-8 h-8 rounded-lg bg-emerald-600 flex items-center justify-center"><i class="fa-solid fa-list-check text-white text-sm"></i></div>
          <h3 class="font-semibold text-slate-800">Prioritised Initiatives</h3>
          <span class="ml-auto flex gap-1 text-xs">
            <span class="bg-red-100 text-red-700 px-1.5 rounded border border-red-200">High</span>
            <span class="bg-amber-100 text-amber-700 px-1.5 rounded border border-amber-200">Medium</span>
            <span class="bg-green-100 text-green-700 px-1.5 rounded border border-green-200">Low</span>
          </span>
        </div>
        {_initiative_cards(initiative_details)}
      </div>
      {_card("Business Alignment", "fa-building", "bg-teal-600", _alignment_table(business_alignments))}
    </div>
  </div>

  <!-- ═══════════════ STEP 5: EXECUTION ═══════════════ -->
  <div>
    {_section_header("Execution Plan", "Roadmap, control mappings, KPIs & KRIs, board talking points", 5)}
    <div class="step-divider flex flex-col gap-5">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {_card("Strategic Roadmap", "fa-timeline", "bg-cyan-600", _roadmap_timeline(board.get("roadmap",[])))}
        <div class="flex flex-col gap-4">
          {_card("KPIs & KRIs", "fa-gauge-high", "bg-indigo-600", f'<div class="flex flex-col gap-2">{kpi_html}</div>')}
          {_card("Board Talking Points", "fa-comments", "bg-sky-600", f'<div class="flex flex-col gap-2">{tp_html}</div>')}
        </div>
      </div>
      {_card("Control Mapping — Initiatives to Frameworks", "fa-sitemap", "bg-indigo-700", _control_mapping_table(control_mappings))}
    </div>
  </div>

  <!-- ═══════════════ APPENDIX: EVIDENCE + CONFIDENCE + REVIEW ═══════════════ -->
  <div>
    {_section_header("Appendix", "Evidence traceability, AI confidence, human review")}
    <div class="step-divider flex flex-col gap-5">
      {_confidence_widget(confidence)}
      {_card("Evidence Traceability", "fa-magnifying-glass", "bg-slate-600", _evidence_table(evidence_traces), f"{len(evidence_traces)} chunks")}
      {_review_section(review)}
    </div>
  </div>

  <!-- FOOTER -->
  <div class="text-center text-xs text-slate-400 py-4 border-t border-slate-200">
    <p>Generated by <strong class="text-slate-600">AI Cyber Strategy Analyst Assistant</strong> &middot; {dt}</p>
    <p class="mt-1 text-slate-500">AI-generated output. Requires human review before use in decision-making.</p>
    <p class="mt-2 flex justify-center gap-4 flex-wrap">
      <a href="https://www.iso.org/isoiec-27001-information-security.html" target="_blank" class="text-blue-500 hover:underline">ISO/IEC 27001:2022</a>
      <a href="https://www.nist.gov/cyberframework" target="_blank" class="text-blue-500 hover:underline">NIST CSF 2.0</a>
      <a href="https://www.cisecurity.org/controls" target="_blank" class="text-blue-500 hover:underline">CIS Controls v8.1</a>
      <a href="https://gdpr.eu/" target="_blank" class="text-blue-500 hover:underline">GDPR</a>
      <a href="https://www.enisa.europa.eu/" target="_blank" class="text-blue-500 hover:underline">ENISA</a>
    </p>
  </div>

</div>
</body>
</html>"""
