"""Admin API: ingest (PDF + URLs) into LightRAG, curriculum generation, drafts, publish."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session

from db import get_db
from schemas.requests import (
    GenerateCurriculumRequest,
    IngestUrlsRequest,
    PublishCurriculumRequest,
)
from services import lightrag as lightrag_service
from services import curriculum as curriculum_service
from services import curriculum_draft as curriculum_draft_service
from services import ingest as ingest_service

router = APIRouter()


@router.post("/ingest/pdf")
async def ingest_pdf(
    file: UploadFile,
    db: Annotated[Session, Depends(get_db)],
):
    """Upload a PDF; extract text and insert into LightRAG. Records in ingested_docs."""
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="PDF file required")
    try:
        result = await ingest_service.ingest_pdf(db, file)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"PDF parse failed: {e}")
    return result


@router.post("/ingest/urls")
async def ingest_urls(
    body: IngestUrlsRequest,
    db: Annotated[Session, Depends(get_db)],
):
    """Submit URLs; fetch, extract text, insert each into LightRAG. Records in ingested_docs."""
    results = await ingest_service.ingest_urls(db, body.urls)
    return {"results": results}


@router.get("/ingest/sources")
def list_ingest_sources(db: Annotated[Session, Depends(get_db)]):
    """List ingested documents (from ingested_docs table)."""
    sources = ingest_service.list_sources(db)
    return {"sources": sources}


@router.post("/curriculum/generate")
async def generate_curriculum(
    body: GenerateCurriculumRequest,
    db: Annotated[Session, Depends(get_db)],
):
    """Retrieve from LightRAG by topic, synthesize with Gemini, save as curriculum_drafts. Returns draft ids."""
    topic = (body.topic or "").strip() or "system design fundamentals"
    question = f"What are the key concepts and tradeoffs for {topic}?"
    context = await lightrag_service.query(question, only_need_context=True)
    if not context:
        raise HTTPException(
            status_code=503,
            detail="LightRAG returned no context. Ingest content first and ensure GEMINI_API_KEY is set.",
        )
    try:
        data = curriculum_service.generate_curriculum_from_context(
            context, topic=topic
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    draft_ids = curriculum_draft_service.save_drafts(db, data)
    return {"draft_ids": draft_ids}


@router.get("/curriculum/drafts")
def list_curriculum_drafts(db: Annotated[Session, Depends(get_db)]):
    """List all curriculum drafts."""
    drafts = curriculum_draft_service.list_drafts(db)
    return {"drafts": drafts}


@router.post("/curriculum/publish")
def publish_curriculum(
    body: PublishCurriculumRequest,
    db: Annotated[Session, Depends(get_db)],
):
    """Publish selected drafts into concepts, quizzes, failure_facts tables."""
    published = curriculum_draft_service.publish_drafts(db, body.draft_ids)
    return {"published": published}
