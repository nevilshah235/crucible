"""SQLAlchemy ORM models for curriculum, admin, progress, and users.

Tables: users, concepts, quizzes, failure_facts, curriculum_drafts, ingested_docs, concept_completions.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    """Authenticated user (Google or other provider). id is provider subject (e.g. google_<sub>)."""

    __tablename__ = "users"

    id = Column(String(256), primary_key=True)
    email = Column(String(512), nullable=True)
    name = Column(String(512), nullable=True)
    avatar_url = Column(String(1024), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Concept(Base):
    """Curriculum concept (track, phase, title, body, prerequisites)."""

    __tablename__ = "concepts"

    id = Column(String(128), primary_key=True)
    track = Column(String(64), nullable=False, default="system_design")
    phase = Column(String(64), nullable=False, default="fundamentals")
    sort_order = Column(Integer, nullable=False, default=1)
    prerequisite_concept_ids = Column(ARRAY(String), nullable=True, default=list)
    title = Column(String(512), nullable=False)
    body = Column(Text, nullable=False)
    tags = Column(ARRAY(String), nullable=True, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    quizzes = relationship("Quiz", back_populates="concept")
    failure_facts = relationship("FailureFact", back_populates="concept")


class Quiz(Base):
    """Quiz linked to a concept; questions stored as JSONB."""

    __tablename__ = "quizzes"

    id = Column(String(128), primary_key=True)
    concept_id = Column(String(128), ForeignKey("concepts.id"), nullable=False)
    questions = Column(JSONB, nullable=False)
    difficulty_tier = Column(String(32), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    concept = relationship("Concept", back_populates="quizzes")


class FailureFact(Base):
    """Failure-mode fact for coach hints; optional concept_id for scoping."""

    __tablename__ = "failure_facts"

    id = Column(String(128), primary_key=True)
    concept_id = Column(String(128), ForeignKey("concepts.id"), nullable=True)
    tags = Column(ARRAY(String), nullable=True, default=list)
    keywords = Column(ARRAY(String), nullable=True, default=list)
    fact = Column(Text, nullable=False)
    prompt_hint = Column(String(1024), nullable=True)
    difficulty_tier = Column(String(32), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    concept = relationship("Concept", back_populates="failure_facts")


class CurriculumDraft(Base):
    """Draft curriculum item (type: concept | quiz | failure) with JSONB payload."""

    __tablename__ = "curriculum_drafts"

    id = Column(String(128), primary_key=True)
    type = Column(String(32), nullable=False)  # concept | quiz | failure
    payload = Column(JSONB, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class IngestedDoc(Base):
    """Record of an ingested document (PDF or URL) for LightRAG."""

    __tablename__ = "ingested_docs"

    doc_id = Column(String(256), primary_key=True)
    name = Column(String(512), nullable=False)
    type = Column(String(32), nullable=False)  # pdf | url
    created_at = Column(DateTime, default=datetime.utcnow)


class ConceptCompletion(Base):
    """Completion record per session (or user) and concept."""

    __tablename__ = "concept_completions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(256), nullable=True)
    session_id = Column(String(256), nullable=True)
    concept_id = Column(String(128), ForeignKey("concepts.id"), nullable=False)
    completed_at = Column(DateTime, default=datetime.utcnow)
    quiz_score = Column(Integer, nullable=True)
    design_submitted = Column(Boolean, default=False)
