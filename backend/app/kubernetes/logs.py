from typing import Any, Dict, List
from loguru import logger
from app.kubernetes.executor import KubectlExecutor


class LogsCollector:
    """Collects logs and failures for problematic pods."""

    KEYWORDS = [
        "exception",
        "error",
        "fail",
        "connection",
        "refused",
        "timeout",
        "missing",
        "env",
        "image",
        "crash",
        "fatal",
        "panic",
    ]

    @classmethod
    def collect_for_pods(cls, problematic_pods: List[Dict[str, Any]], tail_lines: int = 50) -> Dict[str, Any]:
        """Fetch and filter logs for the given list of problematic pods."""
        logger.info("Collecting logs for {} problematic pods", len(problematic_pods))
        logs_summary: Dict[str, Any] = {}

        for pod in problematic_pods:
            name = pod.get("name")
            namespace = pod.get("namespace", "default")
            if not name:
                continue

            key = f"{namespace}/{name}"
            logger.debug("Fetching logs for pod {}", key)

            # Try fetching logs, including previous container instance if it crashed
            res = KubectlExecutor.run(["logs", name, "-n", namespace, f"--tail={tail_lines}"])
            logs_content = res["stdout"]

            if not logs_content.strip() and res["stderr"]:
                logs_content = f"Error fetching logs: {res['stderr'].strip()}"

            # Filter or extract relevant lines if logs are long
            lines = logs_content.splitlines()
            filtered_lines = []
            for line in lines:
                lower_line = line.lower()
                if any(kw in lower_line for kw in cls.KEYWORDS):
                    filtered_lines.append(line)

            # If no keyword matches found but logs exist, keep last 15 lines so we have context
            if not filtered_lines and lines:
                filtered_lines = lines[-15:]

            logs_summary[key] = {
                "pod": name,
                "namespace": namespace,
                "raw_tail_count": len(lines),
                "relevant_logs": filtered_lines if filtered_lines else lines,
            }

        return logs_summary
