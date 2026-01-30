import json
from pathlib import Path

from config import CONTENT_DIR


def get_failures(topic: str | None, keywords: list[str] | None = None, limit: int = 2) -> list[dict]:
    path = CONTENT_DIR / "rag" / "failures.json"
    if not path.exists():
        return []
    data = json.loads(path.read_text())
    entries = data.get("entries", [])
    if not topic and not keywords:
        return entries[:limit]
    topic_lower = (topic or "").lower()
    keywords_lower = [k.lower() for k in (keywords or [])]
    scored = []
    for e in entries:
        tags = [t.lower() for t in e.get("tags", [])]
        kws = [k.lower() for k in e.get("keywords", [])]
        score = 0
        if topic_lower and topic_lower in tags:
            score += 2
        if topic_lower and any(topic_lower in kw for kw in kws):
            score += 1
        for kw in keywords_lower:
            if kw in tags or any(kw in k for k in kws):
                score += 1
        if score > 0:
            scored.append((score, e))
    scored.sort(key=lambda x: -x[0])
    return [e for _, e in scored[:limit]]
