from graph.state import HospitalState

from core.ai_permissions import (
    can_access_workflow
)


def authorize_workflow(
    state: HospitalState
) -> dict:

    planner = state.get(
            "planner"
        )

    message = (
            f"You do not have permission to execute "
            f"the '{planner.target}' workflow."
        )
    
    print(f"Authorization error: {message}")

    return {

            "authorization_denied": True,

            "error": message,

            "result": {
                "success": False,
                "data": None,
            },
        }
