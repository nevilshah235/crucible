"""LLM integration for coach and curriculum using Google Gemini."""

import google.generativeai as genai

from config import GEMINI_API_KEY

COACH_SYSTEM = """You are a System Design Coach. Your only job is to deepen the learner's thinking.

Rules:
- Never give full solutions or implement for them.
- Reply with at most 2 short Socratic questions. No long explanations.
- Focus on tradeoffs, assumptions, and edge cases.
- If you receive [CHALLENGE] facts below, use them to question or pressure-test their design. Do not quote the facts verbatim or reveal their source.

[CHALLENGE]
{rag_snippet}"""


def _ensure_configured() -> None:
    """Configure Gemini API key once (idempotent). No-op if key missing."""
    if not GEMINI_API_KEY:
        return
    genai.configure(api_key=GEMINI_API_KEY)


def get_gemini_model(system_instruction: str | None = None):
    """Return a Gemini model; configures API key if not already set.

    Args:
        system_instruction: Optional system prompt for the model.

    Returns:
        google.generativeai.GenerativeModel instance.
    """
    _ensure_configured()
    return genai.GenerativeModel(
        "gemini-1.5-flash",
        system_instruction=system_instruction or "",
    )


def generate_coach_feedback(
    design_text: str,
    conversation_context: list[dict],
    rag_snippet: str = "",
) -> str:
    """Generate Socratic coach feedback for a learner design using Gemini.

    Args:
        design_text: The learner's design description.
        conversation_context: List of {role, text} turns for recent conversation.
        rag_snippet: Optional challenge hints (failure facts) to inject into the prompt.

    Returns:
        Coach feedback string, or a message if API key is missing or generation fails.
    """
    from services.llm_provider import get_llm_provider

    system = COACH_SYSTEM.format(rag_snippet=rag_snippet or "(none)")
    parts = [f"Learner's design:\n\n{design_text}"]
    if conversation_context:
        parts.append("\n\nRecent conversation:")
        for turn in conversation_context:
            role = turn.get("role", "user")
            text = turn.get("text", "")[:500]
            parts.append(f"\n{role}: {text}")
    user_content = "\n".join(parts)
    return get_llm_provider().generate_text(
        system_instruction=system,
        user_content=user_content,
        max_output_tokens=256,
        temperature=0.7,
    )
