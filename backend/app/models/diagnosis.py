from pydantic import BaseModel, Field


class Diagnosis(BaseModel):
    """AI diagnostic assessment from Senior Kubernetes SRE analysis."""

    root_cause: str = Field(..., description="Root cause of the Kubernetes failure")
    explanation: str = Field(..., description="Detailed technical explanation correlating evidence")
    fix: str = Field(..., description="Practical, beginner-friendly suggested fix")
    kubectl_command: str = Field(..., description="Actionable kubectl command to resolve the issue")
    confidence: int = Field(..., description="Confidence score percentage (0-100)")
    prevention: str | None = Field(None, description="Optional prevention recommendation")
