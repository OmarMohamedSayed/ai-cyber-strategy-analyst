# AI Cyber Strategy Analyst Assistant

> RAG-powered AI assistant that helps CISO teams analyze cybersecurity inputs and generate **board-ready strategy insights** with human-in-the-loop validation.

Built with **FastAPI** | **OpenAI GPT-4o** | **Qdrant** | **LangChain**

**Swagger UI:** `http://localhost:8000/docs` &nbsp; | &nbsp; **ReDoc:** `http://localhost:8000/redoc`

---

## What This System Produces

The AI analyzes your cybersecurity documents (audit findings, risk registers, framework standards, incident reports) and generates three types of board-ready output:

### 1. Interactive HTML Report

A consulting-style interactive report accessible at `GET /strategy/results/{id}/report`

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  ┌──────────┐                                                                   │
│  │ 🛡️ LOGO  │  AI Cyber Strategy Analyst Assistant                              │
│  └──────────┘  2026 Cloud Migration Cyber Strategy                              │
│                                                                                 │
│  ┌──────────────┐  ┌───────────┐  ┌─────────────────────────────┐               │
│  │ ✅ Approved   │  │ 📅 Apr 26 │  │ 🧠 AI Confidence: 82/100   │               │
│  └──────────────┘  └───────────┘  └─────────────────────────────┘               │
│                                                                                 │
│  The organization faces significant cybersecurity challenges during its          │
│  cloud migration phase. Key risks center on IAM gaps, third-party exposure,      │
│  and insufficient resilience controls...                                         │
│                                                                                 │
│  ┌─────────────┐  ┌─────────────────┐  ┌──────────────────────────────┐         │
│  │ Export PDF 📄 │  │ ISO 27001       │  │ NIST CSF  │ CIS v8.1 │ GDPR │         │
│  └─────────────┘  └─────────────────┘  └──────────────────────────────┘         │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─ STEP 1: Strategy Inputs ──────────────────────────────────────────────────────┐
│                                                                                 │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌──────────────────────┐    │
│  │ 🏢 Business Context  │  │ 🔍 Assessment Results│  │ ⚖️ Compliance        │    │
│  │                      │  │                      │  │                      │    │
│  │ 1 items              │  │ 4 items              │  │ 3 items              │    │
│  │ Cloud migration...   │  │ Audit findings,      │  │ ISO 27001, NIST CSF, │    │
│  │                      │  │ Risk register        │  │ CIS Controls         │    │
│  └─────────────────────┘  └─────────────────────┘  └──────────────────────┘    │
└────────────────────────────────────────────────────────────────────────────────┘

┌─ STEP 2: Frameworks & Standards Applied ───────────────────────────────────────┐
│                                                                                 │
│  ┌──────────────────────────────────┐  ┌──────────────────────────────────┐     │
│  │ ISO 27001        v2022  🔗 Ref   │  │ NIST CSF          v2.0  🔗 Ref   │     │
│  │                                   │  │                                   │     │
│  │ Provides ISMS requirements and    │  │ Structures strategy around six    │     │
│  │ Annex A controls that anchor      │  │ functions — Govern, Identify,     │     │
│  │ the governance structure.         │  │ Protect, Detect, Respond, Recover │     │
│  │                                   │  │                                   │     │
│  │ A.5.1  A.8.5  A.8.9  A.5.23     │  │ PR.AA-01  DE.CM-01  RS.RP-01     │     │
│  └──────────────────────────────────┘  └──────────────────────────────────┘     │
│  ┌──────────────────────────────────┐  ┌──────────────────────────────────┐     │
│  │ CIS Controls     v8.1  🔗 Ref   │  │ GDPR              2018  🔗 Ref   │     │
│  │                                   │  │                                   │     │
│  │ Implementation-level safeguards   │  │ Data protection obligations for   │     │
│  │ mapped to implementation groups   │  │ personal data in cloud migration  │     │
│  │ (IG1-IG3).                        │  │ and third-party engagements.      │     │
│  │                                   │  │                                   │     │
│  │ CIS-3  CIS-4  CIS-6  CIS-14     │  │ Art. 25  Art. 28  Art. 32        │     │
│  └──────────────────────────────────┘  └──────────────────────────────────┘     │
└────────────────────────────────────────────────────────────────────────────────┘

