from pydantic import BaseModel


class Diagnosis(BaseModel):
    """Placeholder diagnosis payload shown to the frontend later."""

    root_cause: str | None = None
    suggested_fix: str | None = None
