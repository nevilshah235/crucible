import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
# Content dir: backend/content or repo root content/
_BASE = Path(__file__).resolve().parent
CONTENT_DIR = _BASE / "content"
if not CONTENT_DIR.exists():
    CONTENT_DIR = _BASE.parent / "content"

# CORS: comma-separated origins, or default localhost for dev
CORS_ORIGINS_RAW = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
CORS_ORIGINS = [o.strip() for o in CORS_ORIGINS_RAW.split(",") if o.strip()]
