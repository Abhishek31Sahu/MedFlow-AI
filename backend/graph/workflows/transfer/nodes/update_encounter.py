
from services.encounter_service import transfer_to_new_location


def update_encounter_node(state):

    try:

        updated = transfer_to_new_location(

            encounter_id=state["encounter_id"],

            new_location_id=state["selected_bed"]["location_id"]

        )

        state["updated_encounter"] = updated

        return state

    except Exception as e:

        state["error"] = str(e)

        return state
