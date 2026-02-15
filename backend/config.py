"""Application configuration from environment variables.

Loads .env via dotenv. Exposes DB URL, Gemini API key, LightRAG working dir,
content directory, and CORS origins. Optional: use Settings for typed access in one place.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# --- Database ---
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost:5432/crucible")

# --- LLM (Gemini) ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# --- LightRAG: working dir for local storage (vector/graph; no Milvus/Neo4j required for Phase 1) ---
LIGHTRAG_WORKING_DIR = os.getenv("LIGHTRAG_WORKING_DIR", "")
if not LIGHTRAG_WORKING_DIR:
    LIGHTRAG_WORKING_DIR = str(Path(__file__).resolve().parent.parent / "lightrag_data")

# --- Content: backend/content or repo root content/ ---
_BASE = Path(__file__).resolve().parent
CONTENT_DIR = _BASE / "content"
if not CONTENT_DIR.exists():
    CONTENT_DIR = _BASE.parent / "content"

# --- Auth (NextAuth JWT verification) ---
NEXTAUTH_SECRET = os.getenv("NEXTAUTH_SECRET", "")

# --- CORS: comma-separated origins, or default localhost for dev ---
CORS_ORIGINS_RAW = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
CORS_ORIGINS = [o.strip() for o in CORS_ORIGINS_RAW.split(",") if o.strip()]


class Settings:
    """Typed settings from environment (single place for all config).

    Use for new code; existing module-level constants remain for compatibility.
    """

    def __init__(self) -> None:
        self.database_url: str = os.getenv("DATABASE_URL", "postgresql://localhost:5432/crucible")
        self.gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
        raw_lightrag = os.getenv("LIGHTRAG_WORKING_DIR", "")
        if raw_lightrag:
            self.lightrag_working_dir: str = raw_lightrag
        else:
            self.lightrag_working_dir = str(Path(__file__).resolve().parent.parent / "lightrag_data")
        _base = Path(__file__).resolve().parent
        content_dir = _base / "content"
        self.content_dir: Path = content_dir if content_dir.exists() else _base.parent / "content"
        self.nextauth_secret: str = os.getenv("NEXTAUTH_SECRET", "")
        cors_raw = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
        self.cors_origins: list[str] = [o.strip() for o in cors_raw.split(",") if o.strip()]


# Optional: use for typed access (e.g. from config import settings).
settings = Settings()
