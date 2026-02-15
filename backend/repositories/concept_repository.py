"""Concept repository: default track/phase queries and get by id."""

from sqlalchemy.orm import Session

from db.models import Concept

# Default curriculum track/phase for legacy and Phase 1
DEFAULT_TRACK = "system_design"
DEFAULT_PHASE = "fundamentals"


class ConceptRepository:
    """Data access for Concept model."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, concept_id: str) -> Concept | None:
        """Return concept by primary key, or None if not found."""
        return self.db.query(Concept).filter(Concept.id == concept_id).first()

    def get_default_track_concepts(self) -> list[Concept]:
        """Return all concepts in default track/phase ordered by sort_order."""
        return (
            self.db.query(Concept)
            .filter(Concept.track == DEFAULT_TRACK, Concept.phase == DEFAULT_PHASE)
            .order_by(Concept.sort_order)
            .all()
        )

    def get_first_default_concept(self) -> Concept | None:
        """Return the first concept in default track/phase by sort_order, or None."""
        return (
            self.db.query(Concept)
            .filter(Concept.track == DEFAULT_TRACK, Concept.phase == DEFAULT_PHASE)
            .order_by(Concept.sort_order)
            .first()
        )

    def get_all_ordered_by_track_phase(self) -> list[Concept]:
        """Return all concepts ordered by track, phase, sort_order (for roadmap)."""
        return (
            self.db.query(Concept)
            .order_by(Concept.track, Concept.phase, Concept.sort_order)
            .all()
        )
