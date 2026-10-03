def confirm_reschedule(state):
    """
    Prepare confirmation before changing the appointment.

    This node does NOT modify the appointment.

    Flow:

        availability
            ↓
        confirm_reschedule
            ↓
        WAITING_FOR_CONFIRMATION
            ↓
        response
            ↓
        END

    On the next chat message:
        "Yes" / "No"

    extract_input() handles the confirmation and
    updates workflow_status.
    """

    workflow_data = state.get(
        "workflow_data",
        {},
    )

    availability = state.get(
        "availability",
    )

    current_status = state.get(
        "workflow_status"
    )

    # ==================================================
    # USER ALREADY CONFIRMED
    # ==================================================

    if current_status == "CONFIRMED":

        return {
            "workflow_status": "CONFIRMED",
            "active_workflow": (
                "appointment_reschedule"
            ),
            "missing_fields": [],
            "result": None,
        }

    # ==================================================
    # AVAILABILITY RESULT MISSING
    # ==================================================

    if not availability:

        return {
            "workflow_status": "ERROR",
            "active_workflow": (
                "appointment_reschedule"
            ),
            "result": {
                "success": False,
                "title": "Availability Error",
                "message": (
                    "I could not verify the "
                    "availability of the requested "
                    "appointment slot."
                ),
            },
        }

    # ==================================================
    # SLOT NOT AVAILABLE
    # ==================================================

    if not availability.get("available"):

        reason = availability.get(
            "reason",
            "The requested time is not available.",
        )

        return {
            "workflow_status": (
                "SLOT_UNAVAILABLE"
            ),
            "active_workflow": (
                "appointment_reschedule"
            ),
            "result": {
                "success": False,
                "title": "Slot Not Available",
                "message": reason,
            },
        }

    # ==================================================
    # GET REQUESTED SLOT
    # ==================================================

    appointment_id = workflow_data.get(
        "appointment_id"
    )

    date = workflow_data.get(
        "date"
    )

    start_time = workflow_data.get(
        "start_time"
    )

    end_time = workflow_data.get(
        "end_time"
    )

    # ==================================================
    # BUILD CONFIRMATION MESSAGE
    # ==================================================

    if end_time:

        time_text = (
            f"{start_time} - {end_time}"
        )

    else:

        time_text = start_time

    message = (
        f"Appointment {appointment_id} "
        f"is available for {date} at "
        f"{time_text}. "
        f"Would you like to confirm "
        f"the reschedule?"
    )

    # ==================================================
    # WAIT FOR USER CONFIRMATION
    # ==================================================

    return {
        "active_workflow": (
            "appointment_reschedule"
        ),
        "workflow_status": (
            "WAITING_FOR_CONFIRMATION"
        ),
        "missing_fields": [],
        "result": {
            "success": True,
            "title": "Confirm Reschedule",
            "message": message,
        },
    }