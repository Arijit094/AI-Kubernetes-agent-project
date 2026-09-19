from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.api.health import router as health_router
from app.api.investigate import router as investigate_router
from app.core.config import get_settings
from app.core.logging import configure_logging


@asynccontextmanager
async def lifespan(_app: FastAPI):
    configure_logging()
    settings = get_settings()
    logger.info("Starting AI Kubernetes Agent backend")
    logger.info("Kubeconfig path configured: {}", bool(settings.kubeconfig_path))
    yield
    logger.info("Shutting down AI Kubernetes Agent backend")


def create_app() -> FastAPI:
    settings = get_settings()
    origins = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]

    application = FastAPI(
        title="AI Kubernetes Agent",
        description="On-demand Kubernetes troubleshooting orchestrator.",
        version="0.1.0",
        lifespan=lifespan,
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(health_router)
    application.include_router(investigate_router)
    return application


app = create_app()
