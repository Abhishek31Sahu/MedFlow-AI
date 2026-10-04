from langgraph.types import interrupt


def select_bed(state):

    # If a bed has already been selected,
    # continue the workflow.

    if state.get("selected_bed_id"):

        return state

    # Pause workflow and return recommendations
    # to the frontend.

    selected_bed = interrupt(

        {
            "type": "BED_SELECTION",

            "message": "Select one of the recommended beds.",

            "recommendations": state["recommended_beds"]

        }

    )
    
    state["selected_bed"] = selected_bed["selected_bed"]
    
    state["selected_bed_id"] = selected_bed["bed_id"]

    return state