"""Curriculum draft service: save and publish curriculum drafts to DB."""

import uuid
from typing import Any

from sqlalchemy.orm import Session

from db.models import Concept, FailureFact, Quiz
from repositories import CurriculumDraftRepository


def save_drafts(db: Session, data: dict[str, Any]) -> list[str]:
    """Save generated curriculum data (concepts, quizzes, failure_facts) as drafts.

    Args:
        db: SQLAlchemy session.
        data: Dict with keys concepts, quizzes, failure_facts (each a list of objects).

    Returns:
        List of draft IDs saved.
    """
    repo = CurriculumDraftRepository(db)
    draft_ids: list[str] = []
    for c in data.get("concepts") or []:
        cid = c.get("id") or str(uuid.uuid4())
        repo.merge_one(cid, "concept", c)
        draft_ids.append(cid)
    for q in data.get("quizzes") or []:
        qid = q.get("id") or str(uuid.uuid4())
        repo.merge_one(qid, "quiz", q)
        draft_ids.append(qid)
    for f in data.get("failure_facts") or []:
        fid = f.get("id") or str(uuid.uuid4())
        repo.merge_one(fid, "failure", f)
        draft_ids.append(fid)
    return draft_ids


def list_drafts(db: Session) -> list[dict[str, Any]]:
    """List all curriculum drafts ordered by updated_at desc.

    Args:
        db: SQLAlchemy session.

    Returns:
        List of dicts with id, type, payload, updated_at.
    """
    repo = CurriculumDraftRepository(db)
    rows = repo.list_all()
    return [
        {
            "id": r.id,
            "type": r.type,
            "payload": r.payload,
            "updated_at": r.updated_at.isoformat() if r.updated_at else None,
        }
        for r in rows
    ]


def publish_drafts(db: Session, draft_ids: list[str]) -> list[str]:
    """Publish selected drafts into concepts, quizzes, failure_facts tables.

    Args:
        db: SQLAlchemy session.
        draft_ids: List of draft IDs to publish.

    Returns:
        List of published draft IDs.
    """
    repo = CurriculumDraftRepository(db)
    drafts = repo.get_by_ids(draft_ids)
    for d in drafts:
        p = d.payload or {}
        if d.type == "concept":
            db.merge(
                Concept(
                    id=d.id,
                    track=p.get("track") or "system_design",
                    phase=p.get("phase") or "fundamentals",
                    sort_order=int(p.get("sort_order") or 1),
                    prerequisite_concept_ids=p.get("prerequisite_concept_ids") or [],
                    title=p.get("title") or "",
                    body=p.get("body") or "",
                    tags=p.get("tags") or [],
                )
            )
        elif d.type == "quiz":
            db.merge(
                Quiz(
                    id=d.id,
                    concept_id=p.get("conceptId") or p.get("concept_id") or "",
                    questions=p.get("questions") or [],
                    difficulty_tier=p.get("difficulty_tier"),
                )
            )
        elif d.type == "failure":
            db.merge(
                FailureFact(
                    id=d.id,
                    concept_id=p.get("concept_id"),
                    tags=p.get("tags") or [],
                    keywords=p.get("keywords") or [],
                    fact=p.get("fact") or "",
                    prompt_hint=p.get("promptHint") or p.get("prompt_hint"),
                    difficulty_tier=p.get("difficulty_tier"),
                )
            )
    db.commit()
    return draft_ids
