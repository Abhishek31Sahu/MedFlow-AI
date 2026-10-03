"""
Planner Output
"""

from typing import Literal

from pydantic import BaseModel, Field


class PlannerOutput(BaseModel):

    mode: Literal[
        "single",
        "workflow"
    ]

    target: str

    payload: dict = Field(
        default_factory=dict
    )