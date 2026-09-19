from typing import Any, Dict, List
from loguru import logger
from app.kubernetes.executor import KubectlExecutor


class PodInspector:
    """Inspects Kubernetes pods across namespaces for health issues."""

    UNHEALTHY_STATUSES = {
        "CrashLoopBackOff",
        "ImagePullBackOff",
        "ErrImagePull",
        "Pending",
        "Error",
        "OOMKilled",
        "ContainerCreating",
        "Terminating",
        "CreateContainerConfigError",
        "InvalidImageName",
    }

    @classmethod
    def inspect(cls) -> Dict[str, Any]:
        """Inspect all pods in all namespaces and identify problematic ones."""
        logger.info("Inspecting Kubernetes pods across all namespaces")
        data = KubectlExecutor.run_json(["get", "pods", "-A"])

        if not data or "items" not in data:
            # Fallback or empty result if cluster is unreachable or no pods exist
            return {
                "healthy": True,
                "total_pods": 0,
                "problematic_pods": [],
                "message": "Unable to retrieve pods or cluster is empty/unreachable.",
            }

        items = data.get("items", [])
        total_pods = len(items)
        problematic_pods: List[Dict[str, Any]] = []

        for pod in items:
            metadata = pod.get("metadata", {})
            status_obj = pod.get("status", {})
            
            name = metadata.get("name", "unknown")
            namespace = metadata.get("namespace", "default")
            phase = status_obj.get("phase", "Unknown")
            
            container_statuses = status_obj.get("containerStatuses", [])
            init_container_statuses = status_obj.get("initContainerStatuses", [])
            all_statuses = container_statuses + init_container_statuses

            pod_status_str = phase
            is_unhealthy = phase in {"Failed", "Unknown"}
            reason_detail = ""

            for cs in all_statuses:
                state = cs.get("state", {})
                waiting = state.get("waiting", {})
                terminated = state.get("terminated", {})

                if waiting:
                    reason = waiting.get("reason", "")
                    pod_status_str = reason
                    if reason in cls.UNHEALTHY_STATUSES or phase == "Pending":
                        is_unhealthy = True
                        reason_detail = waiting.get("message", reason)
                elif terminated:
                    reason = terminated.get("reason", "")
                    exit_code = terminated.get("exitCode", 0)
                    if reason != "Completed" and exit_code != 0:
                        pod_status_str = reason
                        is_unhealthy = True
                        reason_detail = terminated.get("message", f"Exit code {exit_code}")

            if not is_unhealthy and phase == "Pending":
                is_unhealthy = True
                pod_status_str = "Pending"

            if is_unhealthy:
                problematic_pods.append({
                    "name": name,
                    "namespace": namespace,
                    "status": pod_status_str,
                    "phase": phase,
                    "message": reason_detail,
                })

        healthy = len(problematic_pods) == 0
        logger.info(
            "Pod inspection complete. Total pods: {}, Problematic pods: {}",
            total_pods,
            len(problematic_pods),
        )

        return {
            "healthy": healthy,
            "total_pods": total_pods,
            "problematic_pods": problematic_pods,
        }