┌─ STEP 3: Threat & Risk Analysis ───────────────────────────────────────────────┐
│                                                                                 │
│  ┌─ Recurring Cyber Themes ────────┐  ┌─ Risk Heat Map ───────────────────┐    │
│  │                                  │  │                                    │    │
│  │  ● IAM Gaps: Weak MFA coverage   │  │  Insufficient IAM   ██████████ 9  │    │
│  │    across cloud workloads...     │  │  Third-party risk   ████████░░ 7  │    │
│  │                                  │  │  Cloud misconfig    ███████░░░ 6  │    │
│  │  ● Third-Party Exposure: Key     │  │  Data protection   ██████░░░░ 5  │    │
│  │    vendors lack compliance...    │  │  Incident response  █████░░░░░ 4  │    │
│  │                                  │  │                                    │    │
│  │  ● Cloud Security: Config        │  │  ■ High ≥7  ■ Med ≥4  ■ Low <4  │    │
│  │    drift in IaaS environments    │  │                                    │    │
│  │                                  │  │                                    │    │
│  │  ● Resilience Gaps: No tested    │  │                                    │    │
│  │    DR for critical workloads     │  │                                    │    │
│  └──────────────────────────────────┘  └────────────────────────────────────┘    │
│                                                                                 │
│  ┌─ Risk Score Details ──── 5 risks ───────────────────────────────────────┐    │
│  │                                                                          │    │
│  │  ┌───────────────────────────────────────────────────────────────── 9 ┐  │    │
│  │  │ Insufficient IAM controls during cloud migration                   │  │    │
│  │  │ Likelihood: High  │  Impact: High                                  │  │    │
│  │  │ Multiple audit findings confirm MFA gaps across 60% of workloads   │  │    │
│  │  └────────────────────────────────────────────────────────────────────┘  │    │
│  │                                                                          │    │
│  │  ┌───────────────────────────────────────────────────────────────── 7 ┐  │    │
│  │  │ Third-party vendor data handling non-compliance                    │  │    │
│  │  │ Likelihood: Medium │  Impact: High                                 │  │    │
│  │  │ 3 critical vendors failed latest security assessment               │  │    │
│  │  └────────────────────────────────────────────────────────────────────┘  │    │
│  └──────────────────────────────────────────────────────────────────────────┘    │
└────────────────────────────────────────────────────────────────────────────────┘

┌─ STEP 4: Cybersecurity Strategy ───────────────────────────────────────────────┐
│                                                                                 │
│  ┌─ Strategic Directions ──────────────────────────────────────────────────┐    │
│  │                                                                          │    │
│  │  🛡️ Risk-Reduction First                  🔄 Resilience-Led              │    │
│  │  Prioritize IAM hardening and             Build DR capabilities and      │    │
│  │  cloud security controls to               cyber resilience before        │    │
│  │  reduce top-scored risks.                 expanding digital services.    │    │
│  │                                                                          │    │
│  │  📈 Digital-Growth Enabling               🔒 Zero-Trust Architecture     │    │
│  │  Balance security investment with         Implement zero-trust across    │    │
│  │  business growth objectives.              all cloud workloads.           │    │
│  └──────────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
│  ┌─ Prioritised Initiatives ───────────────────────────────────────────────┐    │
│  │                                                                          │    │
│  │  ┌──────────────────────────┐  ┌──────────────────────────┐             │    │
│  │  │ MFA Rollout       [HIGH] │  │ Vendor Governance  [HIGH] │             │    │
│  │  │                          │  │                           │             │    │
│  │  │ ⚡ Effort: Medium        │  │ ⚡ Effort: High           │             │    │
│  │  │ 💰 $150K-250K           │  │ 💰 $200K-350K            │             │    │
│  │  │ 📅 Q1 2026 / 6 months   │  │ 📅 Q2 2026 / 9 months    │             │    │
│  │  │ 👤 CISO                  │  │ 👤 CISO + Procurement    │             │    │
│  │  └──────────────────────────┘  └──────────────────────────┘             │    │
│  │  ┌──────────────────────────┐  ┌──────────────────────────┐             │    │
│  │  │ Cloud CSPM        [MED]  │  │ DR Testing         [MED] │             │    │
│  │  │                          │  │                           │             │    │
│  │  │ ⚡ Effort: Medium        │  │ ⚡ Effort: Low            │             │    │
│  │  │ 💰 $100K-180K           │  │ 💰 $50K-100K             │             │    │
│  │  │ 📅 Q2 2026 / 6 months   │  │ 📅 Q3 2026 / 3 months    │             │    │
│  │  │ 👤 Cloud Security Lead   │  │ 👤 IT Operations         │             │    │
│  │  └──────────────────────────┘  └──────────────────────────┘             │    │
│  └──────────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
│  ┌─ Business Alignment ───────────────────────────────────────────────────┐     │
│  │  Initiative          │ Business Objective        │ Rationale            │     │
│  │  ───────────────────────────────────────────────────────────────────── │     │
│  │  MFA Rollout         │ Secure digital transform  │ Directly addresses   │     │
│  │                      │                           │ credential theft...  │     │
│  │  Vendor Governance   │ Supply chain resilience   │ Reduces third-party  │     │
│  │                      │                           │ exposure by 60%...   │     │
│  └──────────────────────────────────────────────────────────────────────────┘    │
└────────────────────────────────────────────────────────────────────────────────┘

