"""IngestedDoc repository: list and add ingested documents."""

from sqlalchemy.orm import Session

from db.models import IngestedDoc


class IngestedDocRepository:
    """Data access for IngestedDoc model."""

    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> list[IngestedDoc]:
        """Return all ingested docs ordered by created_at desc."""
        return (
            self.db.query(IngestedDoc)
            .order_by(IngestedDoc.created_at.desc())
            .all()
        )

    def add(self, doc_id: str, name: str, type: str) -> None:
        """Add an ingested doc record."""
        row = IngestedDoc(doc_id=doc_id, name=name, type=type)
        self.db.add(row)
        self.db.commit()
