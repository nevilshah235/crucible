"""Ingest service: extract text from PDF/URL and insert into LightRAG + DB."""

import uuid
from typing import Any

import httpx
import trafilatura
from fastapi import UploadFile
from pymupdf import open as pymupdf_open
from sqlalchemy.orm import Session

from repositories import IngestedDocRepository
from services import lightrag as lightrag_service


def extract_pdf_text(file: UploadFile) -> str:
    """Extract text from uploaded PDF using PyMuPDF.

    Args:
        file: FastAPI UploadFile (PDF).

    Returns:
        Concatenated page text, or empty string if none.
    """
    content = file.file.read()
    doc = pymupdf_open(stream=content)
    parts = []
    for page in doc:
        parts.append(page.get_text())
    doc.close()
    return "\n\n".join(parts).strip() or ""


def extract_url_text(url: str) -> str:
    """Fetch URL and extract main text using trafilatura.

    Args:
        url: HTTP(S) URL to fetch.

    Returns:
        Extracted main text, stripped.

    Raises:
        httpx.HTTPStatusError: On non-2xx response.
    """
    resp = httpx.get(url, follow_redirects=True, timeout=30)
    resp.raise_for_status()
    text = trafilatura.extract(resp.content, url=url)
    return (text or "").strip()


async def ingest_pdf(db: Session, file: UploadFile) -> dict[str, Any]:
    """Extract text from PDF, insert into LightRAG, record in DB.

    Args:
        db: SQLAlchemy session.
        file: FastAPI UploadFile (PDF).

    Returns:
        Dict with doc_id, name, type.

    Raises:
        ValueError: If file is not PDF or no text extracted.
    """
    text = extract_pdf_text(file)
    if not text:
        raise ValueError("No text extracted from PDF")
    doc_id = str(uuid.uuid4())
    doc_id = await lightrag_service.insert(text, doc_name=doc_id) or doc_id
    name = file.filename or "upload.pdf"
    repo = IngestedDocRepository(db)
    repo.add(doc_id=doc_id, name=name, type="pdf")
    return {"doc_id": doc_id, "name": name, "type": "pdf"}


async def ingest_urls(db: Session, urls: list[str]) -> list[dict[str, Any]]:
    """Fetch each URL, extract text, insert into LightRAG, record in DB.

    Args:
        db: SQLAlchemy session.
        urls: List of URLs to ingest.

    Returns:
        List of {url, doc_id} or {url, error, doc_id: None} per URL.
    """
    results: list[dict[str, Any]] = []
    for url in urls:
        if not isinstance(url, str) or not url.strip():
            continue
        url = url.strip()
        try:
            text = extract_url_text(url)
        except Exception as e:
            results.append({"url": url, "error": str(e), "doc_id": None})
            continue
        if not text:
            results.append({"url": url, "error": "No text extracted", "doc_id": None})
            continue
        doc_id = str(uuid.uuid4())
        doc_id = await lightrag_service.insert(text, doc_name=doc_id) or doc_id
        repo = IngestedDocRepository(db)
        repo.add(doc_id=doc_id, name=url, type="url")
        results.append({"url": url, "doc_id": doc_id})
    return results


def list_sources(db: Session) -> list[dict[str, Any]]:
    """List ingested documents (from ingested_docs table).

    Args:
        db: SQLAlchemy session.

    Returns:
        List of dicts with doc_id, name, type, created_at.
    """
    repo = IngestedDocRepository(db)
    rows = repo.list_all()
    return [
        {
            "doc_id": r.doc_id,
            "name": r.name,
            "type": r.type,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in rows
    ]
