"""
Appointment CRUD Operations

FHIR Appointment resource operations.
"""

from datetime import datetime

from fhir.client import fhir_client
from patient.patient import get_patient
from practitioner.practitioner import get_practitioner

# ==========================================================
# CREATE APPOINTMENT
# ==========================================================

def create_appointment(
    patient_id: str,
    practitioner_id: str,
    start: str,
    end: str,
    reason: str = "General Consultation",
    appointment_type: str = "ROUTINE",
    description: str | None = None,
):

    appointment = {
        "resourceType": "Appointment",

        "status": "booked",

        "appointmentType": {
            "coding": [
                {
                    "system": (
                        "http://terminology.hl7.org/"
                        "CodeSystem/v2-0276"
                    ),
                    "code": appointment_type,
                }
            ],
            "text": appointment_type,
        },

        "start": start,

        "end": end,

        "participant": [
            {
                "actor": {
                    "reference": f"Patient/{patient_id}"
                },
                "status": "accepted",
            },
            {
                "actor": {
                    "reference": f"Practitioner/{practitioner_id}"
                },
                "status": "accepted",
            },
        ],

        "reasonCode": [
            {
                "text": reason
            }
        ],
    }

    if description:
        appointment["description"] = description

    return fhir_client.create(
        "Appointment",
        appointment,
    )


# ==========================================================
# GET SINGLE APPOINTMENT
# ==========================================================

def get_appointment(
    appointment_id: str,
):
    return fhir_client.read(
        "Appointment",
        appointment_id,
    )


# ==========================================================
# GET PATIENT APPOINTMENTS
# ==========================================================

def get_patient_appointments(
    patient_id: str,
):
    return fhir_client.search(
        "Appointment",
        {
            "actor": f"Patient/{patient_id}"
        },
    )


# ==========================================================
# GET PRACTITIONER APPOINTMENTS
# ==========================================================

def get_practitioner_appointments(
    practitioner_id: str,
):
    return fhir_client.search(
        "Appointment",
        {
            "actor": f"Practitioner/{practitioner_id}"
        },
    )


# ==========================================================
# GET APPOINTMENTS BY DATE
# ==========================================================

def get_appointments_by_date(
    date: str,
):
    """
    date format:
    YYYY-MM-DD

    We fetch appointments and filter by the start date.
    """

    bundle = fhir_client.search(
        "Appointment",
        {}
    )

    appointments = []

    for entry in bundle.get("entry", []):

        resource = entry.get("resource", {})

        start = resource.get("start")

        if not start:
            continue

        if start.startswith(date):
            appointments.append(resource)

    return {
        "resourceType": "Bundle",
        "type": "searchset",
        "entry": [
            {
                "resource": appointment
            }
            for appointment in appointments
        ],
        "total": len(appointments),
    }


# ==========================================================
# UPDATE APPOINTMENT
# ==========================================================

def update_appointment(
    appointment_id: str,
    start: str | None = None,
    end: str | None = None,
    reason: str | None = None,
):

    appointment = get_appointment(
        appointment_id
    )

    if start is not None:
        appointment["start"] = start

    if end is not None:
        appointment["end"] = end

    if reason is not None:

        appointment["reasonCode"] = [
            {
                "text": reason
            }
        ]

    return fhir_client.update(
        "Appointment",
        appointment_id,
        appointment,
    )


# ==========================================================
# CANCEL APPOINTMENT
# ==========================================================

def cancel_appointment(
    appointment_id: str,
):
    appointment = get_appointment(
        appointment_id
    )

    appointment["status"] = "cancelled"

    return fhir_client.update(
        "Appointment",
        appointment_id,
        appointment,
    )


# ==========================================================
# MARK PATIENT AS ARRIVED
# ==========================================================

def checkin_appointment(
    appointment_id: str,
):
    appointment = get_appointment(
        appointment_id
    )

    appointment["status"] = "arrived"

    return fhir_client.update(
        "Appointment",
        appointment_id,
        appointment,
    )


# ==========================================================
# COMPLETE APPOINTMENT
# ==========================================================

def complete_appointment(
    appointment_id: str,
):
    appointment = get_appointment(
        appointment_id
    )

    appointment["status"] = "fulfilled"

    return fhir_client.update(
        "Appointment",
        appointment_id,
        appointment,
    )


# ==========================================================
# MARK NO-SHOW
# ==========================================================

def mark_no_show(
    appointment_id: str,
):
    appointment = get_appointment(
        appointment_id
    )

    appointment["status"] = "noshow"

    return fhir_client.update(
        "Appointment",
        appointment_id,
        appointment,
    )


