"""
Hospital Graph State
"""

from typing import Annotated, Any, TypedDict

from langgraph.graph.message import add_messages

from graph.models.planner import PlannerOutput

from graph.models.response import ResponseOutput


class HospitalState(TypedDict):

    # Original request
    user_query: str

    # Conversation messages
    messages: Annotated[list, add_messages]

    # Planner decision
    planner: PlannerOutput | None

    # Authenticated practitioner
    practitioner_id: str | None

    # Current function
    function: str | None

    # Current operation result
    result: Any
    
    # Authentication / Authorization
    user_id: str
    user_role: str
    authorization_denied : bool

    # Workflow data
    resolved_patient: dict | None

    candidate_patients: list

    workflow_data: dict | None

    workflow_status: str | None
    
    active_workflow: str | None

    workflow_status: str | None

    missing_fields: list[str]
    # Error
    error: str | None

    # Final frontend response
    response: ResponseOutput | None
    


