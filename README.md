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

Set `NEXT_PUBLIC_API_URL=http://localhost:8000` in `.env.local` (or copy from `.env.example`).

Open [http://localhost:3000](http://localhost:3000).

## Env vars

| Var | Where | Purpose |
|-----|--------|---------|
| `NEXT_PUBLIC_API_URL` | frontend | FastAPI base URL (local or Cloud Run) |
| `GEMINI_API_KEY` | backend | Google Generative AI (Gemini Flash) for Design Coach |
| `CORS_ORIGINS` | backend | Comma-separated origins (default: localhost:3000). Set to your Vercel URL when deployed. |

## Deploy

- **Frontend:** Deploy to Vercel (`frontend/` as root). Set `NEXT_PUBLIC_API_URL` to your FastAPI (Cloud Run) URL.
- **Backend:** Deploy to GCP Cloud Run (e.g. containerize with `Dockerfile` or use `gcloud run deploy`). Set `GEMINI_API_KEY` and `CORS_ORIGINS` to include your Vercel origin (e.g. `https://your-app.vercel.app`).
