import json
from pathlib import Path

from fastapi import APIRouter, HTTPException

from config import CONTENT_DIR

router = APIRouter()


def _load_json(name: str) -> dict:
    path = CONTENT_DIR / name
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Content not found: {name}")
    return json.loads(path.read_text())


@router.get("/concept")
def get_concept():
    return _load_json("concept.json")


@router.get("/quiz")
def get_quiz():
    return _load_json("quiz.json")
