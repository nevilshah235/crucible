"""Curriculum generation: LightRAG context + Gemini structured output.

Produces concepts, quizzes, and failure_facts. Uses LLM provider (default: Gemini).
"""

from config import GEMINI_API_KEY
from services.llm_provider import get_llm_provider

CURRICULUM_SYSTEM = """You are a curriculum designer for system design learning.

Given retrieved context from a knowledge base, output a JSON object with exactly these keys:
- "concepts": array of objects with: id (string, slug), title, body, tags (array), track ("system_design" or "ml_ops"), phase ("fundamentals"|"patterns"|"tradeoffs"|"failure_modes"|"advanced"), sort_order (int), prerequisite_concept_ids (array of concept ids)
- "quizzes": array of objects with: id (string), conceptId (string, must match a concept id), questions (array of { id, text, options: [{ id, text, correct: boolean }] }), optional difficulty_tier
- "failure_facts": array of objects with: id (string), concept_id (string, optional; null = global), tags, keywords (array), fact, promptHint, optional difficulty_tier

Output only valid JSON, no markdown or explanation. Use the context to create 1-3 concepts, 0-1 quiz per concept, and 0-2 failure_facts per concept where relevant."""


def generate_curriculum_from_context(context: str, topic: str | None = None) -> dict:
    """Send context to Gemini; return parsed JSON with concepts, quizzes, failure_facts.

    Args:
        context: Retrieved knowledge-base context (e.g. from LightRAG).
        topic: Optional topic focus for the prompt.

    Returns:
        Dict with keys concepts, quizzes, failure_facts (each a list of objects).

    Raises:
        ValueError: If GEMINI_API_KEY is missing or Gemini returns invalid/no text.
    """
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY required for curriculum generation")
    user = f"Topic focus: {topic or 'general system design'}\n\nRetrieved context:\n{context[:30000]}"
    return get_llm_provider().generate_json(
        system_instruction=CURRICULUM_SYSTEM,
        user_content=user,
        max_output_tokens=4096,
        temperature=0.3,
    )
