from langgraph.graph import START, END, StateGraph

from graph.workflows.doctor_lab_order.router import workflow_router

from graph.workflows.doctor_lab_order.state import DoctorLabOrderState

from graph.workflows.doctor_lab_order.nodes.extract_lab_order import (
    extract_lab_order,
)
from graph.workflows.doctor_lab_order.nodes.resolve_patient import (
    resolve_patient_node,
)
from graph.workflows.doctor_lab_order.nodes.validate_patient import (
    validate_patient,
)
from graph.workflows.doctor_lab_order.nodes.create_lab_order import (
    create_lab_order,
)
from graph.workflows.doctor_lab_order.nodes.response import (
    response,
)


def build_doctor_lab_order_graph():

    builder = StateGraph(DoctorLabOrderState)

    # ----------------------------------------------------
    # Nodes
    # ----------------------------------------------------

    builder.add_node("extract_lab_order", extract_lab_order)
    builder.add_node("resolve_patient", resolve_patient_node)
    builder.add_node("validate_patient", validate_patient)
    builder.add_node("create_lab_order", create_lab_order)
    builder.add_node("response", response)

    # ----------------------------------------------------
    # Start
    # ----------------------------------------------------

    builder.add_edge(START, "extract_lab_order")

    # ----------------------------------------------------
    # Extract -> Resolve Patient
    # ----------------------------------------------------

    builder.add_edge(
        "extract_lab_order",
        "resolve_patient",
    )

    # ----------------------------------------------------
    # Resolve Patient
    # ----------------------------------------------------

    builder.add_conditional_edges(
        "resolve_patient",
        workflow_router,
        {
            "next": "validate_patient",
            "response": "response",
        },
    )

    # ----------------------------------------------------
    # Validate Patient
    # ----------------------------------------------------

    builder.add_conditional_edges(
        "validate_patient",
        workflow_router,
        {
            "next": "create_lab_order",
            "response": "response",
        },
    )

    # ----------------------------------------------------
    # Create Lab Order
    # ----------------------------------------------------

    builder.add_conditional_edges(
        "create_lab_order",
        workflow_router,
        {
            "next": "response",
            "response": "response",
        },
    )

    # ----------------------------------------------------
    # End
    # ----------------------------------------------------

    builder.add_edge(
        "response",
        END,
    )

    return builder.compile()