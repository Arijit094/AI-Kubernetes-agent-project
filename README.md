# AI Kubernetes Agent

On-demand Kubernetes troubleshooting with a FastAPI orchestrator and a Next.js UI.

This repository is the **project foundation only**. Kubernetes inspection and AI reasoning are placeholders and will be added later.

## Architecture

```text
Frontend → FastAPI Backend → Kubernetes Investigation → AI Agent → Diagnosis UI
```

## Project structure

```text
ai-kubernetes-agent/
├── backend/          FastAPI app (port 8000)
├── frontend/         Next.js app (port 3000)
├── docs/             Architecture notes
├── prompts/          Setup and feature prompts
├── docker-compose.yml
└── README.md
```

## Prerequisites

- Docker Desktop
- (Optional for local dev) Python 3.12+ and Node.js 20+

## Run with Docker

```bash
docker compose up --build
```

Then open:

- Frontend: http://localhost:3000
- Backend health: http://localhost:8000/health

Expected health response:

```json
{
  "status": "healthy",
  "service": "ai-kubernetes-agent"
}
```

## Environment variables

Copy the example files if you start from a clean checkout:

```bash
copy backend\.env.example backend\.env
copy frontend\.env.example frontend\.env.local
```

Backend (`backend/.env`):

```env
OPENROUTER_API_KEY=
OPENROUTER_MODEL=
KUBECONFIG_PATH=
CORS_ORIGINS=http://localhost:3000
```

Frontend (`frontend/.env.local`):

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

`OPENROUTER_*` and `KUBECONFIG_PATH` are reserved for later phases. They are not used yet.

## Local development (optional)

Backend:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## What is not implemented yet

- kubectl / cluster inspection
- AI reasoning
- OpenRouter / InsForge
- Authentication
- Realtime updates
