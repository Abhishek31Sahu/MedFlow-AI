"""
Transfer Summary
"""

from graph.workflows.transfer.state import TransferState


def transfer_summary(
    state: TransferState
) -> TransferState:

    # -----------------------------
    # Error Response
    # -----------------------------
    if state.get("error"):

        state["result"] = {

            "success": False,

            "workflow": "transfer",

            "patient": state.get("resolved_patient"),

            "encounter": state.get("verified_encounter"),

            "selected_bed": state.get("selected_bed"),

            "assigned_bed": state.get("assigned_bed"),

            "doctor_decision": state.get("bed_decision"),

            "error": state["error"],

            "message": f"Transfer failed: {state['error']}"

        }

        return state

    # -----------------------------
    # Success Response
    # -----------------------------
    state["result"] = {

        "success": True,

        "workflow": "transfer",

        "patient": state.get("resolved_patient"),

        "encounter": state.get("updated_encounter"),

        "selected_bed": state.get("selected_bed"),

        "assigned_bed": state.get("assigned_bed"),

        "doctor_decision": state.get("bed_decision"),

        "message": "Patient transferred successfully."

    }

    return state