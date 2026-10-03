"""
Appointment Booking Input
"""

from pydantic import BaseModel, Field


class BookingInput(BaseModel):

    patient_name: str

    practitioner_name: str | None = None

    practitioner_id: str | None = None

    start: str

    end: str

    reason: str = Field(
        default="General Consultation"
    )