"""
Review Active Medications
"""

from graph.workflows.discharge.state import (
    DischargeState
)

from services.medication_service import (
    list_active_medications
)


def review_active_medications(
    state: DischargeState
) -> DischargeState:

    patient_id = state["resolved_patient"]["id"]

    medications = list_active_medications(
        patient_id
    )

    state["medications"] = medications

    return state