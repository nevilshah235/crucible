"""Failure hints for the coach: from DB (failure_facts by concept_id).

Replaces JSON-based get_failures. Used by coach to build RAG snippet for LLM prompt.
"""

from sqlalchemy.orm import Session

from repositories import FailureFactRepository


def get_failure_facts(db: Session, concept_id: str | None, limit: int = 2) -> list[dict]:
    """Return failure_facts for coach hints: concept_id match or global (concept_id IS NULL).

    Args:
        db: SQLAlchemy session.
        concept_id: Optional concept slug; if set, include facts for this concept or global (NULL).
        limit: Max number of facts to return.

    Returns:
        List of dicts with id, tags, keywords, fact, promptHint.
    """
    repo = FailureFactRepository(db)
    return repo.get_failure_facts(concept_id=concept_id, limit=limit)
