import json
from typing import Any, Dict
from loguru import logger
from app.ai.prompt_builder import PromptBuilder
from app.ai.client import OpenRouterClient
from app.models.diagnosis import Diagnosis


class AIAgent:
    """AI Kubernetes SRE reasoning agent."""

    @classmethod
    def analyze(cls, investigation_data: Dict[str, Any]) -> Diagnosis:
        """Analyze investigation evidence using OpenRouter LLM or intelligent fallback."""
        system_prompt = PromptBuilder.SYSTEM_PROMPT
        user_prompt = PromptBuilder.build_user_prompt(investigation_data)

        try:
            raw_content = OpenRouterClient.call(system_prompt, user_prompt)
            parsed = json.loads(raw_content)
            
            return Diagnosis(
                root_cause=parsed.get("root_cause", "Cluster investigation completed"),
                explanation=parsed.get("explanation", "Analyzed cluster telemetry and states."),
                fix=parsed.get("fix", "Inspect cluster resources for anomalies."),
                kubectl_command=parsed.get("kubectl_command", "kubectl get pods -A"),
                confidence=int(parsed.get("confidence", 90)),
                prevention=parsed.get("prevention", "Maintain regular health checks and monitoring."),
            )
        except Exception as e:
            logger.warning("AI reasoning fallback triggered due to error: {}", e)
            return cls._generate_fallback_diagnosis(investigation_data)

    @classmethod
    def _generate_fallback_diagnosis(cls, investigation_data: Dict[str, Any]) -> Diagnosis:
        """Generate an intelligent heuristic diagnosis based on evidence when LLM is unavailable."""
        pods = investigation_data.get("pods", {})
        problematic_pods = pods.get("problematic_pods", [])
        events = investigation_data.get("events", {})
        warning_events = events.get("warning_events", [])
        deployments = investigation_data.get("deployments", {})
        unhealthy_deps = deployments.get("unhealthy_deployments", [])

        if problematic_pods:
            pod = problematic_pods[0]
            name = pod.get("name", "unknown-pod")
            ns = pod.get("namespace", "default")
            status = pod.get("status", "Unknown")
            msg = pod.get("message", "")

            if status == "CrashLoopBackOff":
                return Diagnosis(
                    root_cause=f"Pod '{name}' in namespace '{ns}' is in CrashLoopBackOff",
                    explanation=f"Container failed during startup or runtime repeatedly. Details: {msg or 'Check logs for exceptions or missing env vars.'}",
                    fix="Inspect pod container logs and verify configuration or environment variables.",
                    kubectl_command=f"kubectl logs {name} -n {ns} --tail=100",
                    confidence=92,
                    prevention="Add liveness/readiness probes and validate startup configuration before deployment.",
                )
            elif status in {"ImagePullBackOff", "ErrImagePull"}:
                return Diagnosis(
                    root_cause=f"Image pull failure for pod '{name}' in namespace '{ns}'",
                    explanation=f"Kubernetes failed to pull the container image. Details: {msg or 'Check image tag, registry credentials, or network access.'}",
                    fix="Verify container image name, tag, and image pull secrets.",
                    kubectl_command=f"kubectl describe pod {name} -n {ns}",
                    confidence=95,
                    prevention="Ensure image registry authentication secrets are correctly configured.",
                )
            else:
                return Diagnosis(
                    root_cause=f"Pod '{name}' in namespace '{ns}' is unhealthy (Status: {status})",
                    explanation=f"Pod encountered an issue: {msg or status}",
                    fix="Review pod description and events for failure reasons.",
                    kubectl_command=f"kubectl describe pod {name} -n {ns}",
                    confidence=85,
                    prevention="Monitor pod resource limits and health checks.",
                )

        if unhealthy_deps:
            dep = unhealthy_deps[0]
            name = dep.get("name", "unknown-deployment")
            ns = dep.get("namespace", "default")
            reasons = dep.get("reasons", ["Replica mismatch"])
            return Diagnosis(
                root_cause=f"Deployment '{name}' in namespace '{ns}' has rollout or replica issues",
                explanation=f"Deployment health check failed: {'; '.join(reasons)}",
                fix="Check deployment rollout status and describe deployment for replica details.",
                kubectl_command=f"kubectl rollout status deployment/{name} -n {ns}",
                confidence=90,
                prevention="Review HPA limits and resource availability in cluster nodes.",
            )

        if warning_events:
            event = warning_events[0]
            reason = event.get("reason", "Warning")
            msg = event.get("message", "Cluster warning event detected")
            return Diagnosis(
                root_cause=f"Cluster warning event detected: {reason}",
                explanation=f"Kubernetes reported a warning event: {msg}",
                fix="Inspect cluster events for resource scheduling or mounting bottlenecks.",
                kubectl_command="kubectl get events -A --sort-by='.metadata.creationTimestamp'",
                confidence=80,
                prevention="Ensure adequate node capacity and persistent volume storage.",
            )

        return Diagnosis(
            root_cause="Cluster is currently healthy with no active pod or deployment anomalies",
            explanation="All inspected pods, deployments, services, and events reported normal operational status.",
            fix="No action required. Cluster is operating normally.",
            kubectl_command="kubectl get pods -A",
            confidence=98,
            prevention="Continue standard monitoring and alerting practices.",
        )
