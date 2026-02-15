"""Quiz repository: get by concept_id or first for default track."""

from sqlalchemy.orm import Session

from db.models import Concept, Quiz
from repositories.concept_repository import ConceptRepository


class QuizRepository:
    """Data access for Quiz model."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_concept_id(self, concept_id: str) -> Quiz | None:
        """Return quiz for the given concept_id, or None if not found."""
        return self.db.query(Quiz).filter(Quiz.concept_id == concept_id).first()

    def get_first_for_default_track(self) -> Quiz | None:
        """Return the quiz for the first concept in default track/phase, or None."""
        concept_repo = ConceptRepository(self.db)
        first_concept = concept_repo.get_first_default_concept()
        if not first_concept:
            return None
        return self.get_by_concept_id(first_concept.id)
