"""
Appointment Booking Confirmation
"""

from langgraph.types import interrupt

from graph.workflows.appointment_booking.state import AppointmentBookingState


def confirm_booking(state: AppointmentBookingState) -> AppointmentBookingState:

    patient = state["resolved_patient"]
    practitioner = state["resolved_practitioner"]
    workflow_data = state["workflow_data"]

    # Patient name
    patient_name_data = patient.get("name", [{}])[0]

    patient_name = " ".join(
        patient_name_data.get("given", [])
    )

    family_name = patient_name_data.get("family", "")

    if family_name:
        patient_name = f"{patient_name} {family_name}"

    # Practitioner name
    practitioner_name_data = practitioner.get("name", [{}])[0]

    practitioner_name = " ".join(
        practitioner_name_data.get("given", [])
    )

    family_name = practitioner_name_data.get("family", "")

    if family_name:
        practitioner_name = f"{practitioner_name} {family_name}"

    confirmation = interrupt(
        {
            "type": "appointment_confirmation",

            "patient": {
                "id": patient.get("id"),
                "name": patient_name,
            },

            "practitioner": {
                "id": practitioner.get("id"),
                "name": practitioner_name,
            },

            "start": workflow_data["start"],

            "end": workflow_data["end"],

            "reason": workflow_data.get(
                "reason",
                "General Consultation"
            ),

            "message": "Please confirm this appointment.",
        }
    )

    confirmed = False

    if isinstance(confirmation, dict):
        confirmed = confirmation.get(
            "confirmed",
            False
        )

    elif isinstance(confirmation, bool):
        confirmed = confirmation

    if not confirmed:
        state["booking_confirmed"] = False
        state["workflow_status"] = "CANCELLED"
        state["current_step"] = "BOOKING_CANCELLED"
        state["error"] = "Appointment booking was cancelled."

        return state

    state["booking_confirmed"] = True
    state["current_step"] = "BOOKING_CONFIRMED"

    return state