"""
Find Active Encounter
"""

from graph.workflows.transfer.state import (
    TransferState
)

from services.encounter_service import (
    find_active_encounter
)


def verify_encounter_node(
    state: TransferState
) -> TransferState:

    patient_id = state["resolved_patient"]["id"]

    encounter = find_active_encounter(
        patient_id
    )

    if encounter is None:

        state["error"] = (
            "No active encounter found."
        )

        return state

    state["active_encounter"] = encounter

    state["encounter_id"] = encounter["id"]
    
    encounter = state["active_encounter"]

    if encounter["status"] != "in-progress":

        state["error"] = (
            "Encounter is not active."
        )

        return state
    

    return state