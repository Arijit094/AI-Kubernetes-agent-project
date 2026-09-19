from fastapi import APIRouter
from loguru import logger
from app.services.investigation import InvestigationService

router = APIRouter(tags=["investigation"])


@router.post("/investigate")
def investigate_cluster() -> dict[str, any]:
    """Trigger Kubernetes cluster investigation and AI diagnosis."""
    logger.info("Received POST /investigate request")
    result = InvestigationService.investigate()
    return {
        "status": "success",
        "investigation": result["investigation"],
        "diagnosis": result["diagnosis"],
    }