┌─ STEP 5: Execution Plan ──────────────────────────────────────────────────────┐
│                                                                                 │
│  ┌─ Strategic Roadmap ─────────────┐  ┌─ KPIs & KRIs ─────────────────────┐   │
│  │                                  │  │                                    │   │
│  │  ① Q1 2026: Foundation          │  │  📊 MFA coverage > 95%             │   │
│  │  │  IAM hardening + MFA deploy   │  │  📊 Mean patch time < 72h         │   │
│  │  │                               │  │  📊 Vendor compliance rate > 90%   │   │
│  │  ② Q2 2026: Expansion           │  │  ⚠️  Unpatched critical vulns < 5  │   │
│  │  │  Cloud CSPM + vendor program  │  │  ⚠️  Open high-risk findings < 10 │   │
│  │  │                               │  │                                    │   │
│  │  ③ Q3 2026: Maturity            │  ├─ Board Talking Points ────────────┤   │
│  │     DR testing + optimization    │  │                                    │   │
│  │                                  │  │  🎤 Our top risk is insufficient   │   │
│  └──────────────────────────────────┘  │    IAM controls during migration   │   │
│                                        │  🎤 We recommend a phased approach │   │
│                                        │    starting with MFA in Q1...      │   │
│                                        └────────────────────────────────────┘   │
│                                                                                 │
│  ┌─ Control Mapping — Initiatives to Frameworks ──────────────────────────┐    │
│  │  Initiative      │ ISO 27001  │ NIST CSF    │ CIS Controls │ GDPR      │    │
│  │  ────────────────────────────────────────────────────────────────────── │    │
│  │  MFA Rollout     │ A.8.5      │ PR.AA-01    │ CIS-6        │ Art. 32   │    │
│  │  Vendor Gov.     │ A.5.19     │ GV.SC-04    │ CIS-15       │ Art. 28   │    │
│  │  Cloud CSPM      │ A.8.9      │ PR.DS-01    │ CIS-3        │ Art. 25   │    │
│  │  DR Testing      │ A.5.30     │ RC.RP-01    │ CIS-11       │ —         │    │
│  └──────────────────────────────────────────────────────────────────────────┘    │
└────────────────────────────────────────────────────────────────────────────────┘

