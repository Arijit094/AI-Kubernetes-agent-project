from typing import Any, Dict, List
from loguru import logger
from app.kubernetes.executor import KubectlExecutor


class EventsAnalyzer:
    """Analyzes Kubernetes cluster events for warning and error conditions."""

    WARNING_REASONS = {
        "FailedScheduling",
        "BackOff",
        "FailedMount",
        "FailedPull",
        "ErrImagePull",
        "Unhealthy",
        "FailedCreate",
        "Killing",
        "Failed",
    }

    @classmethod
    def analyze(cls) -> Dict[str, Any]:
        """Fetch all cluster events and filter for warnings or failures."""
        logger.info("Analyzing cluster events across all namespaces")
        data = KubectlExecutor.run_json(["get", "events", "-A"])

        if not data or "items" not in data:
            return {
                "total_events": 0,
                "warning_events": [],
                "message": "No events found or cluster unreachable.",
            }

        items = data.get("items", [])
        warning_events: List[Dict[str, Any]] = []

        for event in items:
            type_str = event.get("type", "Normal")
            reason = event.get("reason", "")
            message = event.get("message", "")
            involved_obj = event.get("involvedObject", {})
            obj_name = involved_obj.get("name", "unknown")
            obj_kind = involved_obj.get("kind", "unknown")
            namespace = involved_obj.get("namespace", "default")
            count = event.get("count", 1)
            last_timestamp = event.get("lastTimestamp") or event.get("eventTime") or "unknown"

            if type_str == "Warning" or reason in cls.WARNING_REASONS:
                warning_events.append({
                    "namespace": namespace,
                    "kind": obj_kind,
                    "name": obj_name,
                    "reason": reason,
                    "message": message,
                    "count": count,
                    "last_timestamp": last_timestamp,
                })

        # Sort or limit warning events to recent/relevant ones
        logger.info("Event analysis complete. Total events: {}, Warnings: {}", len(items), len(warning_events))

        return {
            "total_events": len(items),
            "warning_events": warning_events[:50],  # Limit to top 50 warnings to keep payload clean
        }
