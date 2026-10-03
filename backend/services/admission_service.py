"""
Admission Service

Coordinates the complete patient admission workflow.
"""


# patient_summary_service.py

# discharge_service.py
from patient.patient import get_patient
from encounter.encounter import (
    create_encounter,
    get_patient_encounters,
)

# These modules will be implemented later
# from insurance.insurance import check_insurance
# from bed.bed import (
#     find_available_bed,
#     occupy_bed,
# )


def admit_patient(
    patient_id: str,
    practitioner_id: str,
    ward: str = "General",
):
    """
    Complete admission workflow.
    """

    # -----------------------------------
    # Step 1 : Verify Patient
    # -----------------------------------

    try:
        patient = get_patient(patient_id)

    except Exception:
        return {
            "success": False,
            "message": "Patient not found."
        }

    # -----------------------------------
    # Step 2 : Check Active Encounter
    # -----------------------------------

    encounters = get_patient_encounters(patient_id)

    if "entry" in encounters:

        for entry in encounters["entry"]:

            resource = entry["resource"]

            if resource.get("status") == "in-progress":

                return {
                    "success": False,
                    "message": "Patient already admitted.",
                    "encounter_id": resource["id"]
                }

    # -----------------------------------
    # Step 3 : Insurance
    # -----------------------------------

    # insurance = check_insurance(patient_id)

    insurance = {
        "approved": True,
        "company": "ABC Insurance"
    }

    if not insurance["approved"]:

        return {
            "success": False,
            "message": "Insurance rejected."
        }

    # -----------------------------------
    # Step 4 : Find Bed
    # -----------------------------------

    # bed = find_available_bed(ward)

    bed = {
        "bed_id": "Bed101"
    }

    if bed is None:

        return {
            "success": False,
            "message": "No beds available."
        }

    # -----------------------------------
    # Step 5 : Reserve Bed
    # -----------------------------------

    # occupy_bed(bed["bed_id"])

    # -----------------------------------
    # Step 6 : Create Encounter
    # -----------------------------------

    encounter = create_encounter(

        patient_id=patient_id,

        practitioner_id=practitioner_id,

        location_id=bed["bed_id"]
    )

    # -----------------------------------
    # Step 7 : Response
    # -----------------------------------

    return {

        "success": True,

        "patient_id": patient_id,

        "patient_name":
            patient["name"][0]["given"][0]
            + " "
            + patient["name"][0]["family"],

        "encounter_id": encounter["id"],

        "bed": bed["bed_id"],

        "insurance": insurance["company"],

        "message": "Patient admitted successfully."
    }