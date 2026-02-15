"""Content API: concepts and quizzes from DB.

Legacy: GET /content/concept and GET /content/quiz return first concept/quiz (backward compatible).
By-id: GET /content/concept/:id, GET /content/quiz/:conceptId.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from repositories import ConceptRepository, QuizRepository
from schemas import concept_to_response, quiz_to_response
from schemas.responses import ConceptResponse, QuizResponse

router = APIRouter()


@router.get("/concept", response_model=ConceptResponse)
def get_concept(db: Annotated[Session, Depends(get_db)]):
    """Legacy: return first concept (by sort_order, system_design, fundamentals). Same shape as before.

    Raises:
        HTTPException: 404 if no concept found.
    """
    repo = ConceptRepository(db)
    c = repo.get_first_default_concept()
    if not c:
        raise HTTPException(status_code=404, detail="No concept found. Run seed or publish curriculum.")
    return concept_to_response(c)


@router.get("/concept/{concept_id}", response_model=ConceptResponse)
def get_concept_by_id(concept_id: str, db: Annotated[Session, Depends(get_db)]):
    """Return concept by id.

    Raises:
        HTTPException: 404 if concept not found.
    """
    repo = ConceptRepository(db)
    c = repo.get_by_id(concept_id)
    if not c:
        raise HTTPException(status_code=404, detail=f"Concept not found: {concept_id}")
    return concept_to_response(c)


@router.get("/quiz", response_model=QuizResponse)
def get_quiz(db: Annotated[Session, Depends(get_db)]):
    """Legacy: return first quiz (quiz for first concept). Same shape as before.

    Raises:
        HTTPException: 404 if no concept or quiz found.
    """
    quiz_repo = QuizRepository(db)
    q = quiz_repo.get_first_for_default_track()
    if not q:
        raise HTTPException(status_code=404, detail="No quiz found. Run seed or publish curriculum.")
    return quiz_to_response(q)


@router.get("/quiz/{concept_id}", response_model=QuizResponse)
def get_quiz_by_concept_id(concept_id: str, db: Annotated[Session, Depends(get_db)]):
    """Return quiz for concept_id.

    Raises:
        HTTPException: 404 if no quiz for that concept.
    """
    quiz_repo = QuizRepository(db)
    q = quiz_repo.get_by_concept_id(concept_id)
    if not q:
        raise HTTPException(status_code=404, detail=f"No quiz for concept: {concept_id}")
    return quiz_to_response(q)
