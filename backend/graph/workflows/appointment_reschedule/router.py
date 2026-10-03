def route_after_extract(state):
    """
    Decide what to do after extracting appointment
    reschedule information.
    """

    workflow_status = state.get(
        "workflow_status"
    )

    missing_fields = state.get(
        "missing_fields",
        [],
    )

    # -----------------------------------------
    # Confirmation result
    # -----------------------------------------

    if workflow_status == "CONFIRMED":
        print(
            "RESCHEDULE ROUTER -> RESCHEDULE APPOINTMENT"
        )
        return "reschedule_appointment"

    if workflow_status == "CANCELLED":
        print(
            "RESCHEDULE ROUTER -> RESPONSE"
        )
        return "response"

    # -----------------------------------------
    # Required information is missing
    # -----------------------------------------

    if missing_fields:
        print(
            "RESCHEDULE ROUTER -> RESPONSE"
        )
        print(
            "Missing fields:",
            missing_fields,
        )

        return "response"

    # -----------------------------------------
    # All information available
    # -----------------------------------------

    print(
        "RESCHEDULE ROUTER -> RESOLVE APPOINTMENT"
    )

    return "resolve_appointment"


def route_after_confirmation(state):
    """
    Decide what to do after confirmation.
    """

    workflow_status = state.get(
        "workflow_status"
    )

    # User confirmed
    if workflow_status == "CONFIRMED":
        return "reschedule_appointment"

    # User cancelled
    if workflow_status == "CANCELLED":
        return "response"

    # Still waiting for confirmation
    return "response"