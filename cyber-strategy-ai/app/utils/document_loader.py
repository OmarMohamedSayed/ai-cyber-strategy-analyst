import io
from pathlib import Path

from app.core.config import get_settings


def extract_text(file_bytes: bytes, filename: str) -> str:
    """
    Extract plain text from PDF, DOCX, or TXT.

    PDFs: skips sparse pages (covers, section dividers, image-only pages)
    that yield fewer than min_page_chars characters after extraction.
    All four supported frameworks (ISO 27001, NIST CSF, CIS Controls, GDPR)
    extract cleanly via pypdf — no OCR required.
    """
    ext = Path(filename).suffix.lower()

    if ext == ".txt":
        return file_bytes.decode("utf-8", errors="replace")

    if ext == ".pdf":
        import pypdf

        settings = get_settings()
        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        pages: list[str] = []
        for page in reader.pages:
            text = page.extract_text() or ""
            if len(text.strip()) >= settings.min_page_chars:
                pages.append(text)
        return "\n\n".join(pages)

    if ext == ".docx":
        import docx2txt
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name
        try:
            text = docx2txt.process(tmp_path)
        finally:
            os.unlink(tmp_path)
        return text or ""

    raise ValueError(f"Unsupported file type: {ext}")
