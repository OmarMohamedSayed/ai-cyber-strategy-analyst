"""
Structure-aware chunker with per-framework heading patterns and chunk presets.

Framework-specific settings (from PDF analysis):
  iso27001  → chunk 800 / overlap 100  | decimal headings (4.2, Annex A.5.1)
  nist      → chunk 1200 / overlap 150 | numbered sections (1., 3.1.)
  cis       → chunk 1200 / overlap 200 | "Control N:" + subsection titles
  gdpr      → chunk 1000 / overlap 150 | title-case topic headings
  default   → chunk 700  / overlap 100 | generic headings
"""

import re
import uuid
from typing import Optional

from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.models.domain import DocumentChunk, ChunkMetadata


# ── Per-framework heading regexes ─────────────────────────────────────────────

_HEADING_PATTERNS: dict[str, re.Pattern] = {
    # ISO 27001: "4.2  Context", "Annex A", "A.5.1  Policies..."
    "iso27001": re.compile(
        r"(?m)^(?:"
        r"\d+(?:\.\d+)*\s{1,6}[A-Z].+|"      # 4.2  Title
        r"Annex\s+[A-Z].*|"                    # Annex A
        r"[A-Z]\.\d+(?:\.\d+)*\s+.+"           # A.5.1  Control name
        r")"
    ),
    # NIST CSF 2.0: "1. Introduction", "3.1. The CSF Core"
    "nist": re.compile(
        r"(?m)^(?:"
        r"\d+(?:\.\d+)*\.\s+[A-Z].+|"         # 1. Title  /  3.1. Title
        r"[A-Z]{2,}[A-Z\s\-]+$"               # ALL-CAPS function labels (GOVERN, IDENTIFY…)
        r")"
    ),
    # CIS Controls: "Control 1: ...", "Why is this Control critical?", "Safeguards"
    "cis": re.compile(
        r"(?m)^(?:"
        r"Control\s+\d+[:\s].+|"              # Control 1: Inventory…
        r"Why is this Control critical\?|"
        r"Procedures and tools|"
        r"Safeguards"
        r")"
    ),
    # GDPR briefing: standalone title-case headings (short lines on their own)
    "gdpr": re.compile(
        r"(?m)^[A-Z][A-Za-z\s'\-]{5,60}$"    # "What's new in the GDPR"
    ),
    # Generic fallback
    "default": re.compile(
        r"(?m)^(?:"
        r"#{1,4}\s.+|"                         # Markdown headings
        r"\d+\.\d*\s+[A-Z].+|"                # "1.2 Access Control"
        r"[A-Z][A-Z\s]{4,}$"                  # ALL-CAPS headings
        r")"
    ),
}

# ── Per-framework control_id extractors ───────────────────────────────────────

# ISO: 1-2 digit section (4, 10) with optional decimals (4.2, 10.1.3), OR Annex A.5.1
# Strictly 1-2 leading digits prevents matching "27001" from ToC text
_ISO_ID_RE  = re.compile(r"^([A-Z]\.\d+(?:\.\d+)*|\d{1,2}(?:\.\d+)+|\d{1,2}(?=\s))")
_NIST_ID_RE = re.compile(r"^(\d+(?:\.\d+)*)\.")                          # 3.1.
_CIS_ID_RE  = re.compile(r"^Control\s+(\d+)", re.IGNORECASE)             # Control 5
# GDPR briefing has no Article numbers — use a short slug of the heading itself
_GDPR_SLUG_RE = re.compile(r"[^A-Za-z0-9]+")


def _extract_control_id(heading: str, fw: str) -> Optional[str]:
    """Extract a meaningful control/section ID from a heading string."""
    heading = heading.strip()
    if fw == "iso27001":
        m = _ISO_ID_RE.match(heading)
        return m.group(1) if m else None
    if fw == "nist":
        m = _NIST_ID_RE.match(heading)
        return m.group(1) if m else None
    if fw == "cis":
        m = _CIS_ID_RE.match(heading)
        return f"CIS-{m.group(1)}" if m else None
    if fw == "gdpr":
        # No formal article numbers in the EPSU briefing — slug the heading.
        # Skip pure numeric headings (page numbers caught by the regex).
        if heading.isdigit():
            return None
        slug = _GDPR_SLUG_RE.sub("-", heading).strip("-")[:40]
        return f"GDPR-{slug}" if slug else None
    return None

