"""
Appointment Booking Workflow
"""

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from graph.workflows.appointment_booking.state import (
    AppointmentBookingState
)

from graph.workflows.appointment_booking.router import (
    route_after_patient,
    route_after_practitioner,
    route_after_availability,
    route_after_confirmation,
    route_after_creation,
)

from graph.workflows.appointment_booking.nodes.extract_input import (
    extract_input
)

from graph.workflows.appointment_booking.nodes.resolve_patient import (
    resolve_patient_node
)

from graph.workflows.appointment_booking.nodes.resolve_practitioner import (
    resolve_practitioner_node
)

from graph.workflows.appointment_booking.nodes.check_availability import (
    check_booking_availability
)

from graph.workflows.appointment_booking.nodes.confirm_booking import (
    confirm_booking
)

from graph.workflows.appointment_booking.nodes.create_appointment import (
    create_appointment
)

from graph.workflows.appointment_booking.nodes.response import (
    response
)


def build_appointment_booking_graph():

    builder = StateGraph(
        AppointmentBookingState
    )

    # ======================================================
    # Nodes
    # ======================================================

    builder.add_node(
        "extract_input",
        extract_input
    )

    builder.add_node(
        "resolve_patient",
        resolve_patient_node
    )

    builder.add_node(
        "resolve_practitioner",
        resolve_practitioner_node
    )

    builder.add_node(
        "check_availability",
        check_booking_availability
    )

    builder.add_node(
        "confirm_booking",
        confirm_booking
    )

    builder.add_node(
        "create_appointment",
        create_appointment
    )

    builder.add_node(
        "response",
        response
    )

    # ======================================================
    # Start
    # ======================================================

    builder.add_edge(
        START,
        "extract_input"
    )

    # ======================================================
    # Extract Input → Resolve Patient
    # ======================================================

    builder.add_edge(
        "extract_input",
        "resolve_patient"
    )

    # ======================================================
    # Resolve Patient
    # ======================================================

    builder.add_conditional_edges(
        "resolve_patient",
        route_after_patient,
        {
            "next":
                "resolve_practitioner",

            "response":
                "response",
        }
    )

    # ======================================================
    # Resolve Practitioner
    # ======================================================

    builder.add_conditional_edges(
        "resolve_practitioner",
        route_after_practitioner,
        {
            "next":
                "check_availability",

            "response":
                "response",
        }
    )

    # ======================================================
    # Availability
    # ======================================================

    builder.add_conditional_edges(
        "check_availability",
        route_after_availability,
        {
            "next":
                "confirm_booking",

            "response":
                "response",
        }
    )

    # ======================================================
    # Confirmation
    # ======================================================

    builder.add_conditional_edges(
        "confirm_booking",
        route_after_confirmation,
        {
            "create":
                "create_appointment",

            "response":
                "response",
        }
    )

    # ======================================================
    # Create Appointment
    # ======================================================

    builder.add_conditional_edges(
        "create_appointment",
        route_after_creation,
        {
            "response":
                "response",
        }
    )

    # ======================================================
    # End
    # ======================================================

    builder.add_edge(
        "response",
        END
    )

    return builder.compile()