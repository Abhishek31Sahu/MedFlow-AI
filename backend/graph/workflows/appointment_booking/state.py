"""
Appointment Booking Workflow State
"""

from typing import Any

from graph.state import HospitalState


class AppointmentBookingState(HospitalState):

    # ==========================================================
    # Workflow
    # ==========================================================

    workflow_id: str | None

    workflow_status: str | None

    current_step: str | None

    # ==========================================================
    # Extracted Booking Data
    # ==========================================================

    workflow_data: dict

    # Example:
    #
    # {
    #     "patient_name": "Adesh Tiwari",
    #     "practitioner_name": "Rahul Sharma",
    #     "practitioner_id": None,
    #     "start": "2026-09-21T10:00:00",
    #     "end": "2026-09-21T10:30:00",
    #     "reason": "General Consultation"
    # }

    # ==========================================================
    # Patient Resolution
    # ==========================================================

    resolved_patient: dict | None

    candidate_patients: list

    # ==========================================================
    # Practitioner Resolution
    # ==========================================================

    resolved_practitioner: dict | None

    candidate_practitioners: list

    # ==========================================================
    # Availability
    # ==========================================================

    availability: dict | None

    # ==========================================================
    # Confirmation
    # ==========================================================

    booking_confirmed: bool | None

    # ==========================================================
    # Appointment
    # ==========================================================

    appointment_id: str | None

    appointment: dict | None

    # ==========================================================
    # Workflow Results
    # ==========================================================

    workflow_results: list

    result: Any

    # ==========================================================
    # Error
    # ==========================================================

    error: str | None