# ── Per-framework chunk presets ───────────────────────────────────────────────

_CHUNK_PRESETS: dict[str, tuple[int, int]] = {
    "iso27001": (800, 100),
    "nist":     (1200, 150),
    "cis":      (1200, 200),
    "gdpr":     (1000, 150),
    "default":  (700, 100),
}


def _detect_framework(category: str, source: str) -> str:
    """Map category/source name to a framework key for heading/preset selection."""
    combined = f"{category} {source}".lower()
    if "iso" in combined or "27001" in combined:
        return "iso27001"
    if "nist" in combined or "csf" in combined:
        return "nist"
    if "cis" in combined:
        return "cis"
    if "gdpr" in combined or "epsu" in combined:
        return "gdpr"
    return "default"


def _split_by_structure(text: str, pattern: re.Pattern) -> list[str]:
    """Split text into logical sections using the provided heading pattern."""
    boundaries = [m.start() for m in pattern.finditer(text)]
    if not boundaries:
        return [text]

    sections: list[str] = []

    # Leading text before first heading
    if boundaries[0] > 0:
        preamble = text[: boundaries[0]].strip()
        if preamble:
            sections.append(preamble)

    for i, start in enumerate(boundaries):
        end = boundaries[i + 1] if i + 1 < len(boundaries) else len(text)
        section = text[start:end].strip()
        if section:
            sections.append(section)

    return sections


def chunk_document(
    text: str,
    document_id: str,
    source: str,
    category: str,
    document_type: str,
    chunk_size: int = 0,      # 0 = use framework preset
    chunk_overlap: int = 0,   # 0 = use framework preset
    business_unit: Optional[str] = None,
    framework: Optional[str] = None,  # explicit override
) -> list[DocumentChunk]:
    """
    Structure-aware recursive chunking with overlap.

    Heading patterns and chunk sizes are chosen per-framework automatically
    unless overridden by the caller. control_id is extracted from each
    section heading using per-framework regex extractors.
    """
    fw = framework or _detect_framework(category, source)
    preset_size, preset_overlap = _CHUNK_PRESETS.get(fw, _CHUNK_PRESETS["default"])
    chunk_size = chunk_size or preset_size
    chunk_overlap = chunk_overlap or preset_overlap

    pattern = _HEADING_PATTERNS.get(fw, _HEADING_PATTERNS["default"])
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    structural_sections = _split_by_structure(text, pattern)
    chunks: list[DocumentChunk] = []
    chunk_index = 0

    # Track the last seen control_id so sub-chunks inherit it
    current_control_id: Optional[str] = None

    for section in structural_sections:
        lines = section.strip().splitlines()
        section_title = lines[0].strip() if lines else "Section"

        # Extract control_id from this section's heading; carry forward if not found
        extracted = _extract_control_id(section_title, fw)
        if extracted:
            current_control_id = extracted

        sub_chunks = [section] if len(section) <= chunk_size else splitter.split_text(section)

        for sub in sub_chunks:
            sub = sub.strip()
            if not sub:
                continue
            chunks.append(
                DocumentChunk(
                    id=str(uuid.uuid4()),
                    document_id=document_id,
                    title=section_title[:120],
                    description=sub,
                    category=category,
                    source=source,
                    metadata=ChunkMetadata(
                        chunk_index=chunk_index,
                        document_type=document_type,
                        section=section_title[:120],
                        business_unit=business_unit,
                        framework=fw if fw != "default" else None,
                        control_id=current_control_id,
                    ),
                )
            )
            chunk_index += 1

    return chunks
