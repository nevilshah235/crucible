"""Coach service: build RAG snippet and generate Socratic feedback via LLM."""

from sqlalchemy.orm import Session

from services import rag as rag_service
from services.llm import generate_coach_feedback


def _build_rag_snippet(
    db: Session,
    concept_id: str | None,
    pressure_test: bool,
    limit: int = 2,
) -> str:
    """Build a text snippet of failure-fact hints for the coach prompt.

    Args:
        db: SQLAlchemy session.
        concept_id: Optional concept slug (or topic name); used when pressure_test or concept_id set.
        pressure_test: If True, include hints even when concept_id is missing (fallback concept used).
        limit: Max number of failure facts to include.

    Returns:
        Newline-separated lines of hint (Fact: ...), or empty string if none.
    """
    if not concept_id and not pressure_test:
        return ""
    failures = rag_service.get_failure_facts(
        db, concept_id=concept_id or "caching-basics", limit=limit
    )
    lines = []
    for e in failures:
        hint = e.get("promptHint", "")
        fact = e.get("fact", "")
        lines.append(f"- {hint} (Fact: {fact})")
    return "\n".join(lines) if lines else ""


def get_coach_feedback(
    db: Session,
    design_text: str,
    topic: str | None = None,
    pressure_test: bool = False,
    conversation_context: list[dict] | None = None,
) -> str:
    """Generate Socratic coach feedback for a learner design.

    Args:
        db: SQLAlchemy session (for failure-fact lookup).
        design_text: The learner's design description.
        topic: Optional concept id or topic name for RAG hints.
        pressure_test: If True, include failure-fact hints even when topic is missing.
        conversation_context: List of {role, text} turns for recent conversation.

    Returns:
        Coach feedback string.
    """
    rag_snippet = _build_rag_snippet(
        db, concept_id=topic, pressure_test=pressure_test
    )
    return generate_coach_feedback(
        design_text=design_text,
        conversation_context=conversation_context or [],
        rag_snippet=rag_snippet,
    )
