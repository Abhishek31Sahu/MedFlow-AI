def response(state):

    workflow_data = state.get(
        "workflow_data",
        {}
    )

    appointment_id = (
        state.get("appointment_id")
        or workflow_data.get("appointment_id")
    )

    if state.get("error"):
        return {
            "result": {
                "success": False,
                "title": "Appointment Rescheduling Failed",
                "message": state["error"],
            }
        }

    if not appointment_id:
        return {
            "result": {
                "success": False,
                "title": "Appointment Rescheduling Failed",
                "message": (
                    "Appointment ID is missing."
                ),
            }
        }

    return {
        "result": {
            "success": True,
            "title": "Appointment Rescheduled",
            "message": (
                f"Appointment {appointment_id} "
                f"has been successfully rescheduled."
            ),
        }
    }