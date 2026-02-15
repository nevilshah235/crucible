"""LLM provider interface and Gemini implementation.

Enables swapping LLM implementations (DIP). Default implementation uses Google Gemini.
"""

import json
import re
from typing import Any, Protocol

import google.generativeai as genai

from config import GEMINI_API_KEY
from services.llm import get_gemini_model


class LLMProvider(Protocol):
    """Protocol for LLM providers (coach text and curriculum JSON)."""

    def generate_text(
        self,
        system_instruction: str,
        user_content: str,
        *,
        max_output_tokens: int = 256,
        temperature: float = 0.7,
    ) -> str:
        """Generate plain text response."""
        ...

    def generate_json(
        self,
        system_instruction: str,
        user_content: str,
        *,
        max_output_tokens: int = 4096,
        temperature: float = 0.3,
    ) -> dict[str, Any]:
        """Generate JSON response (parsed dict)."""
        ...


class GeminiLLM:
    """Gemini-backed LLM provider using shared get_gemini_model()."""

    def generate_text(
        self,
        system_instruction: str,
        user_content: str,
        *,
        max_output_tokens: int = 256,
        temperature: float = 0.7,
    ) -> str:
        """Generate plain text using Gemini."""
        if not GEMINI_API_KEY:
            return "Set GEMINI_API_KEY to enable the coach."
        model = get_gemini_model(system_instruction=system_instruction)
        response = model.generate_content(
            user_content,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=max_output_tokens,
                temperature=temperature,
            ),
        )
        if not response or not response.text:
            return "The coach could not generate a response."
        return response.text.strip()

    def generate_json(
        self,
        system_instruction: str,
        user_content: str,
        *,
        max_output_tokens: int = 4096,
        temperature: float = 0.3,
    ) -> dict[str, Any]:
        """Generate JSON using Gemini; returns parsed dict."""
        model = get_gemini_model(system_instruction=system_instruction)
        response = model.generate_content(
            user_content,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=max_output_tokens,
                temperature=temperature,
                response_mime_type="application/json",
            ),
        )
        if not response or not response.text:
            raise ValueError("Gemini returned no text")
        text = response.text.strip()
        if "```" in text:
            match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
            if match:
                text = match.group(1).strip()
        return json.loads(text)


# Default provider used by coach and curriculum services.
_default_llm: LLMProvider | None = None


def get_llm_provider() -> LLMProvider:
    """Return the default LLM provider (Gemini)."""
    global _default_llm
    if _default_llm is None:
        _default_llm = GeminiLLM()
    return _default_llm
