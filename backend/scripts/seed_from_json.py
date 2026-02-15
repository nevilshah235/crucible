#!/usr/bin/env python3
"""One-time seed from content/concept.json, content/quiz.json, content/rag/failures.json into DB.

Run from backend dir: python scripts/seed_from_json.py
Requires: DATABASE_URL set, migrations applied.
"""

import json
import os
import sys
from pathlib import Path

# Add backend to path when run from repo root or backend
_backend = Path(__file__).resolve().parent.parent
if str(_backend) not in sys.path:
    sys.path.insert(0, str(_backend))

from dotenv import load_dotenv
load_dotenv(_backend / ".env")

from sqlalchemy.orm import Session
from db import SessionLocal, init_db
from db.models import Concept, Quiz, FailureFact


def load_json(path: Path) -> dict | list:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text())


def seed(session: Session, content_dir: Path) -> None:
    content_dir = content_dir.resolve()
    concept_path = content_dir / "concept.json"
    quiz_path = content_dir / "quiz.json"
    failures_path = content_dir / "rag" / "failures.json"

    # Concepts
    if concept_path.exists():
        data = load_json(concept_path)
        c = Concept(
            id=data["id"],
            track="system_design",
            phase="fundamentals",
            sort_order=1,
            prerequisite_concept_ids=[],
            title=data["title"],
            body=data["body"],
            tags=data.get("tags") or [],
        )
        session.merge(c)
        session.commit()
        print(f"Seeded concept: {c.id}")

    # Quizzes
    if quiz_path.exists():
        data = load_json(quiz_path)
        q = Quiz(
            id=data["id"],
            concept_id=data["conceptId"],
            questions=data["questions"],
            difficulty_tier=None,
        )
        session.merge(q)
        session.commit()
        print(f"Seeded quiz: {q.id}")

    # Failure facts
    if failures_path.exists():
        data = load_json(failures_path)
        for e in data.get("entries", []):
            f = FailureFact(
                id=e["id"],
                concept_id="caching-basics",
                tags=e.get("tags") or [],
                keywords=e.get("keywords") or [],
                fact=e["fact"],
                prompt_hint=e.get("promptHint"),
                difficulty_tier=None,
            )
            session.merge(f)
        session.commit()
        print(f"Seeded {len(data.get('entries', []))} failure_facts")


def main() -> None:
    # Content dir: repo root content/
    repo_root = _backend.parent
    content_dir = repo_root / "content"
    if not content_dir.exists():
        print("Content dir not found:", content_dir)
        sys.exit(1)

    init_db()
    db = SessionLocal()
    try:
        seed(db, content_dir)
    finally:
        db.close()
    print("Seed done.")


if __name__ == "__main__":
    main()
