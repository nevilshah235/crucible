"""FailureFact repository: query failure_facts for coach hints."""

from sqlalchemy.orm import Session

from db.models import FailureFact


class FailureFactRepository:
    """Data access for FailureFact model (coach hints)."""

    def __init__(self, db: Session):
        self.db = db

    def get_failure_facts(
        self,
        concept_id: str | None = None,
        limit: int = 2,
    ) -> list[dict]:
        """Return failure_facts for coach hints: concept_id match or global (concept_id IS NULL).

        Args:
            concept_id: Optional concept slug; if set, include facts for this concept or global (NULL).
            limit: Max number of facts to return.

        Returns:
            List of dicts with id, tags, keywords, fact, promptHint.
        """
        q = self.db.query(FailureFact)
        if concept_id:
            q = q.filter(
                (FailureFact.concept_id == concept_id)
                | (FailureFact.concept_id.is_(None))
            )
        else:
            q = q.filter(FailureFact.concept_id.is_(None))
        rows = q.order_by(FailureFact.id).limit(limit).all()
        return [
            {
                "id": r.id,
                "tags": r.tags or [],
                "keywords": r.keywords or [],
                "fact": r.fact,
                "promptHint": r.prompt_hint or "",
            }
            for r in rows
        ]