┌─ Appendix: Evidence Traceability + AI Confidence + Human Review ───────────────┐
│                                                                                 │
│  ┌─ 🧠 AI Confidence ─────────────────────────────────────────────────────┐    │
│  │  High · 82/100     ████████████████████░░░░░                            │    │
│  │  📊 8 evidence chunks  │  ✅ No conflicts detected                      │    │
│  │  Strong evidence from multiple framework sources and operational data   │    │
│  └──────────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
│  ┌─ Evidence Traceability ─── 8 chunks ───────────────────────────────────┐    │
│  │  Evidence Title              │ Source           │ Category │ Relevance │    │
│  │  ──────────────────────────────────────────────────────────────────── │    │
│  │  A.8 Technological controls  │ ISO/IEC 27001    │ iso      │ ██░ 0.87 │    │
│  │  3.1. The CSF Core           │ NIST CSF 2.0     │ nist     │ ██░ 0.84 │    │
│  │  Control 6: Access Control   │ CIS Controls     │ cis      │ █░░ 0.79 │    │
│  │  IAM Policy Gap — MFA        │ Internal Audit   │ audit    │ █░░ 0.76 │    │
│  │  Vendor SLA Non-Compliance   │ Third-Party Risk │ risk     │ █░░ 0.73 │    │
│  └──────────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
│  ┌─ 🧑‍💼 Human Review Decision ──────────────────────────────────────────┐    │
│  │  Reviewer: Omar                                    ✅ Approved          │    │
│  │  "Increase resilience priority in Q2."                                  │    │
│  └──────────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
│  ── Generated by AI Cyber Strategy Analyst Assistant · 26 April 2026 ──        │
│  AI-generated output. Requires human review before use in decision-making.      │
│  ISO/IEC 27001:2022 · NIST CSF 2.0 · CIS Controls v8.1 · GDPR · ENISA         │
└────────────────────────────────────────────────────────────────────────────────┘
```

---

### 2. PowerPoint Slides

Branded initiative slides downloaded at `GET /strategy/results/{id}/powerpoint/initiative-slide`

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  Classification: Confidential                                                   │
│                                                                                 │
│  Enabling Organizational Resilience Through Integrated Strategic Pillars         │
│                                                                                 │
│  ┌──────────┐   ┌──────────────────┐   ┌────────────────────┐   ┌──────────┐  │
│  │          │   │ Technology       │   │ Cybersecurity      │   │ Cyber    │  │
│  │ Cyber-   │   │ Pillars        ──>──│ Pillars          ──>──│ Init-    │  │
│  │ security │   │                  │   │                    │   │ iatives  │  │
│  │ Strategy │   │ Build a Strong   │   │ Agile Governance   │   │          │  │
│  │          │   │ Core Platforms   │   │ and Strategy       │   │ A1. MFA  │  │
│  │  ┌────┐  │   │                  │   │                    │   │ A2. IAM  │  │
│  │  │ ⬤  │  │   │ Enable Business  │   │ Modernize Security │   │          │  │
│  │  │    │  │   │ Products         │   │ Operations         │   │ M1. CSPM │  │
│  │  └────┘  │   │                  │   │                    │   │ M2. SIEM │  │
│  │          │   │ Become a Global  │   │ Elevate Resilience │   │ M3. SOC  │  │
│  │          │   │ Benchmark        │   │ and Risk Mgmt      │   │          │  │
│  │          │   │                  │   │                    │   │ E1. DR   │  │
│  │          │   │                  │   │ Nurture People     │   │ E2. BCP  │  │
│  │          │   │                  │   │ and Partnerships   │   │          │  │
│  └──────────┘   └──────────────────┘   └────────────────────┘   └──────────┘  │
│                                                                                 │
│                              Copyright © 2026 Accenture. All rights reserved.   │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│ ┌─────────────────────┐  ┌───────────────────────────┐  ┌────────────────────┐ │
│ │ Security Domain     │  │ Initiative Overview       │  │ Initiative         │ │
│ │ ████████████████████│  │                           │  │ Timeline           │ │
│ │ Identity & Access   │  │ Deploy enterprise-wide    │  │                    │ │
│ │ Management          │  │ MFA with adaptive auth    │  │    Y1    Y2    Y3  │ │
│ │                     │  │ policies, targeting 95%   │  │ Q1Q2Q3Q4Q1Q2Q3Q4  │ │
│ │ Initiative Name     │  │ coverage within 6 months. │  │ ████████░░░░░░░░  │ │
│ │ █████████████████████│  │ Integrates with existing  │  │ ░░░░████████░░░░  │ │
│ │ MFA Rollout for     │  │ IAM infrastructure...     │  │ ░░░░░░░░████████  │ │
│ │ Cloud Workloads     │  │                           │  │                    │ │
│ │                     │  ├───────────────────────────┤  ├────────────────────┤ │
│ │ Start     Duration  │  │ Initiative Owner          │  │ AI use case        │ │
│ │ Q1 2026   6 months  │  │ CISO                      │  │ Use AI to track    │ │
│ │ Budget    FTEs      │  │ Supporting: IT, Risk, HR  │  │ MFA deployment     │ │
│ │ $150-250K 3.5       │  │                           │  │ progress and flag  │ │
│ │                     │  ├───────────────────────────┤  │ coverage gaps...   │ │
│ │ Strategic Objectives│  │ Initiative Projects       │  ├────────────────────┤ │
│ │ ┌─ Secure digital ┐│  │                           │  │ Priority           │ │
│ │ ┌─ Reduce breach  ┐│  │ 1. Phase 1 — Cloud IAM    │  │ [HIGH] Med   Low   │ │
│ │ ┌─ Compliance     ┐│  │    Deploy MFA for all     │  ├────────────────────┤ │
│ │ ┌─ Operational    ┐│  │    cloud admin accounts    │  │ Dependencies       │ │
│ │                     │  │                           │  │ • Cloud migration  │ │
│ │ Maturity Uplift     │  │ 2. Phase 2 — Enterprise   │  │   Phase 1 complete │ │
│ │ x1.2  x1.5  x1.8   │  │    Extend to all users    │  ├────────────────────┤ │
│ │ ──────────────→     │  │    with adaptive policies  │  │ Challenges         │ │
│ │ Y1    Y2    Y3      │  │                           │  │ 1 IAM Gaps         │ │
│ │                     │  │                           │  │ 2 Cloud Security   │ │
│ │ Domains Impacted    │  │                           │  │                    │ │
│ │ 1 Cloud Security    │  │                           │  │                    │ │
│ │ 2 Identity & Access │  │                           │  │                    │ │
│ └─────────────────────┘  └───────────────────────────┘  └────────────────────┘ │
│                              Copyright © 2026 Accenture. All rights reserved.   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

### 3. JSON API Response

Structured analysis results at `GET /strategy/results/{id}`

<details>
<summary>Click to expand full JSON output schema</summary>

```json
{
  "result_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "analysis_name": "2026_cloud_migration_strategy",
  "status": "approved",
  "created_at": "2026-04-26T14:30:00",

  "recurring_themes": [
    "IAM Gaps: Weak MFA coverage across cloud workloads with 60% of admin accounts unprotected",
    "Third-Party Exposure: Key vendors lack SOC 2 compliance and data handling controls",
    "Cloud Security: Configuration drift in IaaS environments with no CSPM baseline",
    "Resilience Gaps: No tested disaster recovery for 4 business-critical cloud workloads"
  ],

  "business_risk_mapping": [
    "[9/9 | High×High] Insufficient IAM controls expose cloud migration to credential-based attacks",
    "[7/9 | Medium×High] Third-party vendor data handling non-compliance threatens regulatory standing",
    "[6/9 | Medium×Medium] Cloud misconfiguration creates data exposure and compliance gaps",
    "[5/9 | Medium×Medium] Inadequate data protection controls risk GDPR penalties",
    "[4/9 | Low×High] Untested DR plans create single points of failure for critical workloads"
  ],

  "prioritized_initiatives": [
    "[High] MFA Rollout | Effort: Medium | Cost: $150K-250K | Q1 2026 / 6 months | Owner: CISO",
    "[High] Vendor Governance Program | Effort: High | Cost: $200K-350K | Q2 2026 / 9 months | Owner: CISO",
    "[Medium] Cloud CSPM Deployment | Effort: Medium | Cost: $100K-180K | Q2 2026 / 6 months | Owner: Cloud Lead",
    "[Medium] DR Testing Program | Effort: Low | Cost: $50K-100K | Q3 2026 / 3 months | Owner: IT Ops"
  ],

  "strategy_options": [
    "Risk-Reduction First: Prioritize IAM hardening and cloud security controls to reduce top-scored risks",
    "Resilience-Led: Build DR capabilities before expanding digital services",
    "Digital-Growth Enabling: Balance security investment with business growth objectives",
    "Zero-Trust Architecture: Implement zero-trust across all cloud workloads"
  ],

  "evidence_traces": [
    {
      "chunk_title": "A.8 Technological controls",
      "source": "ISO/IEC 27001:2022",
      "category": "iso",
      "framework": "iso27001",
      "control_id": "A.8",
      "relevance_score": 0.8742
    }
  ],

  "risk_scores": [
    {
      "risk_statement": "Insufficient IAM controls during cloud migration",
      "likelihood": "High",
      "impact": "High",
      "risk_score": 9,
      "rationale": "Multiple audit findings confirm MFA gaps across 60% of workloads"
    }
  ],

  "control_mappings": [
    {
      "initiative": "MFA Rollout",
      "iso27001": ["A.8.5"],
      "nist_csf": ["PR.AA-01"],
      "cis_controls": ["CIS-6"],
      "gdpr_articles": ["Art. 32"]
    }
  ],

  "business_alignments": [
    {
      "initiative": "MFA Rollout",
      "business_objective": "Secure digital transformation",
      "alignment_rationale": "Directly addresses credential theft risk during cloud migration",
      "dependency": "Cloud migration Phase 1 completion"
    }
  ],

  "initiative_details": [
    {
      "title": "MFA Rollout",
      "priority": "High",
      "effort": "Medium",
      "cost_estimate": "$150K-250K",
      "timeframe": "Q1 2026 / 6 months",
      "owner": "CISO",
      "rationale": "Addresses credential theft risk — top-scored risk at 9/9"
    }
  ],

  "confidence": {
    "level": "high",
    "score": 82,
    "evidence_count": 8,
    "conflicting_signals": false,
    "rationale": "Strong evidence from 4 framework sources and 3 operational datasets"
  },

  "strategy_inputs": [
    {
      "category": "Business Context",
      "sources": ["Analyst-provided context"],
      "item_count": 1,
      "key_findings": ["Enterprise undergoing cloud migration with 3rd-party dependencies"]
    },
    {
      "category": "Assessment Results",
      "sources": ["Internal Audit Findings 2025", "Enterprise Risk Register 2025"],
      "item_count": 4,
      "key_findings": ["IAM Policy Gap — MFA", "Cloud Config Drift", "Vendor SLA Breach"]
    }
  ],

  "framework_references": [
    {
      "name": "ISO/IEC 27001",
      "version": "2022",
      "url": "https://www.iso.org/isoiec-27001-information-security.html",
      "purpose": "Provides ISMS requirements and Annex A controls",
      "applicable_controls": ["A.5.1", "A.8.5", "A.8.9", "A.5.23"]
    }
  ],

  "board_summary": {
    "executive_summary": "The organization faces significant cybersecurity challenges...",
    "roadmap": [
      "Q1 2026: Foundation — IAM hardening + MFA deployment",
      "Q2 2026: Expansion — Cloud CSPM + vendor governance program",
      "Q3 2026: Maturity — DR testing + continuous optimization"
    ],
    "kpis_kris": [
      "KPI: MFA coverage > 95% within 6 months",
      "KPI: Mean patch time < 72 hours",
      "KRI: Unpatched critical vulnerabilities < 5",
      "KRI: Open high-risk audit findings < 10"
    ],
    "talking_points": [
      "Our top risk is insufficient IAM controls — 60% of cloud admin accounts lack MFA",
      "We recommend a phased approach starting with MFA in Q1, expanding to vendor governance in Q2"
    ]
  },

  "clarification_questions": [],

  "review": {
    "reviewer_name": "Omar",
    "status": "approved",
    "comments": "Increase resilience priority in Q2."
  }
}
```

</details>

---

## How It Works

```
Documents (PDF/DOCX/TXT/JSON)
        │
        ▼
  Text Extraction (pypdf, docx2txt)
        │
        ▼
  Structure-Aware Chunking (LangChain)
  ┌─────────────────────────────────────────────┐
  │ ISO 27001  → 800/100  (clause-level chunks) │
  │ NIST CSF   → 1200/150 (section-level)       │
  │ CIS v8.1   → 1200/200 (control blocks)      │
  │ GDPR       → 1000/150 (topic headings)      │
  └─────────────────────────────────────────────┘
        │
        ▼
  Embeddings (OpenAI text-embedding-3-small)
        │
        ▼
  Qdrant Vector DB (Cosine Similarity)
        │
        ▼
  Semantic Retrieval (top-K relevant chunks)
        │
        ▼
  5-Step LLM Pipeline
  ┌─────────────────────────────────────────────┐
  │ 1. Summarize → Recurring cyber themes       │
  │ 2. Risk Map  → Scored business risks        │
  │ 3. Initiatives → Prioritized actions        │
  │ 4. Board Output → Executive summary + KPIs  │
  │ 5. Clarification → Questions for humans     │
  └─────────────────────────────────────────────┘
        │
        ▼
  Human-in-the-Loop Review
  draft → needs_review → approved / rejected
