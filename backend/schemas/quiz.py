"""Quiz response serialization."""

from db.models import Quiz


def quiz_to_response(q: Quiz) -> dict:
    """Map a Quiz model to the API response (id, conceptId, questions)."""
    return {
        "id": q.id,
        "conceptId": q.concept_id,
        "questions": q.questions or [],
    }
