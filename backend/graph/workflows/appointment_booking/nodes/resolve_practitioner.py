"""
Resolve Practitioner
"""

from practitioner.practitioner import (
    get_practitioner
)

from services.practitioner_service import (
    resolve_practitioner
)

from graph.workflows.appointment_booking.state import (
    AppointmentBookingState
)

from langgraph.types import interrupt


def resolve_practitioner_node(
    state
):

    print("1. Enter resolve_practitioner")

    practitioner_name = (
        state["workflow_data"]
        .get("practitioner_name")
    )

    practitioner_id = (
        state["workflow_data"]
        .get("practitioner_id")
    )

    # ======================================================
    # PRACTITIONER ID PROVIDED
    # ======================================================

    if practitioner_id:

        print(
            "2. Practitioner ID provided"
        )

        practitioner = get_practitioner(
            practitioner_id
        )

        if not practitioner:

            state["error"] = (
                "Practitioner not found"
            )

            return state

        state[
            "resolved_practitioner"
        ] = practitioner

        print(
            "3. Practitioner resolved"
        )

        return state

    # ======================================================
    # NAME NOT PROVIDED
    # ======================================================

    if not practitioner_name:

        state["error"] = (
            "Practitioner name is required"
        )

        return state

    # ======================================================
    # SEARCH
    # ======================================================

    print(
        "2. Searching practitioner:"
        f" {practitioner_name}"
    )

    result = resolve_practitioner(
        practitioner_name
    )

    print(
        "3. Search completed"
    )

    # ======================================================
    # MULTIPLE
    # ======================================================

    if result["status"] == "multiple":

        print(
            "4. Before interrupt"
        )

        selection = interrupt(
            {
                "type":
                    "practitioner_selection",

                "practitioners":
                    result["practitioners"]
            }
        )

        print(
            "5. After interrupt"
        )

        print(selection)

        practitioner = get_practitioner(
            selection["practitioner_id"]
        )

        state[
            "resolved_practitioner"
        ] = practitioner

        print(
            "6. Practitioner resolved"
        )

        return state

    # ======================================================
    # SINGLE
    # ======================================================

    elif result["status"] == "resolved":

        print(
            result
        )

        practitioner = get_practitioner(
            result["practitioner"]["id"]
        )

        state[
            "resolved_practitioner"
        ] = practitioner

        print(
            "4. Practitioner resolved"
        )

        return state

    # ======================================================
    # NOT FOUND
    # ======================================================

    else:

        state["error"] = (
            "Practitioner not found"
        )

        return state