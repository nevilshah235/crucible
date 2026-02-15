"""Crucible API: FastAPI app, CORS, and router registration."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import CORS_ORIGINS
from routers import admin, content, coach, curriculum, design, quiz

app = FastAPI(title="Crucible API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(content.router, prefix="/content", tags=["content"])
app.include_router(curriculum.router, prefix="/curriculum", tags=["curriculum"])
app.include_router(quiz.router, prefix="/quiz", tags=["quiz"])
app.include_router(design.router, prefix="/design", tags=["design"])
app.include_router(coach.router, prefix="/coach", tags=["coach"])


@app.get("/health")
def health():
    """Return API health status for readiness checks."""
    return {"status": "ok"}
