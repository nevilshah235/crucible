"""Pydantic response models for API responses."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ConceptResponse(BaseModel):
    """Response for a single concept (content API)."""

    id: str
    title: str
    body: str
    tags: list[str] = Field(default_factory=list)


class QuizResponse(BaseModel):
    """Response for a single quiz (content API)."""

    id: str
    concept_id: str = Field(..., alias="conceptId")
    questions: list[Any] = Field(default_factory=list)

    model_config = {"populate_by_name": True, "serialize_by_alias": True}


class ConceptRoadmapItem(BaseModel):
    """Single concept in roadmap response."""

    id: str
    title: str
    phase: str
    sort_order: int
    prerequisite_concept_ids: list[str] = Field(default_factory=list, alias="prerequisiteConceptIds")
    track: str

    model_config = {"populate_by_name": True, "serialize_by_alias": True}


class RoadmapResponse(BaseModel):
    """Response for GET /curriculum/roadmap."""

    concepts: list[ConceptRoadmapItem]


class ProgressResponse(BaseModel):
    """Response for GET /curriculum/me."""

    completed_concept_ids: list[str] = Field(default_factory=list, alias="completedConceptIds")
    next_recommended_concept_id: str | None = Field(None, alias="nextRecommendedConceptId")
    current_track: str = Field(..., alias="currentTrack")

    model_config = {"populate_by_name": True, "serialize_by_alias": True}


class CoachFeedbackResponse(BaseModel):
    """Response for POST /coach/feedback."""

    feedback: str


class QuizSubmitResultItem(BaseModel):
    """Per-question result in quiz submit response."""

    question_id: str | None = Field(None, alias="questionId")
    correct: bool

    model_config = {"populate_by_name": True, "serialize_by_alias": True}


class QuizSubmitResponse(BaseModel):
    """Response for POST /quiz/submit."""

    score: int
    total: int
    results: list[QuizSubmitResultItem] = Field(default_factory=list)


class IngestSourceItem(BaseModel):
    """Single ingested source in list response."""

    doc_id: str
    name: str
    type: str
    created_at: datetime | None = None


class IngestSourcesResponse(BaseModel):
    """Response for GET /admin/ingest/sources."""

    sources: list[IngestSourceItem]


class DraftItem(BaseModel):
    """Single curriculum draft in list response."""

    id: str
    type: str
    payload: dict[str, Any]
    updated_at: datetime | None = None


class CurriculumDraftsResponse(BaseModel):
    """Response for GET /admin/curriculum/drafts."""

    drafts: list[DraftItem]
