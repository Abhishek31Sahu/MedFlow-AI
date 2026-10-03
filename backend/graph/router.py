from graph.state import HospitalState

from core.ai_permissions import (
    can_access_agent,
    can_access_workflow,
    authorization_error,
)


AGENT_ROUTES = {

    "patient": "patient",
    
    "patient_search":"patient_search",

    "encounter": "encounter",

    "medication": "medication",

    "observation": "observation",

    "appointment": "appointment",

    "summary": "summary",
}


WORKFLOW_ROUTES = {

    "patient_admission": "patient_admission",

    "patient_discharge": "patient_discharge",

    "patient_transfer": "patient_transfer",

    "lab_order": "lab_order",

    "appointment_booking": "appointment_booking",

    "appointment_reschedule": "appointment_reschedule",
}


def route(state: HospitalState):

    user_role = state.get(
        "user_role"
    )

    # ======================================================
    # 1. CONTINUE PENDING WORKFLOW
    # ======================================================

    active_workflow = state.get(
        "active_workflow"
    )

    workflow_status = state.get(
        "workflow_status"
    )

    if (
        active_workflow
        and workflow_status
        and workflow_status not in {
            "COMPLETED",
            "CANCELLED",
            "FAILED",
        }
    ):

        # ----------------------------------------------
        # Authorization for pending workflow
        # ----------------------------------------------

        if not can_access_workflow(
            user_role,
            active_workflow,
        ):

            authorization_error(
                state,
                (
                    f"You do not have permission to continue "
                    f"workflow '{active_workflow}'."
                ),
            )

            return "response"

        if active_workflow not in WORKFLOW_ROUTES:

            raise ValueError(
                f"Unknown Active Workflow: "
                f"{active_workflow}"
            )

        return WORKFLOW_ROUTES[
            active_workflow
        ]

    # ======================================================
    # 2. PLANNER
    # ======================================================

    planner = state.get(
        "planner"
    )

    if planner is None:

        raise ValueError(
            "Planner output is missing."
        )

    print("=" * 60)
    print("Planner Decision")
    print(planner)
    print("=" * 60)

    # ======================================================
    # 3. SINGLE AGENT
    # ======================================================

    if planner.mode == "single":

        target = planner.target

        if target not in AGENT_ROUTES:

            raise ValueError(
                f"Unknown Agent: {target}"
            )

        # ----------------------------------------------
        # Agent-level authorization
        # ----------------------------------------------

        if not can_access_agent(
            user_role,
            target,
        ):

            authorization_error(
                state,
                (
                    f"You do not have permission to use "
                    f"the '{target}' AI operation."
                ),
            )

            return "response"

        return AGENT_ROUTES[target]

    # ======================================================
    # 4. WORKFLOW
    # ======================================================

    if planner.mode == "workflow":

        target = planner.target

        if target not in WORKFLOW_ROUTES:

            raise ValueError(
                f"Unknown Workflow: {target}"
            )

        # ----------------------------------------------
        # Workflow authorization
        # ----------------------------------------------
        if not can_access_workflow(
            user_role,
            target,
        ):
            print("came here")
            return "workflow_authorization"

        return WORKFLOW_ROUTES[target]

    raise ValueError(
        f"Unknown Mode: {planner.mode}"
    )