```

---

## Quick Start

```bash
# 1. Setup
cd cyber-strategy-ai
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # Set your OPENAI_API_KEY

# 2. Start Qdrant
docker run -d --name qdrant -p 6333:6333 qdrant/qdrant

# 3. Start API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 4. Ingest data
cd .. && chmod +x ingest_all.sh && ./ingest_all.sh

# 5. Open Swagger → http://localhost:8000/docs
```

---

## Documentation

This project contains **3 README files** — each covers a different scope:

| README | What It Covers |
|--------|---------------|
| **[`README.md`](README.md)** (this file) | Project overview, output previews, quick start, and architecture |
| **[`cyber-strategy-ai/README.md`](cyber-strategy-ai/README.md)** | Full setup guide, all environment variables, complete API reference with curl examples, output JSON schema, HITL lifecycle, and project structure |
| **[`data/README.md`](data/README.md)** | Detailed description of every document and dataset in the `data/` folder — what each file is, why it's used, and how it flows through the RAG pipeline |

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| API Framework | FastAPI |
| LLM | OpenAI GPT-4o / GPT-4o-mini |
| Embeddings | OpenAI text-embedding-3-small |
| Vector Database | Qdrant |
| Prompt Orchestration | LangChain |
| PDF/DOCX Extraction | pypdf, docx2txt |
| PowerPoint | python-pptx |
| Configuration | pydantic-settings + dotenv |

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/documents/upload` | Upload and ingest PDF/DOCX/TXT |
| `POST` | `/documents/ingest-json` | Ingest structured JSON datasets |
| `GET` | `/documents/items` | List all ingested documents |
| `POST` | `/strategy/run` | Run AI strategy analysis pipeline |
| `GET` | `/strategy/results` | List all strategy results |
| `GET` | `/strategy/results/{id}` | Get specific result (JSON) |
| `GET` | `/strategy/results/{id}/report` | Board-ready HTML report |
| `GET` | `/strategy/results/{id}/powerpoint/initiative-slide` | Download PPTX slides |
| `POST` | `/strategy/clarify` | Submit clarification answers |
| `POST` | `/strategy/results/{id}/review` | Submit human review decision |

