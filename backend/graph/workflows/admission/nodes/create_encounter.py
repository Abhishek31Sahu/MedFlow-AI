"""
Create Encounter
"""

from graph.workflows.admission.state import AdmissionState
from services.encounter_service import admit_patient


def create_encounter(
    state: AdmissionState
) -> AdmissionState:

    try:

        result = admit_patient(

            patient_id=state["resolved_patient"]["id"],

            practitioner_id=state["practitioner_id"],

            location_id=state["location_id"],

            encounter_type=state["workflow_data"].get(
                "encounter_type",
                "IMP"
            )

        )

        state["encounter_id"] = result["encounter_id"]
        state["result"] = result
        state["encounter"] = result
        state["error"] = None

    except Exception as e:

        state["error"] = str(e)
        state["result"] = None
        state["encounter"] = None
        state["encounter_id"] = None

    return state