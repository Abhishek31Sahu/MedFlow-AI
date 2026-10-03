"""
Hospital AI Graph
"""

from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from graph.state import (
    HospitalState
)

from graph.router import (
    route
)

from graph.utils.llm import(
    llm
)

# ==========================================================
# Agents
# ==========================================================
from graph.agents.patient_search_agent import (
    patient_search_agent
)

from graph.agents.planner_agent import (
    planner_agent
)

from graph.agents.patient_agent import (
    patient_agent
)

from graph.agents.encounter_agent import (
    encounter_agent
)

from graph.agents.medication_agent import (
    medication_agent
)

from graph.agents.observation_agent import (
    observation_agent
)

from graph.agents.summary_agent import (
    summary_agent
)

from graph.agents.response_agent import (
    response_agent
)

from graph.agents.appointment_agent import (
    appointment_agent
)


# ==========================================================
# Workflows
# ==========================================================

from graph.workflows.admission.graph import (
    build_admission_graph
)

from graph.workflows.discharge.graph import (
    build_discharge_graph
)

from graph.workflows.transfer.graph import (
    build_transfer_graph
)

from graph.workflows.doctor_lab_order.graph import (
    build_doctor_lab_order_graph
)

from graph.workflows.appointment_booking.graph import (
    build_appointment_booking_graph
)

# NEW
from graph.workflows.appointment_reschedule.graph import (
    build_appointment_reschedule_graph
)

from graph.authorization import (
    authorize_workflow
)


from core.ai_permissions import (
    can_access_workflow,
    authorization_error,
)


def entry_router(state):

    active_workflow = state.get(
        "active_workflow"
    )

    workflow_status = state.get(
        "workflow_status"
    )

    user_role = state.get(
        "user_role"
    )

    if (
        active_workflow
        and workflow_status not in {
            "COMPLETED",
            "CANCELLED",
            "FAILED",
        }
    ):

        # ==============================================
        # Authorization for workflow continuation
        # ==============================================

        if not can_access_workflow(
            user_role,
            active_workflow,
        ):

            return "workflow_authorization"

        return active_workflow

    return "planner"

# ==========================================================
# Graph Builder
# ==========================================================

def build_graph():
    builder = StateGraph(HospitalState)

    builder.add_node("planner", planner_agent)
    builder.add_node("patient", patient_agent)
    builder.add_node("encounter", encounter_agent)
    builder.add_node("medication", medication_agent)
    builder.add_node("observation", observation_agent)
    builder.add_node("appointment", appointment_agent)
    builder.add_node("summary", summary_agent)
    builder.add_node(
    "workflow_authorization",
    authorize_workflow,
)   
    builder.add_node(
    "patient_search",
    patient_search_agent
)

    builder.add_node(
        "patient_admission",
        build_admission_graph().compile()
    )

    builder.add_node(
        "patient_discharge",
        build_discharge_graph().compile()
    )

    builder.add_node(
        "patient_transfer",
        build_transfer_graph().compile()
    )

    builder.add_node(
        "lab_order",
        build_doctor_lab_order_graph()
    )

    builder.add_node(
        "appointment_booking",
        build_appointment_booking_graph()
    )

    builder.add_node(
        "appointment_reschedule",
        build_appointment_reschedule_graph(llm)
    )

    builder.add_node("response", response_agent)

    # IMPORTANT:
    # Do not add entry_router as a node.
    # Do not use set_entry_point("planner").

    builder.add_conditional_edges(
        START,
        entry_router,
        {
            "planner": "planner",
            "patient_search":"patient_search",
            "patient_admission": "patient_admission",
            "patient_discharge": "patient_discharge",
            "patient_transfer": "patient_transfer",
            "lab_order": "lab_order",
            "appointment_booking": "appointment_booking",
            "appointment_reschedule": "appointment_reschedule",
            "workflow_authorization": "workflow_authorization",
        }
    )

    # Existing planner routing
    builder.add_conditional_edges(
        "planner",
        route,
        {
            "patient": "patient",
            "patient_search":"patient_search",
            "encounter": "encounter",
            "medication": "medication",
            "observation": "observation",
            "appointment": "appointment",
            "summary": "summary",
            "patient_admission": "patient_admission",
            "patient_discharge": "patient_discharge",
            "patient_transfer": "patient_transfer",
            "lab_order": "lab_order",
            "appointment_booking": "appointment_booking",
            "appointment_reschedule": "appointment_reschedule",
            "response": "response",
            "workflow_authorization": "workflow_authorization",
        }
    )

    builder.add_edge("patient", "response")
    builder.add_edge("patient_search", "response")
    builder.add_edge("encounter", "response")
    builder.add_edge("medication", "response")
    builder.add_edge("observation", "response")
    builder.add_edge("appointment", "response")
    builder.add_edge("summary", "response")
    builder.add_edge("patient_admission", "response")
    builder.add_edge("patient_discharge", "response")
    builder.add_edge("patient_transfer", "response")
    builder.add_edge("lab_order", "response")
    builder.add_edge("appointment_booking", "response")
    builder.add_edge("appointment_reschedule", "response")
    builder.add_edge("workflow_authorization", "response")
    builder.add_edge("response", END)

    return builder