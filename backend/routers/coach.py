from fastapi import APIRouter

from services.llm import generate_coach_feedback
from services import rag as rag_service

router = APIRouter()


def _build_rag_snippet(topic: str | None, pressure_test: bool, limit: int = 2) -> str:
    if not topic and not pressure_test:
        return ""
    failures = rag_service.get_failures(topic=topic or "caching", limit=limit)
    lines = []
    for e in failures:
        hint = e.get("promptHint", "")
        fact = e.get("fact", "")
        lines.append(f"- {hint} (Fact: {fact})")
    return "\n".join(lines) if lines else ""


@router.post("/feedback")
def coach_feedback(body: dict):
    design_text = body.get("designText", "")
    topic = body.get("topic")
    pressure_test = body.get("pressureTest", False)
    conversation_context = body.get("conversationContext", [])
    rag_snippet = _build_rag_snippet(topic=topic, pressure_test=pressure_test)
    feedback = generate_coach_feedback(
        design_text=design_text,
        conversation_context=conversation_context,
        rag_snippet=rag_snippet,
    )
    return {"feedback": feedback}
