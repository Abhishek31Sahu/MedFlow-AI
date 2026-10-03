"""
Create FHIR Appointment
"""

from database.database import (
    SessionLocal
)

from services.appointment_service import (
    book_appointment
)

from graph.workflows.appointment_booking.state import (
    AppointmentBookingState
)


def create_appointment(
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

    db = SessionLocal()

    try:

        result = book_appointment(

            db=db,

            patient_id=patient["id"],

            practitioner_id=practitioner["id"],

            start=workflow_data[
                "start"
            ],

            end=workflow_data[
                "end"
            ],

            reason=workflow_data.get(
                "reason",
                "General Consultation"
            ),
        )

        state["appointment_id"] = (
            result["appointment_id"]
        )

        state["appointment"] = (
            result["appointment"]
        )

        state["workflow_status"] = (
            "COMPLETED"
        )

        state["current_step"] = (
            "APPOINTMENT_CREATED"
        )

        return state

    except Exception as e:

        state["error"] = str(e)

        state["workflow_status"] = (
            "FAILED"
        )

        state["current_step"] = (
            "APPOINTMENT_CREATION_FAILED"
        )

        return state

    finally:

        db.close()