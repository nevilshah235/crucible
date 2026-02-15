"""Coach API: Socratic feedback on learner designs using LLM and failure-fact hints."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import get_db
from schemas.requests import CoachFeedbackRequest
from schemas.responses import CoachFeedbackResponse
from services.coach import get_coach_feedback

router = APIRouter()


@router.post("/feedback", response_model=CoachFeedbackResponse)
def coach_feedback(
    body: CoachFeedbackRequest,
    db: Annotated[Session, Depends(get_db)],
):
    """Return Socratic coach feedback for the given design and conversation context."""
    conversation_context = [{"role": t.role, "text": t.text} for t in body.conversation_context]
    feedback = get_coach_feedback(
        db=db,
        design_text=body.design_text,
        topic=body.topic,
        pressure_test=body.pressure_test,
        conversation_context=conversation_context,
    )
    return CoachFeedbackResponse(feedback=feedback)
