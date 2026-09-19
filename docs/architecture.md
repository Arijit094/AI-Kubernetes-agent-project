# Architecture

On-demand troubleshooting flow (not a Kubernetes controller/operator):

```text
Frontend
    ↓
FastAPI Backend (Orchestrator)
    ↓
Kubernetes Investigation Layer
    ↓
AI Kubernetes Agent
    ↓
LLM Reasoning (OpenRouter via InsForge)
    ↓
Root Cause + Suggested Fix
    ↓
Frontend Diagnosis
```

This phase only scaffolds the FastAPI backend, Next.js frontend, Docker, and health checks.
Kubernetes inspection and AI reasoning are placeholders for later prompts.
