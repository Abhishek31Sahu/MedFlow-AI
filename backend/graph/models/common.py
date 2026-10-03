"""
Common Models
"""

from pydantic import BaseModel


class AgentDecision(BaseModel):
    """
    Output of Planner Agent
    """

    agent: str