Full API docs with request/response schemas: **[http://localhost:8000/docs](http://localhost:8000/docs)**

---

## Data Sources

The [`data/`](data/) directory contains source documents used for RAG retrieval.

> **See [`data/README.md`](data/README.md)** for a full breakdown of every file — what each document is, why it's included, and how it feeds the analysis pipeline.

| Document | Purpose |
|----------|---------|
| ISO/IEC 27001:2022 | ISMS controls and governance requirements |
| NIST CSF 2.0 | Six-function cybersecurity framework |
| CIS Controls v8.1 | Implementation-level technical safeguards |
| GDPR Briefing | EU data protection obligations |
| Audit findings, risk register, incident reports, business plan | Organizational security posture data |

---

## Repository Structure

```
AI_Cyber_Strategy_Analyst_Assistant/
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions CI
├── docs/
│   ├── architecture.md            # Architecture overview
│   └── demo.md                    # End-to-end demo guide
├── data/                          # Source documents + README describing each
├── cyber-strategy-ai/             # FastAPI application
│   ├── app/
│   │   ├── main.py                # FastAPI entry point
│   │   ├── core/                  # Config + Qdrant client
│   │   ├── routers/               # API endpoints
│   │   ├── services/              # Business logic + LLM pipeline
│   │   ├── prompts/               # LangChain prompt templates
│   │   ├── models/                # Pydantic schemas + domain models
│   │   ├── repositories/          # JSON persistence
│   │   └── utils/                 # Document loading + chunking
│   ├── .env.example               # Environment template (24 variables)
│   └── requirements.txt           # Python dependencies
├── Dockerfile                     # Container build for API
├── docker-compose.yml             # Local API + Qdrant orchestration
├── LICENSE                        # MIT license
├── CONTRIBUTING.md                # Contribution guide
├── SECURITY.md                    # Security policy and reporting
├── CHANGELOG.md                   # Project change history
├── ingest_all.sh                  # Batch ingestion script
└── .gitignore                     # Git ignore rules
```
