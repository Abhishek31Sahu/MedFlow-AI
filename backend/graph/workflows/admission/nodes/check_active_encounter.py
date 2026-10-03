"""
Check Active Encounter
"""

from graph.workflows.admission.state import (
    AdmissionState
)

from services.encounter_service import (
    find_active_encounter
)


def check_active_encounter(
    state: AdmissionState
) -> AdmissionState:

    patient_id = state[
        "resolved_patient"
    ]["id"]

    encounter = find_active_encounter(
        patient_id
    )

    if encounter:

        state["active_encounter"] = encounter

        state["error"] = (

            "Patient already has an active encounter."

        )

    return state