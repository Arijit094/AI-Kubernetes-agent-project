from typing import Any, Dict, List
from loguru import logger
from app.kubernetes.executor import KubectlExecutor


class DeploymentInspector:
    """Inspects Kubernetes deployments for replica mismatches and rollout issues."""

    @classmethod
    def inspect(cls) -> Dict[str, Any]:
        """Inspect all deployments across namespaces."""
        logger.info("Inspecting Kubernetes deployments across all namespaces")
        data = KubectlExecutor.run_json(["get", "deployments", "-A"])

        if not data or "items" not in data:
            return {
                "healthy": True,
                "total_deployments": 0,
                "unhealthy_deployments": [],
                "message": "No deployments found or cluster unreachable.",
            }

        items = data.get("items", [])
        total_deployments = len(items)
        unhealthy_deployments: List[Dict[str, Any]] = []

        for dep in items:
            metadata = dep.get("metadata", {})
            spec = dep.get("spec", {})
            status = dep.get("status", {})

            name = metadata.get("name", "unknown")
            namespace = metadata.get("namespace", "default")
            replicas = spec.get("replicas", 1)
            
            available_replicas = status.get("availableReplicas", 0)
            unavailable_replicas = status.get("unavailableReplicas", 0)
            updated_replicas = status.get("updatedReplicas", 0)

            is_unhealthy = False
            reasons = []

            if available_replicas < replicas:
                is_unhealthy = True
                reasons.append(f"Available replicas ({available_replicas}) less than desired ({replicas})")

            if unavailable_replicas > 0:
                is_unhealthy = True
                reasons.append(f"Unavailable replicas: {unavailable_replicas}")

            # Check deployment conditions for ProgressDeadlineExceeded or ReplicaFailure
            conditions = status.get("conditions", [])
            for cond in conditions:
                cond_type = cond.get("type")
                cond_status = cond.get("status")
                cond_reason = cond.get("reason")
                if cond_type == "Progressing" and cond_status == "False":
                    is_unhealthy = True
                    reasons.append(f"Progressing=False: {cond.get('message', cond_reason)}")
                elif cond_type == "Available" and cond_status == "False":
                    is_unhealthy = True
                    reasons.append(f"Available=False: {cond.get('message', cond_reason)}")

            if is_unhealthy:
                unhealthy_deployments.append({
                    "name": name,
                    "namespace": namespace,
                    "desired_replicas": replicas,
                    "available_replicas": available_replicas,
                    "unavailable_replicas": unavailable_replicas,
                    "reasons": reasons,
                })

        healthy = len(unhealthy_deployments) == 0
        logger.info(
            "Deployment inspection complete. Total: {}, Unhealthy: {}",
            total_deployments,
            len(unhealthy_deployments),
        )

        return {
            "healthy": healthy,
            "total_deployments": total_deployments,
            "unhealthy_deployments": unhealthy_deployments,
        }
