from typing import Literal

from pydantic import BaseModel


class WorkflowPlannerOutput(BaseModel):

    mode: Literal[
        "single",
        "workflow"
    ]

    workflow: str | None = None

    agent: str | None = None

    payload: dict = {}