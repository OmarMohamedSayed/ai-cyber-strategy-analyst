"""
Normalizes heterogeneous JSON datasets into the standard chunk format.

Supported schemas (auto-detected from field names):

  audit_finding     → fields: id, framework_name, control_id, title, description, domain, source, metadata
  risk_register     → fields: risk_id, title, description, likelihood, impact, risk_score, mitigation, category
  cloud_migration   → fields: id, workload, description, cloud_model, business_priority, risk, impact, current_gap, recommended_control, owner
  third_party_risk  → fields: vendor_id, vendor_name, service, access_level, data_access, risk_level, risk_score, compliance_status, identified_issues, impact, mitigation
  incident_report   → fields: id/incident_id, title, description, severity, date, affected_systems, root_cause, remediation
  business_plan     → fields: id, title, description, objective, timeline, owner (generic fallback)
"""

from typing import Optional


class NormalizedItem:
    __slots__ = ("title", "description", "section", "framework", "control_id")

    def __init__(
        self,
        title: str,
        description: str,
        section: Optional[str] = None,
        framework: Optional[str] = None,
        control_id: Optional[str] = None,
    ):
        self.title = title[:120]
        self.description = description
        self.section = section
        self.framework = framework
        self.control_id = control_id


def _detect_schema(item: dict) -> str:
    keys = set(item.keys())
    if "risk_id" in keys or ("risk_score" in keys and "mitigation" in keys and "likelihood" in keys):
        return "risk_register"
    if "vendor_id" in keys or "vendor_name" in keys:
        return "third_party_risk"
    if "workload" in keys or "cloud_model" in keys or "current_gap" in keys:
        return "cloud_migration"
    if "framework_name" in keys or "control_id" in keys:
        return "audit_finding"
    if "incident_id" in keys or ("severity" in keys and "root_cause" in keys):
        return "incident_report"
    return "generic"


