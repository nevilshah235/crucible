from fastapi import APIRouter

router = APIRouter()

# In-memory for MVP; no DB
_design_store: dict = {}


@router.post("/submit")
def submit_design(body: dict):
    design_text = body.get("designText", "")
    _design_store["latest"] = design_text
    return {"accepted": True, "designId": "latest"}
