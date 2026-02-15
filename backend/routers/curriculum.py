"""Curriculum API: roadmap (tracks/phases/concepts) and progress (completed, next recommended)."""

from typing import Annotated

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from auth_deps import get_optional_user_id
from db import get_db
from db.models import ConceptCompletion
from repositories import ConceptRepository
from schemas import concept_to_roadmap_item
from schemas.responses import ConceptRoadmapItem, ProgressResponse, RoadmapResponse

router = APIRouter()


@router.get("/roadmap", response_model=RoadmapResponse)
def get_roadmap(db: Annotated[Session, Depends(get_db)]):
    """Return all concepts as roadmap (id, title, phase, sort_order, prerequisite_concept_ids, track)."""
    repo = ConceptRepository(db)
    concepts = repo.get_all_ordered_by_track_phase()
    return RoadmapResponse(
        concepts=[ConceptRoadmapItem(**concept_to_roadmap_item(c)) for c in concepts]
    )


@router.get("/me", response_model=ProgressResponse)
def get_progress(
    db: Annotated[Session, Depends(get_db)],
    user_id: Annotated[str | None, Depends(get_optional_user_id)] = None,
    x_session_id: str | None = Header(None, alias="X-Session-Id"),
):
    """Return completed_concept_ids, next_recommended_concept_id, current_track.

    Keyed by user_id when authenticated (Phase S0), else X-Session-Id for anonymous.
    """
    q = db.query(ConceptCompletion.concept_id)
    if user_id:
        q = q.filter(ConceptCompletion.user_id == user_id)
    elif x_session_id:
        q = q.filter(ConceptCompletion.session_id == x_session_id)
    else:
        q = q.filter(False)  # no identity
    completed = q.all()
    completed_ids = [r[0] for r in completed]
    repo = ConceptRepository(db)
    all_concepts = repo.get_default_track_concepts()
    next_id = None
    for c in all_concepts:
        if c.id in completed_ids:
            continue
        prereqs = c.prerequisite_concept_ids or []
        if all(pid in completed_ids for pid in prereqs):
            next_id = c.id
            break
    return ProgressResponse(
        completedConceptIds=completed_ids,
        nextRecommendedConceptId=next_id,
        currentTrack="system_design",
    )