def normalize_item(item: dict) -> Optional[NormalizedItem]:
    schema = _detect_schema(item)

    if schema == "audit_finding":
        description = item.get("description", "")
        if not description:
            return None
        domain = item.get("domain", "")
        if domain:
            description = f"[{domain}] {description}"
        fw_raw = (item.get("framework_name") or "").lower()
        framework = _map_framework(fw_raw) or "audit"
        return NormalizedItem(
            title=item.get("title") or item.get("control_id") or "Audit Finding",
            description=description,
            section=domain or item.get("metadata", {}).get("section"),
            framework=framework,
            control_id=item.get("control_id") or item.get("id"),
        )

    if schema == "risk_register":
        parts = [item.get("description", "")]
        likelihood = item.get("likelihood", "")
        impact = item.get("impact", "")
        risk_score = item.get("risk_score", "")
        mitigation = item.get("mitigation", "")
        category = item.get("category", "")
        if likelihood or impact:
            parts.append(f"Likelihood: {likelihood} | Impact: {impact} | Risk Score: {risk_score}")
        if category:
            parts.append(f"Category: {category}")
        if mitigation:
            parts.append(f"Mitigation: {mitigation}")
        owner = item.get("owner", "")
        if owner:
            parts.append(f"Owner: {owner}")
        description = "\n".join(p for p in parts if p)
        if not description:
            return None
        return NormalizedItem(
            title=item.get("title") or item.get("risk_id") or "Risk",
            description=description,
            section=category or "Risk Register",
            framework="risk",
            control_id=item.get("risk_id") or item.get("id"),
        )

    if schema == "cloud_migration":
        parts = [item.get("description", "")]
        cloud_model = item.get("cloud_model", "")
        priority = item.get("business_priority", "")
        risk = item.get("risk", "")
        impact = item.get("impact", "")
        gap = item.get("current_gap", "")
        control = item.get("recommended_control", "")
        owner = item.get("owner", "")
        if cloud_model or priority:
            parts.append(f"Cloud Model: {cloud_model} | Business Priority: {priority}")
        if risk:
            parts.append(f"Risk: {risk}")
        if impact:
            parts.append(f"Impact: {impact}")
        if gap:
            parts.append(f"Current Gap: {gap}")
        if control:
            parts.append(f"Recommended Control: {control}")
        if owner:
            parts.append(f"Owner: {owner}")
        description = "\n".join(p for p in parts if p)
        if not description:
            return None
        workload = item.get("workload", "")
        return NormalizedItem(
            title=workload or item.get("id") or "Cloud Workload",
            description=description,
            section=f"Cloud Migration – {cloud_model}" if cloud_model else "Cloud Migration",
            framework="cloud",
            control_id=item.get("id"),
        )

    if schema == "third_party_risk":
        parts = []
        vendor = item.get("vendor_name", "")
        service = item.get("service", "")
        access = item.get("access_level", "")
        data_access = item.get("data_access", "")
        risk_level = item.get("risk_level", "")
        risk_score = item.get("risk_score", "")
        compliance = item.get("compliance_status", "")
        issues = item.get("identified_issues", "")
        impact = item.get("impact", "")
        mitigation = item.get("mitigation", "")
        owner = item.get("owner", "")
        if vendor or service:
            parts.append(f"Vendor: {vendor} | Service: {service}")
        if access or data_access:
            parts.append(f"Access Level: {access} | Data Access: {data_access}")
        if risk_level or risk_score:
            parts.append(f"Risk Level: {risk_level} | Risk Score: {risk_score}")
        if compliance:
            parts.append(f"Compliance Status: {compliance}")
        if issues:
            parts.append(f"Identified Issues: {issues}")
        if impact:
            parts.append(f"Impact: {impact}")
        if mitigation:
            parts.append(f"Mitigation: {mitigation}")
        if owner:
            parts.append(f"Owner: {owner}")
        description = "\n".join(p for p in parts if p)
        if not description:
            return None
        return NormalizedItem(
            title=f"{vendor} – {service}" if vendor else item.get("vendor_id", "Vendor"),
            description=description,
            section="Third-Party Risk",
            framework="third_party",
            control_id=item.get("vendor_id"),
        )

    if schema == "incident_report":
        parts = [item.get("description", "")]
        severity = item.get("severity", "")
        date = item.get("date") or item.get("incident_date", "")
        systems = item.get("affected_systems", "")
        root_cause = item.get("root_cause", "")
        remediation = item.get("remediation", "")
        if severity or date:
            parts.append(f"Severity: {severity} | Date: {date}")
        if systems:
            parts.append(f"Affected Systems: {systems}")
        if root_cause:
            parts.append(f"Root Cause: {root_cause}")
        if remediation:
            parts.append(f"Remediation: {remediation}")
        description = "\n".join(p for p in parts if p)
        if not description:
            return None
        return NormalizedItem(
            title=item.get("title") or item.get("incident_id") or "Incident",
            description=description,
            section=f"Severity: {severity}" if severity else "Incident Report",
            framework="incident",
            control_id=item.get("incident_id") or item.get("id"),
        )

    # Generic fallback
    description = item.get("description") or item.get("summary") or item.get("notes") or ""
    if not description:
        return None
    title = item.get("title") or item.get("name") or item.get("id") or "Item"
    return NormalizedItem(title=title, description=description)


def normalize_dataset(items: list[dict]) -> list[NormalizedItem]:
    """Normalize a list of raw JSON items. Skips items with no useful description."""
    normalized = []
    for item in items:
        result = normalize_item(item)
        if result:
            normalized.append(result)
    return normalized


# ── Framework name mapping ────────────────────────────────────────────────────

_FRAMEWORK_MAP = {
    "iso27001": "iso27001", "iso_27001": "iso27001", "iso": "iso27001",
    "nist": "nist", "nist_csf": "nist",
    "cis": "cis", "cis_controls": "cis",
    "gdpr": "gdpr",
    "internal_policy": "internal", "internal": "internal",
}


def _map_framework(raw: str) -> Optional[str]:
    return _FRAMEWORK_MAP.get(raw.lower().replace(" ", "_"))
