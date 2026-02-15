"""Database package: models, engine, and session.

Usage:
    from db import get_db, init_db, SessionLocal
    from db.models import Concept, Quiz, ...
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config import DATABASE_URL
from db.models import Base

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """FastAPI dependency that yields a DB session and closes it on exit."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Create all tables. Safe to call on existing DB (no-op for existing tables)."""
    Base.metadata.create_all(bind=engine)
