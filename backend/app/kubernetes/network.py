from typing import Any, Dict, List
from loguru import logger
from app.kubernetes.executor import KubectlExecutor


class NetworkInspector:
    """Inspects Kubernetes services and endpoints for missing endpoints or misconfigurations."""

    @classmethod
    def inspect(cls) -> Dict[str, Any]:
        """Inspect services and their corresponding endpoints across namespaces."""
        logger.info("Inspecting Kubernetes networking (services and endpoints)")
        
        svc_data = KubectlExecutor.run_json(["get", "services", "-A"])
        ep_data = KubectlExecutor.run_json(["get", "endpoints", "-A"])

        services = svc_data.get("items", []) if svc_data else []
        endpoints_items = ep_data.get("items", []) if ep_data else []

        # Map endpoints by namespace/name for quick lookup
        ep_map: Dict[str, bool] = {}
        for ep in endpoints_items:
            ns = ep.get("metadata", {}).get("namespace", "default")
            name = ep.get("metadata", {}).get("name", "unknown")
            subsets = ep.get("subsets", [])
            has_addresses = any(sub.get("addresses") for sub in subsets)
            ep_map[f"{ns}/{name}"] = has_addresses

        total_services = len(services)
        services_without_endpoints: List[Dict[str, Any]] = []

        for svc in services:
            metadata = svc.get("metadata", {})
            spec = svc.get("spec", {})
            
            name = metadata.get("name", "unknown")
            namespace = metadata.get("namespace", "default")
            svc_type = spec.get("type", "ClusterIP")
            selector = spec.get("selector")

            # ExternalName or headless services without selectors might not need endpoints
            if svc_type == "ExternalName" or not selector:
                continue

            key = f"{namespace}/{name}"
            has_ep = ep_map.get(key, False)

            if not has_ep:
                services_without_endpoints.append({
                    "name": name,
                    "namespace": namespace,
                    "type": svc_type,
                    "selector": selector,
                    "issue": "Service has selector but zero active endpoints (possible selector mismatch or backing pods not running)",
                })

        healthy = len(services_without_endpoints) == 0
        logger.info(
            "Network inspection complete. Total services: {}, Services without endpoints: {}",
            total_services,
            len(services_without_endpoints),
        )

        return {
            "healthy": healthy,
            "total_services": total_services,
            "services_without_endpoints": services_without_endpoints,
        }
