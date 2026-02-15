"""Design API: submit learner design (in-memory store for MVP)."""

from typing import Annotated

from fastapi import APIRouter, Depends, Header

from auth_deps import get_optional_user_id

router = APIRouter()

# In-memory for MVP; keyed by user_id or session_id (Phase S0)
_design_store: dict = {}


def _design_key(
    user_id: Annotated[str | None, Depends(get_optional_user_id)] = None,
    x_session_id: str | None = Header(None, alias="X-Session-Id"),
) -> str:
    """Resolve store key: prefer user_id when authenticated, else session_id, else 'anonymous'."""
    if user_id:
        return f"user:{user_id}"
    if x_session_id:
        return f"session:{x_session_id}"
    return "anonymous"


@router.post("/submit")
def submit_design(
    body: dict,
    store_key: Annotated[str, Depends(_design_key)],
):
    """Accept design text (and optional pipeline) and store; return acceptance and designId."""
    design_text = body.get("designText", "")
    pipeline = body.get("pipeline")
    _design_store[store_key] = {"designText": design_text, "pipeline": pipeline}
    return {"accepted": True, "designId": store_key}
