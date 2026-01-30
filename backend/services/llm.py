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


def generate_coach_feedback(
    design_text: str,
    conversation_context: list[dict],
    rag_snippet: str = "",
) -> str:
    if not GEMINI_API_KEY:
        return "Set GEMINI_API_KEY to enable the coach."
    genai.configure(api_key=GEMINI_API_KEY)
    system = COACH_SYSTEM.format(rag_snippet=rag_snippet or "(none)")
    model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=system)
    # Stateless: no chat object; fold context into one user message
    parts = [f"Learner's design:\n\n{design_text}"]
    if conversation_context:
        parts.append("\n\nRecent conversation:")
        for turn in conversation_context:
            role = turn.get("role", "user")
            text = turn.get("text", "")[:500]
            parts.append(f"\n{role}: {text}")
    user_content = "\n".join(parts)
    response = model.generate_content(
        user_content,
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=256,
            temperature=0.7,
        ),
    )
    if not response or not response.text:
        return "The coach could not generate a response."
    return response.text.strip()
