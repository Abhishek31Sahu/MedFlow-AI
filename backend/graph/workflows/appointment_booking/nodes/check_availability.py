"""
Check Appointment Availability
"""

from database.database import (
    SessionLocal
)

from services.appointment_service import (
    check_availability
)

from graph.workflows.appointment_booking.state import (
    AppointmentBookingState
)


def check_booking_availability(
    state: AppointmentBookingState
) -> AppointmentBookingState:

    patient = (
        state["resolved_patient"]
    )

    practitioner = (
        state["resolved_practitioner"]
    )

    workflow_data = (
        state["workflow_data"]
    )

    practitioner_id = (
        practitioner["id"]
    )

    start = workflow_data[
        "start"
    ]

    end = workflow_data[
        "end"
    ]

    db = SessionLocal()

    try:

        availability = check_availability(
            db=db,
            practitioner_id=practitioner_id,
            start=start,
            end=end
        )

        state["availability"] = (
            availability
        )

        if not availability.get(
            "available"
        ):

            state["error"] = (
                availability.get(
                    "reason",
                    "Practitioner is not available "
                    "during the requested time."
                )
            )

            state["workflow_status"] = (
                "FAILED"
            )

            state["current_step"] = (
                "SLOT_NOT_AVAILABLE"
            )

            return state

        state["current_step"] = (
            "SLOT_AVAILABLE"
        )

        return state

    except Exception as e:

        state["error"] = str(e)

        state["workflow_status"] = (
            "FAILED"
        )

        state["current_step"] = (
            "AVAILABILITY_CHECK_FAILED"
        )

        return state

    finally:

        db.close()