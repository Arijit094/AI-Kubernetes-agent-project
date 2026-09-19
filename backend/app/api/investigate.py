from fastapi import APIRouter
from loguru import logger
from app.services.investigation import InvestigationService

router = APIRouter(tags=["investigation"])


@router.post("/investigate")
def investigate_cluster() -> dict[str, any]:
    """Trigger Kubernetes cluster investigation and return troubleshooting evidence."""
    logger.info("Received POST /investigate request")
    investigation_data = InvestigationService.investigate()
    return {
        "status": "success",
        "investigation": investigation_data,
    }
