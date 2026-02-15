"""CurriculumDraft repository: list, get by ids, merge drafts."""

from typing import Any

from sqlalchemy.orm import Session

from db.models import CurriculumDraft


class CurriculumDraftRepository:
    """Data access for CurriculumDraft model."""

    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> list[CurriculumDraft]:
        """Return all drafts ordered by updated_at desc."""
        return (
            self.db.query(CurriculumDraft)
            .order_by(CurriculumDraft.updated_at.desc())
            .all()
        )

    def get_by_ids(self, draft_ids: list[str]) -> list[CurriculumDraft]:
        """Return drafts with given IDs."""
        if not draft_ids:
            return []
        return (
            self.db.query(CurriculumDraft)
            .filter(CurriculumDraft.id.in_(draft_ids))
            .all()
        )

    def merge_one(self, id: str, type: str, payload: dict[str, Any]) -> None:
        """Merge a single draft (insert or update)."""
        row = CurriculumDraft(id=id, type=type, payload=payload)
        self.db.merge(row)
        self.db.commit()
