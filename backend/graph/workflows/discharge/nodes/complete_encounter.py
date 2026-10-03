"""
Complete Encounter
"""

from graph.workflows.discharge.state import (
    DischargeState
)

from services.encounter_service import (
    discharge_patient
)


def complete_encounter(
    state: DischargeState
) -> DischargeState:

    result = discharge_patient(

        state["encounter_id"]

    )

    state["result"] = result

    return state