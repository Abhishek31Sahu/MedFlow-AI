"""
Appointment Decision Model
"""

from typing import Any, Literal

from pydantic import BaseModel, Field


class AppointmentDecision(
    BaseModel
):

    function: Literal[
        "check_availability",
        "appointment_details",
        "patient_appointments",
        "practitioner_appointments",
        "cancel_appointment"
    ]

    payload: dict[str, Any] = Field(
        default_factory=dict
    )