from typing import Any, Dict
from loguru import logger
from app.kubernetes import (
    PodInspector,
    LogsCollector,
    EventsAnalyzer,
    DeploymentInspector,
    NetworkInspector,
)


class InvestigationService:
    """Orchestrates Kubernetes evidence gathering (Pods, Logs, Events, Deployments, Network)."""

    @classmethod
    def investigate(cls) -> Dict[str, Any]:
        """Run full cluster investigation and return structured evidence."""
        logger.info("Starting cluster investigation orchestrator...")

        # 1. Check Pods
        pods_evidence = PodInspector.inspect()

        # 2. Collect Logs for problematic pods
        problematic_pods = pods_evidence.get("problematic_pods", [])
        logs_evidence = LogsCollector.collect_for_pods(problematic_pods)

        # 3. Analyze Events
        events_evidence = EventsAnalyzer.analyze()

        # 4. Inspect Deployments
        deployments_evidence = DeploymentInspector.inspect()

        # 5. Check Networking
        network_evidence = NetworkInspector.inspect()

        investigation_result = {
            "pods": pods_evidence,
            "logs": logs_evidence,
            "events": events_evidence,
            "deployments": deployments_evidence,
            "network": network_evidence,
        }

        logger.info("Cluster investigation completed successfully.")
        return investigation_result
