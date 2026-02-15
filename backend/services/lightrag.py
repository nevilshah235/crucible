"""
LightRAG service using Google Gemini only (LLM + embeddings).

Uses lightrag.llm.gemini: gemini_complete_if_cache, gemini_embed.
Requires GEMINI_API_KEY. Working dir and storage default to local (no Milvus/Neo4j required for Phase 1).
"""

import asyncio
import os
from typing import Literal

from config import GEMINI_API_KEY, LIGHTRAG_WORKING_DIR

# Lazy imports so app starts without lightrag deps if not used
_rag = None
_rag_lock = asyncio.Lock()

# Default Gemini model names for LightRAG
LIGHTRAG_LLM_MODEL = os.getenv("LIGHTRAG_LLM_MODEL", "gemini-1.5-flash")
LIGHTRAG_EMBED_MODEL = os.getenv("LIGHTRAG_EMBED_MODEL", "gemini-embedding-001")
# gemini-embedding-001 output dimension (from LightRAG gemini.py)
GEMINI_EMBED_DIM = 1536


async def _get_rag():
    """Initialize and return LightRAG instance (singleton).

    Uses Gemini for LLM and embeddings. Returns None if GEMINI_API_KEY is not set.
    """
    global _rag
    if _rag is not None:
        return _rag
    if not GEMINI_API_KEY:
        return None
    async with _rag_lock:
        if _rag is not None:
            return _rag
        from lightrag import LightRAG, QueryParam  # noqa: F401
        from lightrag.llm.gemini import gemini_complete_if_cache, gemini_embed
        from lightrag.kg.shared_storage import initialize_pipeline_status
        from lightrag.utils import EmbeddingFunc

        os.makedirs(LIGHTRAG_WORKING_DIR, exist_ok=True)

        async def llm_model_func(
            prompt: str,
            system_prompt: str | None = None,
            history_messages: list | None = None,
            **kwargs,
        ) -> str:
            return await gemini_complete_if_cache(
                LIGHTRAG_LLM_MODEL,
                prompt,
                system_prompt=system_prompt,
                history_messages=history_messages or [],
                api_key=GEMINI_API_KEY,
                **kwargs,
            )

        rag = LightRAG(
            working_dir=LIGHTRAG_WORKING_DIR,
            llm_model_func=llm_model_func,
            embedding_func=EmbeddingFunc(
                embedding_dim=GEMINI_EMBED_DIM,
                func=gemini_embed,
            ),
        )
        await rag.initialize_storages()
        await initialize_pipeline_status()
        _rag = rag
    return _rag


async def insert(text: str, doc_name: str | None = None) -> str | None:
    """Insert text into LightRAG.

    Args:
        text: Raw text to index.
        doc_name: Optional id for the document; one is generated if not provided.

    Returns:
        doc_id string, or None if LightRAG unavailable (no API key).
    """
    rag = await _get_rag()
    if rag is None:
        return None
    import uuid
    doc_id = doc_name or str(uuid.uuid4())
    await rag.ainsert(text, ids=[doc_id])
    return doc_id


async def query(
    question: str,
    mode: Literal["naive", "local", "global", "hybrid"] = "hybrid",
    limit: int | None = None,
    only_need_context: bool = True,
) -> str:
    """Query LightRAG and return retrieved context (or full response if only_need_context=False).

    Args:
        question: Natural language question.
        mode: LightRAG query mode (naive, local, global, hybrid).
        limit: Optional top_k / chunk_top_k.
        only_need_context: If True, return only context; else full model response.

    Returns:
        Retrieved context string, or empty string if LightRAG unavailable.
    """
    rag = await _get_rag()
    if rag is None:
        return ""
    from lightrag import QueryParam
    param = QueryParam(mode=mode, only_need_context=only_need_context)
    if limit is not None:
        param.chunk_top_k = limit
        param.top_k = limit
    result = await rag.aquery(question, param=param)
    return result if isinstance(result, str) else ""
