from datetime import datetime
from database.database import (
    SessionLocal
)
from appointment.appointment import (
    get_practitioner_id_from_appointment,
    get_patient_id_from_appointment,
    get_patient_appointments_between,
)

from services.appointment_service import (
    check_availability as check_slot_availability,
)

from graph.utils.date_time import (
    make_datetime,
)



def check_availability(
    state
):
    
    db = SessionLocal()

    if state.get("error"):
        return state

    appointment = state[
        "appointment"
    ]

    workflow_data = state[
        "workflow_data"
    ]

    appointment_id = state[
        "appointment_id"
    ]

    # ---------------------------------------
    # Existing duration
    # ---------------------------------------

    old_start = appointment.get(
        "start"
    )

    old_end = appointment.get(
        "end"
    )

    if not old_start or not old_end:

        state["error"] = (
            "Existing appointment does "
            "not contain valid start/end times."
        )

        return state

    old_start_dt = datetime.fromisoformat(
        old_start.replace(
            "Z",
            "+00:00",
        )
    )

    old_end_dt = datetime.fromisoformat(
        old_end.replace(
            "Z",
            "+00:00",
        )
    )

    duration = (
        old_end_dt - old_start_dt
    )

    # ---------------------------------------
    # New start
    # ---------------------------------------

    new_start = make_datetime(
        workflow_data["date"],
        workflow_data["start_time"],
    )

    # ---------------------------------------
    # New end
    # ---------------------------------------

    if workflow_data.get(
        "end_time"
    ):

        new_end = make_datetime(
            workflow_data["date"],
            workflow_data["end_time"],
        )

    else:

        new_start_dt = (
            datetime.fromisoformat(
                new_start
            )
        )

        new_end = (
            new_start_dt + duration
        ).strftime(
            "%Y-%m-%dT%H:%M:%S"
        )

    practitioner_id = (
        get_practitioner_id_from_appointment(
            appointment
        )
    )

    patient_id = (
        get_patient_id_from_appointment(
            appointment
        )
    )

    if not practitioner_id:

        state["error"] = (
            "Could not determine the "
            "practitioner for this appointment."
        )

        return state

    # ---------------------------------------
    # Practitioner availability
    # ---------------------------------------

    availability = (
        check_slot_availability(
            db=db,
            practitioner_id=practitioner_id,
            start=new_start,
            end=new_end,
            exclude_appointment_id=(
                appointment_id
            ),
        )
    )

    if not availability["available"]:

        state["availability"] = (
            availability
        )

        state["error"] = (
            availability["reason"]
        )

        return state

    # ---------------------------------------
    # Patient conflict
    # ---------------------------------------

    if patient_id:

        conflicts = (
            get_patient_appointments_between(
                patient_id=patient_id,
                start=new_start,
                end=new_end,
            )
        )

        conflicts = [
            item
            for item in conflicts
            if str(item.get("id"))
            != str(appointment_id)
        ]

        if conflicts:

            state["availability"] = {
                "available": False,
                "reason": (
                    "Patient already has "
                    "another appointment "
                    "during this time."
                ),
                "conflicts": conflicts,
            }

            state["error"] = (
                "Patient already has another "
                "appointment during this time."
            )

            return state

    # ---------------------------------------
    # Success
    # ---------------------------------------
    workflow_data["new_start"] = new_start
    workflow_data["new_end"] = new_end
    state["new_start"] = (
        new_start
    )

    state["new_end"] = (
        new_end
    )

    state["availability"] = {
        "available": True,
        "reason": (
            "New appointment time is available."
        ),
    }

    state["workflow_status"] = (
        "WAITING_FOR_CONFIRMATION"
    )

    state["result"] = {
        "success": True,
        "title": "Confirm Rescheduling",
        "message": (
            f"Appointment {appointment_id} "
            f"is available at "
            f"{new_start}. "
            f"Do you want to reschedule it?"
        ),
        "data": {
            "appointment_id":
                appointment_id,
            "old_start":
                old_start,
            "old_end":
                old_end,
            "new_start":
                new_start,
            "new_end":
                new_end,
        },
    }

    return state