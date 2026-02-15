"""Quiz API: submit quiz answers and get score/results (legacy: first quiz by default track)."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from repositories import QuizRepository
from schemas.requests import QuizSubmitRequest
from schemas.responses import QuizSubmitResponse, QuizSubmitResultItem

router = APIRouter()


@router.post("/submit", response_model=QuizSubmitResponse)
def submit_quiz(body: QuizSubmitRequest, db: Annotated[Session, Depends(get_db)]):
    """Submit quiz answers; return score, total, and per-question correctness."""
    answers = body.answers
    quiz_repo = QuizRepository(db)
    quiz_row = quiz_repo.get_first_for_default_track()
    if not quiz_row:
        raise HTTPException(status_code=404, detail="No quiz found. Run seed or publish curriculum.")
    questions = quiz_row.questions or []
    questions_by_id = {q["id"]: q for q in questions}
    results: list[QuizSubmitResultItem] = []
    score = 0
    for ans in answers:
        qid = ans.question_id
        selected = ans.selected_option_id
        q = questions_by_id.get(qid) if qid else None
        correct = False
        if q:
            for opt in q.get("options") or []:
                if opt.get("id") == selected and opt.get("correct"):
                    correct = True
                    score += 1
                    break
        results.append(QuizSubmitResultItem(questionId=qid, correct=correct))
    return QuizSubmitResponse(score=score, total=len(questions), results=results)
