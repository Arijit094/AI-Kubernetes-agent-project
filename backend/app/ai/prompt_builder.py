import json
from typing import Any, Dict


class PromptBuilder:
    """Builds structured prompts for OpenRouter LLM acting as a Senior Kubernetes SRE."""

    SYSTEM_PROMPT = """You are a Senior Kubernetes SRE expert at troubleshooting cluster failures.
Your job is to analyze Kubernetes investigation evidence (Pod statuses, container logs, cluster events, deployment health, and service networking) and determine the exact root cause of failure.

You must be precise, practical, and beginner-friendly. Avoid vague advice.

You must respond ONLY with a valid JSON object matching this exact schema:
{
  "root_cause": "Concise summary of the root cause",
  "explanation": "Detailed technical explanation correlating logs, events, and pod states",
  "fix": "Actionable, step-by-step fix recommendation",
  "kubectl_command": "Specific kubectl command to fix or verify the issue",
  "confidence": 95,
  "prevention": "Best practice recommendation to prevent recurrence"
}"""

    @classmethod
    def build_user_prompt(cls, investigation_data: Dict[str, Any]) -> str:
        """Format investigation evidence into a clear prompt for the LLM."""
        evidence_str = json.dumps(investigation_data, indent=2)
        return f"""Please analyze the following Kubernetes cluster investigation evidence and provide your SRE diagnosis in JSON format:

```json
{evidence_str}
```

Remember to output strictly valid JSON conforming to the requested schema."""
