# 01-prompt-project-setup.md
## Context
We are building an **AI Kubernetes Troubleshooting Agent**.
Architecture:
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
This is an **on-demand troubleshooting system**.
---
## Goal
Set up the project foundation: FastAPI backend, Next.js frontend, Docker, env vars, health endpoint. Do not implement Kubernetes logic or AI yet.
