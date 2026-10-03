from langgraph.types import interrupt


def select_bed(state):

    # Already resumed
    if state.get("bed_decision"):
        return state

    decision = interrupt(
        {
            "type": "BED_SELECTION",
            "message": "Review the AI bed recommendations.",
            "patient": state["resolved_patient"],
            "requirements": state["patient_requirements"],
            "recommended_beds": state["recommended_beds"]
        }
    )

    state["bed_decision"] = decision
    print("Decision:", decision)
    action = decision["action"]

    if action == "select":

        state["selected_bed"] = decision["selected_bed"]
        state["selected_bed_id"] = decision["selected_bed"]["bed_id"]

    elif action == "manual":

        state["selected_bed_id"] = decision["bed_id"]
        state["manual_reason"] = decision.get("reason")

    elif action == "reject":

        state["error"] = decision.get(
            "reason",
            "Doctor rejected all recommended beds."
        )

    return state