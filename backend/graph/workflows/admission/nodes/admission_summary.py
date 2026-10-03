"""
Admission Summary
"""

from graph.workflows.admission.state import AdmissionState


def admission_summary(
    state: AdmissionState,
) -> AdmissionState:

    # ======================================================
    # Failure
    # ======================================================

    if state.get("error"):

        state["workflow_status"] = "FAILED"

        state["result"] = {

            "success": False,

            "workflow": "Admission",

            "message": state["error"],

            "patient": state.get("resolved_patient"),

            "bed": state.get("selected_bed"),

            "encounter_id": state.get("encounter_id"),

            "allocation_id": state.get("allocation_id")

        }

        return state

    # ======================================================
    # Success
    # ======================================================

    state["workflow_status"] = "COMPLETED"

    state["result"] = {

        "success": True,

        "workflow": "Admission",

        "message": "Patient admitted successfully.",

        "patient": state.get("resolved_patient"),

        "bed": state.get("selected_bed"),

        "encounter_id": state.get("encounter_id"),

        "allocation_id": state.get("allocation_id"),

        "location_id": state.get("location_id")

    }

    return state