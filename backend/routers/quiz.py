import json
from pathlib import Path

from fastapi import APIRouter

from config import CONTENT_DIR

router = APIRouter()


def _load_quiz() -> dict:
    path = CONTENT_DIR / "quiz.json"
    return json.loads(path.read_text())


@router.post("/submit")
def submit_quiz(body: dict):
    answers = body.get("answers", [])
    quiz = _load_quiz()
    questions_by_id = {q["id"]: q for q in quiz["questions"]}
    results = []
    score = 0
    for ans in answers:
        qid = ans.get("questionId")
        selected = ans.get("selectedOptionId")
        q = questions_by_id.get(qid)
        correct = False
        if q:
            for opt in q["options"]:
                if opt["id"] == selected and opt.get("correct"):
                    correct = True
                    score += 1
                    break
        results.append({"questionId": qid, "correct": correct})
    return {"score": score, "total": len(quiz["questions"]), "results": results}