# ==========================================================
# FIND PRACTITIONER APPOINTMENTS IN TIME RANGE
# ==========================================================

def get_practitioner_appointments_between(
    practitioner_id: str,
    start: str,
    end: str,
):
    """
    Get practitioner appointments and return the ones
    whose time range overlaps the requested period.
    """

    bundle = get_practitioner_appointments(
        practitioner_id
    )

    appointments = []

    for entry in bundle.get("entry", []):

        resource = entry.get("resource", {})

        # Cancelled / no-show appointments should not
        # block a new booking.
        status = resource.get("status")

        if status in {
            "cancelled",
            "noshow",
            "entered-in-error",
        }:
            continue

        existing_start = resource.get("start")
        existing_end = resource.get("end")

        if not existing_start or not existing_end:
            continue

        # String ISO dates can be compared safely when
        # they use the same ISO format.
        if (
            start < existing_end
            and end > existing_start
        ):
            appointments.append(resource)

    return appointments


# ==========================================================
# FIND PATIENT APPOINTMENT CONFLICTS
# ==========================================================

def get_patient_appointments_between(
    patient_id: str,
    start: str,
    end: str,
):
    """
    Find overlapping appointments for a patient.
    """

    bundle = get_patient_appointments(
        patient_id
    )

    appointments = []

    for entry in bundle.get("entry", []):

        resource = entry.get("resource", {})

        status = resource.get("status")

        if status in {
            "cancelled",
            "noshow",
            "entered-in-error",
        }:
            continue

        existing_start = resource.get("start")
        existing_end = resource.get("end")

        if not existing_start or not existing_end:
            continue

        if (
            start < existing_end
            and end > existing_start
        ):
            appointments.append(resource)

    return appointments


# ==========================================================
# EXTRACT PATIENT ID
# ==========================================================

def get_patient_id_from_appointment(
    appointment: dict,
):

    for participant in appointment.get(
        "participant",
        [],
    ):

        actor = participant.get(
            "actor",
            {}
        )

        reference = actor.get(
            "reference"
        )

        if reference and reference.startswith(
            "Patient/"
        ):
            return reference.split(
                "/"
            )[-1]

    return None


# ==========================================================
# EXTRACT PRACTITIONER ID
# ==========================================================

def get_practitioner_id_from_appointment(
    appointment: dict,
):

    for participant in appointment.get(
        "participant",
        [],
    ):

        actor = participant.get(
            "actor",
            {}
        )

        reference = actor.get(
            "reference"
        )

        if reference and reference.startswith(
            "Practitioner/"
        ):
            return reference.split(
                "/"
            )[-1]

    return None


# ==========================================================
# PRINT APPOINTMENT
# ==========================================================

def print_appointment(appointment):
    participants = appointment.get("participant", [])

    patient_id = None
    practitioner_id = None

    for participant in participants:
        reference = participant.get("actor", {}).get("reference", "")

        if reference.startswith("Patient/"):
            patient_id = reference.split("/", 1)[1]

        elif reference.startswith("Practitioner/"):
            practitioner_id = reference.split("/", 1)[1]

    patient = None
    practitioner = None

    if patient_id:
        patient = get_patient(patient_id)

    if practitioner_id:
        practitioner = get_practitioner(practitioner_id)

    patient_name = "Unknown"

    if patient:
        name = patient.get("name", [{}])[0]

        given = " ".join(name.get("given", []))
        family = name.get("family", "")

        patient_name = f"{given} {family}".strip()

    practitioner_name = "Unknown"
    practitioner_designation = None

    if practitioner:
        name = practitioner.get("name", [{}])[0]

        given = " ".join(name.get("given", []))
        family = name.get("family", "")

        practitioner_name = f"{given} {family}".strip()

        qualifications = practitioner.get("qualification", [])

        if qualifications:
            practitioner_designation = (
                qualifications[0]
                .get("code", {})
                .get("text")
            )

    return {
        "id": appointment.get("id"),
        "status": appointment.get("status"),
        "appointment_type": (
            appointment.get("appointmentType", {})
            .get("coding", [{}])[0]
            .get("code")
            or appointment.get("appointmentType", {})
            .get("text")
        ),
        "reason": (
            appointment.get("reasonCode", [{}])[0]
            .get("text")
        ),
        "start": appointment.get("start"),
        "end": appointment.get("end"),

        "patient_id": patient_id,
        "patient_name": patient_name,

        "practitioner_id": practitioner_id,
        "practitioner_name": practitioner_name,
        "practitioner_designation": practitioner_designation,
    }