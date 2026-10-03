from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from graph.workflows.appointment_reschedule.state import (
    AppointmentRescheduleState,
)

from graph.workflows.appointment_reschedule.router import (
    route_after_extract,
    route_after_confirmation,
)

from graph.workflows.appointment_reschedule.nodes.extract_input import (
    extract_input,
)

from graph.workflows.appointment_reschedule.nodes.resolve_appointment import (
    resolve_appointment,
)

from graph.workflows.appointment_reschedule.nodes.check_availability import (
    check_availability,
)

from graph.workflows.appointment_reschedule.nodes.confirm_reschedule import (
    confirm_reschedule,
)

from graph.workflows.appointment_reschedule.nodes.reschedule_appointment import (
    reschedule_appointment,
)

from graph.workflows.appointment_reschedule.nodes.response import (
    response,
)


def build_appointment_reschedule_graph(
    llm,
):
    """
    Build appointment reschedule workflow.

    Flow:

        START
          ↓
        extract_input
          ↓
        router
          ├── missing → response → END
          │
          └── complete
                ↓
        resolve_appointment
                ↓
        check_availability
                ↓
        confirm_reschedule
                ↓
        reschedule_appointment
                ↓
        response
                ↓
               END
    """

    builder = StateGraph(
        AppointmentRescheduleState
    )

    # --------------------------------------------------
    # Nodes
    # --------------------------------------------------

    builder.add_node(
        "extract_input",
        lambda state: extract_input(
            state,
            llm,
        ),
    )

    builder.add_node(
        "resolve_appointment",
        resolve_appointment,
    )

    builder.add_node(
        "check_availability",
        check_availability,
    )

    builder.add_node(
        "confirm_reschedule",
        confirm_reschedule,
    )

    builder.add_node(
        "reschedule_appointment",
        reschedule_appointment,
    )

    builder.add_node(
        "response",
        response,
    )

    # --------------------------------------------------
    # Start
    # --------------------------------------------------

    builder.add_edge(
        START,
        "extract_input",
    )

    # --------------------------------------------------
    # After extraction
    # --------------------------------------------------

    builder.add_conditional_edges(
    "extract_input",
    route_after_extract,
    {
        "response": "response",
        "resolve_appointment": "resolve_appointment",
        "reschedule_appointment": "reschedule_appointment",
    }
)

    # --------------------------------------------------
    # Main workflow
    # --------------------------------------------------

    builder.add_edge(
        "resolve_appointment",
        "check_availability",
    )

    builder.add_edge(
        "check_availability",
        "confirm_reschedule",
    )

    # --------------------------------------------------
    # Confirmation
    # --------------------------------------------------

    builder.add_conditional_edges(
        "confirm_reschedule",
        route_after_confirmation,
        {
            "reschedule_appointment":
                "reschedule_appointment",

            "response":
                "response",
        },
    )

    # --------------------------------------------------
    # Final mutation
    # --------------------------------------------------

    builder.add_edge(
        "reschedule_appointment",
        "response",
    )

    # --------------------------------------------------
    # End
    # --------------------------------------------------

    builder.add_edge(
        "response",
        END,
    )

    return builder.compile()