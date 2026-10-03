"""
Appointment Booking Response
"""

from graph.workflows.appointment_booking.state import AppointmentBookingState


def response(state: AppointmentBookingState):
    """
    Build the final response after appointment booking.
    """

    print("Enter appointment_booking_response")

    # =====================================================
    # ERROR
    # =====================================================

    if state.get("error"):
        state["result"] = {
            "success": False,
            "message": state["error"],
        }

        return state

    # =====================================================
    # APPOINTMENT
    # =====================================================

    appointment = state.get("appointment", {})

    appointment_id = (
        state.get("appointment_id")
        or appointment.get("id")
    )

    # =====================================================
    # PATIENT
    # =====================================================

    patient = state.get("resolved_patient", {})

    patient_id = patient.get("id")
    patient_name = "Unknown"

    if patient:
        name_data = patient.get("name", [{}])[0]

        given = " ".join(
            name_data.get("given", [])
        )

        family = name_data.get("family", "")

        patient_name = f"{given} {family}".strip()

    # =====================================================
    # PRACTITIONER
    # =====================================================

    practitioner = state.get("resolved_practitioner", {})

    practitioner_id = practitioner.get("id")
    practitioner_name = "Unknown"
    practitioner_designation = None

    if practitioner:
        name_data = practitioner.get("name", [{}])[0]

        given = " ".join(
            name_data.get("given", [])
        )

        family = name_data.get("family", "")

        practitioner_name = f"{given} {family}".strip()

        qualifications = practitioner.get(
            "qualification",
            []
        )

        if qualifications:
            practitioner_designation = (
                qualifications[0]
                .get("code", {})
                .get("text")
            )

    # =====================================================
    # APPOINTMENT TYPE
    # =====================================================

    appointment_type = (
        appointment.get("appointmentType", {})
        .get("coding", [{}])[0]
        .get("code")
    )

    if not appointment_type:
        appointment_type = (
            appointment.get("appointmentType", {})
            .get("text")
        )

    # =====================================================
    # REASON
    # =====================================================

    reason = ""

    reason_codes = appointment.get(
        "reasonCode",
        []
    )

    if reason_codes:
        reason = reason_codes[0].get(
            "text",
            ""
        )

    # =====================================================
    # SAVE FINAL RESULT
    # =====================================================

    state["result"] = {
        "success": True,
        "message": "Appointment booked successfully.",

        "appointment_id": appointment_id,

        "patient": {
            "id": patient_id,
            "name": patient_name,
        },

        "practitioner": {
            "id": practitioner_id,
            "name": practitioner_name,
            "designation": practitioner_designation,
        },

        "appointment": {
            "status": appointment.get("status"),
            "appointment_type": appointment_type,
            "reason": reason,
            "start": appointment.get("start"),
            "end": appointment.get("end"),
        },
    }

    print("Appointment booking response created")

    return state