"""
Appointment Function Registry
"""

from database.database import SessionLocal

from services.appointment_service import (
    check_availability,
    appointment_details,
    cancel_appointment
)

from appointment.appointment import (
    get_patient_appointments,
    get_practitioner_appointments
)


# ==========================================================
# CHECK AVAILABILITY
# ==========================================================

def appointment_check_availability(
    practitioner_id: str,
    start: str,
    end: str
):

    db = SessionLocal()

    try:

        return check_availability(
            db=db,
            practitioner_id=practitioner_id,
            start=start,
            end=end
        )

    finally:

        db.close()


# ==========================================================
# PATIENT APPOINTMENTS
# ==========================================================

def appointment_patient_appointments(
    patient_id: str
):

    return get_patient_appointments(
        patient_id=patient_id
    )


# ==========================================================
# PRACTITIONER APPOINTMENTS
# ==========================================================

def appointment_practitioner_appointments(
    practitioner_id: str
):

    return get_practitioner_appointments(
        practitioner_id=practitioner_id
    )


# ==========================================================
# APPOINTMENT DETAILS
# ==========================================================

def appointment_get_details(
    appointment_id: str
):

    return appointment_details(
        appointment_id
    )


# ==========================================================
# CANCEL APPOINTMENT
# ==========================================================

def appointment_cancel(
    appointment_id: str
):

    return cancel_appointment(
        appointment_id
    )


# ==========================================================
# FUNCTION REGISTRY
# ==========================================================

FUNCTIONS = {

    "check_availability":
        appointment_check_availability,

    "appointment_details":
        appointment_get_details,

    "patient_appointments":
        appointment_patient_appointments,

    "practitioner_appointments":
        appointment_practitioner_appointments,

    "cancel_appointment":
        appointment_cancel,

}