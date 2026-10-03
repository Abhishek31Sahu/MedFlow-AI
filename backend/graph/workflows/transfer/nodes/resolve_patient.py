"""
Resolve Patient
"""



from services.patient_service import patient_details
from graph.workflows.admission.state import (
    AdmissionState
)

from services.patient_search_service import (
    resolve_patient
)

from langgraph.types import interrupt

def resolve_patient_node(state):

    print("1. Enter resolve_patient")

    patient_name = state["workflow_data"]["patient_name"]

    result = resolve_patient(patient_name)

    print("2. Search completed")

    if result["status"] == "multiple":

        print("3. Before interrupt")

        selection = interrupt(
            {
                "type": "patient_selection",
                "patients": result["patients"]
            }
        )

        print("4. After interrupt")   # <--- This is the important one

        print(selection)

        patient = patient_details(
            selection["patient_id"]
        )

        print("5. Patient resolved")

        state["resolved_patient"] = patient

        return state
    elif result["status"] == "resolved":
        print(result)
        patient = patient_details(result["patient"]["id"])
        state["resolved_patient"] = patient
        return state
    
    else:
        state["error"] = "Patient not found"
        return state