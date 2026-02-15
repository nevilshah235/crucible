"""Pydantic request models for POST/PUT bodies."""

from typing import Any

from pydantic import BaseModel, Field


class IngestUrlsRequest(BaseModel):
    """Request body for POST /admin/ingest/urls."""

    urls: list[str] = Field(..., min_length=1, description="List of URLs to ingest")


class GenerateCurriculumRequest(BaseModel):
    """Request body for POST /admin/curriculum/generate."""

    topic: str | None = Field(None, description="Topic focus for curriculum generation")


class PublishCurriculumRequest(BaseModel):
    """Request body for POST /admin/curriculum/publish."""

    draft_ids: list[str] = Field(..., min_length=1, description="IDs of drafts to publish")


class CoachConversationTurn(BaseModel):
    """Single turn in coach conversation context."""

    role: str = "user"
    text: str = ""


class CoachFeedbackRequest(BaseModel):
    """Request body for POST /coach/feedback."""

    design_text: str = Field("", alias="designText")
    topic: str | None = Field(None, description="Concept id or topic name")
    pressure_test: bool = Field(False, alias="pressureTest")
    conversation_context: list[CoachConversationTurn] = Field(default_factory=list, alias="conversationContext")

    model_config = {"populate_by_name": True}


class QuizAnswerItem(BaseModel):
    """Single answer in quiz submit."""

    question_id: str | None = Field(None, alias="questionId")
    selected_option_id: str | None = Field(None, alias="selectedOptionId")

    model_config = {"populate_by_name": True}


class QuizSubmitRequest(BaseModel):
    """Request body for POST /quiz/submit."""

    answers: list[QuizAnswerItem] = Field(default_factory=list)
