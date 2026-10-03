"""
Discharge Summary
"""

from graph.workflows.discharge.state import (
    DischargeState
)


def discharge_summary(
    state: DischargeState
) -> DischargeState:

    state["result"] = {
    "success": True,
    "workflow": "discharge",
    "patient": state["resolved_patient"],
    "encounter": state["verified_encounter"],
    "doctor_decision": (
        state["doctor_decision"]
        if state.get("medication_review")
        else None
    ),
    "message": "Patient discharged successfully."
}

    return state