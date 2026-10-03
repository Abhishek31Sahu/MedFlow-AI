"""
Find Active Encounter
"""

from graph.workflows.discharge.state import (
    DischargeState
)

from services.encounter_service import (
    find_active_encounter
)


def find_active_encounter_node(
    state: DischargeState
) -> DischargeState:

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
    print("encounter",state["encounter_id"])
    return state