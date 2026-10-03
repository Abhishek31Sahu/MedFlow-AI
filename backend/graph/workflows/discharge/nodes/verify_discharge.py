"""
Verify Discharge
"""

from graph.workflows.discharge.state import (
    DischargeState
)

from services.encounter_service import (
    encounter_details
)


def verify_discharge(
    state: DischargeState
) -> DischargeState:

    encounter = encounter_details(

        state["encounter_id"]

    )

    state["verified_encounter"] = encounter

    return state