from services.appointment_service import (
    reschedule_appointment as reschedule_service,
)


def reschedule_appointment(
    state
):
   
    if state.get("error"):
        return state

    if state.get(
        "workflow_status"
    ) != "CONFIRMED":

        return state

    try:

        updated = reschedule_service(
            
            appointment_id=state["workflow_data"][
                "appointment_id"
            ],
            new_start=state["workflow_data"][
                "new_start"
            ],
            new_end=state["workflow_data"][
                "new_end"
            ],
        )

        state["appointment"] = (
            updated
        )

        state["workflow_status"] = (
            "COMPLETED"
        )

        state["active_workflow"] = None

        state["missing_fields"] = []

        return state

    except Exception as exc:

        state["error"] = str(exc)

        return state