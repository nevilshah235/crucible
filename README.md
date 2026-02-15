# Crucible

One full learning loop: concept → quiz → design → Socratic coach feedback → RAG pressure test.

## Run locally

### Backend (FastAPI)

Install [uv](https://docs.astral.sh/uv/) once (e.g. `curl -LsSf https://astral.sh/uv/install.sh | sh` or `brew install uv`).

```bash
cd backend
uv sync
uv run uvicorn main:app --reload --port 8000
```

Or activate `.venv` and run `uvicorn main:app --reload --port 8000` yourself. Dependencies are managed by uv (`pyproject.toml` + `uv.lock`); use `uv add <package>` to add dependencies.

Set `GEMINI_API_KEY` in `.env` or environment.

### Frontend (Next.js)

```bash
cd frontend
npm install
npm run dev
```

Set `NEXT_PUBLIC_API_URL=http://localhost:8000` in `.env.local`. For Google sign-in (Phase S0), copy `frontend/.env.local.example` to `frontend/.env.local` and set `NEXTAUTH_SECRET`, `NEXTAUTH_URL`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`. Use the same `NEXTAUTH_SECRET` in `backend/.env` so the API can verify JWTs.

Open [http://localhost:3000](http://localhost:3000).

## Phase 1: DB and LightRAG (Google-only)

Backend uses **PostgreSQL** for curriculum (concepts, quizzes, failure_facts, drafts, ingested_docs) and **LightRAG with Gemini** for ingestion and retrieval (no OpenAI).

1. **Database**: Create a DB and set `DATABASE_URL` in `.env` (e.g. `postgresql://user:pass@localhost:5432/crucible`).
2. **Migrations**: From `backend/`: `uv run alembic upgrade head`.
3. **Seed** (one-time): `uv run python scripts/seed_from_json.py` to load `content/concept.json`, `quiz.json`, `rag/failures.json` into the DB.
4. **LightRAG**: Uses `GEMINI_API_KEY` for both LLM and embeddings. Optional `LIGHTRAG_WORKING_DIR` (default: repo `lightrag_data/`).

**Admin UI**: Open [http://localhost:3000/admin](http://localhost:3000/admin) to ingest sources (PDF/URLs), generate curriculum from LightRAG+Gemini, and publish drafts to the learner app. Learner app: [http://localhost:3000](http://localhost:3000) (link to Admin in header).

**Content**: `GET /content/concept`, `GET /content/quiz` (first concept/quiz from DB); `GET /content/concept/:id`, `GET /content/quiz/:conceptId`; `GET /curriculum/roadmap`, `GET /curriculum/me` (progress).

## Env vars

| Var | Where | Purpose |
|-----|--------|---------|
| `NEXT_PUBLIC_API_URL` | frontend | FastAPI base URL (local or Cloud Run) |
| `NEXTAUTH_SECRET` | frontend + backend | Same value in both; backend verifies JWT. At least 32 chars. |
| `NEXTAUTH_URL` | frontend | App URL (e.g. `http://localhost:3000`) |
| `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` | frontend | Google OAuth (Phase S0 sign-in) |
| `GEMINI_API_KEY` | backend | Gemini for Coach, LightRAG (LLM + embeddings), curriculum generation |
| `DATABASE_URL` | backend | PostgreSQL connection string |
| `LIGHTRAG_WORKING_DIR` | backend | Optional; default repo `lightrag_data/` |
| `CORS_ORIGINS` | backend | Comma-separated origins (default: localhost:3000). Set to your Vercel URL when deployed. |

## Backend code style

Backend uses **Google-style docstrings** and a thin layered structure (routers → services → repositories). See [backend/docs/code_style.md](backend/docs/code_style.md) for docstring and style conventions.

## Deploy

- **Frontend:** Deploy to Vercel (`frontend/` as root). Set `NEXT_PUBLIC_API_URL` to your FastAPI (Cloud Run) URL.
- **Backend:** Deploy to GCP Cloud Run (e.g. containerize with `Dockerfile` or use `gcloud run deploy`). Set `GEMINI_API_KEY` and `CORS_ORIGINS` to include your Vercel origin (e.g. `https://your-app.vercel.app`).
