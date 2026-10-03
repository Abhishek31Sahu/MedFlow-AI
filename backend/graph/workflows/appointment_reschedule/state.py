from typing import TypedDict
from graph.state import HospitalState

class AppointmentRescheduleState(HospitalState):

    query: str
    practitioner_id: str

    # Pending workflow information
    active_workflow: str | None
    workflow_status: str | None
    missing_fields: list[str]

    # Appointment
    appointment_id: str
    appointment: dict

    # New appointment time
    new_start: str
    new_end: str

    # Availability
    availability: dict

    # Confirmation
    confirmation: bool | None

    # Result
    result: dict
    error: str